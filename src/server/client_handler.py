#This daemon passes messages between the server and the client.
#It does not have authority over verifying game state or the validity of data inside of messages-
#-just that they are formatted correctly

#It receives input in a buffer from the server and the client, then sorts, validates, and formats their message before sending to-
#-the intended recipient.

import json
import queue
import socket

def client_handler(from_server, to_server, client_socket, address):
    player_id = -1
    from_client = queue.Queue()
    receive_buffer = b""
    client_socket.settimeout(0.1)

    try:
        msg = from_server.get()

        if msg.get("msg_type") == "CONNECTED":
            player_id = msg.get("player_id")
            handle_generic_msg(msg, client_socket)

        elif msg.get("msg_type") == "ERROR":
            if not handle_error(msg, client_socket):
                return

        else:
            raise ValueError("Unexpected initialization message")

        while (True):
            receive_buffer = receive_from_socket(client_socket, from_client, receive_buffer)
            if not from_server.empty():
                process_server_msg(from_server, client_socket)
            if not from_client.empty():
                process_client_msg(from_client, to_server, player_id)

    except (OSError, ValueError) as e:
        print(f"Client {address} disconnected: {e}")

    finally:
        client_socket.close()

def handle_generic_msg(msg, client_socket):
    try:
        serialized_msg = json.dumps(msg) + "\n"
        client_socket.sendall(serialized_msg.encode("utf-8"))
        print(msg)

    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid message format: {e}")

    except OSError as e:
        raise ConnectionError(f"Failed to send message: {e}")

def handle_error(msg, client_socket):
    handle_generic_msg(msg, client_socket)

    if msg.get("ends_conn", False):
        return False

    return True

def receive_from_socket(client_socket, from_client, buffer):
    try:
        data = client_socket.recv(4096)
    except socket.timeout:
        return buffer

    if not data:
        raise ConnectionError("Client disconnected.")

    buffer += data

    while b"\n" in buffer:
        raw_msg, buffer = buffer.split(b"\n", 1)
        if not raw_msg.strip():
            continue
        from_client.put(json.loads(raw_msg.decode("utf-8")))

    return buffer

def process_server_msg(from_server, client_socket):
    msg = from_server.get()
    match msg.get("msg_type"):
        case "STATE_UPDATE":
            handle_generic_msg(msg, client_socket)
        case "ERROR":
            handle_error(msg, client_socket)
        case _:
            raise ValueError("Invalid message type from server")

def process_client_msg(from_client, to_server, player_id):
    msg = from_client.get()
    match msg.get("msg_type"):
            case "GAME_START" | "DRAW" | "PLACE":
                to_server.put((player_id, msg))
            case _:
                to_server.put((
                    player_id,
                    {
                        "msg_type": "ERROR",
                        "message": "Invalid message type from client",
                        "ends_conn": False
                    }
                ))