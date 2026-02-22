# Guide de Bonnes Pratiques & Amélioration Continue — NexIA

> Dernière mise à jour : 2026-02-16

## 1. Leçons apprises (à mettre à jour)

- **Les sous-agents échouent souvent silencieusement** → vérifier les outputs, sauvegarder progressivement
- **DuckDuckGo rate-limite** → `sleep(2)`, nouvelle instance `DDGS()` par requête
- **Pollinations.ai instable** → utiliser Unsplash pour les images
- **wacli crash sur serveur 4Go** → utiliser message tool OpenClaw
- **Gmail SMTP nécessite mot de passe d'application** (pas le mdp normal)

## 2. Process de prospection optimisé

| Étape | Action | Limite |
|-------|--------|--------|
| 1 | Scraping API gouv | Illimité, gratuit |
| 2 | Enrichissement DuckDuckGo | ~50-100/jour |
| 3 | Envoi emails via SMTP Gmail | 500/jour max |
| 4 | Relances J+3, J+7, J+14 | — |
| 5 | Suivi réponses | — |

## 3. Métriques à suivre

- Nombre de prospects contactés
- Taux de réponse
- Taux de conversion
- Revenue généré

## 4. Axes d'amélioration technique

- [ ] Installer un vrai email sender (Brevo gratuit 300 emails/jour)
- [ ] Obtenir Brave Search API pour enrichissement plus rapide
- [ ] Ajouter enrichissement LinkedIn
- [ ] Automatiser les relances avec cron jobs
- [ ] Créer plus de démos sectorielles

## 5. Axes d'amélioration business

- [ ] Tester différents prix
- [ ] Ajouter des témoignages réels dès le premier client
- [ ] Créer du contenu SEO (blog articles)
- [ ] Référencement Google My Business
- [ ] Partenariats avec associations d'artisans
