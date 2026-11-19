#This file holds all the methods which construct valid JSONs for communicating between server and client.

def send_connected_msg(to_client, player_id):
    msg = {
            "msg_type": "CONNECTED",
            "player_id": player_id
        }

    to_client.put(msg)

def send_error_msg(to_client, msg, ends_conn=False):
    error = {
        "msg_type": "ERROR",
        "msg": msg,
        "ends_conn": ends_conn
    }

    to_client.put(error)