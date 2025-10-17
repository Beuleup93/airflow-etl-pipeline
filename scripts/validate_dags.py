#!/usr/bin/env python3
"""
Script de validation des DAGs Airflow
Vérifie que tous les DAGs sont syntaxiquement corrects
"""
import sys
import os
import subprocess
from pathlib import Path

def validate_dags():
    """Valide tous les DAGs du projet"""
    print("Validation des DAGs Airflow...")
    
    # Chemin vers les DAGs
    dags_dir = Path(__file__).parent.parent / "dags"
    
    if not dags_dir.exists():
        print("ERREUR: Repertoire dags/ introuvable")
        return False
    
    # Liste des fichiers DAG
    dag_files = list(dags_dir.glob("*.py"))
    
    if not dag_files:
        print("ERREUR: Aucun fichier DAG trouve")
        return False
    
    print(f"{len(dag_files)} fichier(s) DAG trouve(s)")
    
    all_valid = True
    
    for dag_file in dag_files:
        print(f"\nValidation de {dag_file.name}...")
        
        try:
            # Validation syntaxique Python
            with open(dag_file, 'r') as f:
                compile(f.read(), dag_file, 'exec')
            print(f"OK: Syntaxe Python")
            
            # Test d'import
            sys.path.insert(0, str(dags_dir))
            module_name = dag_file.stem
            __import__(module_name)
            print(f"OK: Import")
            
        except SyntaxError as e:
            print(f"ERREUR: Erreur de syntaxe: {e}")
            all_valid = False
        except ImportError as e:
            print(f"ERREUR: Erreur d'import: {e}")
            all_valid = False
        except Exception as e:
            print(f"ERREUR: Erreur inattendue: {e}")
            all_valid = False
    
    if all_valid:
        print(f"\nSUCCES: Tous les DAGs sont valides !")
        return True
    else:
        print(f"\nERREUR: Certains DAGs ont des erreurs")
        return False

if __name__ == "__main__":
    success = validate_dags()
    sys.exit(0 if success else 1)
