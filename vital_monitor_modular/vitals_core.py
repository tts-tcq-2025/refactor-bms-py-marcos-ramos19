from typing import List
from vitals_config import TEMP_MIN, TEMP_MAX, PULSE_MIN, PULSE_MAX, SPO2_MIN

def _in_range(value: float, lo: float, hi: float) -> bool:
    return lo <= value <= hi

def evaluate_vitals(temperature: float, pulseRate: float, spo2: float) -> List[str]:
    checks = [
        (_in_range(temperature, TEMP_MIN, TEMP_MAX), 'Temperature critical!'),
        (_in_range(pulseRate, PULSE_MIN, PULSE_MAX), 'Pulse Rate is out of range!'),
        (spo2 >= SPO2_MIN, 'Oxygen Saturation out of range!'),        
    ]
    return [msg for ok, msg in checks if not ok]