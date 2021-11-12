#!/bin/bash

# Quick script to get a virtualenv
# $ ./venv.sh -> will open a shell inside virtualenv
# $ ./venv.sh pytest -> will run "pytest" within virtualenv

set -e

if [ ! -d ".venv" ]; then
	python3 -m venv .venv
fi


SOURCES=". ~/.bashrc; source .venv/bin/activate"
if [ $# -eq 0 ]; then
    echo "Dropping you into a NEW shell with venv sourced, so:"
    echo "  - You won't have your bash history from this session"
    echo "  - To end virtualenv, just quit shell with 'exit' or 'ctrl+d' (don't use 'deactivate')"
    bash --rcfile <(echo "${SOURCES};")
else
	# not quite sure why this needs to be stringified, but it does
	COMMAND="$@"
    bash  -c "${SOURCES}; $COMMAND"
fi
