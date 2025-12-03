#!/bin/bash

echo "Starting Compiler...."
echo "Using Python for compiling C language"

python3 lexical_analysis.py
if [ $? -ne 0 ]; then
    echo "Lexical Analysis failed"
    exit 1
fi

python3 syntax_analyzer.py
if [ $? -ne 0 ]; then
    echo "Syntax Analysis failed"
    exit 1
fi