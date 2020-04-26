from click import command, option, echo, group
from dotenv import load_dotenv
import os

from jwt_utils import create_jwt

load_dotenv()

@group()
def mqtt_client():
    project_id = os.getenv("GCP_PROJECT_ID")
    private_key_file = os.getenv('PRIVATE_KEY_FILE')
    algorithm = os.getenv('ALGORITHM')

    password = create_jwt(project_id, private_key_file, algorithm)


@mqtt_client.command()
@option('--num_messages', default=1, help='Number of messages.')
@option('--device_messages', prompt='Your device message', help='The message to send.')
def send_message(num_messages: int, device_messages: str):
    """Simple program that sends messages."""
    for _ in range(num_messages):
        echo('Sending message: %s' % device_messages)

if __name__ == '__main__':
    mqtt_client()
