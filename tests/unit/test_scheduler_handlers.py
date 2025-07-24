
from datetime import time, date
import unittest
from unittest.mock import Mock

from src.handlers.scheduler_handler import SchedulerHandler
from src.services.scheduler_management_service import SchedulerManagementService

class TestSchedulerHandler(unittest.TestCase):

    def setUp(self):
        self.mock_service = Mock(spec=SchedulerManagementService)
        self.handler = SchedulerHandler(self.mock_service)

    def test_get_busy_slots_command_valid_date(self):
        mock_slots = [(time(11, 0), time(12, 0)), (time(14, 0), time(16, 0))]
        self.mock_service.get_busy_slots.return_value = mock_slots

        result = self.handler.get_busy_slots_command("2025-07-25")

        self.mock_service.get_busy_slots.assert_called_with("2025-07-25")
        
        expected_output = "[('11:00', '12:00'), ('14:00', '16:00')]"
        self.assertEqual(result, expected_output)

    def test_get_busy_slots_command_no_slots_found(self):
        self.mock_service.get_busy_slots.return_value = []

        result = self.handler.get_busy_slots_command("2025-07-26")

        expected_output = "[]"
        self.assertEqual(result, expected_output)
        
    def test_get_busy_slots_command_invalid_date(self):
        self.mock_service.get_busy_slots.side_effect = ValueError("Некорректный формат даты: 25-07-2025")

        result = self.handler.get_busy_slots_command("25-07-2025")

        expected_output = "Ошибка получения занятых слотов: Некорректный формат даты: 25-07-2025"
        self.assertEqual(result, expected_output)

    def test_get_free_slots_command_valid_date(self):
        mock_free_slots = [(time(9, 0), time(10, 0)), (time(12, 0), time(13, 0))]
        mock_busy_slots = [(time(10, 0), time(12, 0))]
        self.mock_service.get_free_slots.return_value = mock_free_slots
        self.mock_service.get_busy_slots.return_value = mock_busy_slots

        result = self.handler.get_free_slots_command("2025-07-25")
        
        self.mock_service.get_free_slots.assert_called_with("2025-07-25")
        self.mock_service.get_busy_slots.assert_called_with("2025-07-25")

        expected_output = "[('09:00', '10:00'), ('12:00', '13:00')]"
        self.assertEqual(result, expected_output)

    def test_get_free_slots_command_no_free_slots(self):
        self.mock_service.get_free_slots.return_value = []
        self.mock_service.get_busy_slots.return_value = [(time(9,0), time(18,0))]

        result = self.handler.get_free_slots_command("2025-07-26")

        expected_output = "Нет свободных слотов для 2025-07-26."
        self.assertEqual(result, expected_output)

    def test_get_free_slots_command_day_not_in_db(self):
        self.mock_service.get_free_slots.return_value = []
        self.mock_service.get_busy_slots.return_value = []

        result = self.handler.get_free_slots_command("2025-07-27")
        
        expected_output = "День 2025-07-27 не занесен в базу как занятый."
        self.assertEqual(result, expected_output)

    def test_get_free_slots_command_invalid_input(self):
        with self.assertRaises(ValueError) as cm:
            self.handler.get_free_slots_command("2025-07-25 extra_arg")
        
        self.assertEqual(
            str(cm.exception),
            "Неверный формат команды. get_free_slots принимает один аргумент - дата"
        )

    def test_get_free_slots_command_service_error(self):
        self.mock_service.get_free_slots.side_effect = ValueError("Некорректная дата")

        result = self.handler.get_free_slots_command("invalid-date")
        
        expected_output = "Ошибка получения свободных слотов: Некорректная дата"
        self.assertEqual(result, expected_output)

    def test_is_available_command_available(self):
        self.mock_service.is_available.return_value = True

        result = self.handler.is_available_command("2025-07-25 10:00 11:00")
        
        self.mock_service.is_available.assert_called_with("2025-07-25", "10:00", "11:00")

        self.assertEqual(result, "True")

    def test_is_available_command_not_available(self):
        self.mock_service.is_available.return_value = False

        result = self.handler.is_available_command("2025-07-25 10:00 11:00")

        self.assertEqual(result, "False")
        
    def test_is_available_command_invalid_input_count(self):
        with self.assertRaises(ValueError) as cm:
            self.handler.is_available_command("2025-07-25 10:00")
        
        self.assertEqual(
            str(cm.exception),
            "Неверный формат команды. get_free_slots принимает три аргумента - дата, начало промежутка времени, конец промежутка времени"
        )
        
    def test_is_available_command_invalid_time_format(self):
        self.mock_service.is_available.side_effect = ValueError("Некорректный формат времени: '10:00_am'")

        result = self.handler.is_available_command("2025-07-25 10:00_am 11:00")
        
        expected_output = "Ошибка проверки промежутка времени: Некорректный формат времени: '10:00_am'"
        self.assertEqual(result, expected_output)

    def test_is_available_command_start_after_end(self):
        self.mock_service.is_available.side_effect = ValueError("Время начала должно быть раньше времени окончания.")

        result = self.handler.is_available_command("2025-07-25 11:00 10:00")
        
        expected_output = "Ошибка проверки промежутка времени: Время начала должно быть раньше времени окончания."
        self.assertEqual(result, expected_output)
    
    def test_find_slot_for_duration_command_found(self):
        found_slot = (date(2025, 7, 25), time(9, 0), time(10, 30))
        self.mock_service.find_slot_for_duration.return_value = found_slot

        result = self.handler.find_slot_for_duration_command("90")
        
        self.mock_service.find_slot_for_duration.assert_called_with("90")

        expected_output = "(2025-07-25, 09:00, 10:30)"
        self.assertEqual(result, expected_output)

    def test_find_slot_for_duration_command_not_found(self):
        self.mock_service.find_slot_for_duration.return_value = None

        result = self.handler.find_slot_for_duration_command("60")

        self.assertEqual(result, "Ни один из дней в базе не подошел.")
        
    def test_find_slot_for_duration_command_invalid_input_count(self):
        with self.assertRaises(ValueError) as cm:
            self.handler.find_slot_for_duration_command("60 extra_arg")
        
        self.assertEqual(
            str(cm.exception),
            "Неверный формат команды. find_slot_for_duration принимает один аргумент - число минут"
        )
        
    def test_find_slot_for_duration_command_invalid_minutes_format(self):
        self.mock_service.find_slot_for_duration.side_effect = ValueError("Некорректный формат продолжительности: 'abc'")

        result = self.handler.find_slot_for_duration_command("abc")
        
        expected_output = "Ошибка проверки промежутка времени: Некорректный формат продолжительности: 'abc'"
        self.assertEqual(result, expected_output)

    