# Protocol Blueprint
### Transport Layer & Packet Framing Mechanism
**Transport Protocol**: TCP
**Serialization Format**: Structured JSON
**Framing Rule**: Every JSON object is UTF-8 encoded and terminated by a newline character \n (0x0A). The receiver accumulates incoming bytes into a stream buffer until a \n is encountered, extracts the complete line, and deserializes the JSON object.
**Wire Stream Example (Continuous Stream)**:
```
{"msg_type":"CONNECT"}\n
{"msg_type":"LOBBY_WAIT","playerno":1}\n
{"msg_type":"START_GAME","playerno":1}\n
{"msg_type":"GAME_START","cards":[...]}\n
```
**JSON Schema/Structure Specification (STATE_UPDATE)**:
```
{
  "msg_type": "STATE_UPDATE",
  "cardinplay": {
    "color": "RED",
    "type": "5"
  },
  "curturnid": 2,
  "players": [
    {
      "id": 1,
      "handsize": 4
    },
    {
      "id": 2,
      "handsize": 6
    },
    {
      "id": 3,
      "handsize": 3
    }
  ]
}
```

### Application Message Types
##### CONNECT
Client -> Server
Request to join the game room. As long as the game has not already started and there are less than four players already in the lobby, the client is added to the lobby.
```
msg_type: String, must be "CONNECT"
```
##### LOBBY_WAIT
Server -> Client
Notification that the player has successfully entered the lobby before the game has begun, assigning them the lowest unassigned player number out of 1, 2, 3, or 4.
```
msg_type: String, must be "LOBBY_WAIT"
playerno: Int, player's assigned id, must be between 1 and 4
```
##### START_GAME
Client -> Server
Request to start game. Only the first player to enter the lobby may send this request, and this request is only accepted when there are 2 or more players waiting. ID is not explicitly sent, instead using the TCP socket to identify the player, since another client could maliciously make the game start early by spoofing IDs or IPs.
```
msg_type: String, must be "START_GAME"
```
##### GAME_START
Server -> Clients
Indicates that the game has started to all clients and distributes hands.

```
msg_type: String, must be "GAME_START"
```
##### DRAW
Client -> Server
Requests to draw a card from the server into the client hand. Response from server contains a JSON with a random card. ID is not explicitly sent, instead using the TCP socket to identify the player, since another client could maliciously make another client draw by spoofing IDs or IPs.
```
msg_type: String, must be "DRAW"
```
##### PLACE
Client -> Server
Requests to put a card from the client hand into play on the "center of the table." This request is accepted if the card presented by the client is in the current list of acceptable cards to play. When rejected, the server sends an error message saying why the request was rejected. ID is not explicitly sent, instead using the TCP socket to identify the player, since another client could maliciously make another client place a card by spoofing IDs or IPs.

```
msg_type: String, must be "PLACE"
card: {
  color: String, must be a valid color in UNO or "n/a"
  type: String, must be a number or type from UNO
}
```
##### DEAL
Server -> Client
Deals a single card to a client.
```
msg_type: String, must be "DEAL"
  card: {
    color: String, must be a valid color in UNO or "n/a"
    type: String, must be a number or type from UNO
  }
```
##### STATE_UPDATE
Server -> Clients
Sends the current total number of cards in each client's hands, who's turn it is, the turn queue order, as well as the current card in play. This message is sent every time a client's hand size changes, or a card is played.

```
msg_type: String, must be "STATE_UPDATE"
cardinplay: {
  color: String, must be a valid color in UNO or "n/a"
  type: String, must be a number or type from UNO
}
curturnid: Int, id of the current player who's turn it is.
playerids: an array of player objects {
  player: {
    id: Int, player id
    handsize: Int, the current player's hand size
}
```
##### GAME_OVER
Server -> Client
Sent when a client runs out of cards, declaring them the winner. This packet sends an ordered list of how many cards each player had in the end. 
```
msg_type: String, must be "GAME_OVER"
winner: Int, winning ID.
players: {
    player: {
      id: Int, player id
      handsize: Int, the current player's hand size
  }
```
##### ERROR
Server -> Client
Server notifies the client of a rejected request, malformed packet, unplayable card, out-of-turn move, or otherwise erroneous input.
```
msg_type: String, must be "ERROR"
msg: String, a message indicating why the error is being sent.
```
##### FORFEIT
Client -> Server
Notifies the server that a client is disconnecting so that their turn may be skipped on future rotations. ID is not explicitly sent, instead using the TCP socket to identify the player, since another client could maliciously make another client forfeit by spoofing IDs or IPs.
```
msg_type: String, must be "FORFEIT"
```


