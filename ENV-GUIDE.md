# 🔐 Guide des Variables d'Environnement

## 🎯 **Approche Hybride : YAML + .env**

Ce projet utilise une **approche hybride** recommandée en entreprise :
- **`config.yaml`** : Configuration générale et non-sensible
- **`.env`** : Variables sensibles (mots de passe, clés API, etc.)

## 📁 **Structure de Configuration**

```
airflow-etl/
├── config.yaml          # Configuration générale
├── .env                 # Variables sensibles (NE PAS COMMITER)
├── env.example          # Exemple de variables d'environnement
└── include/
    └── config_loader.py # Chargeur hybride
```

## 🔧 **Utilisation**

### 1. **Créer le fichier .env**
```bash
# Copier l'exemple
cp env.example .env

# Modifier les valeurs sensibles
nano .env
```

### 2. **Variables d'environnement disponibles**
```bash
# Base de données
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=postgres

# Notifications
NOTIFICATION_EMAIL=beuleup2018@gmail.com

# APIs
FAKE_STORE_API_URL=https://fakestoreapi.com
API_TIMEOUT=30
API_MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO

# Environnement
ENVIRONMENT=development
```

## 🏢 **Avantages de cette Approche**

### ✅ **Sécurité**
- **Variables sensibles** dans `.env` (non commitées)
- **Configuration générale** dans `config.yaml` (versionnée)
- **Séparation** claire des responsabilités

### ✅ **Flexibilité**
- **Environnements multiples** : dev, staging, prod
- **Surcharge** des valeurs par environnement
- **Fallback** vers les valeurs YAML

### ✅ **Maintenance**
- **Un seul endroit** pour les variables sensibles
- **Documentation** des variables nécessaires
- **Validation** des variables au démarrage

## 🔄 **Ordre de Priorité**

1. **Variables d'environnement** (`.env` ou système)
2. **Fichier YAML** (`config.yaml`)
3. **Valeurs par défaut** (dans le code)

## 🚀 **Exemples d'Utilisation**

### **Environnement de Développement**
```bash
# .env
DB_HOST=localhost
DB_PASSWORD=dev_password
ENVIRONMENT=development
```

### **Environnement de Production**
```bash
# .env
DB_HOST=prod-db.company.com
DB_PASSWORD=super_secure_password
ENVIRONMENT=production
```

## 🛡️ **Bonnes Pratiques**

### ✅ **À FAIRE**
- Utiliser `.env` pour les secrets
- Documenter toutes les variables
- Fournir des valeurs par défaut
- Valider les variables au démarrage

### ❌ **À ÉVITER**
- Commiter le fichier `.env`
- Hardcoder des secrets dans le code
- Oublier de documenter les variables
- Utiliser des valeurs de production en dev

## 📊 **Comparaison des Approches**

| Approche | Sécurité | Flexibilité | Maintenance | Complexité |
|----------|-----------|-------------|-------------|------------|
| **YAML seul** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **.env seul** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| **YAML + .env** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 **Recommandation**

L'approche **YAML + .env** est la **meilleure pratique** car elle combine :
- **Sécurité** maximale pour les secrets
- **Flexibilité** pour les environnements
- **Maintenabilité** élevée
- **Séparation** claire des responsabilités
