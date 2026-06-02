# Exercise — CI/CD Pipeline with GitHub Actions & Koyeb

## Obiettivo

Capire come funziona una pipeline CI/CD realistica:

```
push su main
    │
    ▼
[CI] pytest ──(fail)──► pipeline bloccata
    │ (pass)
    ▼
[CI] docker build + push → ghcr.io
    │
    ▼
[CD] koyeb service update → app live
```

---

## Struttura del progetto

```
.
├── app/
│   ├── __init__.py
│   ├── converter.py      # logica di conversione (pura, testabile)
│   └── main.py           # FastAPI REST API
├── tests/
│   └── test_converter.py # unit test con pytest
├── Dockerfile
├── requirements.txt
└── .github/
    └── workflows/
        ├── ci.yml        # test → build → push su GHCR
        └── deploy.yml    # deploy su Koyeb
```

---

## Eseguire l'app in locale

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentazione interattiva disponibile su http://localhost:8000/docs

Endpoint disponibili:

```
GET /health
GET /convert/celsius/{value}      # es. /convert/celsius/100  → 212°F
GET /convert/fahrenheit/{value}   # es. /convert/fahrenheit/32 → 0°C
```

---

## Eseguire i test in locale

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Build Docker in locale

```bash
docker build -t temperature-converter .
docker run -p 8000:8000 temperature-converter
```

---

## Setup GitHub Actions

### 1. Rendere il package GHCR pubblico (opzionale)

Dopo il primo push, vai su:  
`GitHub → profilo → Packages → temperature-converter → Package settings → Change visibility → Public`

Se il package rimane privato, Koyeb ha bisogno di un registry secret (vedi sotto).

### 2. Segreti da configurare nel repository

Vai su `Settings → Secrets and variables → Actions` e aggiungi:

| Secret | Valore |
|--------|--------|
| `KOYEB_API_TOKEN` | API token da [app.koyeb.com/user/settings/api](https://app.koyeb.com/user/settings/api) |
| `KOYEB_APP_NAME` | Nome dell'app su Koyeb (es. `temperature-api`) |
| `KOYEB_SERVICE_NAME` | Nome del servizio su Koyeb (es. `web`) |

> `GITHUB_TOKEN` è automatico — non va aggiunto manualmente.

### 3. Prima deploy su Koyeb (una tantum)

Il workflow CD aggiorna un servizio già esistente. Crealo la prima volta dalla UI di Koyeb:

1. Crea una nuova app → scegli **Docker**
2. Image: `ghcr.io/<tuo-utente>/<tuo-repo>:latest`
3. Se GHCR è privato: aggiungi un **Registry Secret** con le tue credenziali GitHub
4. Port: `8000`
5. Nota il nome app e servizio → inseriscili nei segreti sopra

Da quel momento ogni push su `main` aggiorna automaticamente il servizio.

---

## Come funziona la pipeline (spiegazione per gli studenti)

### `ci.yml` — Continuous Integration

| Step | Cosa fa |
|------|---------|
| `actions/checkout` | Scarica il codice del repository |
| `actions/setup-python` | Installa Python 3.12 con cache pip |
| `pip install` | Installa le dipendenze |
| `pytest --cov` | Esegue i test; la pipeline si blocca se fallisce |
| `docker/login-action` | Si autentica a GHCR con il token automatico |
| `docker/metadata-action` | Genera i tag (`latest` + `sha-<commit>`) |
| `docker/build-push-action` | Build e push dell'immagine |

Il job `build-and-push` ha `needs: test` → non parte mai se i test falliscono.

### `deploy.yml` — Continuous Deployment

Si attiva solo quando `ci.yml` termina con successo (`workflow_run`).  
Usa la Koyeb CLI per dire al servizio di usare la nuova immagine `latest`.

---

## Domande per la discussione

1. Perché separare CI e CD in due file distinti?
2. Cosa succede se un test fallisce? Chi viene notificato?
3. Qual è la differenza tra `sha-<commit>` e `latest` come tag Docker?
4. Come si fa il rollback a una versione precedente?
5. Come si aggiunge un environment di staging prima della produzione?
