from click import command, option, echo

@command()
@option('--num_messages', default=1, help='Number of messages.')
@option('--device_messages', prompt='Your device message', help='The message to send.')
def send_message(num_messages, device_messages):
    """Simple program that sends messages."""
    for _ in range(num_messages):
        echo('Sending message: %s' % device_messages)

if __name__ == '__main__':
    send_message()