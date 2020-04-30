import ssl
import paho.mqtt.client as mqtt

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(client, userdata, flags, rc):
    print('on_connect', mqtt.connack_string(rc))

def on_disconnect(client, userdata, rc):
    print('on_disconnect', error_str(rc))

def on_publish(client, userdata, mid):
    print('on_publish')

def on_message(client, userdata, message):
    payload = str(message.payload.decode('utf-8'))
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

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
        project_id, cloud_region, registry_id, device_id)

    print('Client ID \'{}\''.format(client_id))

    client = mqtt.Client(client_id=client_id)

    client.username_pw_set(username='unused', password=password)

    # Assign callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to MQTT bridge
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # Configuration topic
    mqtt_config_topic = '/devices/{}/config'.format(device_id)
    client.subscribe(mqtt_config_topic, qos=1)

    # Command topic
    mqtt_command_topic = '/devices/{}/commands/#'.format(device_id)
    client.subscribe(mqtt_command_topic, qos=0)

    return client
