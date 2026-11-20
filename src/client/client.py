#The client is just an interface for the user and server to communicate information.
#It has no authority over game state, and simply displays information from the server in a-
#-human readable format, and passes the user's requests for game actions to the server, to which
#it then tells the user how the server responded. e.g. "drew 1 card," or "waiting for server," or "That card doesn't match!"

import argparse
import socket
import sys
import threading
import queue
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

from src.client.server_handler import server_handler
from src.client.ui_manager import ui_consumer
from src.client.client_protocol import send_draw_request, send_game_start, send_play_request

def parse_args():

    parser = argparse.ArgumentParser(
        description="UNO Game Client"
    )

    parser.add_argument(
        "-i",
        required=True,
        metavar="HOSTNAME",
        help="DNS hostname of the UNO server"
    )

    parser.add_argument(
        "-p",
        type=int,
        default=5000,
        help="Server port number (default: 5000)"
    )

    return parser.parse_args()


def resolve_server(hostname, port):

    try:
        addresses = socket.getaddrinfo(
            hostname,
            port,
            type=socket.SOCK_STREAM
        )

        print(f"Successfully resolved hostname: {hostname}")

        return addresses

    except socket.gaierror:
        print(
            f"ERROR: Could not resolve server hostname '{hostname}'.\n"
            "Please check your hostname and your router's DNS configuration."
        )

        sys.exit(1)


def connect_to_server(addresses):

    for family, socktype, proto, canonname, sockaddr in addresses:

        client_socket = socket.socket(
            family,
            socktype,
            proto
        )

        try:
            client_socket.connect(sockaddr)

            print("Successfully connected to server!")

            return client_socket

        except OSError:
            client_socket.close()

    raise ConnectionError("Could not establish a connection to the server.")

def cli_prompt(outgoing, stop):
    session = PromptSession()

    HELP_TEXT = """Commands:
        draw [n]               draw n cards (default 1)
        play <index> [color]   play the card at that index; give a color for wild cards
        help                   show this message"""

    with patch_stdout():
        while not stop.is_set():
            try:
                line = session.prompt("> ")
            except (EOFError, KeyboardInterrupt):
                break

            parts = line.strip().casefold().split()

            match parts:
                case []:
                    continue
                case ["draw"]:
                    send_draw_request(outgoing, 1)
                case ["draw", amount] if amount.isdigit():
                    send_draw_request(outgoing, int(amount))
                case ["play", index] if index.isdigit():
                    send_play_request(outgoing, int(index), None)
                case ["play", index, color] if index.isdigit():
                    send_play_request(outgoing, int(index), color)
                case ["help"]:
                    print(HELP_TEXT)
                case _:
                    print(f"Unrecognized input: {line!r}. Type 'help' for accepted inputs.")

def main():
    args = parse_args()
    addresses = resolve_server(args.i, args.p)
    client_socket = connect_to_server(addresses)

    outgoing = queue.Queue()
    incoming = queue.Queue()
    stop = threading.Event()

    connection_handler = threading.Thread(
        target=server_handler,
        args=(
            client_socket,
            outgoing,
            incoming,
            stop
        ),
        daemon=True
    )
    connection_handler.start()

    init_message = incoming.get()
    my_id = -1

    if init_message.get("msg_type") == "CONNECTED":
        my_id = init_message.get("player_id")
        print(f"Server connection confirmed! You are player {my_id}")
    else:
        print(init_message.get("msg"))
        print("Connection to server rejected! Closing client connection...")
        stop.set()
        connection_handler.join(timeout=2)
        sys.exit(0)

    game_started = False
    msg = None
    while not game_started:
        if my_id == 1:
            input("Press enter to start the game!")
            send_game_start(outgoing)

        msg = incoming.get()
        if msg.get("msg_type") == "STATE_UPDATE":
            print("GAME STARTED!")
            game_started = True
        elif msg.get("msg_type") == "ERROR":
            print("ERROR: " + msg.get("msg"))
        else:
            raise ValueError("Invalid message recieved before game start.")

    ui_thread = threading.Thread(
        target=ui_consumer,
        args=(
            incoming,
            msg,
            my_id,
            stop
        ),
        daemon=True
    )
    ui_thread.start()

    while not stop.is_set():
        cli_prompt(outgoing, stop)

    time.sleep(2)

    sys.exit(0)

if __name__ == "__main__":
    main()