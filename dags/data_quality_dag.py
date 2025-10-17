"""
DAG pour les contrôles de qualité des données
Utilise la syntaxe moderne d'Airflow 2.0+ avec @dag et @task
"""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
import sys
import os

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'include'))

from config_loader import config
import pandas as pd
from sqlalchemy import create_engine, text

# Configuration par défaut
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,  # Désactivé en développement
    'email_on_retry': False,    # Désactivé en développement
    'retries': config.get('retry.retries', 1),
    'retry_delay': timedelta(minutes=config.get('retry.retry_delay_minutes', 5)),
    'email': [config.get('notifications.email', 'beuleup2018@gmail.com')]
}

@dag(
    dag_id='data_quality_checks',
    default_args=default_args,
    description='Contrôles de qualité des données e-commerce',
    schedule=config.get('dags.data_quality.schedule', '@daily'),
    catchup=config.get('dags.data_quality.catchup', False),
    max_active_runs=config.get('dags.data_quality.max_active_runs', 1),
    tags=config.get('dags.data_quality.tags', ['data-quality', 'validation', 'monitoring'])
)
def data_quality_checks():
    """Contrôles de qualité des données avec syntaxe moderne"""
    
    @task
    def check_data_completeness():
        """Vérifier la complétude des données"""
        print("Verification de la completude des donnees...")
        
        # Configuration de la base de données
        db_config = config.get_database_config()
        conn_str = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        engine = create_engine(conn_str)
        
        try:
            # Vérification des comptes
            with engine.connect() as connection:
                # Comptage des enregistrements
                customers_count = connection.execute(text("SELECT COUNT(*) FROM customers")).scalar()
                products_count = connection.execute(text("SELECT COUNT(*) FROM products")).scalar()
                orders_count = connection.execute(text("SELECT COUNT(*) FROM orders")).scalar()
                sessions_count = connection.execute(text("SELECT COUNT(*) FROM user_sessions")).scalar()
                
                # Vérification des valeurs nulles
                customers_email_nulls = connection.execute(text("SELECT COUNT(*) FROM customers WHERE email IS NULL")).scalar()
                products_name_nulls = connection.execute(text("SELECT COUNT(*) FROM products WHERE name IS NULL")).scalar()
                orders_customer_email_nulls = connection.execute(text("SELECT COUNT(*) FROM orders WHERE customer_email IS NULL")).scalar()
                
                checks = {
                    'customers_count': customers_count,
                    'products_count': products_count,
                    'orders_count': orders_count,
                    'sessions_count': sessions_count,
                    'customers_email_nulls': customers_email_nulls,
                    'products_name_nulls': products_name_nulls,
                    'orders_customer_email_nulls': orders_customer_email_nulls
                }
                
                print(f"Table customers: {customers_count} enregistrements")
                print(f"Table products: {products_count} enregistrements")
                print(f"Table orders: {orders_count} enregistrements")
                print(f"Table user_sessions: {sessions_count} enregistrements")
                print(f"Emails clients nuls: {customers_email_nulls}")
                print(f"Noms produits nuls: {products_name_nulls}")
                print(f"Emails commandes nuls: {orders_customer_email_nulls}")
                
                return checks
                
        except Exception as e:
            print(f"Erreur lors de la verification: {e}")
            return {'error': str(e)}
        finally:
            engine.dispose()

    @task
    def check_data_consistency(completeness_results):
        """Vérifier la cohérence des données"""
        print("Verification de la coherence des donnees...")
        
        if 'error' in completeness_results:
            print("Erreur dans les resultats de completude, skip de la coherence")
            return {'error': 'Completeness check failed'}
        
        # Configuration de la base de données
        db_config = config.get_database_config()
        conn_str = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        engine = create_engine(conn_str)
        
        try:
            with engine.connect() as connection:
                # Vérification des emails valides
                invalid_emails = connection.execute(text("""
                    SELECT COUNT(*) FROM customers 
                    WHERE email NOT LIKE '%@%.%' OR email = ''
                """)).scalar()
                
                # Vérification des prix positifs
                negative_prices = connection.execute(text("""
                    SELECT COUNT(*) FROM products 
                    WHERE price < 0
                """)).scalar()
                
                # Vérification des quantités positives
                negative_quantities = connection.execute(text("""
                    SELECT COUNT(*) FROM orders 
                    WHERE quantity <= 0
                """)).scalar()
                
                # Vérification des sessions avec durée positive
                invalid_durations = connection.execute(text("""
                    SELECT COUNT(*) FROM user_sessions 
                    WHERE duration < 0
                """)).scalar()
                
                consistency_checks = {
                    'invalid_emails': invalid_emails,
                    'negative_prices': negative_prices,
                    'negative_quantities': negative_quantities,
                    'invalid_durations': invalid_durations
                }
                
                print(f"Emails invalides: {invalid_emails}")
                print(f"Prix negatifs: {negative_prices}")
                print(f"Quantites negatives: {negative_quantities}")
                print(f"Durees invalides: {invalid_durations}")
                
                return consistency_checks
                
        except Exception as e:
            print(f"Erreur lors de la verification de coherence: {e}")
            return {'error': str(e)}
        finally:
            engine.dispose()

    @task
    def check_data_freshness():
        """Vérifier la fraîcheur des données"""
        print("Verification de la fraicheur des donnees...")
        
        # Configuration de la base de données
        db_config = config.get_database_config()
        conn_str = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        engine = create_engine(conn_str)
        
        try:
            with engine.connect() as connection:
                # Vérification de la dernière mise à jour
                last_order_date = connection.execute(text("""
                    SELECT MAX(order_date) FROM orders
                """)).scalar()
                
                last_session_date = connection.execute(text("""
                    SELECT MAX(session_date) FROM user_sessions
                """)).scalar()
                
                freshness_checks = {
                    'last_order_date': str(last_order_date) if last_order_date else 'Aucune commande',
                    'last_session_date': str(last_session_date) if last_session_date else 'Aucune session'
                }
                
                print(f"Derniere commande: {freshness_checks['last_order_date']}")
                print(f"Derniere session: {freshness_checks['last_session_date']}")
                
                return freshness_checks
                
        except Exception as e:
            print(f"Erreur lors de la verification de fraicheur: {e}")
            return {'error': str(e)}
        finally:
            engine.dispose()

    @task
    def generate_quality_report(completeness_results, consistency_results, freshness_results):
        """Générer un rapport de qualité"""
        print("Generation du rapport de qualite...")
        
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completeness': completeness_results,
            'consistency': consistency_results,
            'freshness': freshness_results
        }
        
        # Analyse des résultats
        issues = []
        
        if 'error' not in completeness_results:
            if completeness_results.get('customers_count', 0) == 0:
                issues.append("Aucun client dans la base")
            if completeness_results.get('products_count', 0) == 0:
                issues.append("Aucun produit dans la base")
            if completeness_results.get('orders_count', 0) == 0:
                issues.append("Aucune commande dans la base")
            if completeness_results.get('customers_email_nulls', 0) > 0:
                issues.append(f"{completeness_results['customers_email_nulls']} emails clients nuls")
        
        if 'error' not in consistency_results:
            if consistency_results.get('invalid_emails', 0) > 0:
                issues.append(f"{consistency_results['invalid_emails']} emails invalides")
            if consistency_results.get('negative_prices', 0) > 0:
                issues.append(f"{consistency_results['negative_prices']} prix negatifs")
            if consistency_results.get('negative_quantities', 0) > 0:
                issues.append(f"{consistency_results['negative_quantities']} quantites negatives")
        
        report['issues'] = issues
        report['status'] = 'PASS' if len(issues) == 0 else 'FAIL'
        
        print(f"Rapport de qualite genere: {report['status']}")
        if issues:
            print("Problemes detectes:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Aucun probleme detecte - Qualite des donnees OK")
        
        return report

    # Orchestration des contrôles de qualité avec dépendances explicites
    # Étape 1: Vérifications parallèles
    completeness_task = check_data_completeness()
    freshness_task = check_data_freshness()
    
    # Étape 2: Vérification de cohérence (dépend de complétude)
    consistency_task = check_data_consistency(completeness_task)
    
    # Étape 3: Rapport final (dépend de toutes les vérifications)
    quality_report_task = generate_quality_report(completeness_task, consistency_task, freshness_task)
    
    # Définir les dépendances explicites
    completeness_task >> consistency_task >> quality_report_task
    freshness_task >> quality_report_task

# Création de l'instance du DAG
dag_instance = data_quality_checks()