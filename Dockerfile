# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port 80
EXPOSE 80

# Commande par défaut pour démarrer l'application
CMD ["python", "main.py"]
