"""
DAG pour orchestrer le pipeline ETL e-commerce
Utilise la syntaxe moderne d'Airflow 2.0+ avec @dag et @task
"""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
import sys
import os

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'include'))

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader
from config_loader import config

# Configuration par défaut depuis le fichier config.yaml
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
    dag_id='etl_ecommerce_pipeline',
    default_args=default_args,
    description='Pipeline ETL pour données e-commerce',
    schedule=config.get('dags.etl_ecommerce.schedule', '@daily'),
    catchup=config.get('dags.etl_ecommerce.catchup', False),
    max_active_runs=config.get('dags.etl_ecommerce.max_active_runs', 1),
    tags=config.get('dags.etl_ecommerce.tags', ['etl', 'ecommerce'])
)
def etl_ecommerce_pipeline():
    """Pipeline ETL e-commerce avec syntaxe moderne"""
    
    @task
    def extract_data():
        """Extraction de toutes les données"""
        print("Debut de l'extraction des donnees...")
        
        # Configuration des chemins depuis le fichier .env
        file_paths = config.get_file_paths()
        csv_path = os.path.join(file_paths['raw_data_path'], 'orders.csv')
        json_path = os.path.join(file_paths['raw_data_path'], 'user_sessions.json')
        
        # Extraction avec notre module
        extractor = DataExtractor()
        raw_data = extractor.extract_all_data(csv_path, json_path)
        
        print(f"Extraction terminee: {raw_data['extraction_summary']}")
        return raw_data

    @task
    def transform_data(raw_data):
        """Transformation et nettoyage des données"""
        print("Debut de la transformation des donnees...")
        
        # Transformation avec notre module (utilise les données d'extract)
        transformer = DataTransformer()
        transformed_data = transformer.transform_all_data(raw_data)
        
        print(f"Transformation terminee: {transformed_data['transformation_summary']}")
        return transformed_data

    @task
    def load_data(transformed_data):
        """Chargement des données dans PostgreSQL"""
        print("Debut du chargement des donnees...")
        
        # Configuration de la base de données depuis le fichier config.yaml
        db_config = config.get_database_config()
        
        # Chargement avec notre module (utilise les données de transform)
        loader = DataLoader(db_config)
        load_result = loader.load_all_data(transformed_data)
        
        if load_result['success']:
            print(f"Chargement reussi: {load_result['summary']}")
        else:
            print(f"Erreur de chargement: {load_result['error']}")
        
        # Fermeture de la connexion
        loader.close_connection()
        
        return load_result

    @task
    def send_notification(load_result):
        """Notification de fin de pipeline (simulation)"""
        print("Notification de fin de pipeline...")
        
        # Vérification du résultat du chargement
        if load_result.get('success', False):
            message = f"""
            Pipeline ETL termine avec succes !
            
            Resultats :
            - {load_result.get('loaded_products', 0)} produits charges
            - {load_result.get('loaded_orders', 0)} commandes chargees
            - {load_result.get('loaded_sessions', 0)} sessions chargees
            
            Heure de fin : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
        else:
            message = f"""
            Pipeline ETL termine avec des erreurs !
            
            Erreur : {load_result.get('error', 'Erreur inconnue')}
            
            Heure de fin : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
        
        print(message)
        print("Notification simulee (pas d'envoi email en developpement)")
        return "notification_sent"

    # Orchestration du pipeline avec transfert de données
    # Étape 1: Extraction
    raw_data = extract_data()
    
    # Étape 2: Transformation (utilise les données d'extract)
    transformed_data = transform_data(raw_data)
    
    # Étape 3: Chargement (utilise les données de transform)
    load_result = load_data(transformed_data)
    
    # Étape 4: Notification (utilise le résultat de load)
    send_notification(load_result)

# Création de l'instance du DAG
dag_instance = etl_ecommerce_pipeline()