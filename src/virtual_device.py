from click import command, option, echo, group, Choice
from dotenv import load_dotenv
import os

from jwt_utils import create_jwt
from client import get_client

load_dotenv()

@group()
@option('--project_id', default=os.getenv("GCP_PROJECT_ID"), help='GCP project id')
@option('--cloud_region', default=os.getenv("CLOUD_REGION"), help='GCP project region')
@option('--registry_id', default=os.getenv("REGISTRY_ID"), help='GCP regisry id')
@option('--device_id', prompt='Your device id', help='Device id')
@option('--private_key_file', default=os.getenv('PRIVATE_KEY_FILE'), help='Private key file path')
@option('--algorithm', default=os.getenv('ALGORITHM'), help='Algorithm')
@option('--mqtt_bridge_hostname', default='mqtt.googleapis.com', help='MQTT bridge hostname')
@option('--mqtt_bridge_port', default=8883, help='MQTT bridge port 8883 or 443')
def mqtt_client(project_id, cloud_region, registry_id, device_id, private_key_file,
                algorithm, mqtt_bridge_hostname, mqtt_bridge_port):
    password = create_jwt(project_id, private_key_file, algorithm)
    get_client(project_id, cloud_region, registry_id, device_id,
            password, mqtt_bridge_hostname, mqtt_bridge_port, ca_certs)


@mqtt_client.command()
@option('--num_messages', default=1, help='Number of messages.')
@option('--device_messages', prompt='Your device message', help='The message to send.')
def send_message(num_messages: int, device_messages: str):
    """Simple program that sends messages."""
    for _ in range(num_messages):
        echo('Sending message: %s' % device_messages)

if __name__ == '__main__':
    mqtt_client()
