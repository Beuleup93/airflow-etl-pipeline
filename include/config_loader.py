"""
Module de chargement de la configuration
Charge le fichier config.yaml et les variables d'environnement
Fournit un accès centralisé à la configuration
"""
import yaml
import os
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    """Classe pour charger et gérer la configuration du projet"""
    
    def __init__(self, config_path: str = None):
        """
        Initialise le chargeur de configuration
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        if config_path is None:
            # Chemin par défaut : remonte de 2 niveaux depuis le dossier dags
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '..', 'config.yaml')
        
        self.config_path = config_path
        self._config = None
        
        # Chargement des variables d'environnement
        self._load_env_variables()
        
        # Chargement de la configuration YAML
        self._load_config()
    
    def _load_env_variables(self):
        """Charge les variables d'environnement depuis le fichier .env"""
        try:
            # Cherche le fichier .env dans le répertoire du projet
            current_dir = os.path.dirname(os.path.abspath(__file__))
            env_path = os.path.join(current_dir, '..', '.env')
            load_dotenv(env_path)
            print(f"Variables d'environnement chargées depuis: {env_path}")
        except Exception as e:
            print(f"Fichier .env non trouvé ou erreur de chargement: {e}")
    
    def _load_config(self):
        """Charge le fichier de configuration YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
            print(f"Configuration chargée depuis: {self.config_path}")
        except FileNotFoundError:
            print(f"Fichier de configuration non trouvé: {self.config_path}")
            self._config = {}
        except yaml.YAMLError as e:
            print(f"Erreur lors du chargement du fichier YAML: {e}")
            self._config = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration
        
        Args:
            key: Clé de configuration (support des clés imbriquées avec '.')
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            Valeur de configuration ou valeur par défaut
        """
        if self._config is None:
            return default
        
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_database_config(self) -> Dict[str, Any]:
        """Récupère la configuration de la base de données"""
        # Priorité aux variables d'environnement, puis au fichier YAML
        return {
            'host': os.getenv('DB_HOST', self.get('database.host', 'localhost')),
            'port': int(os.getenv('DB_PORT', self.get('database.port', 5432))),
            'database': os.getenv('DB_NAME', self.get('database.database', 'ecommerce_db')),
            'user': os.getenv('DB_USER', self.get('database.user', 'dataengineer')),
            'password': os.getenv('DB_PASSWORD', self.get('database.password', 'dataengineer123'))
        }
    
    def get_data_paths(self) -> Dict[str, str]:
        """Récupère les chemins des données"""
        return self.get('data_paths', {})
    
    def get_dag_config(self, dag_name: str) -> Dict[str, Any]:
        """Récupère la configuration d'un DAG spécifique"""
        return self.get(f'dags.{dag_name}', {})
    
    def get_notification_config(self) -> Dict[str, Any]:
        """Récupère la configuration des notifications"""
        return {
            'email': os.getenv('NOTIFICATION_EMAIL', self.get('notifications.email', 'beuleup2018@gmail.com')),
            'on_failure': self.get('notifications.on_failure', True),
            'on_retry': self.get('notifications.on_retry', False),
            'on_success': self.get('notifications.on_success', False)
        }
    
    def get_retry_config(self) -> Dict[str, Any]:
        """Récupère la configuration des retry"""
        return self.get('retry', {})
    
    def get_api_config(self, api_name: str) -> Dict[str, Any]:
        """Récupère la configuration d'une API spécifique"""
        return self.get(f'apis.{api_name}', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Récupère la configuration des logs"""
        return {
            'level': os.getenv('LOG_LEVEL', self.get('logging.level', 'INFO')),
            'file': os.getenv('LOG_FILE', self.get('logging.file', './logs/etl_pipeline.log'))
        }
    
    def get_etl_config(self) -> Dict[str, Any]:
        """Récupère la configuration ETL"""
        return {
            'batch_size': int(os.getenv('BATCH_SIZE', self.get('etl.batch_size', 1000))),
            'max_retries': int(os.getenv('MAX_RETRIES', self.get('etl.max_retries', 3))),
            'retry_delay': int(os.getenv('RETRY_DELAY', self.get('etl.retry_delay', 5)))
        }
    
    def get_file_paths(self) -> Dict[str, str]:
        """Récupère les chemins des fichiers"""
        return {
            'raw_data_path': os.getenv('RAW_DATA_PATH', self.get('data_paths.raw_data_dir', './data/raw')),
            'processed_data_path': os.getenv('PROCESSED_DATA_PATH', self.get('data_paths.processed_data_dir', './data/processed')),
            'output_data_path': os.getenv('OUTPUT_DATA_PATH', self.get('data_paths.output_data_dir', './data/output'))
        }


# Instance globale de configuration
config = ConfigLoader()
