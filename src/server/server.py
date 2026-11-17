#This is the file for the code with all the main server thread's functionality
#The server is responsible for managing and communicating all parts of the game state to the other parts of the system.

#There's a thread listener which makes new client connections and sends them to the main thread through the queue
#The main thread listens to the queue and either adds that new client connection to it's list or starts the game and ends the
#listener thread.
