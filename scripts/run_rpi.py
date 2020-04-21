#!/usr/bin/env python3

from tracker import run_for_context
from tracker.ui_context.rpi import RPi

if __name__ == '__main__':
    run_for_context(RPi())
