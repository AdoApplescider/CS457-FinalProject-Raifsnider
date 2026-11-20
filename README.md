### What is this project?
This is a simplified implementation of UNO, meant to run with at least 2, and up to 4 players.

The objective of the game is that the first player to empty their hand wins. Players take turns placing a singular card into play, after which, the next player must place a card with either a matching color or number on top of. Wildcards can be played at any time, and the player who played the card can choose what color it appears as. Cards can be drawn by any player at any time. There are additionally cards with extra effects, like one that skips the upcoming player when played, one that reverses turn order, and two types which cause the next player to draw cards.

### How do I start the application?
First, the server must be opened using the command `python -m src.server.server` where you can optionally define `-p <port number>`, otherwise the server opens on port 5000 by default.

Next, you open up to four clients using the command `python -m src.client.client -i <DNS host name> -p <server port>`.
When there are at least two clients connected to the server, the first client can press enter on their command line to start up the game.