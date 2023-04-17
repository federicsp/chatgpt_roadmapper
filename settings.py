from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Roadmapper"
    no_db: bool = True    # if True, doesn't connect to MongoDB
    connection_string: str = "mongodb://localhost:27017/"
    db_name: str = "roadmapperz"
    templates_directory: str = "templates"

settings = Settings()