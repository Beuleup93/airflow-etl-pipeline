# Tutoriel Complet - Projet Airflow ETL

## Table des matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Architecture et composants](#architecture-et-composants)
3. [Configuration et environnement](#configuration-et-environnement)
4. [Modules de traitement des données](#modules-de-traitement-des-données)
5. [Orchestration avec Airflow](#orchestration-avec-airflow)
6. [Tests et qualité du code](#tests-et-qualité-du-code)
7. [CI/CD et déploiement](#cicd-et-déploiement)
8. [Utilisation pratique](#utilisation-pratique)
9. [Concepts avancés](#concepts-avancés)
10. [Troubleshooting](#troubleshooting)

## Images du tutoriel

Ce tutoriel inclut des captures d'écran pour illustrer les concepts :

- **Interface Airflow** : Vues des DAGs, graphiques d'exécution, logs détaillés
- **CI/CD** : Workflows GitHub Actions réussis
- **Architecture** : Schémas des deux approches (Astro CLI vs Docker Compose)

Les images sont organisées dans le dossier `images/` et montrent les interfaces réelles du projet en fonctionnement.

---

## 1. Vue d'ensemble du projet

### Objectif du projet

Ce projet implémente un pipeline ETL (Extract, Transform, Load) orchestré avec Apache Airflow pour traiter des données e-commerce. Il démontre les bonnes pratiques de l'ingénierie des données modernes.

### Technologies utilisées

- **Apache Airflow 2.8.1** : Orchestration et planification des tâches
- **Python 3.11** : Langage de programmation principal
- **PostgreSQL** : Base de données relationnelle
- **Docker** : Containerisation et déploiement
- **GitHub Actions** : CI/CD automatisé
- **Pandas** : Manipulation des données
- **SQLAlchemy** : ORM pour la base de données

### Structure du projet

```
airflow-etl/
├── dags/                          # DAGs Airflow
│   ├── etl_ecommerce_dag.py       # Pipeline ETL principal
│   ├── data_quality_dag.py       # Contrôles qualité
│   └── monitoring_dag.py          # Surveillance système
├── include/                       # Modules Python
│   ├── extract.py                 # Extraction des données
│   ├── transform.py               # Transformation des données
│   ├── load.py                   # Chargement des données
│   └── config_loader.py          # Gestion de la configuration
├── tests/                         # Tests automatisés
│   ├── unit/                     # Tests unitaires
│   └── integration/               # Tests d'intégration
├── data/                         # Données sources
│   └── raw/                      # Données brutes
├── scripts/                      # Scripts utilitaires
├── .github/workflows/            # CI/CD GitHub Actions
├── config.yaml                   # Configuration centrale
├── .env                         # Variables d'environnement
└── docker-compose.yml           # Services Docker
```

---

## 2. Architecture et composants

### Architecture générale

Le projet suit une architecture en couches :

1. **Couche de données** : PostgreSQL, fichiers CSV/JSON
2. **Couche de traitement** : Modules Python (extract/transform/load)
3. **Couche d'orchestration** : Apache Airflow
4. **Couche de déploiement** : Docker, GitHub Actions

### Composants principaux

#### A. Modules de traitement (include/)

**extract.py** - Extraction des données
- Extraction depuis API REST
- Lecture de fichiers CSV/JSON
- Gestion des erreurs de connexion
- Logging des opérations

**transform.py** - Transformation des données
- Nettoyage des données (doublons, valeurs manquantes)
- Validation des données (format email, valeurs positives)
- Enrichissement (calculs de métriques)
- Normalisation des formats

**load.py** - Chargement des données
- Connexion à PostgreSQL
- Création des tables
- Insertion des données
- Gestion des relations entre tables

**config_loader.py** - Gestion de la configuration
- Chargement depuis config.yaml
- Surcharge par variables d'environnement
- Validation des paramètres
- Gestion des chemins relatifs

#### B. DAGs Airflow (dags/)

**etl_ecommerce_dag.py** - Pipeline ETL principal
- Extraction des données sources
- Transformation et nettoyage
- Chargement en base de données
- Notifications de statut

**data_quality_dag.py** - Contrôles qualité
- Vérification de complétude
- Contrôle de cohérence
- Validation de fraîcheur
- Génération de rapports

**monitoring_dag.py** - Surveillance système
- Santé de la base de données
- Métriques de performance
- Alertes système
- Tableaux de bord

---

## 3. Configuration et environnement

### Configuration centralisée

Le projet utilise une configuration centralisée avec Astro CLI :

#### config.yaml - Configuration générale
```yaml
database:
  host: postgres
  port: 5432
  name: ecommerce_db
  user: postgres
  password: postgres

data_paths:
  raw_data: data/raw/
  processed_data: data/processed/

dags:
  etl_ecommerce:
    schedule: '@daily'
    tags: ['etl', 'ecommerce']
    max_active_runs: 1
```

#### Configuration Airflow (airflow_settings.yaml)
```yaml
airflow:
  connections:
    - conn_id: postgres_default
      conn_type: postgres
      conn_host: postgres
      conn_schema: ecommerce_db
      conn_login: postgres
      conn_password: postgres
      conn_port: 5432
  variables:
    - variable_name: notification_email
      variable_value: "beuleup2018@gmail.com"
```

### Gestion des environnements

#### Architecture de développement (Astro CLI)

**Avantages :**
- **Simplicité** : Un seul commande `astro dev start`
- **Services automatiques** : PostgreSQL + Airflow fournis
- **Configuration intégrée** : Pas besoin de Docker Compose
- **Développement rapide** : Setup en quelques secondes

**Architecture :**
```
Astro CLI Environment:
├── PostgreSQL (service postgres:5432)
│   ├── Métadonnées Airflow
│   └── ecommerce_db (notre base)
├── Airflow Scheduler
├── Airflow API Server (port 8080)
├── Airflow DAG Processor
└── Airflow Triggerer
```

**Utilisation :**
```bash
# Démarrage
astro dev start

# Vérification
astro dev ps

# Arrêt
astro dev stop
```

#### Architecture de production (Docker Compose)

**Avantages :**
- **Contrôle total** : Configuration personnalisée
- **Scalabilité** : Services séparés et redimensionnables
- **Monitoring** : pgAdmin, logs centralisés
- **Sécurité** : Configuration de production

**Architecture :**
```
Production Environment:
├── PostgreSQL (service postgres:5432)
│   ├── Métadonnées Airflow
│   └── ecommerce_db
├── pgAdmin (port 5050) - Administration DB
├── Airflow Webserver (port 8080)
├── Airflow Scheduler
├── Airflow Worker (optionnel)
└── Redis (optionnel) - Pour CeleryExecutor
```

**Utilisation :**
```bash
# Démarrage production
docker-compose -f docker-compose.prod.yml up -d

# Vérification
docker-compose -f docker-compose.prod.yml ps

# Arrêt
docker-compose -f docker-compose.prod.yml down
```

#### Quand utiliser quoi ?

**Développement :**
- **Astro CLI** : Développement, tests, debug
- **Configuration simple** : `config.yaml` + `airflow_settings.yaml`
- **Services intégrés** : Pas de configuration Docker

**Production :**
- **Docker Compose** : Déploiement, production, monitoring
- **Configuration avancée** : Services séparés, volumes persistants
- **Monitoring complet** : pgAdmin, logs, alertes

#### Comparaison des approches

| Aspect | Développement (Astro CLI) | Production (Docker Compose) |
|--------|---------------------------|------------------------------|
| **Complexité** | Simple (1 commande) | Complexe (configuration multiple) |
| **Services** | Intégrés automatiquement | Services séparés |
| **Base de données** | PostgreSQL intégré | PostgreSQL + pgAdmin |
| **Monitoring** | Interface Airflow uniquement | pgAdmin + logs centralisés |
| **Scalabilité** | Limitée | Haute (services redimensionnables) |
| **Sécurité** | Configuration de base | Configuration de production |
| **Déploiement** | Local uniquement | Production + CI/CD |
| **Maintenance** | Automatique | Manuelle (volumes, logs) |

#### Cas d'usage recommandés

**Utiliser Astro CLI pour :**
- Développement de DAGs
- Tests et debugging
- Formation et apprentissage
- Prototypage rapide

**Utiliser Docker Compose pour :**
- Déploiement en production
- Environnements de staging
- Démonstrations client
- Intégration avec CI/CD

### Configuration Astro CLI

**Astro CLI fournit automatiquement :**
- **Service PostgreSQL** : Nommé `postgres` sur le port 5432
- **Credentials par défaut** : `postgres/postgres`
- **Base de données** : `ecommerce_db` (créée par `init_db.sql`)
- **Connexions Airflow** : Configurées dans `airflow_settings.yaml`
- **Services Airflow** : Scheduler, API, DAG processor, Triggerer
- **Interface web** : http://localhost:8080 (admin/admin)

### Configuration prioritaire

1. Configuration YAML (config.yaml)
2. Configuration Airflow (airflow_settings.yaml)
3. Valeurs par défaut (code)

---

## 4. Modules de traitement des données

### A. Module d'extraction (extract.py)

#### Classe DataExtractor

```python
class DataExtractor:
    def __init__(self, config_loader):
        self.config = config_loader
        self.logger = logger
    
    def extract_from_api(self, endpoint):
        """Extraction depuis API REST"""
        # Gestion des timeouts
        # Retry automatique
        # Validation des réponses
    
    def extract_from_csv(self, file_path):
        """Extraction depuis fichier CSV"""
        # Détection automatique du séparateur
        # Gestion des encodages
        # Validation du schéma
    
    def extract_from_json(self, file_path):
        """Extraction depuis fichier JSON"""
        # Parsing JSON
        # Validation de la structure
        # Gestion des erreurs
```

#### Points clés de l'extraction

- **Robustesse** : Gestion des erreurs de réseau et de fichiers
- **Performance** : Streaming pour gros volumes
- **Monitoring** : Logs détaillés des opérations
- **Validation** : Vérification de l'intégrité des données

### B. Module de transformation (transform.py)

#### Classe DataTransformer

```python
class DataTransformer:
    def __init__(self, config_loader):
        self.config = config_loader
        self.logger = logger
    
    def clean_data(self, df):
        """Nettoyage des données"""
        # Suppression des doublons
        # Gestion des valeurs manquantes
        # Normalisation des formats
    
    def validate_data(self, df, rules):
        """Validation des données"""
        # Vérification des formats
        # Contrôles de cohérence
        # Alertes sur anomalies
    
    def enrich_data(self, df):
        """Enrichissement des données"""
        # Calculs de métriques
        # Ajout de champs dérivés
        # Agrégations
```

#### Types de transformations

**Nettoyage**
- Suppression des doublons
- Gestion des valeurs manquantes
- Normalisation des formats de date
- Standardisation des textes

**Validation**
- Format des emails
- Valeurs numériques positives
- Cohérence des dates
- Unicité des identifiants

**Enrichissement**
- Calcul de durées de session
- Agrégation des montants
- Classification des produits
- Métriques de performance

### C. Module de chargement (load.py)

#### Classe DataLoader

```python
class DataLoader:
    def __init__(self, config_loader):
        self.config = config_loader
        self.engine = self._create_engine()
        self.logger = logger
    
    def load_customers(self, customers_data):
        """Chargement des clients"""
        # Insertion en base
        # Gestion des conflits
        # Retour des IDs générés
    
    def load_products(self, products_data):
        """Chargement des produits"""
        # Validation des données
        # Insertion par batch
        # Gestion des erreurs
    
    def load_orders(self, orders_data, customers):
        """Chargement des commandes"""
        # Résolution des relations
        # Calculs de totaux
        # Validation des contraintes
```

#### Gestion des relations

**Tables principales**
- `customers` : Informations clients
- `products` : Catalogue produits
- `orders` : Commandes
- `user_sessions` : Sessions utilisateurs

**Relations**
- Orders → Customers (customer_id)
- Orders → Products (product_id)
- Sessions → Customers (customer_id)

#### Stratégies de chargement

**Idempotence**
- Nettoyage avant chargement
- Gestion des doublons
- Transactions atomiques

**Performance**
- Chargement par batch
- Indexation optimisée
- Parallélisation

---

## 5. Orchestration avec Airflow

### Concepts Airflow

#### DAG (Directed Acyclic Graph)
Un DAG est un graphe orienté acyclique qui définit l'ordre d'exécution des tâches.

#### Tâches (Tasks)
Les tâches sont les unités de travail atomiques dans un DAG.

#### Dépendances
Les dépendances définissent l'ordre d'exécution entre les tâches.

### DAG principal - ETL E-commerce

#### Structure du DAG

```python
@dag(
    dag_id='etl_ecommerce_pipeline',
    description='Pipeline ETL pour données e-commerce',
    schedule='@daily',
    catchup=False,
    tags=['etl', 'ecommerce']
)
def etl_ecommerce_pipeline():
    
    @task
    def extract_data():
        """Extraction des données sources"""
        # Appel du module extract
        # Retour des données via XCom
    
    @task
    def transform_data(raw_data):
        """Transformation des données"""
        # Appel du module transform
        # Utilisation des données de extract_data
    
    @task
    def load_data(transformed_data):
        """Chargement en base de données"""
        # Appel du module load
        # Gestion des erreurs
    
    @task
    def send_notification(load_result):
        """Notification du statut"""
        # Email de notification
        # Logs détaillés
    
    # Orchestration
    raw_data = extract_data()
    transformed_data = transform_data(raw_data)
    load_result = load_data(transformed_data)
    send_notification(load_result)
```

#### Flux de données

1. **Extraction** → Données brutes
2. **Transformation** → Données nettoyées
3. **Chargement** → Base de données
4. **Notification** → Statut final

### DAG de qualité des données

#### Objectifs
- Vérifier la complétude des données
- Contrôler la cohérence
- Valider la fraîcheur
- Générer des rapports

#### Tâches de qualité

```python
@task
def check_data_completeness():
    """Vérification de complétude"""
    # Comptage des enregistrements
    # Détection des données manquantes
    # Alertes sur anomalies

@task
def check_data_consistency():
    """Contrôle de cohérence"""
    # Vérification des contraintes
    # Validation des relations
    # Détection des incohérences

@task
def check_data_freshness():
    """Validation de fraîcheur"""
    # Vérification des timestamps
    # Détection des données obsolètes
    # Alertes temporelles
```

### DAG de monitoring

#### Surveillance système

```python
@task
def check_dag_status():
    """Statut des DAGs"""
    # Vérification des exécutions
    # Détection des échecs
    # Métriques de performance

@task
def check_database_health():
    """Santé de la base de données"""
    # Connexions actives
    # Espace disque
    # Performance des requêtes

@task
def check_system_metrics():
    """Métriques système"""
    # Utilisation CPU/RAM
    # Espace disque
    # Réseau
```

### Gestion des erreurs

#### Stratégies de retry
- Nombre de tentatives configurable
- Délai exponentiel entre tentatives
- Gestion des erreurs temporaires

#### Alertes et notifications
- Email en cas d'échec
- Notifications Slack
- Logs détaillés

#### Monitoring
- Métriques de performance
- Tableaux de bord
- Alertes proactives

---

## 6. Tests et qualité du code

### Structure des tests

#### Tests unitaires (tests/unit/)

**test_extract.py** - Tests d'extraction
```python
def test_extract_from_api_success():
    """Test extraction API réussie"""
    # Mock des réponses API
    # Validation des données
    # Vérification des logs

def test_extract_from_csv_error():
    """Test gestion d'erreur CSV"""
    # Simulation d'erreur de fichier
    # Vérification de la gestion d'erreur
    # Validation des messages
```

**test_transform.py** - Tests de transformation
```python
def test_clean_data():
    """Test nettoyage des données"""
    # Données avec doublons
    # Vérification de la suppression
    # Validation du résultat

def test_validate_email():
    """Test validation email"""
    # Emails valides/invalides
    # Vérification des règles
    # Gestion des erreurs
```

**test_load.py** - Tests de chargement
```python
def test_load_customers_success():
    """Test chargement clients réussi"""
    # Mock de la base de données
    # Insertion de données
    # Vérification des résultats

def test_load_orders_with_relations():
    """Test chargement avec relations"""
    # Données avec relations
    # Vérification des contraintes
    # Validation des IDs
```

**test_dags.py** - Tests des DAGs
```python
def test_dag_creation():
    """Test création des DAGs"""
    # Vérification des paramètres
    # Validation des tâches
    # Contrôle des dépendances

def test_dag_dependencies():
    """Test dépendances des DAGs"""
    # Vérification de l'ordre
    # Validation des XComs
    # Contrôle des flux
```

#### Tests d'intégration (tests/integration/)

**test_pipeline_integration.py** - Tests end-to-end
```python
def test_full_pipeline_with_mock_data():
    """Test pipeline complet avec données mock"""
    # Base de données de test
    # Exécution complète
    # Vérification des résultats

def test_data_flow_consistency():
    """Test cohérence du flux de données"""
    # Vérification des transformations
    # Validation des relations
    # Contrôle de l'intégrité
```

### Outils de qualité

#### Linting
- **flake8** : Style de code Python
- **black** : Formatage automatique
- **isort** : Organisation des imports
- **mypy** : Vérification des types

#### Tests
- **pytest** : Framework de tests
- **pytest-cov** : Couverture de code
- **mock** : Simulation d'objets

#### Sécurité
- **bandit** : Détection de vulnérabilités
- **safety** : Vérification des dépendances

### Configuration des tests

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --tb=short
    --cov=include
    --cov-report=html
    --cov-report=xml
```

#### Scripts de test
```python
# scripts/run_tests.py
def run_tests():
    """Exécution des tests"""
    # Configuration de l'environnement
    # Exécution des tests
    # Génération des rapports
```

---

## 7. CI/CD et déploiement

### GitHub Actions

#### Workflow CI (ci.yml)

**Interface GitHub Actions - Workflow réussi :**
![GitHub Actions - Workflow CI réussi](images/github-actions-ci-success.png)

*Interface GitHub Actions montrant l'exécution réussie du workflow CI avec tous les jobs : Tests, Code Quality, Security Scan, Build Docker Image, et Notify Results.*

**Job 1 : Tests**
```yaml
test:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:13
      env:
        POSTGRES_DB: ecommerce_db
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
  steps:
    - name: Checkout code
    - name: Set up Python
    - name: Install dependencies
    - name: Run unit tests
    - name: Run integration tests
    - name: Run DAG tests
```

**Job 2 : Qualité du code**
```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - name: Install linting tools
    - name: Run flake8
    - name: Run black
    - name: Run isort
    - name: Run mypy
```

**Job 3 : Sécurité**
```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - name: Install security tools
    - name: Run bandit
    - name: Run safety
```

**Job 4 : Build Docker**
```yaml
build-docker:
  runs-on: ubuntu-latest
  steps:
    - name: Set up Docker Buildx
    - name: Build Docker image
```

### Docker

#### Dockerfile
```dockerfile
FROM apache/airflow:2.8.1-python3.11

# Installation des dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie du code
COPY dags/ /opt/airflow/dags/
COPY include/ /opt/airflow/include/
COPY scripts/ /opt/airflow/scripts/
COPY data/ /opt/airflow/data/
COPY config.yaml /opt/airflow/config.yaml
COPY .env /opt/airflow/.env

# Configuration des permissions
USER root
RUN chown -R airflow:airflow /opt/airflow
USER airflow

EXPOSE 8080
CMD ["airflow", "webserver"]
```

#### Fichiers Docker pour la production

**Dockerfile** - Image personnalisée Airflow
```dockerfile
FROM apache/airflow:2.8.1-python3.11

# Configuration des variables d'environnement
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=/opt/airflow/include

# Installation des dépendances
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install -r /opt/airflow/requirements.txt

# Copie du code source
COPY dags/ /opt/airflow/dags/
COPY include/ /opt/airflow/include/
COPY config.yaml /opt/airflow/config.yaml
COPY airflow_settings.yaml /opt/airflow/airflow_settings.yaml

EXPOSE 8080
CMD ["airflow", "webserver"]
```

**docker-compose.prod.yml** - Orchestration production
```yaml
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: ecommerce_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init_db.sql:/docker-entrypoint-initdb.d/init_db.sql

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"

  airflow-webserver:
    build: .
    command: webserver
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:postgres@postgres:5432/ecommerce_db
    depends_on:
      - postgres

  airflow-scheduler:
    build: .
    command: scheduler
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:postgres@postgres:5432/ecommerce_db
    depends_on:
      - postgres
```

### Déploiement

#### Environnement de développement
```bash
# Démarrage des services avec Astro CLI
astro dev start

# Initialisation de la base de données
astro dev exec postgres psql -U postgres -d ecommerce_db -f init_db.sql

# Vérification des services
astro dev ps
```

#### Environnement de production
```bash
# Build de l'image Docker (pour déploiement)
docker build -t airflow-etl:latest .

# Déploiement avec Astro CLI
astro deploy
```

---

## 8. Utilisation pratique

### Démarrage du projet

#### Prérequis
- Astro CLI installé
- Git
- Python 3.11 (pour les tests locaux)

#### Installation
```bash
# Clone du repository
git clone https://github.com/Beuleup93/airflow-etl-pipeline.git
cd airflow-etl-pipeline

# Démarrage des services avec Astro CLI
astro dev start

# Vérification du statut
astro dev ps
```

#### Accès aux interfaces
- **Airflow UI** : http://localhost:8080
- **Base de données PostgreSQL** : localhost:5432 (service `postgres`)
- **Base de données** : `ecommerce_db` (créée par `init_db.sql`)

#### Interface Airflow - Vue des DAGs
Une fois Airflow démarré, vous accédez à l'interface web qui affiche tous les DAGs disponibles :

![Interface Airflow - Liste des DAGs](images/airflow-dags-list.png)

*Interface Airflow montrant les 3 DAGs du projet : `etl_ecommerce_pipeline`, `data_quality_checks`, et `monitoring_dag`, tous avec un statut de succès.*

### Exécution des DAGs

#### DAG ETL E-commerce
1. Accéder à l'interface Airflow
2. Activer le DAG `etl_ecommerce_pipeline`
3. Déclencher une exécution manuelle
4. Surveiller l'exécution dans le graph view

**Vue graphique du DAG ETL :**
![DAG ETL E-commerce - Vue graphique](images/etl-ecommerce-dag-graph.png)

*Vue graphique du DAG `etl_ecommerce_pipeline` montrant les 4 tâches séquentielles : `extract_data` → `transform_data` → `load_data` → `send_notification`, toutes avec un statut de succès.*

**Détails d'exécution et code du DAG :**
![DAG ETL E-commerce - Code et détails](images/etl-ecommerce-dag-code.png)

*Interface Airflow montrant les détails d'exécution du DAG ETL et l'éditeur de code avec la syntaxe moderne `@dag` et `@task`.*

#### DAG de qualité des données
1. Activer le DAG `data_quality_dag`
2. Programmer l'exécution quotidienne
3. Consulter les rapports de qualité

**Vue graphique du DAG de qualité :**
![DAG Data Quality - Vue graphique](images/data-quality-dag-graph.png)

*Vue graphique du DAG `data_quality_checks` montrant les tâches de vérification : `check_data_completeness`, `check_data_freshness`, `check_data_consistency`, et `generate_quality_report` avec leurs dépendances.*

#### DAG de monitoring
1. Activer le DAG `monitoring_dag`
2. Configurer les alertes
3. Surveiller les métriques

**Vue graphique du DAG de monitoring :**
![DAG Monitoring - Vue graphique et logs](images/monitoring-dag-graph-logs.png)

*Vue graphique du DAG `monitoring_dag` montrant les tâches de surveillance : `check_system_metrics`, `check_dag_status`, `check_data_freshness`, `check_database_health`, et `generate_monitoring_report`. Les logs détaillés montrent l'exécution de la tâche `check_system_metrics` avec les métriques calculées.*

### Tests locaux

#### Exécution des tests
```bash
# Création de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installation des dépendances
pip install -r requirements.txt

# Exécution des tests
make test
# ou
python -m pytest tests/ -v
```

#### Tests spécifiques
```bash
# Tests unitaires seulement
pytest tests/unit/ -v

# Tests d'intégration
pytest tests/integration/ -v

# Tests avec couverture
pytest --cov=include tests/
```

### Monitoring et debugging

#### Logs Airflow
```bash
# Logs des tâches
astro dev logs

# Logs de la base de données
astro dev logs postgres

# Logs en temps réel
astro dev logs -f
```

#### Debugging des DAGs
1. Vérifier la syntaxe des DAGs
2. Contrôler les connexions
3. Valider les variables
4. Analyser les logs d'exécution

#### Monitoring des performances
- Métriques de base de données
- Utilisation des ressources
- Temps d'exécution des tâches
- Taux de succès/échec

---

## 9. Concepts avancés

### Gestion des données

#### Stratégies de traitement
- **Batch processing** : Traitement par lots
- **Stream processing** : Traitement en temps réel
- **Micro-batch** : Traitement par petits lots

#### Optimisations de performance
- **Parallélisation** : Exécution simultanée
- **Caching** : Mise en cache des données
- **Indexation** : Optimisation des requêtes
- **Partitionnement** : Division des données

### Sécurité

#### Authentification et autorisation
- Gestion des utilisateurs Airflow
- Rôles et permissions
- Connexions sécurisées
- Variables chiffrées

#### Protection des données
- Chiffrement des données sensibles
- Audit des accès
- Sauvegarde sécurisée
- Conformité RGPD

### Scalabilité

#### Montée en charge
- Scaling horizontal
- Distribution des tâches
- Load balancing
- Auto-scaling

#### Architecture distribuée
- Multi-nœuds Airflow
- Bases de données distribuées
- Stockage distribué
- Réseau haute performance

### Intégration

#### APIs et services externes
- Intégration REST/GraphQL
- Webhooks
- Message queues
- Event streaming

#### Outils de monitoring
- Prometheus/Grafana
- ELK Stack
- Datadog
- New Relic

---

## 10. Troubleshooting

### Problèmes courants

#### Erreurs de connexion
```bash
# Vérification des services
astro dev ps

# Test de connexion PostgreSQL
astro dev exec postgres psql -U postgres -d ecommerce_db -c "SELECT 1;"

# Vérification des logs
astro dev logs postgres
```

#### Erreurs de DAGs
```bash
# Validation des DAGs
python scripts/validate_dags.py

# Vérification de la syntaxe
python -m py_compile dags/*.py

# Test des imports
python -c "from dags.etl_ecommerce_dag import etl_ecommerce_pipeline"
```

#### Erreurs de tests
```bash
# Exécution avec debug
pytest tests/ -v -s --tb=long

# Tests spécifiques
pytest tests/unit/test_dags.py::TestETLEcommerceDAG -v

# Vérification de l'environnement
python -c "import sys; print(sys.path)"
```

### Solutions aux erreurs fréquentes

#### "Module not found"
- Vérifier le PYTHONPATH
- Contrôler les imports relatifs
- Valider la structure des packages

#### "Database connection failed"
- Vérifier les paramètres de connexion
- Contrôler le statut de PostgreSQL
- Valider les credentials

#### "DAG not found"
- Vérifier la syntaxe des DAGs
- Contrôler les imports
- Valider les décorateurs

#### "Task failed"
- Analyser les logs détaillés
- Vérifier les dépendances
- Contrôler les données d'entrée

### Bonnes pratiques

#### Développement
- Tests avant déploiement
- Code review systématique
- Documentation à jour
- Versioning des changements

#### Production
- Monitoring continu
- Alertes proactives
- Sauvegardes régulières
- Plan de reprise d'activité

#### Maintenance
- Mise à jour des dépendances
- Optimisation des performances
- Nettoyage des logs
- Audit de sécurité

---

## Conclusion

Ce tutoriel couvre tous les aspects du projet Airflow ETL, de l'architecture à l'utilisation pratique. Il sert de référence complète pour comprendre et maîtriser les concepts d'ingénierie des données modernes.

### Points clés à retenir

1. **Architecture modulaire** : Séparation claire des responsabilités
2. **Configuration centralisée** : Gestion flexible des paramètres
3. **Tests complets** : Couverture unitaire et intégration
4. **CI/CD automatisé** : Déploiement et qualité du code
5. **Monitoring intégré** : Surveillance et alertes
6. **Documentation détaillée** : Maintenance et évolution

### Prochaines étapes

- Exploration des concepts avancés
- Intégration d'outils supplémentaires
- Optimisation des performances
- Déploiement en production
- Formation de l'équipe

Ce projet démontre les compétences essentielles d'un Data Engineer moderne et constitue une base solide pour des projets plus complexes.
