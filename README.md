# Projet 2 - Orchestration ETL avec Apache Airflow

Ce projet implémente l'orchestration du pipeline ETL e-commerce en utilisant Apache Airflow avec la syntaxe moderne.

## Objectifs

- **Orchestration** : Automatiser l'exécution du pipeline ETL
- **Monitoring** : Surveiller les performances et les erreurs
- **Scheduling** : Planifier l'exécution des tâches
- **Alerting** : Notifications en cas d'échec
- **Data Quality** : Contrôles de qualité automatisés

## Architecture

```
airflow-etl/
├── dags/                          # DAGs Airflow
│   ├── etl_ecommerce_dag.py      # DAG principal ETL
│   ├── data_quality_dag.py        # DAG contrôles qualité
│   ├── monitoring_dag.py          # DAG monitoring
│   └── exampledag.py              # DAG d'exemple Astro
├── airflow_settings.yaml          # Configuration Airflow
├── requirements.txt               # Dépendances Python
└── README.md                     # Documentation
```

## Technologies

- **Apache Airflow 2.8.1** : Orchestrateur de workflows
- **Astro CLI** : Outil de gestion Airflow moderne
- **PostgreSQL** : Base de données (fournie par Astro CLI)
- **Python 3.11** : Langage de programmation
- **Docker** : Containerisation (pour la production)

## Installation et Démarrage

### Prérequis
- Astro CLI installé
- Git

### Étapes

1. **Démarrer Airflow**
   ```bash
   cd airflow-etl
   astro dev start
   ```

2. **Accéder à l'interface Airflow**
   - URL : http://localhost:8080
   - Login : admin
   - Password : admin

3. **Activer les DAGs**
   - Aller dans l'interface Airflow
   - Activer `etl_ecommerce_pipeline`
   - Activer `data_quality_checks`
   - Activer `monitoring_dag`

4. **Exécution des DAGs**
   - **Exécution manuelle** : Cliquer sur "Trigger" pour lancer immédiatement
   - **Exécution automatique** : Les DAGs s'exécutent selon leur schedule configuré
   - **Monitoring** : Surveiller l'exécution dans l'interface Airflow

## DAGs Disponibles

### 1. ETL E-commerce Pipeline (`etl_ecommerce_pipeline`)
- **Schedule** : `@daily` (quotidien)
- **Tâches** :
  - `extract_data` : Extraction des données (API, CSV, JSON)
  - `transform_data` : Transformation et nettoyage
  - `load_data` : Chargement PostgreSQL
  - `send_notification` : Notification de fin
- **Dépendances** : Extraction → Transformation → Chargement → Notification

### 2. Data Quality Checks (`data_quality_checks`)
- **Schedule** : `@daily` (quotidien)
- **Tâches** :
  - `check_data_completeness` : Vérification complétude
  - `check_data_consistency` : Vérification cohérence
  - `check_data_freshness` : Vérification fraîcheur
  - `generate_quality_report` : Rapport de qualité
- **Dépendances** : Vérifications en parallèle → Rapport

### 3. Monitoring (`monitoring_dag`)
- **Schedule** : `@hourly` (toutes les heures)
- **Tâches** :
  - `check_system_metrics` : Métriques système
  - `check_dag_status` : Statut des DAGs
  - `check_data_freshness` : Fraîcheur des données
  - `check_database_health` : Santé de la DB
  - `generate_monitoring_report` : Rapport de monitoring
- **Dépendances** : Vérifications en parallèle → Rapport

## Fonctionnalités

### Syntaxe Moderne Airflow 2.0+
- **`@dag`** : Décorateur pour définir les DAGs
- **`@task`** : Décorateur pour définir les tâches
- **Dépendances automatiques** : Gérées par les paramètres des fonctions
- **XCom automatique** : Partage de données entre tâches

### Monitoring et Alerting
- **Vérifications de santé** : Base de données, système, DAGs
- **Rapports automatiques** : Qualité des données, santé du système
- **Notifications** : Email en cas d'échec

### Qualité des Données
- **Complétude** : Vérification des données manquantes
- **Cohérence** : Vérification des relations entre tables
- **Qualité** : Validation des formats et valeurs

## Concepts Appris

- **DAGs** : Directed Acyclic Graphs
- **Tasks** : Unités de travail atomiques
- **Scheduling** : Planification des exécutions
- **XCom** : Partage de données entre tâches
- **Monitoring** : Surveillance des performances
- **Data Quality** : Contrôles automatisés
- **Syntaxe moderne** : `@dag` et `@task` decorators

## Tests

```bash
# Tests des DAGs
python scripts/validate_dags.py

# Tests unitaires
pytest tests/
```

## Prochaines Étapes

- **Projet 3** : AWS Cloud (S3, Glue, EMR)
- **Projet 4** : Databricks et Spark
- **Projet 5** : dbt et Snowflake
- **Projet 6** : Data Governance
- **Projet 7** : DevOps et DataOps
- **Projet 8** : Monitoring avec Grafana
- **Projet 9** : Projet final intégré

## Support

Pour toute question ou problème, consultez la documentation Airflow ou ouvrez une issue.