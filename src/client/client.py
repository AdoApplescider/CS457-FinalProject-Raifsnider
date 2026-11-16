#The client is just an interface for the user and server to communicate information.
#It has no authority over game state, and simply displays information from the server in a-
#-human readable format, and passes the user's requests for game actions to the server, to which
#it then tells the user how the server responded. e.g. "drew 1 card," or "waiting for server," or "That card doesn't match!"