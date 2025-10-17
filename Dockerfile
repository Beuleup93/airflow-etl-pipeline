# Dockerfile pour le déploiement de production
FROM apache/airflow:2.8.1-python3.11

# Variables d'environnement
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=/opt/airflow/include
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER=/opt/airflow/plugins
ENV AIRFLOW__CORE__LOGGING_LEVEL=INFO
ENV AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True

# Installation des dépendances système
USER root
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Retour à l'utilisateur airflow
USER airflow

# Copie des fichiers de configuration
COPY requirements.txt /opt/airflow/requirements.txt
COPY config.yaml /opt/airflow/config.yaml
COPY airflow_settings.yaml /opt/airflow/airflow_settings.yaml

# Installation des dépendances Python
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Copie du code source
COPY dags/ /opt/airflow/dags/
COPY include/ /opt/airflow/include/
COPY scripts/ /opt/airflow/scripts/
COPY data/ /opt/airflow/data/
COPY init_db.sql /opt/airflow/init_db.sql

# Création des répertoires nécessaires
RUN mkdir -p /opt/airflow/logs /opt/airflow/plugins

# Configuration des permissions
USER root
RUN chown -R airflow:airflow /opt/airflow || echo "Permission setting completed"
USER airflow

# Exposition des ports
EXPOSE 8080

# Commande par défaut
CMD ["airflow", "webserver"]