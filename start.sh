#!/bin/sh

uv export > requirements.txt



kubectl -n grist exec deploy/grav -- pkill uvicorn
kubectl -n grist exec deploy/grav -- /grav/start_remote.sh
