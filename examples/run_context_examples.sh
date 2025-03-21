#!/bin/bash

# Script to demonstrate contextual logging with different settings

echo "==============================================================="
echo "Running with no context (CONTEXT_DISPLAY=none)"
echo "==============================================================="
CONTEXT_DISPLAY=none python context_logging_example.py

echo ""
echo "==============================================================="
echo "Running with function context (CONTEXT_DISPLAY=function)"
echo "==============================================================="
CONTEXT_DISPLAY=function python context_logging_example.py

echo ""
echo "==============================================================="
echo "Running with class and function context (CONTEXT_DISPLAY=class_function)"
echo "==============================================================="
CONTEXT_DISPLAY=class_function python context_logging_example.py

echo ""
echo "==============================================================="
echo "Running with full context (CONTEXT_DISPLAY=full)"
echo "==============================================================="
CONTEXT_DISPLAY=full python context_logging_example.py 