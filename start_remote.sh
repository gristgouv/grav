#!/bin/sh

cd /grav
pip install -r /grav/requirements.txt
. ./.env
uvicorn src.grav.app:app --port 80 --host 0.0.0.0

