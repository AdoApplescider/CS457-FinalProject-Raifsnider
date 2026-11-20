#This file contains the code that updates the gamestate UI in response to recieved messages from the server

from src.client.game_state import GameState

def ui_consumer(incoming, player_id, stop):
    game = GameState()
    game.my_player_id = player_id
    notification = "Type in the prompt below. (placeholder)"

    while not stop.is_set():

        msg = incoming.get()

        if msg == None:
            break
        elif msg.get("msg_type") == "STATE_UPDATE":
            game.update_state(msg)
            # construct ui
            # print ui
        elif msg.get("msg_type") == "ERROR":
            notification = "ERROR: " + msg.get("msg")
        elif msg.get("msg_type") == "MESSAGE":
            notification = msg.get("msg")
        else:
            notification = f"ERROR: Unrecognized message type {msg.get("msg_type")} recieved."