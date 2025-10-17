"""
Module de chargement des données pour Airflow
Reproduit la même logique que le Projet 1
"""
import pandas as pd
from typing import Dict, List, Any
from sqlalchemy import create_engine, text
import psycopg2
from psycopg2.extras import RealDictCursor


class DataLoader:
    """Classe pour le chargement des données dans PostgreSQL"""
    
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.engine = None
        self.connection = None
    
    def connect_to_database(self):
        """Connexion à la base de données PostgreSQL"""
        try:
            # Connexion SQLAlchemy
            connection_string = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            self.engine = create_engine(connection_string)
            
            # Connexion psycopg2 pour les requêtes directes
            self.connection = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            
            print("Connexion a la base de donnees etablie")
            return True
        except Exception as e:
            print(f"Erreur de connexion a la base de donnees: {e}")
            return False
    
    def clean_all_tables(self):
        """Nettoyage de toutes les tables (idempotence)"""
        print("Nettoyage des tables existantes...")
        
        try:
            with self.connection.cursor() as cursor:
                # Désactiver les contraintes de clé étrangère temporairement
                cursor.execute("SET session_replication_role = replica;")
                
                # Nettoyage des tables dans l'ordre inverse des dépendances
                tables_to_clean = ['user_sessions', 'orders', 'products', 'customers']
                for table in tables_to_clean:
                    cursor.execute(f"DELETE FROM {table};")
                    print(f"Table {table} nettoyee")
                
                # Réactiver les contraintes
                cursor.execute("SET session_replication_role = DEFAULT;")
                self.connection.commit()
                
            print("Nettoyage des tables termine")
            return True
        except Exception as e:
            print(f"Erreur lors du nettoyage: {e}")
            return False
    
    def load_customers(self, orders: List[Dict[str, Any]], sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chargement des clients (extraction des emails uniques)"""
        print("Chargement des clients...")
        print(f"Nombre de commandes recues: {len(orders)}")
        print(f"Nombre de sessions recues: {len(sessions)}")
        
        # Extraction des emails uniques
        emails = set()
        for order in orders:
            if order.get('customer_email'):
                emails.add(order['customer_email'])
        for session in sessions:
            if session.get('customer_email'):
                emails.add(session['customer_email'])
        
        print(f"Emails uniques trouves: {len(emails)}")
        print(f"Emails: {list(emails)}")
        
        # Création des clients
        customers = []
        for i, email in enumerate(emails, 1):
            customer = {
                'email': email,
                'first_name': f"Client_{i}",
                'last_name': f"Nom_{i}"
            }
            customers.append(customer)
        
        # Chargement en base
        try:
            df_customers = pd.DataFrame(customers)
            df_customers.to_sql('customers', self.engine, if_exists='append', index=False)
            print(f"Clients charges: {len(customers)}")
            return customers
        except Exception as e:
            print(f"Erreur chargement clients: {e}")
            return []
    
    def load_products(self, products: List[Dict[str, Any]]) -> bool:
        """Chargement des produits"""
        print("Chargement des produits...")
        
        try:
            df_products = pd.DataFrame(products)
            # Adapter les colonnes à la structure de la table
            df_adapted = df_products[['name', 'price', 'category', 'description']].copy()
            df_adapted.to_sql('products', self.engine, if_exists='append', index=False)
            print(f"Produits charges: {len(products)}")
            return True
        except Exception as e:
            print(f"Erreur chargement produits: {e}")
            return False
    
    def load_orders(self, orders: List[Dict[str, Any]], customers: List[Dict[str, Any]]) -> bool:
        """Chargement des commandes"""
        print("Chargement des commandes...")
        
        try:
            # Adapter les colonnes à la structure de la table
            orders_adapted = []
            for order in orders:
                order_adapted = {
                    'customer_email': order['customer_email'],
                    'product_id': order['product_id'],
                    'quantity': order['quantity'],
                    'total_price': order['unit_price'] * order['quantity']
                }
                orders_adapted.append(order_adapted)
            
            df_orders = pd.DataFrame(orders_adapted)
            df_orders.to_sql('orders', self.engine, if_exists='append', index=False)
            print(f"Commandes chargees: {len(orders)}")
            return True
        except Exception as e:
            print(f"Erreur chargement commandes: {e}")
            return False
    
    def load_sessions(self, sessions: List[Dict[str, Any]], customers: List[Dict[str, Any]]) -> bool:
        """Chargement des sessions utilisateur"""
        print("Chargement des sessions...")
        
        try:
            # Adapter les colonnes à la structure de la table
            sessions_adapted = []
            for session in sessions:
                session_adapted = {
                    'customer_email': session['customer_email'],
                    'session_id': session['session_id'],
                    'duration': 0,  # Pas de durée dans nos données
                    'page_views': session.get('pages_viewed', 0)
                }
                sessions_adapted.append(session_adapted)
            
            df_sessions = pd.DataFrame(sessions_adapted)
            df_sessions.to_sql('user_sessions', self.engine, if_exists='append', index=False)
            print(f"Sessions chargees: {len(sessions)}")
            return True
        except Exception as e:
            print(f"Erreur chargement sessions: {e}")
            return False
    
    def load_all_data(self, transformed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Chargement de toutes les données"""
        print("Debut du chargement des donnees...")
        
        # Connexion à la base
        if not self.connect_to_database():
            return {'success': False, 'error': 'Connexion DB echouee'}
        
        # Nettoyage des tables
        if not self.clean_all_tables():
            return {'success': False, 'error': 'Nettoyage echoue'}
        
        # Chargement des clients (extraction des emails uniques)
        customers = self.load_customers(transformed_data['orders'], transformed_data['sessions'])
        if not customers:
            return {'success': False, 'error': 'Chargement clients echoue'}
        
        # Chargement des autres données
        products_loaded = self.load_products(transformed_data['products'])
        orders_loaded = self.load_orders(transformed_data['orders'], customers)
        sessions_loaded = self.load_sessions(transformed_data['sessions'], customers)
        
        if products_loaded and orders_loaded and sessions_loaded:
            print("Chargement termine avec succes")
            return {
                'success': True,
                'summary': {
                    'customers_count': len(customers),
                    'products_count': len(transformed_data['products']),
                    'orders_count': len(transformed_data['orders']),
                    'sessions_count': len(transformed_data['sessions'])
                }
            }
        else:
            return {'success': False, 'error': 'Chargement partiel echoue'}
    
    def close_connection(self):
        """Fermeture de la connexion"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
