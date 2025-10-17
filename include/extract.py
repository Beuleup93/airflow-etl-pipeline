"""
Module d'extraction des données pour Airflow
Reproduit la même logique que le Projet 1
"""
import requests
import pandas as pd
import json
from typing import Dict, List, Any


class DataExtractor:
    """Classe pour l'extraction des données depuis différentes sources"""
    
    def __init__(self):
        self.api_base_url = "https://fakestoreapi.com"
    
    def extract_products_from_api(self) -> List[Dict[str, Any]]:
        """Extraction des produits depuis l'API Fake Store"""
        try:
            response = requests.get(f"{self.api_base_url}/products")
            response.raise_for_status()
            products = response.json()
            print(f"Extraction API: {len(products)} produits extraits")
            return products
        except Exception as e:
            print(f"Erreur extraction API: {e}")
            return []
    
    def extract_orders_from_csv(self, csv_path: str) -> List[Dict[str, Any]]:
        """Extraction des commandes depuis un fichier CSV"""
        try:
            df = pd.read_csv(csv_path)
            orders = df.to_dict('records')
            print(f"Extraction CSV: {len(orders)} commandes extraites")
            return orders
        except Exception as e:
            print(f"Erreur extraction CSV: {e}")
            return []
    
    def extract_sessions_from_json(self, json_path: str) -> List[Dict[str, Any]]:
        """Extraction des sessions depuis un fichier JSON"""
        try:
            with open(json_path, 'r') as f:
                sessions = json.load(f)
            print(f"Extraction JSON: {len(sessions)} sessions extraites")
            return sessions
        except Exception as e:
            print(f"Erreur extraction JSON: {e}")
            return []
    
    def extract_all_data(self, csv_path: str, json_path: str) -> Dict[str, Any]:
        """Extraction de toutes les données"""
        print("Debut de l'extraction des donnees...")
        
        # Extraction en parallèle
        products = self.extract_products_from_api()
        orders = self.extract_orders_from_csv(csv_path)
        sessions = self.extract_sessions_from_json(json_path)
        
        return {
            'products': products,
            'orders': orders,
            'sessions': sessions,
            'extraction_summary': {
                'products_count': len(products),
                'orders_count': len(orders),
                'sessions_count': len(sessions)
            }
        }
