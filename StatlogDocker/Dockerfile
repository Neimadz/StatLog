# Utilisez l'image Python officielle en tant qu'image de base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les scripts Python et le fichier requirements.txt dans le conteneur
COPY main.py script.py requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script Python
CMD ["python", "main.py"]