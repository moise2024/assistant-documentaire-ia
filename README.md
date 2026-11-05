# Assistant documentaire PNUD — prototype

Prototype : recherche dans un corpus de documents publics, appel à une API LLM, expérimentation de prompts et vérification des réponses à partir des sources.

## Lancer

```bash
python -m venv .venv
# Windows : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Renseigner `LLM_BASE_URL`, `LLM_API_KEY` et `LLM_MODEL` dans l’environnement (ou charger le fichier `.env` avec votre outil ; l’application ne lit volontairement pas `.env` automatiquement). Puis lancer `streamlit run app.py` et cliquer **Préparer les documents**. Les PDF téléchargés sont stockés localement dans `data/` et ignorés par Git.

L’API doit proposer le format `POST {base_url}/chat/completions` compatible OpenAI. Le code ne journalise pas la clé. Ne pas saisir de données confidentielles : la question et les passages retrouvés sont transmis au fournisseur configuré.

## Recherche et génération

Le texte des PDF est extrait page par page. TF-IDF sélectionne les cinq passages les plus pertinents localement. Le modèle reçoit la question, la consigne choisie et ces seuls passages. La réponse affiche les références [S1]… et chaque extrait/page consulté. Sans passage ayant un score lexical positif, l’application s’abstient d’appeler le modèle.

## Expérimentation et limites

Trois consignes sont comparables dans l’interface : concise, structurée et prudente. Utiliser le jeu de questions dans `evaluation/questions.json`; évaluer fidélité aux extraits, exactitude des citations, refus quand la réponse manque et clarté. Le jeu constitue un protocole, pas des résultats déjà mesurés. TF-IDF peut manquer des synonymes ou des formulations éloignées. Les citations nécessitent une vérification humaine dans les PDF d’origine.

Le corpus initial est défini dans `corpus/sources.json` et provient de publications officielles du PNUD :

- [Document de Programme de Coopération Côte d’Ivoire 2026–2030](https://www.undp.org/fr/cote-d-ivoire/publications/document-de-programme-de-cooperation-cpd-2026-2030)
- [UNDP Annual Report 2024](https://www.undp.org/publications/undp-annual-report-2024)
- [Évaluation indépendante du programme de pays Côte d’Ivoire](https://www.undp.org/evaluation/publications/icpe-cote-divoire)

Le rapport d’évaluation est une page web : il est référencé au catalogue mais n’est pas encore indexé tant qu’une copie PDF accessible n’est pas ajoutée localement (les fichiers à télécharger doivent être des documents publics et autorisés).
