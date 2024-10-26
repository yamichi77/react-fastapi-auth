#!/bin/sh

if [ -f pyproject.toml ]; then
    poetry install
    if [ "$1" = "--dev" ]; then
        poetry run python -m debugpy --listen "0.0.0.0:5678" -m uvicorn api.main:app --host "0.0.0.0" --port "8000" --proxy-headers --reload
    else 
        # poetry run uvicorn api.main:app --host "0.0.0.0" --port "8001" --reload
        poetry run python -m debugpy --listen "0.0.0.0:5678" -m uvicorn api.main:app --host "0.0.0.0" --port "8000" --proxy-headers --reload
    fi
fi
