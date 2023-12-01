from pathlib import Path

from nguylinc_python_utils.connexion import setup_app

from api.init_models import Base

schema_path = Path(__file__).parent / "openapi.yaml"
app, session = setup_app(Base, schema_path)

if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", port=8080, reload=True)
