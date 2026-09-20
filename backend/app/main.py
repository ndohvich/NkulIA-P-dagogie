"""Point d'entrée de l'API locale NkulIA.

Ce process FastAPI tourne dans le même exécutable que la fenêtre
PyWebView (voir desktop/main.py) — ce n'est pas un serveur distant.
Voir docs/adr/0001-architecture-offline-first.md.
"""

from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="NkulIA API", version="0.1.0", docs_url="/api/docs")
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Sonde utilisée par la fenêtre desktop avant d'afficher l'interface
    (voir desktop/main.py, attendre_que_l_api_reponde) et par la CI."""
    return {"status": "ok", "service": "nkulia-api"}
