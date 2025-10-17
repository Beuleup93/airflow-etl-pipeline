#!/usr/bin/env python3
"""
Script pour exécuter la suite de tests du projet Airflow ETL
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERREUR lors de l'execution: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Exécuter la suite de tests du projet Airflow ETL")
    parser.add_argument("--unit", action="store_true", help="Exécuter seulement les tests unitaires")
    parser.add_argument("--integration", action="store_true", help="Exécuter seulement les tests d'intégration")
    parser.add_argument("--coverage", action="store_true", help="Générer un rapport de couverture")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    parser.add_argument("--fast", action="store_true", help="Exécution rapide (sans tests lents)")
    
    args = parser.parse_args()
    
    # Changement vers le répertoire du projet
    project_dir = Path(__file__).parent.parent
    os.chdir(project_dir)
    
    print("Suite de tests du projet Airflow ETL")
    print(f"Repertoire de travail: {project_dir}")
    
    # Construction de la commande pytest
    cmd_parts = ["./venv/bin/python", "-m", "pytest"]
    
    if args.unit:
        cmd_parts.append("tests/unit/")
    elif args.integration:
        cmd_parts.append("tests/integration/")
    else:
        cmd_parts.append("tests/")
    
    if args.coverage:
        cmd_parts.extend(["--cov=include", "--cov-report=html", "--cov-report=term"])
    
    if args.verbose:
        cmd_parts.append("-v")
    
    if args.fast:
        cmd_parts.extend(["-m", "not slow"])
    
    # Ajout des options par défaut
    cmd_parts.extend(["--tb=short", "--strict-markers"])
    
    command = " ".join(cmd_parts)
    
    # Exécution des tests
    success = run_command(command, "Exécution des tests")
    
    if args.coverage and success:
        print(f"\nRapport de couverture genere dans: {project_dir}/htmlcov/index.html")
    
    if success:
        print("\nSUCCES: Tous les tests sont passes avec succes !")
        return 0
    else:
        print("\nERREUR: Certains tests ont echoue.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
