# 📋 Configuration du Projet Airflow ETL

## 🎯 **Approche de Configuration Centralisée**

Ce projet utilise une approche de configuration centralisée avec un fichier YAML, ce qui est une **bonne pratique** en entreprise pour les projets Airflow.

## 📁 **Structure de Configuration**

```
airflow-etl/
├── config.yaml              # Configuration centralisée
├── include/
│   ├── config_loader.py     # Module de chargement de config
│   ├── extract.py           # Modules ETL
│   ├── transform.py
│   └── load.py
└── dags/
    ├── etl_ecommerce_dag.py # DAGs utilisant la config
    ├── data_quality_dag.py
    └── monitoring_dag.py
```

## 🔧 **Avantages de cette Approche**

### ✅ **Avantages :**
- **Configuration centralisée** : Un seul fichier pour toute la config
- **Facilité de maintenance** : Changements sans toucher au code
- **Environnements multiples** : Dev, Staging, Prod
- **Sécurité** : Séparation config/sensibles
- **Réutilisabilité** : Config partagée entre DAGs
- **Versioning** : Configuration versionnée avec le code

### 🏢 **Pratiques en Entreprise :**
- **Configuration par environnement** (dev/staging/prod)
- **Variables sensibles** dans des secrets managers
- **Validation** de la configuration au démarrage
- **Documentation** des paramètres

## 📝 **Utilisation dans les DAGs**

```python
from config_loader import config

# Récupération de configuration
db_config = config.get_database_config()
schedule = config.get('dags.etl_ecommerce.schedule', '@daily')
email = config.get('notifications.email')
```

## 🔄 **Alternatives Courantes**

### 1. **Variables Airflow**
```python
from airflow.models import Variable
db_host = Variable.get("db_host")
```

### 2. **Connexions Airflow**
```python
from airflow.hooks.base import BaseHook
conn = BaseHook.get_connection("postgres_default")
```

### 3. **Fichiers .env**
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. **Configuration par DAG**
```python
# Dans chaque DAG
DAG_CONFIG = {
    'schedule': '@daily',
    'retries': 1
}
```

## 🚀 **Bonnes Pratiques**

1. **Validation** : Vérifier la config au démarrage
2. **Documentation** : Commenter chaque paramètre
3. **Valeurs par défaut** : Toujours fournir des fallbacks
4. **Sécurité** : Ne jamais commiter de secrets
5. **Environnements** : Config différente par environnement

## 📊 **Comparaison des Approches**

| Approche | Complexité | Flexibilité | Sécurité | Maintenance |
|----------|-------------|-------------|----------|-------------|
| **YAML Config** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Variables Airflow | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Connexions | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ |
| Fichiers .env | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |

## 🎯 **Recommandation**

Pour un projet professionnel, l'approche **YAML + ConfigLoader** est recommandée car elle offre :
- **Flexibilité** maximale
- **Maintenabilité** élevée  
- **Sécurité** appropriée
- **Réutilisabilité** entre DAGs
