# Makefile pour le projet Airflow ETL

.PHONY: help test test-unit test-integration test-coverage test-fast clean install lint format

# Aide
help:
	@echo "Commandes disponibles pour les tests:"
	@echo ""
	@echo "  make test              - Exécuter tous les tests"
	@echo "  make test-unit         - Exécuter les tests unitaires"
	@echo "  make test-integration  - Exécuter les tests d'intégration"
	@echo "  make test-coverage     - Exécuter les tests avec couverture"
	@echo "  make test-fast         - Exécuter les tests rapides"
	@echo "  make clean             - Nettoyer les fichiers temporaires"
	@echo "  make install           - Installer les dépendances"
	@echo "  make lint              - Vérifier le code avec flake8"
	@echo "  make format            - Formater le code avec black"
	@echo ""

# Tests
test:
	@echo "Execution de tous les tests..."
	./venv/bin/python scripts/run_tests.py

test-unit:
	@echo "Execution des tests unitaires..."
	./venv/bin/python scripts/run_tests.py --unit

test-integration:
	@echo "Execution des tests d'integration..."
	./venv/bin/python scripts/run_tests.py --integration

test-coverage:
	@echo "Execution des tests avec couverture..."
	./venv/bin/python scripts/run_tests.py --coverage

test-fast:
	@echo "Execution des tests rapides..."
	./venv/bin/python scripts/run_tests.py --fast

# Installation
install:
	@echo "Installation des dependances..."
	./venv/bin/pip install -r requirements.txt
	./venv/bin/pip install pytest pytest-cov flake8 black

# Linting
lint:
	@echo "Verification du code avec flake8..."
	./venv/bin/flake8 include/ dags/ tests/ --max-line-length=100 --ignore=E203,W503

# Formatage
format:
	@echo "Formatage du code avec black..."
	./venv/bin/black include/ dags/ tests/ --line-length=100

# Nettoyage
clean:
	@echo "Nettoyage des fichiers temporaires..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete

# Tests avec Airflow
test-airflow:
	@echo "Tests avec Airflow..."
	astro dev bash -c "python -m pytest tests/ -v"

# Validation des DAGs
validate-dags:
	@echo "Validation des DAGs..."
	astro dev bash -c "python dags/etl_ecommerce_dag.py"
	astro dev bash -c "python dags/data_quality_dag.py"
	astro dev bash -c "python dags/monitoring_dag.py"

# Démarrage d'Airflow
start-airflow:
	@echo "Demarrage d'Airflow..."
	astro dev start

# Arrêt d'Airflow
stop-airflow:
	@echo "Arret d'Airflow..."
	astro dev stop

# Redémarrage d'Airflow
restart-airflow:
	@echo "Redemarrage d'Airflow..."
	astro dev stop
	astro dev start

# Statut d'Airflow
status-airflow:
	@echo "Statut d'Airflow..."
	astro dev ps

# Déploiement
deploy-dev:
	@echo "Deploiement en developpement..."
	@./scripts/deploy.sh development

deploy-prod:
	@echo "Deploiement en production..."
	@./scripts/deploy.sh production

# Docker
build:
	@echo "Construction de l'image Docker..."
	@docker build -t airflow-etl:latest .

run:
	@echo "Demarrage des services..."
	@docker-compose up -d

stop:
	@echo "Arret des services..."
	@docker-compose down

logs:
	@echo "Affichage des logs..."
	@docker-compose logs -f

# Nettoyage Docker
clean-docker:
	@echo "Nettoyage des ressources Docker..."
	@docker system prune -f
	@docker volume prune -f

# Validation
validate:
	@echo "Validation des DAGs..."
	@./venv/bin/python scripts/validate_dags.py
