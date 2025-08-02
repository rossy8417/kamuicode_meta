#!/bin/bash
# Script to inline minimal unit implementation into workflow

UNIT_PATH=$1
JOB_NAME=$2
WORKFLOW_FILE=$3

if [ ! -f "$UNIT_PATH" ]; then
  echo "Error: Unit file not found: $UNIT_PATH" >&2
  exit 1
fi

# Extract the job steps from minimal unit
# Skip workflow metadata and extract just the steps section
awk '
  /^jobs:/ { in_jobs=1; next }
  in_jobs && /^  [a-zA-Z_-]+:/ { in_job=1; next }
  in_job && /^    steps:/ { in_steps=1; next }
  in_steps && /^    [a-zA-Z_-]+:/ { in_steps=0 }
  in_steps && /^      -/ { print_steps=1 }
  print_steps { print }
' "$UNIT_PATH" >> "$WORKFLOW_FILE"