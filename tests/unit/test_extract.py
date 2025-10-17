"""
Tests unitaires pour le module extract.py
"""
import pytest
import pandas as pd
import json
import os
from unittest.mock import patch, mock_open
import sys

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'include'))

from extract import DataExtractor


class TestDataExtractor:
    """Tests pour la classe DataExtractor"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.extractor = DataExtractor()
    
    def test_init(self):
        """Test de l'initialisation de la classe"""
        assert self.extractor.api_base_url == "https://fakestoreapi.com"
    
    @patch('requests.get')
    def test_extract_products_from_api_success(self, mock_get):
        """Test de l'extraction des produits depuis l'API avec succès"""
        # Mock de la réponse API
        mock_products = [
            {'id': 1, 'title': 'Product 1', 'price': 10.99},
            {'id': 2, 'title': 'Product 2', 'price': 20.99}
        ]
        mock_response = mock_get.return_value
        mock_response.json.return_value = mock_products
        mock_response.raise_for_status.return_value = None
        
        # Test
        result = self.extractor.extract_products_from_api()
        
        # Vérifications
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['title'] == 'Product 1'
        mock_get.assert_called_once_with("https://fakestoreapi.com/products")
    
    @patch('requests.get')
    def test_extract_products_from_api_failure(self, mock_get):
        """Test de l'extraction des produits depuis l'API avec échec"""
        # Mock de l'erreur
        mock_get.side_effect = Exception("API Error")
        
        # Test
        result = self.extractor.extract_products_from_api()
        
        # Vérifications
        assert result == []
    
    def test_extract_orders_from_csv_success(self):
        """Test de l'extraction des commandes depuis CSV avec succès"""
        # Données de test
        test_data = [
            {'order_id': 1, 'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2},
            {'order_id': 2, 'customer_email': 'test2@example.com', 'product_id': 2, 'quantity': 1}
        ]
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_df = pd.DataFrame(test_data)
            mock_read_csv.return_value = mock_df
            
            # Test
            result = self.extractor.extract_orders_from_csv('test.csv')
            
            # Vérifications
            assert len(result) == 2
            assert result[0]['order_id'] == 1
            assert result[0]['customer_email'] == 'test@example.com'
    
    def test_extract_orders_from_csv_failure(self):
        """Test de l'extraction des commandes depuis CSV avec échec"""
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.side_effect = Exception("File not found")
            
            # Test
            result = self.extractor.extract_orders_from_csv('nonexistent.csv')
            
            # Vérifications
            assert result == []
    
    def test_extract_sessions_from_json_success(self):
        """Test de l'extraction des sessions depuis JSON avec succès"""
        # Données de test
        test_data = [
            {'session_id': 'sess_001', 'customer_email': 'test@example.com', 'duration': 1200},
            {'session_id': 'sess_002', 'customer_email': 'test2@example.com', 'duration': 800}
        ]
        
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            # Test
            result = self.extractor.extract_sessions_from_json('test.json')
            
            # Vérifications
            assert len(result) == 2
            assert result[0]['session_id'] == 'sess_001'
            assert result[0]['customer_email'] == 'test@example.com'
    
    def test_extract_sessions_from_json_failure(self):
        """Test de l'extraction des sessions depuis JSON avec échec"""
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = Exception("File not found")
            
            # Test
            result = self.extractor.extract_sessions_from_json('nonexistent.json')
            
            # Vérifications
            assert result == []
    
    @patch.object(DataExtractor, 'extract_products_from_api')
    @patch.object(DataExtractor, 'extract_orders_from_csv')
    @patch.object(DataExtractor, 'extract_sessions_from_json')
    def test_extract_all_data(self, mock_sessions, mock_orders, mock_products):
        """Test de l'extraction de toutes les données"""
        # Mock des données
        mock_products.return_value = [{'id': 1, 'title': 'Product 1'}]
        mock_orders.return_value = [{'order_id': 1, 'customer_email': 'test@example.com'}]
        mock_sessions.return_value = [{'session_id': 'sess_001', 'customer_email': 'test@example.com'}]
        
        # Test
        result = self.extractor.extract_all_data('orders.csv', 'sessions.json')
        
        # Vérifications
        assert 'products' in result
        assert 'orders' in result
        assert 'sessions' in result
        assert 'extraction_summary' in result
        assert result['extraction_summary']['products_count'] == 1
        assert result['extraction_summary']['orders_count'] == 1
        assert result['extraction_summary']['sessions_count'] == 1
        
        # Vérification des appels
        mock_products.assert_called_once()
        mock_orders.assert_called_once_with('orders.csv')
        mock_sessions.assert_called_once_with('sessions.json')
