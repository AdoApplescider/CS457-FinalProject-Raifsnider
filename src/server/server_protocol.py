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

def send_state_update(to_clients, game):
    n = len(game.players)

    active_color = game.active_color.value
    active_type = game.active_type.value
    active_player = game.active_player
    turn_order = [((game.active_player + i * game.turn_step) % n) + 1 for i in range(n)]
    player_hand_sizes = [{"id": p.id, "hand_size": len(p.hand)}for p in game.players]

    for player in game.players:
        my_hand = player.hand_to_dict()

        msg = {
                    "msg_type": "STATE_UPDATE",
                    "active_color": active_color,
                    "active_type": active_type,
                    "active_player_id": active_player,
                    "turn_order": turn_order,
                    "player_hand_sizes": player_hand_sizes,
                    "my_hand": my_hand
                }

        to_clients[player.id].put(msg)