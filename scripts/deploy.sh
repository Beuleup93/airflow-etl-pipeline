#!/bin/bash

# Script de déploiement pour le projet Airflow ETL
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
IMAGE_TAG=${2:-latest}

echo "🚀 Déploiement du projet Airflow ETL"
echo "Environment: $ENVIRONMENT"
echo "Image Tag: $IMAGE_TAG"

# Fonction pour afficher les messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérifier Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker n'est pas installé"
        exit 1
    fi
    
    # Vérifier Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose n'est pas installé"
        exit 1
    fi
    
    log "✅ Prérequis vérifiés"
}

# Build de l'image Docker
build_image() {
    log "Construction de l'image Docker..."
    
    docker build -t airflow-etl:$IMAGE_TAG .
    
    if [ $? -eq 0 ]; then
        log "✅ Image construite avec succès"
    else
        log "❌ Échec de la construction de l'image"
        exit 1
    fi
}

# Déploiement en production
deploy_production() {
    log "Déploiement en production..."
    
    # Arrêter les services existants
    docker-compose -f docker-compose.prod.yml down
    
    # Démarrer les services
    docker-compose -f docker-compose.prod.yml up -d
    
    # Attendre que les services soient prêts
    log "Attente du démarrage des services..."
    sleep 30
    
    # Vérifier le statut des services
    docker-compose -f docker-compose.prod.yml ps
    
    log "✅ Déploiement en production terminé"
}

# Déploiement en développement
deploy_development() {
    log "Déploiement en développement..."
    
    # Utiliser docker-compose standard
    docker-compose down
    docker-compose up -d
    
    log "✅ Déploiement en développement terminé"
}

# Tests de santé
health_check() {
    log "Vérification de la santé des services..."
    
    # Vérifier PostgreSQL
    if docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres; then
        log "✅ PostgreSQL est opérationnel"
    else
        log "❌ PostgreSQL n'est pas accessible"
        exit 1
    fi
    
    # Vérifier Airflow Webserver
    if curl -f http://localhost:8080/health > /dev/null 2>&1; then
        log "✅ Airflow Webserver est opérationnel"
    else
        log "❌ Airflow Webserver n'est pas accessible"
        exit 1
    fi
    
    log "✅ Tous les services sont opérationnels"
}

# Nettoyage
cleanup() {
    log "Nettoyage des ressources..."
    
    # Supprimer les images inutilisées
    docker image prune -f
    
    # Supprimer les volumes inutilisés
    docker volume prune -f
    
    log "✅ Nettoyage terminé"
}

# Fonction principale
main() {
    log "Début du déploiement"
    
    check_prerequisites
    build_image
    
    case $ENVIRONMENT in
        "production")
            deploy_production
            ;;
        "development")
            deploy_development
            ;;
        *)
            echo "❌ Environment non supporté: $ENVIRONMENT"
            echo "Usage: $0 [production|development] [image_tag]"
            exit 1
            ;;
    esac
    
    health_check
    cleanup
    
    log "🎉 Déploiement terminé avec succès !"
    log "🌐 Airflow UI: http://localhost:8080"
    log "🗄️ pgAdmin: http://localhost:5050"
}

# Exécution
main "$@"
