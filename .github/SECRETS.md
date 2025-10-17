# Configuration des Secrets GitHub

Ce document explique comment configurer les secrets nécessaires pour le déploiement automatique.

## 🔐 Secrets requis

### **1. Secrets de base (obligatoires)**
- `GITHUB_TOKEN` : Token GitHub (automatique)
- `SLACK_WEBHOOK` : Webhook Slack pour les notifications (optionnel)

### **2. Secrets de base de données (production)**
- `DB_HOST` : Adresse de la base de données
- `DB_PORT` : Port de la base de données
- `DB_NAME` : Nom de la base de données
- `DB_USER` : Utilisateur de la base de données
- `DB_PASSWORD` : Mot de passe de la base de données

### **3. Secrets de déploiement (production)**
- `DEPLOY_HOST` : Serveur de déploiement
- `DEPLOY_USER` : Utilisateur de déploiement
- `DEPLOY_KEY` : Clé SSH pour le déploiement
- `DOCKER_REGISTRY` : Registre Docker
- `DOCKER_USERNAME` : Nom d'utilisateur Docker
- `DOCKER_PASSWORD` : Mot de passe Docker

### **4. Secrets de monitoring (optionnel)**
- `GRAFANA_API_KEY` : Clé API Grafana
- `PROMETHEUS_URL` : URL Prometheus
- `ALERTMANAGER_URL` : URL AlertManager

## 📋 Configuration des secrets

### **Étape 1 : Accéder aux paramètres du repository**
1. Allez sur votre repository GitHub
2. Cliquez sur "Settings"
3. Dans le menu de gauche, cliquez sur "Secrets and variables"
4. Cliquez sur "Actions"

### **Étape 2 : Ajouter les secrets**
1. Cliquez sur "New repository secret"
2. Entrez le nom du secret (ex: `DB_PASSWORD`)
3. Entrez la valeur du secret
4. Cliquez sur "Add secret"

### **Étape 3 : Vérifier les secrets**
Les secrets sont automatiquement disponibles dans les workflows GitHub Actions via `${{ secrets.SECRET_NAME }}`

## 🔒 Bonnes pratiques de sécurité

### **1. Rotation des secrets**
- Changez régulièrement les mots de passe
- Utilisez des tokens avec expiration
- Surveillez l'utilisation des secrets

### **2. Accès minimal**
- Donnez seulement les permissions nécessaires
- Utilisez des tokens spécifiques par service
- Limitez l'accès par environnement

### **3. Audit et monitoring**
- Surveillez les accès aux secrets
- Loggez les utilisations sensibles
- Configurez des alertes de sécurité

## 🚨 Dépannage

### **Problème : Secret non trouvé**
```bash
Error: Secret 'DB_PASSWORD' not found
```
**Solution :** Vérifiez que le secret est bien configuré dans GitHub

### **Problème : Permission refusée**
```bash
Error: Permission denied
```
**Solution :** Vérifiez les permissions du token GitHub

### **Problème : Connexion échouée**
```bash
Error: Connection failed
```
**Solution :** Vérifiez les credentials de la base de données

## 📞 Support

Pour toute question sur la configuration des secrets :
1. Consultez la documentation GitHub Actions
2. Vérifiez les logs de déploiement
3. Contactez l'équipe DevOps
