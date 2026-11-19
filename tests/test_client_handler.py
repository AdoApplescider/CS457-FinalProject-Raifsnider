import unittest
import socket
import threading
import queue
import json

from src.server.client_handler import client_handler


class TestClientConnection(unittest.TestCase):

    def test_client_connection(self):

        # Create a pair of connected sockets
        server_socket, client_socket = socket.socketpair()

        from_server = queue.Queue()
        to_server = queue.Queue()

        # Simulate the main server registering the player
        from_server.put({
            "msg_type": "CONNECTED",
            "player_id": 1
        })

        # Start the client handler
        handler = threading.Thread(
            target=client_handler,
            args=(
                from_server,
                to_server,
                server_socket,
                ("test", 0)
            ),
            daemon=True
        )

        handler.start()

        # Receive the CONNECTED message
        response = b""

        while b"\n" not in response:
            response += client_socket.recv(4096)

        response = response.split(b"\n", 1)[0]
        response = json.loads(response.decode("utf-8"))

        # Verify the response
        self.assertEqual(response["msg_type"], "CONNECTED")
        self.assertEqual(response["player_id"], 1)

        # Disconnect
        client_socket.close()
        handler.join(timeout=2)

        self.assertFalse(handler.is_alive())


    def test_client_message_forwarding(self):

        server_socket, client_socket = socket.socketpair()

        from_server = queue.Queue()
        to_server = queue.Queue()

        from_server.put({
            "msg_type": "CONNECTED",
            "player_id": 7
        })

        handler = threading.Thread(
            target=client_handler,
            args=(
                from_server,
                to_server,
                server_socket,
                ("test", 0)
            ),
            daemon=True
        )

        handler.start()

        # Consume the initial CONNECTED message
        response = b""

        while b"\n" not in response:
            response += client_socket.recv(4096)

        # Send a message to the handler
        message = {
            "msg_type": "DRAW"
        }

        client_socket.sendall(
            (json.dumps(message) + "\n").encode("utf-8")
        )

        # Wait for the main server to receive it
        player_id, received_message = to_server.get(timeout=2)

        self.assertEqual(player_id, 7)
        self.assertEqual(received_message["msg_type"], "DRAW")

        # Cleanup
        client_socket.close()
        handler.join(timeout=2)


    def test_multiple_messages(self):

        server_socket, client_socket = socket.socketpair()

        from_server = queue.Queue()
        to_server = queue.Queue()

        from_server.put({
            "msg_type": "CONNECTED",
            "player_id": 3
        })

        handler = threading.Thread(
            target=client_handler,
            args=(
                from_server,
                to_server,
                server_socket,
                ("test", 0)
            ),
            daemon=True
        )

        handler.start()

        # Consume CONNECTED response
        response = b""

        while b"\n" not in response:
            response += client_socket.recv(4096)

        # Send two messages together
        messages = [
            {"msg_type": "DRAW"},
            {"msg_type": "PLACE", "card_id": 5}
        ]

        payload = "".join(
            json.dumps(msg) + "\n"
            for msg in messages
        )

        client_socket.sendall(payload.encode("utf-8"))

        # Verify both messages arrive
        received = [
            to_server.get(timeout=2),
            to_server.get(timeout=2)
        ]

        self.assertEqual(received[0][1]["msg_type"], "DRAW")
        self.assertEqual(received[1][1]["msg_type"], "PLACE")

        client_socket.close()
        handler.join(timeout=2)


    def test_fragmented_message(self):

        server_socket, client_socket = socket.socketpair()

        from_server = queue.Queue()
        to_server = queue.Queue()

        from_server.put({
            "msg_type": "CONNECTED",
            "player_id": 4
        })

        handler = threading.Thread(
            target=client_handler,
            args=(from_server, to_server, server_socket, ("test", 0)),
            daemon=True
        )

        handler.start()

        # Consume CONNECTED
        response = b""
        while b"\n" not in response:
            response += client_socket.recv(4096)

        # Send only part of a JSON message
        client_socket.sendall(b'{"msg_type":')

        # The message should not be forwarded yet
        with self.assertRaises(queue.Empty):
            to_server.get(timeout=0.3)

        # Send the rest
        client_socket.sendall(b'"DRAW"}\n')

        player_id, message = to_server.get(timeout=2)

        self.assertEqual(player_id, 4)
        self.assertEqual(message["msg_type"], "DRAW")

        client_socket.close()
        handler.join(timeout=2)

if __name__ == "__main__":
    unittest.main()