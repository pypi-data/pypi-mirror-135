# CaptureJob

This library provides the ability to copy stdout and stderr files to cloud storage.

## Usage

Programmatically it is used like this:
```
from capturejob import CaptureJob

CaptureJob()
```

but mainly its intended to be used in a dockerfile command script followng execution of a command script.

```
echo "Running batch"

cd /work && poetry run python src/etl_noop/batchrun.py

JOB="...
CAPTURE_CONNECTION_STRING="..." 
CAPTURE_CONTAINER_NAME="..."
poetry run python -m capturejob 

echo "Done"
```

## Configuration

The following environment variables need to be set

- JOB:  A name of the job which is used in the storage folder name created
- CAPTURE_CONNECTION_STRING: Azure connection string
- CAPTURE_CONTAINER_NAME: Azure container name
