#This file holds all the methods which construct valid JSONs for communicating between client and server.

def send_draw_request(outgoing, amount):
    msg = {
            "msg_type": "DRAW",
            "amount": amount
        }

    outgoing.put(msg)

def send_play_request(outgoing, card_index, chosen_color=None):
    msg = {
            "msg_type": "PLAY",
            "card_index": card_index,
            "chosen_color": chosen_color
        }

    outgoing.put(msg)