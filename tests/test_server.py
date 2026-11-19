import queue

from unittest.mock import MagicMock

from src.server.server import process_lobby

def test_player_connection():
    from_clients = queue.Queue()
    to_clients = {}

    game = MagicMock()
    game.add_player.return_value = MagicMock(id=1)

    fake_client_queue = queue.Queue()

    from_clients.put(("listener", fake_client_queue))

    process_lobby(from_clients, to_clients, game)

    assert 1 in to_clients
    assert to_clients[1] is fake_client_queue

    print("Player connection test passed!")