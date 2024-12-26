from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurations
DATABASE_URL = os.getenv("mysql://root:''@localhost:3306/BanqueDB")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Par défaut, False
