# Virtual Device - GCP

## Project description
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads)

## Getting started
Install dependencies
```sh
$ pip install -r requirements.txt
```

Create `.env` file and define the variables
```sh
$ cp env.sample .env
```

## Usage
```sh
$ python src/virtual_device.py --device_id <my-device-id> publish --topic state --message <my-message>
```

```sh
virtual_device.py [OPTIONS] COMMAND [ARGS]...

Options:
  --project_id TEXT            GCP project id
  --cloud_region TEXT          GCP project region
  --registry_id TEXT           GCP regisry id
  --device_id TEXT             Device id
  --private_key_file TEXT      Private key file path
  --algorithm TEXT             Algorithm
  --mqtt_bridge_hostname TEXT  MQTT bridge hostname
  --mqtt_bridge_port INTEGER   MQTT bridge port 8883 or 443
  --ca_certs TEXT              CA root from https://pki.google.com/roots.pem
  --help                       Show this message and exit.

Commands:
  publish
  subscribe
```