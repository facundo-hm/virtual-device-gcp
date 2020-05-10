from typing import Tuple
from click import (
    command, option, echo, group, Choice, pass_context, Context
)
from dotenv import load_dotenv
import os
import time
from threading import Thread

from jwt_utils import create_jwt
from client import (
    get_client, subscribe_to_topic, disconnect,
    publishPayload, CONFIG_TOPIC, COMMANDS_TOPIC
)

load_dotenv()

CLIENT = 'client'
DEVICE_ID = 'device_id'
EVENTS_TOPIC = 'events'
STATE_TOPIC = 'state'
EXIT_VALUE = 'exit'

class NonBlockingInput(Thread):
    def __init__(self, input_callback = None, name='non-blocking-input'):
        self.input_callback = input_callback
        self._running = True
        super().__init__(name=name)
        self.start()

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            self.input_callback(input())

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
@pass_context
def mqtt_client(ctx: Context, project_id: str, cloud_region: str, registry_id: str,
                device_id: str, private_key_file: str, algorithm: str, 
                mqtt_bridge_hostname: str, mqtt_bridge_port: int, ca_certs: str):
    password = create_jwt(project_id, private_key_file, algorithm)
    client = get_client(project_id, cloud_region, registry_id, device_id, password,
                        mqtt_bridge_hostname, mqtt_bridge_port, ca_certs)

    time.sleep(2)

    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    ctx.obj[CLIENT] = client
    ctx.obj[DEVICE_ID] = device_id


@mqtt_client.command()
@option(
    '--topic',
    '--t',
    type=Choice([CONFIG_TOPIC, COMMANDS_TOPIC], case_sensitive=True),
    required=True,
    multiple=True)
@pass_context
def subscribe(ctx: Context, topic: Tuple[str]):
    client = ctx.obj[CLIENT]
    device_id = ctx.obj[DEVICE_ID]

    def readInput(value):
        if (value == EXIT_VALUE):
            disconnect(client)
            non_blocking_input.stop()

    non_blocking_input = NonBlockingInput(readInput)

    for t in topic:
        subscribe_to_topic(client, device_id, t)

    echo('Type exit <Enter> to disconnect')


@mqtt_client.command()
@option('--message',
        prompt='Your device message', help='The message to send.')
@option('--topic',
        prompt='MQTT topic',
        type=Choice([EVENTS_TOPIC, STATE_TOPIC],
        case_sensitive=True))
@pass_context
def publish(ctx: Context, message: str, topic: str):
    client = ctx.obj[CLIENT]
    deviceId = ctx.obj[DEVICE_ID]

    publishPayload(client, deviceId, topic, message)

    time.sleep(2)

    disconnect(client)


if __name__ == '__main__':
    mqtt_client()
