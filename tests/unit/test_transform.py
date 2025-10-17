"""
Tests unitaires pour le module transform.py
"""
import pytest
import pandas as pd
import sys
import os

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'include'))

from transform import DataTransformer


class TestDataTransformer:
    """Tests pour la classe DataTransformer"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.transformer = DataTransformer()
    
    def test_clean_text(self):
        """Test de la fonction clean_text"""
        # Test avec texte normal
        assert self.transformer.clean_text("  Hello World  ") == "hello world"
        
        # Test avec texte vide
        assert self.transformer.clean_text("") == ""
        
        # Test avec None
        assert self.transformer.clean_text(None) == ""
    
    def test_validate_email(self):
        """Test de la validation des emails"""
        # Emails valides
        assert self.transformer.validate_email("test@example.com") == True
        assert self.transformer.validate_email("user.name@domain.co.uk") == True
        
        # Emails invalides
        assert self.transformer.validate_email("invalid-email") == False
        assert self.transformer.validate_email("@example.com") == False
        assert self.transformer.validate_email("test@") == False
        assert self.transformer.validate_email("") == False
        assert self.transformer.validate_email(None) == False
    
    def test_transform_products(self):
        """Test de la transformation des produits"""
        # Données de test
        products = [
            {
                'id': 1,
                'title': '  Product 1  ',
                'price': 10.99,
                'category': '  Electronics  ',
                'description': '  A great product  ',
                'image': 'image1.jpg',
                'rating': {'rate': 4.5, 'count': 100}
            }
        ]
        
        # Test
        result = self.transformer.transform_products(products)
        
        # Vérifications
        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['name'] == 'product 1'  # Texte nettoyé
        assert result[0]['price'] == 10.99
        assert result[0]['category'] == 'electronics'  # Texte nettoyé
        assert result[0]['description'] == 'a great product'  # Texte nettoyé
        assert result[0]['rating'] == 4.5
        assert result[0]['rating_count'] == 100
    
    def test_transform_orders(self):
        """Test de la transformation des commandes"""
        # Données de test avec la nouvelle structure
        orders = [
            {
                'order_reference': 'ORD-001',
                'customer_email': 'test@example.com',
                'product_id': 1,
                'quantity': 2,
                'unit_price': 10.99,
                'order_date': '2024-01-01',
                'status': 'completed',
                'payment_method': 'credit_card'
            },
            {
                'order_reference': 'ORD-002',
                'customer_email': 'invalid-email',  # Email invalide
                'product_id': 2,
                'quantity': 1,
                'unit_price': 20.99,
                'order_date': '2024-01-02',
                'status': 'pending',
                'payment_method': 'paypal'
            }
        ]
        
        # Test
        result = self.transformer.transform_orders(orders)
        
        # Vérifications (seul le premier ordre doit être conservé)
        assert len(result) == 1
        assert result[0]['order_reference'] == 'ORD-001'
        assert result[0]['customer_email'] == 'test@example.com'
        assert result[0]['product_id'] == 1
        assert result[0]['quantity'] == 2
    
    def test_transform_sessions(self):
        """Test de la transformation des sessions"""
        # Données de test avec la nouvelle structure
        sessions = [
            {
                'session_id': 'sess_001',
                'customer_email': 'test@example.com',
                'session_start': '2024-01-01T10:00:00',
                'session_end': '2024-01-01T10:20:00',
                'pages_viewed': 5,
                'items_viewed': ['1', '2'],
                'conversion': True,
                'device_type': 'desktop',
                'browser': 'Chrome',
                'ip_address': '192.168.1.1'
            },
            {
                'session_id': 'sess_002',
                'customer_email': 'invalid-email',  # Email invalide
                'session_start': '2024-01-02T10:00:00',
                'session_end': '2024-01-02T10:10:00',
                'pages_viewed': 3,
                'items_viewed': ['3'],
                'conversion': False,
                'device_type': 'mobile',
                'browser': 'Safari',
                'ip_address': '192.168.1.2'
            }
        ]
        
        # Test
        result = self.transformer.transform_sessions(sessions)
        
        # Vérifications (seule la première session doit être conservée)
        assert len(result) == 1
        assert result[0]['session_id'] == 'sess_001'
        assert result[0]['customer_email'] == 'test@example.com'
        assert result[0]['pages_viewed'] == 5
        assert result[0]['conversion'] == True
    
    def test_enrich_orders(self):
        """Test de l'enrichissement des commandes"""
        # Données de test
        orders = [
            {'order_id': 1, 'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2}
        ]
        products = [
            {'id': 1, 'name': 'Product 1', 'price': 10.99}
        ]
        
        # Test
        result = self.transformer.enrich_orders(orders, products)
        
        # Vérifications
        assert len(result) == 1
        assert result[0]['product_name'] == 'Product 1'
        assert result[0]['product_price'] == 10.99
        assert result[0]['total_amount'] == 21.98  # 2 * 10.99
    
    def test_enrich_sessions(self):
        """Test de l'enrichissement des sessions"""
        # Données de test avec la nouvelle structure
        sessions = [
            {
                'session_id': 'sess_001',
                'customer_email': 'test@example.com',
                'pages_viewed': 15,
                'items_viewed': ['1', '2', '3'],
                'conversion': True
            }
        ]
        
        # Test
        result = self.transformer.enrich_sessions(sessions)
        
        # Vérifications
        assert len(result) == 1
        assert result[0]['items_viewed_count'] == 3
        assert result[0]['session_quality'] == 'high'  # pages_viewed > 10
        assert result[0]['conversion_rate'] == 1.0
    
    def test_transform_all_data(self):
        """Test de la transformation de toutes les données"""
        # Données de test avec la nouvelle structure
        raw_data = {
            'products': [
                {'id': 1, 'title': 'Product 1', 'price': 10.99, 'category': 'Electronics', 'description': 'A product', 'image': 'img.jpg', 'rating': {'rate': 4.5, 'count': 100}}
            ],
            'orders': [
                {'order_reference': 'ORD-001', 'customer_email': 'test@example.com', 'product_id': 1, 'quantity': 2, 'unit_price': 10.99, 'order_date': '2024-01-01', 'status': 'completed', 'payment_method': 'credit_card'}
            ],
            'sessions': [
                {'session_id': 'sess_001', 'customer_email': 'test@example.com', 'session_start': '2024-01-01T10:00:00', 'session_end': '2024-01-01T10:20:00', 'pages_viewed': 5, 'items_viewed': ['1'], 'conversion': True, 'device_type': 'desktop', 'browser': 'Chrome', 'ip_address': '192.168.1.1'}
            ]
        }
        
        # Test
        result = self.transformer.transform_all_data(raw_data)
        
        # Vérifications
        assert 'products' in result
        assert 'orders' in result
        assert 'sessions' in result
        assert 'transformation_summary' in result
        assert result['transformation_summary']['products_count'] == 1
        assert result['transformation_summary']['orders_count'] == 1
        assert result['transformation_summary']['sessions_count'] == 1
