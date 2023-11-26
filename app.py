import logging
from pathlib import Path

import connexion
from connexion.middleware import MiddlewarePosition
from flask.cli import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from models.utils import init_db

load_dotenv()
logging.basicConfig(level=logging.INFO)
session = init_db(db_type="postgres", host="localhost")

origins = ["http://localhost:5173", "https://lincolnnguyen.me"]

app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml', validate_responses=True, strict_validation=True)
app.add_middleware(
    CORSMiddleware,
    position=MiddlewarePosition.BEFORE_ROUTING,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", port=8080, reload=True)
