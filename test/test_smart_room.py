import unittest
import mock.GPIO as GPIO
from unittest.mock import patch, PropertyMock
from unittest.mock import Mock

from mock.adafruit_bmp280 import Adafruit_BMP280_I2C
from src.smart_room import SmartRoom, SmartRoomError
from mock.senseair_s8 import SenseairS8


class TestSmartRoom(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_room_occupancy(self, mock_distance_sensor: Mock):
        system = SmartRoom()
        mock_distance_sensor.return_value = True
        occupied = system.check_room_occupancy()
        self.assertTrue(occupied)

    @patch.object(GPIO, "input")
    def test_check_enough_light(self, mock_photoresistor: Mock):
        system = SmartRoom()
        mock_photoresistor.return_value = True
        enough = system.check_enough_light()
        self.assertTrue(enough)

    @patch.object(SmartRoom, "check_room_occupancy")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(GPIO, "output")
    def test_should_turn_on_light_when_person_is_in_room_and_not_enough_light(self, mock_lightbulb: Mock, mock_check_enough_light: Mock, mock_check_room_occupancy: Mock):
        system = SmartRoom()
        mock_check_room_occupancy.return_value = True
        mock_check_enough_light.return_value = False
        system.manage_light_level()
        mock_lightbulb.assert_called_with(system.LED_PIN, True)

    @patch.object(SmartRoom, "check_room_occupancy")
    @patch.object(SmartRoom, "check_enough_light")
    @patch.object(GPIO, "output")
    def test_should_not_turn_on_light_when_person_is_in_room_and_enough_light(self, mock_lightbulb: Mock, mock_check_enough_light: Mock, mock_check_room_occupancy: Mock):
        system = SmartRoom()
        mock_check_room_occupancy.return_value = True
        mock_check_enough_light.return_value = True
        system.manage_light_level()
        mock_lightbulb.assert_called_with(system.LED_PIN, False)

    @patch.object(SmartRoom, "change_servo_angle")
    @patch.object(Adafruit_BMP280_I2C, "temperature", new_callable=PropertyMock)
    def test_manage_window_open(self, mock_temperatures: Mock, mock_servo: Mock):
        system = SmartRoom()
        system.manage_window()
        mock_temperatures.side_effect = [20, 22]
        mock_servo.assert_called_with(12)



