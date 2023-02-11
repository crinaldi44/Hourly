"""Setup for the database."""

import os

from flask_sqlalchemy import SQLAlchemy

from open_alchemy import init_yaml

database = SQLAlchemy()

SPEC_FILE = os.path.join(os.path.abspath("openapi"), "openapi.yaml")
MODELS_FILENAME = os.path.join(os.path.abspath("models"), "models.py")
init_yaml(SPEC_FILE, base=database.Model, models_filename=MODELS_FILENAME)
