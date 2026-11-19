#This is the file for the code with all the main server thread's functionality
#The server is responsible for managing and communicating all parts of the game state to the other parts of the system.

#There's a thread listener which makes new client connections and sends them to the main thread through the queue
#The main thread listens to the queue and either adds that new client connection to it's list or starts the game and ends the
#listener thread.

import socket
import threading
import queue
import argparse

from src.models.game import Game
from .client_handler import client_handler
from . import server_protocol

def parse_args():
    parser = argparse.ArgumentParser(
        description="The Multi-client TCP server for a game of UNO."
    )

    parser.add_argument(
        "-p", "--port",
        type=int,
        default=5000,
        help="Listening port (default: 5000)"
    )

    args = parser.parse_args()

    return args

def initialize_listener(args):
    listener = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    listener.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    listener.bind(("0.0.0.0", args.port))
    listener.listen()

    print(f"UNO Server Listening on 0.0.0.0:{args.port}")

    return listener

def listener_thread(listener_socket, from_clients, game):
    listener_socket.settimeout(1.0)

    try:
        while not game.started:
            try:
                client_socket, address = listener_socket.accept()

                to_client = queue.Queue()

                client_thread = threading.Thread(
                    target=client_handler,
                    args=(
                        to_client,
                        from_clients,
                        client_socket,
                        address
                    ),
                    daemon=True
                )

                from_clients.put(("listener", to_client))
                client_thread.start()

            except socket.timeout:
                continue

    finally:
        listener_socket.close()

def process_lobby(from_clients, to_clients, game):
    source, message = from_clients.get()

    if source == "listener":
        try:
            to_client = message
            player = game.add_player()
            server_protocol.send_connected_msg(to_client, player.id)
            to_clients[player.id] = to_client
            print(f"Player {player.id} joined!")
        except (ValueError, RuntimeError) as msg:
            server_protocol.send_error_msg(to_client, str(msg), True)
    else:
        if message.get("msg_type") == "START_GAME":
            try:
                game.start()
                print("Game started!")
            except (ValueError, RuntimeError) as msg:
                server_protocol.send_error_msg(to_clients[source], str(msg))
        else:
            server_protocol.send_error_msg(to_clients[source], "Game has not yet begun.")


def main():
    args = parse_args()
    listener_socket = initialize_listener(args)
    from_threads = queue.Queue()
    to_clients = {}
    game = Game()

    listener = threading.Thread(
        target=listener_thread,
        args=(
            listener_socket,
            from_threads,
            game
        ),
        daemon=True
    )
    listener.start()

    print("Waiting for players...")
    while not game.started:
        process_lobby(from_threads, to_clients, game)

    #TODO: process game protocol

if __name__ == "__main__":
    main()