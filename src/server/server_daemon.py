#This daemon passes messages between the server and the client.
#It does not have authority over verifying game state or the validity of data inside of messages-
#-just that they are formatted correctly

#It recieves input in a buffer from the server and the client, then sorts, validates, and formats their message before sending to-
#-the intended recipient.

#If the input buffer is full, daemon sends a message to indicate this, and then the client or server must block until the-
#-daemon indicates that it is not full anymore.
