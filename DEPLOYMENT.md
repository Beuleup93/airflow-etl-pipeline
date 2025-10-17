# Guide de Déploiement - Airflow ETL Pipeline

Ce guide explique comment déployer le projet Airflow ETL en utilisant Astro CLI pour le développement et Docker Compose pour la production.

## Déploiement

### 1. Développement avec Astro CLI

Le développement se fait avec Astro CLI qui fournit automatiquement PostgreSQL et Airflow :

#### Démarrage
```bash
astro dev start
```

#### Services fournis automatiquement
- PostgreSQL (service `postgres`)
- Airflow Scheduler
- Airflow API Server (port 8080)
- Airflow DAG Processor
- Airflow Triggerer
### 2. Production avec Docker Compose

Pour la production, utilisez Docker Compose avec les fichiers fournis :

#### Démarrage production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### Services de production
- PostgreSQL avec pgAdmin
- Airflow Webserver
- Airflow Scheduler
- Volumes persistants pour les données

Avant le premier déploiement, configurez les secrets GitHub :

```bash
# Secrets obligatoires
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your-secure-password

# Secrets optionnels
SLACK_WEBHOOK=your-slack-webhook-url
DOCKER_REGISTRY=your-registry
DOCKER_USERNAME=your-username
DOCKER_PASSWORD=your-password
```

## 🐳 **Déploiement Local**

### **1. Déploiement en développement**

```bash
# Cloner le repository
git clone <your-repo-url>
cd airflow-etl

# Démarrer les services
docker-compose up -d

# Vérifier le statut
docker-compose ps
```

### **2. Déploiement en production**

```bash
# Utiliser le script de déploiement
./scripts/deploy.sh production

# Ou utiliser docker-compose directement
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 **Configuration des Environnements**

### **1. Variables d'environnement**

#### **Développement**
```bash
# .env.development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=postgres
AIRFLOW_ENV=development
```

#### **Production**
```bash
# .env.production
DB_HOST=prod-db-host
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=prod_user
DB_PASSWORD=secure_prod_password
AIRFLOW_ENV=production
```

### **2. Configuration Docker**

#### **Dockerfile**
- Image de base : `apache/airflow:2.8.1-python3.11`
- Dépendances : Installées via `requirements.txt`
- Configuration : Copiée depuis le repository
- Ports : 8080 (Airflow), 5432 (PostgreSQL)

#### **Docker Compose**
- **Services** : PostgreSQL, Airflow Webserver, Airflow Scheduler
- **Volumes** : DAGs, logs, données
- **Réseau** : Communication inter-services
- **Santé** : Health checks automatiques

## 📊 **Monitoring et Observabilité**

### **1. Endpoints de santé**

#### **Airflow**
- **UI** : http://localhost:8080
- **Health** : http://localhost:8080/health
- **API** : http://localhost:8080/api/v1/health

#### **PostgreSQL**
- **Port** : 5432
- **Health** : `pg_isready -U postgres`

#### **pgAdmin**
- **UI** : http://localhost:5050
- **Admin** : admin@example.com / admin

### **2. Logs et Monitoring**

#### **Logs Airflow**
```bash
# Voir les logs
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler

# Logs en temps réel 
docker-compose logs -f airflow-webserver
```

#### **Logs PostgreSQL**
```bash
# Voir les logs
docker-compose logs postgres
```

## 🔄 **Rollback et Récupération**

### **1. Rollback automatique**

```bash
# Via GitHub Actions
# 1. Allez sur l'onglet "Actions"
# 2. Sélectionnez "Rollback Deployment"
# 3. Cliquez sur "Run workflow"
# 4. Choisissez l'environnement et la version
```

### **2. Rollback manuel**

```bash
# Arrêter les services
docker-compose down

# Récupérer une version précédente
git checkout <previous-commit>

# Redémarrer avec la version précédente
docker-compose up -d
```

## 🚨 **Dépannage**

### **1. Problèmes courants**

#### **Service non accessible**
```bash
# Vérifier le statut
docker-compose ps

# Redémarrer un service
docker-compose restart airflow-webserver
```

#### **Base de données non accessible**
```bash
# Vérifier la connexion
docker-compose exec postgres pg_isready -U postgres

# Voir les logs
docker-compose logs postgres
```

#### **DAGs non chargés**
```bash
# Vérifier les DAGs
docker-compose exec airflow-webserver airflow dags list

# Forcer le rechargement
docker-compose restart airflow-webserver
```

### **2. Logs de débogage**

```bash
# Logs détaillés
docker-compose logs --tail=100 airflow-webserver

# Logs en temps réel
docker-compose logs -f airflow-scheduler
```

## 📈 **Optimisations**

### **1. Performance**

#### **Ressources**
- **CPU** : Minimum 2 cores
- **RAM** : Minimum 4GB
- **Stockage** : Minimum 20GB

#### **Configuration**
```yaml
# docker-compose.prod.yml
services:
  airflow-webserver:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### **2. Sécurité**

#### **Secrets**
- Utilisez des secrets GitHub
- Chiffrez les données sensibles
- Rotation régulière des mots de passe

#### **Réseau**
- Limitez l'accès aux ports
- Utilisez des réseaux privés
- Configurez des firewalls

## 📞 **Support**

### **1. Documentation**
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose](https://docs.docker.com/compose/)
- [GitHub Actions](https://docs.github.com/en/actions)

### **2. Contact**
- **Issues** : Créez une issue sur GitHub
- **Discussions** : Utilisez les discussions GitHub
- **Email** : beuleup2018@gmail.com

---

**🎉 Félicitations ! Votre pipeline Airflow ETL est maintenant prêt pour le déploiement automatique !**
