#!/usr/bin/env python3
import csv, re, time, random
from ddgs import DDGS

SRC = '/home/clawdbot/.openclaw/workspace/nexia/prospects/artisans-idf.csv'
OUT = '/home/clawdbot/.openclaw/workspace/nexia/prospects/artisans-enrichis.csv'
MAX = 100
TIMEOUT = 240

existing = set()
enriched = []
try:
    with open(OUT, 'r') as f:
        for row in csv.DictReader(f):
            existing.add(row['nom'])
            enriched.append(row)
except FileNotFoundError:
    pass

print(f"Déjà enrichis: {len(existing)}")

by_metier = {}
with open(SRC, 'r') as f:
    for row in csv.DictReader(f):
        if row['nom'] not in existing:
            m = row.get('metier', 'Autre')
            by_metier.setdefault(m, []).append(row)

# Round-robin
metiers = list(by_metier.keys())
prospects = []
idx = 0
while len(prospects) < MAX:
    added = False
    for m in metiers:
        if idx < len(by_metier[m]) and len(prospects) < MAX:
            prospects.append(by_metier[m][idx])
            added = True
    if not added:
        break
    idx += 1

print(f"Traitement de {len(prospects)} prospects")

phone_re = re.compile(r'0[1-9](?:[\s\.\-]?\d{2}){4}')
email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

start = time.time()
count = 0
new_count = 0
consecutive_429 = 0

def save():
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['nom','metier','ville','adresse','telephone','email'])
        w.writeheader()
        w.writerows(enriched)

for p in prospects:
    if time.time() - start > TIMEOUT:
        print("⏰ Timeout")
        break
    
    nom = p['nom']
    ville = p['ville']
    metier = p.get('metier', '')
    adresse = p.get('adresse', '')
    clean_nom = nom.split('(')[0].strip()
    
    phones = []
    emails = []
    got_429 = False
    
    try:
        results = DDGS().text(f'"{clean_nom}" {ville} téléphone', max_results=3)
        for r in results:
            text = f"{r.get('title','')} {r.get('body','')} {r.get('href','')}"
            phones += phone_re.findall(text)
            emails += email_re.findall(text)
        consecutive_429 = 0
    except Exception as e:
        err = str(e)
        if '429' in err:
            got_429 = True
            consecutive_429 += 1
            if consecutive_429 >= 3:
                wait = min(30, 5 * consecutive_429)
                print(f"  ⏸ Rate limited, pause {wait}s...")
                time.sleep(wait)
        else:
            print(f"  ⚠ {err[:80]}")
    
    phones = list(dict.fromkeys([''.join(re.findall(r'\d', ph)) for ph in phones]))
    emails = list(dict.fromkeys([e for e in emails if not any(e.endswith(x) for x in ['.png','.jpg','.gif','.svg'])]))
    
    phone = phones[0] if phones else ''
    email = emails[0] if emails else ''
    
    enriched.append({
        'nom': nom, 'metier': metier, 'ville': ville,
        'adresse': adresse, 'telephone': phone, 'email': email
    })
    
    count += 1
    if phone or email:
        new_count += 1
        print(f"✅ {count}. {nom} ({metier}, {ville}) → ☎ {phone} ✉ {email}")
    else:
        print(f"❌ {count}. {nom} ({metier}, {ville})")
    
    if count % 10 == 0:
        save()
        print(f"💾 {len(enriched)} total, {new_count} enrichis")
    
    # Adaptive delay
    delay = random.uniform(3, 5) if not got_429 else random.uniform(8, 15)
    time.sleep(delay)

save()
elapsed = int(time.time() - start)
print(f"\n🏁 {count} traités en {elapsed}s, {new_count} enrichis ({new_count*100//max(count,1)}%), {len(enriched)} total")
