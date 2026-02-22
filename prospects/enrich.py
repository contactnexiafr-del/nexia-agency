#!/usr/bin/env python3
import csv, re, time, sys
from ddgs import DDGS

SRC = '/home/clawdbot/.openclaw/workspace/nexia/prospects/artisans-idf.csv'
OUT = '/home/clawdbot/.openclaw/workspace/nexia/prospects/artisans-enrichis.csv'
MAX = 100
TIMEOUT = 240

# Load existing enriched names
existing = set()
enriched = []
try:
    with open(OUT, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing.add(row['nom'])
            enriched.append(row)
except FileNotFoundError:
    pass

print(f"Déjà enrichis: {len(existing)}")

# Load source, skip already done
prospects = []
with open(SRC, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['nom'] not in existing:
            prospects.append(row)

print(f"Restants: {len(prospects)}, traitement de {min(MAX, len(prospects))}")

phone_re = re.compile(r'0[1-9](?:[\s\.\-]?\d{2}){4}')
email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

start = time.time()
count = 0
new_count = 0

def save():
    with open(OUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nom','metier','ville','adresse','telephone','email'])
        writer.writeheader()
        writer.writerows(enriched)

for p in prospects[:MAX]:
    if time.time() - start > TIMEOUT:
        print("⏰ Timeout atteint")
        break
    
    nom = p['nom']
    ville = p['ville']
    metier = p.get('metier', '')
    adresse = p.get('adresse', '')
    
    query = f"{nom} {ville} téléphone"
    phones = []
    emails = []
    
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        for r in results:
            text = f"{r.get('title','')} {r.get('body','')}"
            phones += phone_re.findall(text)
            emails += email_re.findall(text)
    except Exception as e:
        print(f"  ⚠ Erreur recherche {nom}: {e}")
    
    # Clean phones
    phones = list(dict.fromkeys([''.join(re.findall(r'\d', ph)) for ph in phones]))
    emails = list(dict.fromkeys(emails))
    
    phone = phones[0] if phones else ''
    email = emails[0] if emails else ''
    
    enriched.append({
        'nom': nom, 'metier': metier, 'ville': ville,
        'adresse': adresse, 'telephone': phone, 'email': email
    })
    
    count += 1
    if phone or email:
        new_count += 1
        print(f"✅ {count}. {nom} ({metier}) → ☎ {phone} ✉ {email}")
    else:
        print(f"❌ {count}. {nom} ({metier}) → rien trouvé")
    
    if count % 10 == 0:
        save()
        print(f"💾 Sauvegardé ({len(enriched)} total)")
    
    time.sleep(2)

save()
print(f"\n🏁 Terminé: {count} traités, {new_count} enrichis, {len(enriched)} total dans le fichier")
