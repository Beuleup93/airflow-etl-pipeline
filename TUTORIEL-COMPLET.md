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

Le projet utilise une approche de configuration hybride :

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

#### .env - Variables sensibles
```bash
DB_HOST=postgres
DB_USER=postgres
DB_PASSWORD=postgres
NOTIFICATION_EMAIL=beuleup2018@gmail.com
```

### Gestion des environnements

**Développement local**
- Docker Compose pour les services
- Base de données PostgreSQL locale
- Airflow en mode développement

**Production**
- Docker Compose avec volumes persistants
- Configuration de sécurité renforcée
- Monitoring et alertes

### Variables d'environnement prioritaires

1. Variables d'environnement (.env)
2. Configuration YAML (config.yaml)
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

#### Docker Compose
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: ecommerce_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  airflow:
    build: .
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql://postgres:postgres@postgres:5432/ecommerce_db
    volumes:
      - ./dags:/opt/airflow/dags
      - ./include:/opt/airflow/include
      - ./data:/opt/airflow/data
```

### Déploiement

#### Environnement de développement
```bash
# Démarrage des services
docker-compose up -d

# Initialisation de la base de données
docker-compose exec postgres psql -U postgres -d ecommerce_db -f init_db.sql

# Vérification des services
docker-compose ps
```

#### Environnement de production
```bash
# Build de l'image
docker build -t airflow-etl:latest .

# Déploiement avec docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d
```

---

## 8. Utilisation pratique

### Démarrage du projet

#### Prérequis
- Docker et Docker Compose
- Git
- Python 3.11 (pour les tests locaux)

#### Installation
```bash
# Clone du repository
git clone https://github.com/Beuleup93/airflow-etl-pipeline.git
cd airflow-etl-pipeline

# Démarrage des services
docker-compose up -d

# Vérification du statut
docker-compose ps
```

#### Accès aux interfaces
- **Airflow UI** : http://localhost:8080
- **pgAdmin** : http://localhost:5050
- **Base de données** : localhost:5432

### Exécution des DAGs

#### DAG ETL E-commerce
1. Accéder à l'interface Airflow
2. Activer le DAG `etl_ecommerce_pipeline`
3. Déclencher une exécution manuelle
4. Surveiller l'exécution dans le graph view

#### DAG de qualité des données
1. Activer le DAG `data_quality_dag`
2. Programmer l'exécution quotidienne
3. Consulter les rapports de qualité

#### DAG de monitoring
1. Activer le DAG `monitoring_dag`
2. Configurer les alertes
3. Surveiller les métriques

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
docker-compose logs airflow

# Logs de la base de données
docker-compose logs postgres

# Logs en temps réel
docker-compose logs -f airflow
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
docker-compose ps

# Test de connexion PostgreSQL
docker-compose exec postgres psql -U postgres -d ecommerce_db -c "SELECT 1;"

# Vérification des logs
docker-compose logs postgres
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
