import ssl
from paho.mqtt.client import Client, connack_string, error_string
from click import secho, echo

CONFIG_TOPIC = 'config'
COMMANDS_TOPIC = 'commands'

def error_str(rc):
    return '{}: {}'.format(rc, error_string(rc))

def on_connect(client, userdata, flags, rc):
    secho('on_connect: ', fg='bright_green', nl=False)
    echo(connack_string(rc))

def on_disconnect(client, userdata, rc):
    secho('on_disconnect: ', fg='bright_green', nl=False)
    echo(error_str(rc))

def on_publish(client, userdata, msg):
    secho('on_publish: ', fg='bright_green', nl=False)
    echo('The message has been sent.')

def on_message(client, userdata, message):
    payload = str(message.payload.decode('utf-8'))

    secho('Received message: ', fg='bright_green', nl=False)
    echo('\'{}\' on topic \'{}\' with Qos {}'.format(
        payload, message.topic, str(message.qos)
    ))

def get_client(
    project_id: str,
    cloud_region: str,
    registry_id: str,
    device_id: str,
    password: str,
    mqtt_bridge_hostname: str,
    mqtt_bridge_port: str,
    ca_certs: str):
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id, cloud_region, registry_id, device_id
    )

    secho('Client ID: ', fg='bright_green', nl=False)
    echo('\'{}\''.format(client_id))

    client = Client(client_id=client_id)

    client.username_pw_set(username='unused', password=password)
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Assign callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to MQTT bridge
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    client.loop_start()

    return client

def subscribe_to_config(client: Client, device_id: str):
    mqtt_config_topic = '/devices/{}/config'.format(device_id)
    client.subscribe(mqtt_config_topic, qos=1)

def subscribe_to_command(client: Client, device_id: str):
    mqtt_command_topic = '/devices/{}/commands/#'.format(device_id)
    client.subscribe(mqtt_command_topic, qos=0)

def subscribe_to_topic(client: Client, device_id: str, topic: str):
    if topic == CONFIG_TOPIC:
        subscribe_to_config(client, device_id)

    if topic == COMMANDS_TOPIC:
        subscribe_to_command(client, device_id)

def disconnect(client: Client):
    client.disconnect()
    client.loop_stop()

def publishPayload(client: Client, device_id: str, topic:str, payload: str):
    mqtt_topic = '/devices/{}/{}'.format(device_id, topic)
    client.publish(mqtt_topic, payload, qos=1)
