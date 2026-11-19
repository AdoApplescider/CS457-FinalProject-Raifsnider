#The client is just an interface for the user and server to communicate information.
#It has no authority over game state, and simply displays information from the server in a-
#-human readable format, and passes the user's requests for game actions to the server, to which
#it then tells the user how the server responded. e.g. "drew 1 card," or "waiting for server," or "That card doesn't match!"

import argparse
import socket
import sys

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


def main():
    args = parse_args()
    addresses = resolve_server(args.i, args.p)
    client_socket = connect_to_server(addresses)

    # TODO: Start client communication handler

if __name__ == "__main__":
    main()