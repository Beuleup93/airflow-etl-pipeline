"""
Tests unitaires pour le module load.py
"""
import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch, MagicMock

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'include'))

from load import DataLoader


class TestDataLoader:
    """Tests pour la classe DataLoader"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'ecommerce_db',
            'user': 'postgres',
            'password': 'postgres'
        }
        self.loader = DataLoader(self.db_config)
    
    @patch('psycopg2.connect')
    @patch('sqlalchemy.create_engine')
    def test_connect_to_database_success(self, mock_engine, mock_connect):
        """Test de la connexion à la base de données avec succès"""
        # Mock des connexions
        mock_connect.return_value = MagicMock()
        mock_engine.return_value = MagicMock()
        
        # Test
        result = self.loader.connect_to_database()
        
        # Vérifications
        assert result == True
        mock_connect.assert_called_once_with(
            host='localhost',
            port=5432,
            database='ecommerce_db',
            user='postgres',
            password='postgres'
        )
    
    @patch('psycopg2.connect')
    @patch('sqlalchemy.create_engine')
    def test_connect_to_database_failure(self, mock_engine, mock_connect):
        """Test de la connexion à la base de données avec échec"""
        # Mock de l'erreur
        mock_connect.side_effect = Exception("Connection failed")
        
        # Test
        result = self.loader.connect_to_database()
        
        # Vérifications
        assert result == False
    
    @patch.object(DataLoader, 'connect_to_database')
    def test_clean_all_tables_success(self, mock_connect):
        """Test du nettoyage des tables avec succès"""
        # Mock de la connexion
        mock_connect.return_value = True
        mock_cursor = MagicMock()
        self.loader.connection = MagicMock()
        self.loader.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = self.loader.clean_all_tables()
        
        # Vérifications
        assert result == True
        # Vérification que les tables sont nettoyées dans le bon ordre
        expected_calls = [
            'DELETE FROM user_sessions;',
            'DELETE FROM orders;',
            'DELETE FROM products;',
            'DELETE FROM customers;'
        ]
        for call in expected_calls:
            mock_cursor.execute.assert_any_call(call)
    
    @patch.object(DataLoader, 'connect_to_database')
    def test_clean_all_tables_failure(self, mock_connect):
        """Test du nettoyage des tables avec échec"""
        # Mock de la connexion
        mock_connect.return_value = True
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database error")
        self.loader.connection = MagicMock()
        self.loader.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Test
        result = self.loader.clean_all_tables()
        
        # Vérifications
        assert result == False
    
    def test_load_customers(self):
        """Test du chargement des clients"""
        # Données de test
        orders = [
            {'customer_email': 'test1@example.com'},
            {'customer_email': 'test2@example.com'},
            {'customer_email': 'test1@example.com'}  # Doublon
        ]
        sessions = [
            {'customer_email': 'test3@example.com'}
        ]
        
        with patch.object(self.loader, 'engine') as mock_engine:
            # Test
            result = self.loader.load_customers(orders, sessions)
            
            # Vérifications (3 emails uniques)
            assert len(result) == 3
            emails = [customer['email'] for customer in result]
            assert 'test1@example.com' in emails
            assert 'test2@example.com' in emails
            assert 'test3@example.com' in emails
    
    @patch('pandas.DataFrame.to_sql')
    def test_load_products_success(self, mock_to_sql):
        """Test du chargement des produits avec succès"""
        # Données de test avec la nouvelle structure
        products = [
            {'name': 'Product 1', 'price': 10.99, 'category': 'Electronics', 'description': 'A great product'},
            {'name': 'Product 2', 'price': 20.99, 'category': 'Clothing', 'description': 'Another product'}
        ]
        
        # Test
        result = self.loader.load_products(products)
        
        # Vérifications
        assert result == True
        mock_to_sql.assert_called_once()
    
    @patch('pandas.DataFrame.to_sql')
    def test_load_products_failure(self, mock_to_sql):
        """Test du chargement des produits avec échec"""
        # Mock de l'erreur
        mock_to_sql.side_effect = Exception("Database error")
        
        # Données de test
        products = [{'id': 1, 'name': 'Product 1', 'price': 10.99}]
        
        # Test
        result = self.loader.load_products(products)
        
        # Vérifications
        assert result == False
    
    @patch('pandas.DataFrame.to_sql')
    def test_load_orders_success(self, mock_to_sql):
        """Test du chargement des commandes avec succès"""
        # Données de test avec la nouvelle structure
        orders = [
            {'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2, 'unit_price': 10.99, 'order_date': '2024-01-01'}
        ]
        customers = [
            {'customer_id': 1, 'email': 'test@example.com'}
        ]
        
        # Test
        result = self.loader.load_orders(orders, customers)
        
        # Vérifications
        assert result == True
        mock_to_sql.assert_called_once()
    
    @patch('pandas.DataFrame.to_sql')
    def test_load_sessions_success(self, mock_to_sql):
        """Test du chargement des sessions avec succès"""
        # Données de test avec la nouvelle structure
        sessions = [
            {'session_id': 'sess_001', 'customer_email': 'test@example.com', 'session_start': '2024-01-01T10:00:00', 'pages_viewed': 5}
        ]
        customers = [
            {'customer_id': 1, 'email': 'test@example.com'}
        ]
        
        # Test
        result = self.loader.load_sessions(sessions, customers)
        
        # Vérifications
        assert result == True
        mock_to_sql.assert_called_once()
    
    @patch.object(DataLoader, 'connect_to_database')
    @patch.object(DataLoader, 'clean_all_tables')
    @patch.object(DataLoader, 'load_customers')
    @patch.object(DataLoader, 'load_products')
    @patch.object(DataLoader, 'load_orders')
    @patch.object(DataLoader, 'load_sessions')
    def test_load_all_data_success(self, mock_sessions, mock_orders, mock_products, mock_customers, mock_clean, mock_connect):
        """Test du chargement de toutes les données avec succès"""
        # Mock des méthodes
        mock_connect.return_value = True
        mock_clean.return_value = True
        mock_customers.return_value = [{'customer_id': 1, 'email': 'test@example.com'}]
        mock_products.return_value = True
        mock_orders.return_value = True
        mock_sessions.return_value = True
        
        # Données de test
        transformed_data = {
            'products': [{'id': 1, 'name': 'Product 1'}],
            'orders': [{'order_id': 1, 'customer_email': 'test@example.com'}],
            'sessions': [{'session_id': 'sess_001', 'customer_email': 'test@example.com'}]
        }
        
        # Test
        result = self.loader.load_all_data(transformed_data)
        
        # Vérifications
        assert result['success'] == True
        assert 'summary' in result
        assert result['summary']['products_count'] == 1
        assert result['summary']['orders_count'] == 1
        assert result['summary']['sessions_count'] == 1
    
    @patch.object(DataLoader, 'connect_to_database')
    def test_load_all_data_connection_failure(self, mock_connect):
        """Test du chargement avec échec de connexion"""
        # Mock de l'échec de connexion
        mock_connect.return_value = False
        
        # Données de test
        transformed_data = {
            'products': [],
            'orders': [],
            'sessions': []
        }
        
        # Test
        result = self.loader.load_all_data(transformed_data)
        
        # Vérifications
        assert result['success'] == False
        assert 'Connexion DB echouee' in result['error']
