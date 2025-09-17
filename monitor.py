from time import sleep
import sys
from typing import Callable, List

TEMP_MIN, TEMP_MAX = 95.0, 102.0      
PULSE_MIN, PULSE_MAX = 60, 100       
SPO2_MIN = 90                         

def _in_range(value: float, lo: float, hi: float) -> bool:
    return lo <= value <= hi

def evaluate_vitals(temperature: float, pulseRate: float, spo2: float) -> List[str]:
    checks = [
        (_in_range(temperature, TEMP_MIN, TEMP_MAX), 'Temperature critical!'),
        (_in_range(pulseRate, PULSE_MIN, PULSE_MAX), 'Pulse Rate is out of range!'),
        (spo2 >= SPO2_MIN, 'Oxygen Saturation out of range!'),
    ]
    return [msg for ok, msg in checks if not ok]

def _blink(out, times: int = 6, sleep_fn: Callable[[float], None] = sleep) -> None:
    for _ in range(times):
        print('\r* ', end='', file=out); out.flush(); sleep_fn(1)
        print('\r *', end='', file=out); out.flush(); sleep_fn(1)
    print('', file=out)

def default_notifier(message: str, out=sys.stdout, blink_fn: Callable[..., None] = _blink) -> None:
    print(message, file=out)
    blink_fn(out)

def vitals_ok(temperature: float, pulseRate: float, spo2: float, *, notifier: Callable[[str], None] | None = None) -> bool:
    alerts = evaluate_vitals(temperature, pulseRate, spo2)
    if alerts:
        notify = notifier or default_notifier
        for msg in alerts:
            notify(msg)
        return False
    return True