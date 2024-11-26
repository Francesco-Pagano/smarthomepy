import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, mock_distance_sensor: Mock):
        system = SmartRoom()
        mock_distance_sensor.return_value = True
        occupied = system.check_room_occupancy(system.INFRARED_PIN)
        self.assertTrue(occupied)