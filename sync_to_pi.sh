#!/bin/bash

rsync -azP \
  --exclude=tracker.sqlite \
  --exclude=sync_to_pi.sh \
  --exclude=venv \
  --exclude=.git \
  --exclude=.idea \
  --exclude=__pycache__ \
  ./ pi:programming/tracker
