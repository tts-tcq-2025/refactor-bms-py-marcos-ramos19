import unittest
from monitor import (
    vitals_ok,
    evaluate_vitals,
    TEMP_MIN,
    TEMP_MAX,
    PULSE_MIN,
    PULSE_MAX,
    SPO2_MIN,
)

class SpyNotifier:
    def __init__(self) -> None:
        self.messages = []

    def __call__(self, message: str) -> None:
        self.messages.append(message)

class MonitorTest(unittest.TestCase):
    # Helper to avoid I/O and sleeps
    def _call(self, t: float, p: float, s: float):
        spy = SpyNotifier()
        ok = vitals_ok(t, p, s, notifier=spy)
        return ok, spy.messages

    # -------- Pure function tests --------
    def test_all_ok_at_happy_values(self):
        self.assertEqual(evaluate_vitals(98.1, 70, 98), [])

    def test_temperature_bounds_inclusive(self):
        self.assertEqual(evaluate_vitals(TEMP_MIN, 70, 98), [])
        self.assertEqual(evaluate_vitals(TEMP_MAX, 70, 98), [])
        self.assertIn('Temperature critical!',
                      evaluate_vitals(TEMP_MIN - 0.1, 70, 98))
        self.assertIn('Temperature critical!',
                      evaluate_vitals(TEMP_MAX + 0.1, 70, 98))

    def test_pulse_bounds_inclusive(self):
        self.assertEqual(evaluate_vitals(98.1, PULSE_MIN, 98), [])
        self.assertEqual(evaluate_vitals(98.1, PULSE_MAX, 98), [])
        self.assertIn('Pulse Rate is out of range!',
                      evaluate_vitals(98.1, PULSE_MIN - 1, 98))
        self.assertIn('Pulse Rate is out of range!',
                      evaluate_vitals(98.1, PULSE_MAX + 1, 98))

    def test_spo2_min_inclusive(self):
        self.assertEqual(evaluate_vitals(98.1, 70, SPO2_MIN), [])
        self.assertIn('Oxygen Saturation out of range!',
                      evaluate_vitals(98.1, 70, SPO2_MIN - 1))

    def test_multiple_violations_are_all_reported(self):
        msgs = evaluate_vitals(TEMP_MAX + 1, PULSE_MAX + 1, SPO2_MIN - 1)
        self.assertIn('Temperature critical!', msgs)
        self.assertIn('Pulse Rate is out of range!', msgs)
        self.assertIn('Oxygen Saturation out of range!', msgs)
        self.assertEqual(len(msgs), 3)

    # -------- Facade tests with notifier --------
    def test_vitals_not_ok_triggers_notifier_per_alert(self):
        ok, msgs = self._call(99.0, PULSE_MAX + 1, SPO2_MIN - 5)
        self.assertFalse(ok)
        self.assertEqual(len(msgs), 2)
        self.assertIn('Pulse Rate is out of range!', msgs)
        self.assertIn('Oxygen Saturation out of range!', msgs)

    def test_vitals_ok_true_and_notifier_not_called(self):
        ok, msgs = self._call(98.1, 70, 98)
        self.assertTrue(ok)
        self.assertEqual(msgs, [])

if __name__ == '__main__':
    unittest.main()