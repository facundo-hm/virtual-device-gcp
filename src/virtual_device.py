from click import command, option, echo, group, Choice
from dotenv import load_dotenv
import os

from jwt_utils import create_jwt
from client import get_client, subscribe_to_config, subscribe_to_command

load_dotenv()

@group()
@option(
    '--project_id',
    default=os.getenv('GCP_PROJECT_ID'),
    help='GCP project id')
@option(
    '--cloud_region',
    default=os.getenv('CLOUD_REGION'),
    help='GCP project region')
@option(
    '--registry_id',
    default=os.getenv('REGISTRY_ID'),
    help='GCP regisry id')
@option(
    '--device_id',
    default=os.getenv('DEVICE_ID'),
    help='Device id')
@option(
    '--private_key_file',
    default=os.getenv('PRIVATE_KEY_FILE'),
    help='Private key file path')
@option(
    '--algorithm',
    default=os.getenv('ALGORITHM'),
    help='Algorithm')
@option(
    '--mqtt_bridge_hostname',
    default='mqtt.googleapis.com',
    help='MQTT bridge hostname')
@option(
    '--mqtt_bridge_port',
    default=8883,
    help='MQTT bridge port 8883 or 443')
@option(
    '--ca_certs',
    default=os.getenv('CA_CERTS'),
    help='CA root from https://pki.google.com/roots.pem')
@option('--config', is_flag=True)
@option('--command', is_flag=True)
def mqtt_client(
    project_id: str,
    cloud_region: str,
    registry_id: str,
    device_id: str,
    private_key_file: str,
    algorithm: str,
    mqtt_bridge_hostname: str,
    mqtt_bridge_port: int,
    ca_certs: str,
    config: bool,
    command: bool):
    password = create_jwt(project_id, private_key_file, algorithm)
    client = get_client(project_id, cloud_region, registry_id, device_id, password,
                        mqtt_bridge_hostname, mqtt_bridge_port, ca_certs)

    if config:
        subscribe_to_config(client, device_id)

    if command:
        subscribe_to_command(client, device_id)


@mqtt_client.command()
@option('--num_messages', default=1, help='Number of messages.')
@option('--device_messages', prompt='Your device message', help='The message to send.')
def send_message(num_messages: int, device_messages: str):
    """Simple program that sends messages."""
    for _ in range(num_messages):
        echo('Sending message: %s' % device_messages)

if __name__ == '__main__':
    mqtt_client()
