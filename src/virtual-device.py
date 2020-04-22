from click import command, option, echo
from dotenv import load_dotenv
import os

load_dotenv()

# test env var
print(os.getenv("GCP_PROJECT_ID"))

@command()
@option('--num_messages', default=1, help='Number of messages.')
@option('--device_messages', prompt='Your device message', help='The message to send.')
def send_message(num_messages: int, device_messages: str):
    """Simple program that sends messages."""
    for _ in range(num_messages):
        echo('Sending message: %s' % device_messages)

if __name__ == '__main__':
    send_message()