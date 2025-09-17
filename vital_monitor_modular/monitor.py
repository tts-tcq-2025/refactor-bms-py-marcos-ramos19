from time import sleep
import sys 
from typing import Callable
from vitals_core import evaluate_vitals
from vitals_config import *

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
