#!/bin/sh
NUM_CPUS=$(nproc)
NUM_WORKERS=$((2 * $NUM_CPUS + 1))
gunicorn --chdir /app app:app -w $NUM_WORKERS -b 0.0.0.0:80
