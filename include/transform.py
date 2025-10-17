"""
Module de transformation des données pour Airflow
Reproduit la même logique que le Projet 1
"""
import pandas as pd
from typing import Dict, List, Any
import re
from datetime import datetime


class DataTransformer:
    """Classe pour la transformation et le nettoyage des données"""
    
    def __init__(self):
        self.validated_data = {}
    
    def clean_text(self, text: str) -> str:
        """Nettoyage et normalisation du texte"""
        if pd.isna(text) or text is None:
            return ""
        return str(text).strip().lower()
    
    def validate_email(self, email: str) -> bool:
        """Validation du format email"""
        if pd.isna(email) or email is None:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, str(email)))
    
    def transform_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transformation des produits"""
        print("Transformation des produits...")
        
        transformed_products = []
        for product in products:
            # Nettoyage des données
            clean_product = {
                'id': product.get('id'),
                'name': self.clean_text(product.get('title', '')),
                'price': float(product.get('price', 0)),
                'category': self.clean_text(product.get('category', '')),
                'description': self.clean_text(product.get('description', '')),
                'image_url': product.get('image', ''),
                'rating': float(product.get('rating', {}).get('rate', 0)),
                'rating_count': int(product.get('rating', {}).get('count', 0))
            }
            transformed_products.append(clean_product)
        
        print(f"Produits transformes: {len(transformed_products)}")
        return transformed_products
    
    def transform_orders(self, orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transformation des commandes"""
        print("Transformation des commandes...")
        
        transformed_orders = []
        for order in orders:
            # Nettoyage et validation
            clean_order = {
                'order_reference': str(order.get('order_reference', '')),
                'customer_email': str(order.get('customer_email', '')).strip(),
                'product_id': int(order.get('product_id', 0)),
                'quantity': int(order.get('quantity', 0)),
                'unit_price': float(order.get('unit_price', 0)),
                'order_date': order.get('order_date', ''),
                'status': self.clean_text(order.get('status', '')),
                'payment_method': self.clean_text(order.get('payment_method', ''))
            }
            
            # Validation des données
            if (clean_order['order_reference'] and 
                self.validate_email(clean_order['customer_email']) and
                clean_order['product_id'] > 0 and
                clean_order['quantity'] > 0):
                transformed_orders.append(clean_order)
        
        print(f"Commandes transformees: {len(transformed_orders)}")
        return transformed_orders
    
    def transform_sessions(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transformation des sessions utilisateur"""
        print("Transformation des sessions...")
        
        transformed_sessions = []
        for session in sessions:
            # Nettoyage des données
            clean_session = {
                'session_id': str(session.get('session_id', '')),
                'customer_email': str(session.get('customer_email', '')).strip(),
                'session_start': session.get('session_start', ''),
                'session_end': session.get('session_end', ''),
                'pages_viewed': int(session.get('pages_viewed', 0)),
                'items_viewed': session.get('items_viewed', []),
                'conversion': bool(session.get('conversion', False)),
                'device_type': self.clean_text(session.get('device_type', 'desktop')),
                'browser': self.clean_text(session.get('browser', '')),
                'ip_address': session.get('ip_address', '')
            }
            
            # Validation des données
            if (clean_session['session_id'] and 
                self.validate_email(clean_session['customer_email'])):
                transformed_sessions.append(clean_session)
        
        print(f"Sessions transformees: {len(transformed_sessions)}")
        return transformed_sessions
    
    def transform_all_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transformation de toutes les données"""
        print("Debut de la transformation des donnees...")
        
        # Transformation des données
        products = self.transform_products(raw_data['products'])
        orders = self.transform_orders(raw_data['orders'])
        sessions = self.transform_sessions(raw_data['sessions'])
        
        # Enrichissement des données
        enriched_orders = self.enrich_orders(orders, products)
        enriched_sessions = self.enrich_sessions(sessions)
        
        return {
            'products': products,
            'orders': enriched_orders,
            'sessions': enriched_sessions,
            'transformation_summary': {
                'products_count': len(products),
                'orders_count': len(enriched_orders),
                'sessions_count': len(enriched_sessions)
            }
        }
    
    def enrich_orders(self, orders: List[Dict[str, Any]], products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrichissement des commandes avec les données produits"""
        print("Enrichissement des commandes...")
        
        # Création d'un dictionnaire des produits pour lookup rapide
        products_dict = {p['id']: p for p in products}
        
        enriched_orders = []
        for order in orders:
            product = products_dict.get(order['product_id'])
            if product:
                enriched_order = order.copy()
                enriched_order['product_name'] = product['name']
                enriched_order['product_price'] = product['price']
                enriched_order['total_amount'] = order['quantity'] * product['price']
                enriched_orders.append(enriched_order)
        
        print(f"Commandes enrichies: {len(enriched_orders)}")
        return enriched_orders
    
    def enrich_sessions(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrichissement des sessions avec des métriques calculées"""
        print("Enrichissement des sessions...")
        
        enriched_sessions = []
        for session in sessions:
            enriched_session = session.copy()
            # Calcul de métriques basées sur les données disponibles
            pages_viewed = session.get('pages_viewed', 0)
            items_viewed = session.get('items_viewed', [])
            
            # Calcul de métriques
            enriched_session['items_viewed_count'] = len(items_viewed) if isinstance(items_viewed, list) else 0
            enriched_session['session_quality'] = 'high' if pages_viewed > 10 else 'low'
            enriched_session['conversion_rate'] = 1.0 if session.get('conversion', False) else 0.0
            enriched_sessions.append(enriched_session)
        
        print(f"Sessions enrichies: {len(enriched_sessions)}")
        return enriched_sessions
