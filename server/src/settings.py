from os import environ

class Config:
    POSTGRES_HOST=environ.get("POSTGRES_HOST", "ugr_project_db")
    POSTGRES_USER=environ.get("POSTGRES_USER", "admin")
    POSTGRES_DB=environ.get("POSTGRES_DB", "ugr_project")
    POSTGRES_PASSWORD=environ.get("POSTGRES_PASSWORD", "changeme")

config = Config()