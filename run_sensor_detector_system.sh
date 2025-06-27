#!/bin/bash
SENSOR_DETECTOR_PROJECT_PATH="/home/developer/Documents/material_detector_machine/sensor-detector-system"

# Activate virtual environment
source "$SENSOR_DETECTOR_PROJECT_PATH/.venv/bin/activate"

# Run python script
python3 "$SENSOR_DETECTOR_PROJECT_PATH/main.py"

deactivate