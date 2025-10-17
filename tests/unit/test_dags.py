"""
Tests unitaires pour les DAGs Airflow
"""
import pytest
import sys
import os
from datetime import datetime, timedelta

# Ajout du chemin des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'include'))

# Import des DAGs
from dags.etl_ecommerce_dag import etl_ecommerce_pipeline
from dags.data_quality_dag import data_quality_checks
from dags.monitoring_dag import monitoring_dag


class TestETLEcommerceDAG:
    """Tests pour le DAG ETL e-commerce"""
    
    def test_dag_creation(self):
        """Test de la création du DAG"""
        dag = etl_ecommerce_pipeline()
        
        # Vérifications
        assert dag.dag_id == 'etl_ecommerce_pipeline'
        assert dag.description == 'Pipeline ETL pour données e-commerce'
        assert dag.schedule_interval == '@daily'
        assert dag.catchup == False
        assert 'etl' in dag.tags
        assert 'ecommerce' in dag.tags
        # Le tag 'data-pipeline' n'est pas configuré dans config.yaml
    
    def test_dag_tasks(self):
        """Test des tâches du DAG"""
        dag = etl_ecommerce_pipeline()
        task_ids = [task.task_id for task in dag.tasks]
        
        # Vérifications
        expected_tasks = ['extract_data', 'transform_data', 'load_data', 'send_notification']
        for task in expected_tasks:
            assert task in task_ids
    
    def test_dag_dependencies(self):
        """Test des dépendances entre tâches"""
        dag = etl_ecommerce_pipeline()
        
        # Vérification des dépendances
        extract_task = dag.get_task('extract_data')
        transform_task = dag.get_task('transform_data')
        load_task = dag.get_task('load_data')
        notification_task = dag.get_task('send_notification')
        
        # Vérifications
        assert transform_task in extract_task.downstream_list
        assert load_task in transform_task.downstream_list
        assert notification_task in load_task.downstream_list


class TestDataQualityDAG:
    """Tests pour le DAG de contrôles qualité"""
    
    def test_dag_creation(self):
        """Test de la création du DAG"""
        dag = data_quality_checks()
        
        # Vérifications
        assert dag.dag_id == 'data_quality_checks'
        assert dag.description == 'Contrôles de qualité des données e-commerce'
        assert dag.schedule_interval == '@daily'
        assert dag.catchup == False
        assert 'data-quality' in dag.tags
        assert 'validation' in dag.tags
        assert 'monitoring' in dag.tags
    
    def test_dag_tasks(self):
        """Test des tâches du DAG"""
        dag = data_quality_checks()
        task_ids = [task.task_id for task in dag.tasks]
        
        # Vérifications
        expected_tasks = [
            'check_data_completeness',
            'check_data_consistency', 
            'check_data_freshness',
            'generate_quality_report'
        ]
        for task in expected_tasks:
            assert task in task_ids
    
    def test_dag_dependencies(self):
        """Test des dépendances entre tâches"""
        dag = data_quality_checks()
        
        # Vérification des dépendances
        completeness_task = dag.get_task('check_data_completeness')
        consistency_task = dag.get_task('check_data_consistency')
        freshness_task = dag.get_task('check_data_freshness')
        report_task = dag.get_task('generate_quality_report')
        
        # Vérifications (toutes les tâches de vérification alimentent le rapport)
        assert report_task in completeness_task.downstream_list
        assert report_task in consistency_task.downstream_list
        assert report_task in freshness_task.downstream_list


class TestMonitoringDAG:
    """Tests pour le DAG de monitoring"""
    
    def test_dag_creation(self):
        """Test de la création du DAG"""
        dag = monitoring_dag()
        
        # Vérifications
        assert dag.dag_id == 'monitoring_dag'
        assert dag.description == 'Monitoring et surveillance du système'
        assert dag.schedule_interval == '@hourly'
        assert dag.catchup == False
        assert 'monitoring' in dag.tags
        assert 'health-check' in dag.tags
        assert 'alerting' in dag.tags
    
    def test_dag_tasks(self):
        """Test des tâches du DAG"""
        dag = monitoring_dag()
        task_ids = [task.task_id for task in dag.tasks]
        
        # Vérifications
        expected_tasks = [
            'check_dag_status',
            'check_database_health',
            'check_data_freshness',
            'check_system_metrics',
            'generate_monitoring_report'
        ]
        for task in expected_tasks:
            assert task in task_ids
    
    def test_dag_dependencies(self):
        """Test des dépendances entre tâches"""
        dag = monitoring_dag()
        
        # Vérification des dépendances
        dag_status_task = dag.get_task('check_dag_status')
        db_health_task = dag.get_task('check_database_health')
        freshness_task = dag.get_task('check_data_freshness')
        metrics_task = dag.get_task('check_system_metrics')
        report_task = dag.get_task('generate_monitoring_report')
        
        # Vérifications (toutes les tâches de vérification alimentent le rapport)
        assert report_task in dag_status_task.downstream_list
        assert report_task in db_health_task.downstream_list
        assert report_task in freshness_task.downstream_list
        assert report_task in metrics_task.downstream_list


class TestDAGConfiguration:
    """Tests pour la configuration des DAGs"""
    
    def test_default_args_consistency(self):
        """Test de la cohérence des default_args entre DAGs"""
        etl_dag = etl_ecommerce_pipeline()
        quality_dag = data_quality_checks()
        monitoring_dag_instance = monitoring_dag()
        
        # Vérifications
        assert etl_dag.default_args['owner'] == 'data-engineer'
        assert quality_dag.default_args['owner'] == 'data-engineer'
        assert monitoring_dag_instance.default_args['owner'] == 'data-engineer'
        
        assert etl_dag.default_args['retries'] == 1
        assert quality_dag.default_args['retries'] == 1
        assert monitoring_dag_instance.default_args['retries'] == 1
    
    def test_schedules(self):
        """Test des intervalles de planification"""
        etl_dag = etl_ecommerce_pipeline()
        quality_dag = data_quality_checks()
        monitoring_dag_instance = monitoring_dag()
        
        # Vérifications
        assert etl_dag.schedule == '@daily'
        assert quality_dag.schedule == '@daily'
        assert monitoring_dag_instance.schedule == '@hourly'
    
    def test_catchup_settings(self):
        """Test des paramètres catchup"""
        etl_dag = etl_ecommerce_pipeline()
        quality_dag = data_quality_checks()
        monitoring_dag_instance = monitoring_dag()
        
        # Vérifications
        assert etl_dag.catchup == False
        assert quality_dag.catchup == False
        assert monitoring_dag_instance.catchup == False
