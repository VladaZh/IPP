import yaml

from app.main import app

with open("openapi.yaml", "w", encoding="utf-8") as file:
    yaml.dump(app.openapi(), file, allow_unicode=True, sort_keys=False)
    