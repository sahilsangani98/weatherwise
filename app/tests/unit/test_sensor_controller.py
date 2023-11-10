# app/tests/test_sensor_controller.py
"""SensorController unit test stubs"""
from __future__ import absolute_import
import unittest
from app.tests.unit import BaseTestCase
from app.controllers.cache_controller import MetricCache, SensorCache
from unittest.mock import patch, Mock, MagicMock
# from app.controllers.sensor_controller import retrieve_metric, persist_metrics
from app.controllers.sensor_controller import persist_metrics, retrieve_metric
from app.models.reports_model import ReportsTable
from datetime import datetime
import pandas as pd


class TestSensorController(BaseTestCase):
    """Test cases for the sensor controller."""

    def setUp(self):
        self.metric_cache = MetricCache()
        self.sensor_cache = SensorCache()

        # Assign mock metric cache to the attribute you are using
        self.metric_cache.data = {
                "temperature": 1,
                "humidity": 2,
                "wind_speed": 3
            }
    
        # Assign mock sensor cache to the attribute you are using
        self.sensor_cache.data = {1, 2, 3}

        self.mock_reports_table = None

    @patch("app.controllers.sensor_controller.db.session.add")
    @patch("app.controllers.sensor_controller.db.session.commit")
    @patch("app.controllers.sensor_controller.db.session.close")
    def test_persist_metrics(self, add_mock: Mock, commit_mock: Mock, close_mock: Mock):
        """Test case for retrieve_metric
        """
        sensor_id = 1
        report_data = {
            "recorded_at": datetime.utcnow(),
            "metrics": {
                "temperature": 25.0, 
                "humidity": 50.0,
                "wind_speed": 30.0,
            },
        }

        # Ensure no exceptions are raised during execution
        try:
            persist_metrics(sensor_id, report_data)
            # Ensure the expected methods are called
            add_mock.assert_called()
            commit_mock.assert_called()
            # close_mock.assert_called()
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()