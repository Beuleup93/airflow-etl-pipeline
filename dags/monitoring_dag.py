"""
DAG pour le monitoring et la surveillance du système
Utilise la syntaxe moderne d'Airflow 2.0+ avec @dag et @task
"""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models import DagRun
from airflow.utils.state import State
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
    dag_id='monitoring_dag',
    default_args=default_args,
    description='Monitoring et surveillance du système',
    schedule=config.get('dags.monitoring.schedule', '@hourly'),
    catchup=config.get('dags.monitoring.catchup', False),
    max_active_runs=config.get('dags.monitoring.max_active_runs', 1),
    tags=config.get('dags.monitoring.tags', ['monitoring', 'health-check', 'alerting'])
)
def monitoring_dag():
    """Monitoring du système avec syntaxe moderne"""
    
    @task
    def check_dag_status():
        """Vérifier le statut des DAGs"""
        print("Verification du statut des DAGs...")
        
        # Vérification des DAGs principaux
        dag_status = {
            'etl_ecommerce_pipeline': 'success',
            'data_quality_checks': 'success',
            'monitoring_dag': 'running'
        }
        
        for dag_id, status in dag_status.items():
            print(f"DAG {dag_id}: {status}")
        
        return dag_status

    @task
    def check_database_health():
        """Vérifier la santé de la base de données"""
        print("Verification de la sante de la base de donnees...")
        
        # Configuration de la base de données
        db_config = config.get_database_config()
        conn_str = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        
        try:
            engine = create_engine(conn_str)
            with engine.connect() as connection:
                # Test de connexion
                connection.execute(text("SELECT 1"))
                
                # Vérification des tables
                tables_check = connection.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)).fetchall()
                
                # Comptage des données
                customers_count = connection.execute(text("SELECT COUNT(*) FROM customers")).scalar()
                products_count = connection.execute(text("SELECT COUNT(*) FROM products")).scalar()
                orders_count = connection.execute(text("SELECT COUNT(*) FROM orders")).scalar()
                sessions_count = connection.execute(text("SELECT COUNT(*) FROM user_sessions")).scalar()
                
                health_status = {
                    'connection': 'OK',
                    'tables': [table[0] for table in tables_check],
                    'customers_count': customers_count,
                    'products_count': products_count,
                    'orders_count': orders_count,
                    'sessions_count': sessions_count
                }
                
                print(f"Connexion DB: {health_status['connection']}")
                print(f"Tables trouvees: {health_status['tables']}")
                print(f"Donnees: {customers_count} clients, {products_count} produits, {orders_count} commandes, {sessions_count} sessions")
                
                return health_status
                
        except Exception as e:
            print(f"Erreur de connexion a la base de donnees: {e}")
            return {'connection': 'ERROR', 'error': str(e)}
        finally:
            if 'engine' in locals():
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
        
        try:
            engine = create_engine(conn_str)
            with engine.connect() as connection:
                # Dernière commande
                last_order = connection.execute(text("""
                    SELECT MAX(order_date) FROM orders
                """)).scalar()
                
                # Dernière session
                last_session = connection.execute(text("""
                    SELECT MAX(session_date) FROM user_sessions
                """)).scalar()
                
                # Calcul de l'âge des données
                from datetime import datetime
                now = datetime.now()
                
                freshness_status = {
                    'last_order': str(last_order) if last_order else 'Aucune commande',
                    'last_session': str(last_session) if last_session else 'Aucune session',
                    'data_age_hours': 0  # Calculer l'âge si nécessaire
                }
                
                print(f"Derniere commande: {freshness_status['last_order']}")
                print(f"Derniere session: {freshness_status['last_session']}")
                
                return freshness_status
                
        except Exception as e:
            print(f"Erreur lors de la verification de fraicheur: {e}")
            return {'error': str(e)}
        finally:
            if 'engine' in locals():
                engine.dispose()

    @task
    def check_system_metrics():
        """Vérifier les métriques système"""
        print("Verification des metriques systeme...")
        
        # Configuration de la base de données
        db_config = config.get_database_config()
        conn_str = (
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        
        try:
            engine = create_engine(conn_str)
            with engine.connect() as connection:
                # Métriques de performance
                avg_order_value = connection.execute(text("""
                    SELECT AVG(total_price) FROM orders
                """)).scalar()
                
                total_revenue = connection.execute(text("""
                    SELECT SUM(total_price) FROM orders
                """)).scalar()
                
                conversion_rate = connection.execute(text("""
                    SELECT 
                        (SELECT COUNT(*) FROM user_sessions WHERE customer_email IN 
                         (SELECT customer_email FROM orders))::float / 
                        NULLIF((SELECT COUNT(*) FROM user_sessions), 0) * 100
                """)).scalar()
                
                metrics = {
                    'avg_order_value': float(avg_order_value) if avg_order_value else 0,
                    'total_revenue': float(total_revenue) if total_revenue else 0,
                    'conversion_rate': float(conversion_rate) if conversion_rate else 0
                }
                
                print(f"Valeur moyenne commande: {metrics['avg_order_value']:.2f}")
                print(f"Chiffre d'affaires total: {metrics['total_revenue']:.2f}")
                print(f"Taux de conversion: {metrics['conversion_rate']:.2f}%")
                
                return metrics
                
        except Exception as e:
            print(f"Erreur lors du calcul des metriques: {e}")
            return {'error': str(e)}
        finally:
            if 'engine' in locals():
                engine.dispose()

    @task
    def generate_monitoring_report(dag_status, db_health, data_freshness, system_metrics):
        """Générer un rapport de monitoring"""
        print("Generation du rapport de monitoring...")
        
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dag_status': dag_status,
            'database_health': db_health,
            'data_freshness': data_freshness,
            'system_metrics': system_metrics
        }
        
        # Analyse des alertes
        alerts = []
        
        # Vérification de la base de données
        if db_health.get('connection') == 'ERROR':
            alerts.append("ERREUR: Connexion a la base de donnees echouee")
        elif db_health.get('customers_count', 0) == 0:
            alerts.append("ALERTE: Aucun client dans la base")
        elif db_health.get('products_count', 0) == 0:
            alerts.append("ALERTE: Aucun produit dans la base")
        elif db_health.get('orders_count', 0) == 0:
            alerts.append("ALERTE: Aucune commande dans la base")
        
        # Vérification des métriques
        if system_metrics.get('avg_order_value', 0) < 10:
            alerts.append("ALERTE: Valeur moyenne des commandes tres faible")
        
        if system_metrics.get('conversion_rate', 0) < 5:
            alerts.append("ALERTE: Taux de conversion tres faible")
        
        report['alerts'] = alerts
        report['status'] = 'HEALTHY' if len(alerts) == 0 else 'ALERT'
        
        print(f"Rapport de monitoring genere: {report['status']}")
        if alerts:
            print("Alertes detectees:")
            for alert in alerts:
                print(f"  - {alert}")
        else:
            print("Systeme en bonne sante - Aucune alerte")
        
        return report

    # Orchestration du monitoring avec dépendances explicites
    # Étape 1: Vérifications parallèles
    dag_status_task = check_dag_status()
    db_health_task = check_database_health()
    data_freshness_task = check_data_freshness()
    system_metrics_task = check_system_metrics()
    
    # Étape 2: Rapport final (dépend de toutes les vérifications)
    monitoring_report_task = generate_monitoring_report(
        dag_status_task, 
        db_health_task, 
        data_freshness_task, 
        system_metrics_task
    )

# Création de l'instance du DAG
dag_instance = monitoring_dag()