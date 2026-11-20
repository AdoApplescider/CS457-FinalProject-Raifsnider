#This file contains the code that updates the gamestate UI in response to recieved messages from the server

from src.client.game_state import GameState

def ui_consumer(incoming, msg, my_id, stop):
    state = GameState.from_msg(msg)
    notification = "Type 'help' below for info on the possible inputs!"
    print(render_state(state, my_id, notification))

    while not stop.is_set():

        msg = incoming.get()

        if msg == None:
            break
        elif msg.get("msg_type") == "STATE_UPDATE":
            state = GameState.from_msg(msg)
        elif msg.get("msg_type") == "ERROR":
            notification = "ERROR: " + msg.get("msg")
        elif msg.get("msg_type") == "MESSAGE":
            notification = msg.get("msg")
        elif msg.get("msg_type") == "GAME_OVER":
            print(render_scoreboard(msg, my_id))
            stop.set()
        else:
            notification = f"ERROR: Unrecognized message type {msg.get("msg_type")} recieved."
        print(render_state(state, my_id, notification))
        notification = "Type 'help' below for info on the possible inputs!"

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"

def render_state(state, my_id, notification=""):
    if state.active_player_id == my_id:
        turn_line = "It's your turn!"
    else:
        turn_line = f"It's Player {state.active_player_id}'s turn!"

    card_line = f"Card in play: {state.active_color.value} {state.active_type.value}"

    order_line = "Upcoming turn order: " + " -> ".join(
        f"Player {pid}" for pid in state.turn_order
    )

    sizes_line = "Player hand sizes: " + ". ".join(
        f"Player {pid}, {plural(n, 'card')}" for pid, n in state.hand_sizes.items()
    )

    hand_line = "Your hand:\n  " + "\n  ".join(
        f"{i}. {c.color.value} {c.type.value}"
        for i, c in enumerate(state.my_hand, start=1)
    )

    notification_line = f"Notifications: {notification or '(none)'}"

    return "\n".join([
        turn_line,
        card_line,
        order_line,
        sizes_line,
        hand_line,
        "------------------",
        notification_line,
        "------------------",
    ])

def render_scoreboard(msg, my_id):
    scores = msg["scores"]
    lines = ["===== FINAL SCORES ====="]

    placement = 0
    prev_size = None
    for position, entry in enumerate(scores, start=1):
        pid = entry["id"]
        size = entry["hand_size"]

        if size != prev_size:
            placement = position
            prev_size = size

        name = "You" if pid == my_id else f"Player {pid}"
        lines.append(f"{ordinal(placement)}: {name} - {plural(size, 'card')} left")

    lines.append("========================")
    return "\n".join(lines)