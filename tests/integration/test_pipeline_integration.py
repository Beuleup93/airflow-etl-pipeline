"""
Tests d'intégration pour le pipeline ETL complet
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import json

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'include'))

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader


class TestPipelineIntegration:
    """Tests d'intégration pour le pipeline complet"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader({
            'host': 'localhost',
            'port': 5432,
            'database': 'ecommerce_db',
            'user': 'postgres',
            'password': 'postgres'
        })
    
    @patch('requests.get')
    def test_full_pipeline_with_mock_data(self, mock_get):
        """Test du pipeline complet avec des données mockées"""
        # Mock des données API
        mock_products = [
            {
                'id': 1,
                'title': 'Product 1',
                'price': 10.99,
                'category': 'Electronics',
                'description': 'A great product',
                'image': 'image1.jpg',
                'rating': {'rate': 4.5, 'count': 100}
            }
        ]
        mock_response = mock_get.return_value
        mock_response.json.return_value = mock_products
        mock_response.raise_for_status.return_value = None
        
        # Données de test pour CSV et JSON avec la nouvelle structure
        test_orders = [
            {'order_reference': 'ORD-001', 'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2, 'unit_price': 10.99, 'order_date': '2024-01-01', 'status': 'completed', 'payment_method': 'credit_card'}
        ]
        test_sessions = [
            {'session_id': 'sess_001', 'customer_email': 'test@example.com', 'session_start': '2024-01-01T10:00:00', 'session_end': '2024-01-01T10:20:00', 'pages_viewed': 5, 'items_viewed': ['1'], 'conversion': True, 'device_type': 'desktop', 'browser': 'Chrome', 'ip_address': '192.168.1.1'}
        ]
        
        with patch('pandas.read_csv') as mock_csv, \
             patch('builtins.open', mock_open(read_data=json.dumps(test_sessions))):
            
            mock_csv.return_value = pd.DataFrame(test_orders)
            
            # Test du pipeline complet
            # 1. Extraction
            raw_data = self.extractor.extract_all_data('orders.csv', 'sessions.json')
            
            # 2. Transformation
            transformed_data = self.transformer.transform_all_data(raw_data)
            
            # 3. Chargement (mocké)
            with patch.object(self.loader, 'connect_to_database', return_value=True), \
                 patch.object(self.loader, 'clean_all_tables', return_value=True), \
                 patch.object(self.loader, 'load_customers', return_value=[{'customer_id': 1, 'email': 'test@example.com'}]), \
                 patch.object(self.loader, 'load_products', return_value=True), \
                 patch.object(self.loader, 'load_orders', return_value=True), \
                 patch.object(self.loader, 'load_sessions', return_value=True):
                
                load_result = self.loader.load_all_data(transformed_data)
            
            # Vérifications
            assert raw_data['extraction_summary']['products_count'] == 1
            assert raw_data['extraction_summary']['orders_count'] == 1
            assert raw_data['extraction_summary']['sessions_count'] == 1
            
            assert transformed_data['transformation_summary']['products_count'] == 1
            assert transformed_data['transformation_summary']['orders_count'] == 1
            assert transformed_data['transformation_summary']['sessions_count'] == 1
            
            assert load_result['success'] == True
            assert load_result['summary']['products_count'] == 1
            assert load_result['summary']['orders_count'] == 1
            assert load_result['summary']['sessions_count'] == 1
    
    def test_data_flow_consistency(self):
        """Test de la cohérence du flux de données"""
        # Données de test
        raw_data = {
            'products': [
                {'id': 1, 'title': 'Product 1', 'price': 10.99, 'category': 'Electronics', 'description': 'A product', 'image': 'img.jpg', 'rating': {'rate': 4.5, 'count': 100}}
            ],
            'orders': [
                {'order_reference': 'ORD-001', 'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2, 'unit_price': 10.99, 'order_date': '2024-01-01', 'status': 'completed', 'payment_method': 'credit_card'}
            ],
            'sessions': [
                {'session_id': 'sess_001', 'customer_email': 'test@example.com', 'session_start': '2024-01-01T10:00:00', 'session_end': '2024-01-01T10:20:00', 'pages_viewed': 15, 'items_viewed': ['1'], 'conversion': True, 'device_type': 'desktop', 'browser': 'Chrome', 'ip_address': '192.168.1.1'}
            ]
        }
        
        # Test de la transformation
        transformed_data = self.transformer.transform_all_data(raw_data)
        
        # Vérifications de cohérence
        assert len(transformed_data['products']) == 1
        assert len(transformed_data['orders']) == 1
        assert len(transformed_data['sessions']) == 1
        
        # Vérification de l'enrichissement des commandes
        enriched_order = transformed_data['orders'][0]
        assert 'total_amount' in enriched_order
        assert enriched_order['total_amount'] == 21.98  # 2 * 10.99
        
        # Vérification de l'enrichissement des sessions
        enriched_session = transformed_data['sessions'][0]
        assert 'items_viewed_count' in enriched_session
        assert 'session_quality' in enriched_session
        assert enriched_session['session_quality'] == 'high'  # pages_viewed > 10
    
    def test_error_handling_in_pipeline(self):
        """Test de la gestion des erreurs dans le pipeline"""
        # Test avec des données invalides
        raw_data = {
            'products': [],
            'orders': [
                {'order_id': 1, 'customer_email': 'invalid-email', 'product_id': 1, 'quantity': 2}  # Email invalide
            ],
            'sessions': [
                {'session_id': 'sess_001', 'customer_email': 'invalid-email', 'duration': 1200}  # Email invalide
            ]
        }
        
        # Test de la transformation
        transformed_data = self.transformer.transform_all_data(raw_data)
        
        # Vérifications (les données invalides doivent être filtrées)
        assert len(transformed_data['orders']) == 0  # Email invalide filtré
        assert len(transformed_data['sessions']) == 0  # Email invalide filtré
    
    def test_configuration_loading(self):
        """Test du chargement de la configuration"""
        from config_loader import config
        
        # Test de la configuration de la base de données
        db_config = config.get_database_config()
        assert 'host' in db_config
        assert 'port' in db_config
        assert 'database' in db_config
        assert 'user' in db_config
        assert 'password' in db_config
        
        # Test de la configuration des notifications
        notification_config = config.get_notification_config()
        assert 'email' in notification_config
        assert 'on_failure' in notification_config
        
        # Test de la configuration ETL
        etl_config = config.get_etl_config()
        assert 'batch_size' in etl_config
        assert 'max_retries' in etl_config
        assert 'retry_delay' in etl_config


def mock_open(read_data):
    """Helper function pour mock open"""
    from unittest.mock import mock_open as _mock_open
    return _mock_open(read_data=read_data)
