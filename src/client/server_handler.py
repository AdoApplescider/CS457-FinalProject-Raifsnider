#This file handles the input and output from the client to the server

import json
import queue
import socket

def server_handler(sock, outgoing, incoming, stop):
    sock.settimeout(0.05)
    buffer = b""
    try:
        while not stop.is_set():
            try:
                while True:
                    msg = outgoing.get_nowait()
                    sock.sendall((json.dumps(msg) + "\n").encode("utf-8"))
            except queue.Empty:
                pass

            try:
                data = sock.recv(4096)
            except socket.timeout:
                continue
            if not data:
                break

            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line.strip():
                    continue
                try:
                    incoming.put(json.loads(line))
                except ValueError:
                    print("Dropping malformed message:", line[:100])
    except OSError as e:
        print("Socket error:", e)
    finally:
        sock.close()
        incoming.put(None)