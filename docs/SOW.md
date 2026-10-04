# CS 457 Project Statement of Work (SOW) & Protocol Specification Template

**Student Name:** Adam James Raifsnider 
**Date:** [2026-09-20]  
**Course:** CS 457 - Computer Networks  
**Target Server Domain:** `server.raifsnider.edu`  

---

## 1. Game Selection & Scope (Sprint 0)

> Planning is going to be an iterative process through the sprints so you don't have to have all the details now. Focus on big overview concepts. You will be updating the SOW as we plan.
> You have a lot of freedom to choose a game. There are a couple caveats.  

> - It must run in the console. The lab nodes won't be able to handle extensive graphics.
> - It has to be self-contained. You can use a internet-connector to download you code, but because the architecture must run 5 nodes you won't be able to run 
> - You are encouraged to use python, but I'm not going to make it a strict requirement. The instructor and TA's ability to help with C or Rust, etc will be diminished in other languages.

### 1.1 Game Overview
- **Chosen Game:** UNO
- **Player Capacity:** 4 Players (Simulated via 4 CML Client nodes)
- **Game Summary:** Regular cards have a color and a number, and there are special cards with certain effects. There is always one card in the center of the table and players may place a card of the same color or number on top of that card, which ends their turn. The first player to have zero cards wins. Players are dealt 7 cards at the beginning of the game, and may draw more at any time. Players take turns in a set order (this order can be reversed by playing a reverse card).

### 1.2 Core Game Rules & Win/Draw Conditions
- **Turn Mechanics:** As soon as any player places a valid card, their turn immediately ends and goes to the next player in order. Each player has a round turn order as though they are sitting at a table and taking turns clockwise or counterclockwise.
- **Victory Condition:** If a player has zero cards left at the end of their turn, they are declared the winner.
- **Draw/Tie Condition:** There are no ties or draws in this game.

---

## 2. Application-Layer Messaging Protocol Blueprint (Sprint 1 Deliverable)

### 2.1 Message Transport & Serialization Format
- **Transport Protocol:** TCP
- **Serialization Format:** JSON
- **Framing Mechanism:** JSON payloads (includes player hand, opponent card counts, and the card currently on the table)

### 2.2 Message Schema Definitions

#### Message Types:
1. `CONNECT` (Client -> Server): Request to join the game room.
2. `LOBBY_WAIT` (Server -> Client): Notification that server is waiting for at least three players. Player turn order is determined by what order players joined in.
3. `GAME_START` (Server -> Clients): Game initiated, hands are dealt.
4. `DRAW` (Client -> Server): Player draws a random card and adds it to their hand.
5. `PLACE` (Client -> Server): Player places a card and ends their turn.
5. `STATE_UPDATE` (Server -> Clients): Broadcast current game board. Includes the card on the table, active player turn, and how many cards each player has.
6. `GAME_OVER` (Server -> Clients): Victory and final scores.
7. `ERROR` (Server -> Client): Invalid move or malformed packet error.

#### Example JSON Protocol Schema:
```json
{
  "msg_type": "PLACE",
  "player_id": "Player_1",
  "card": {
    "color": "green",
    "type": "reverse"
  },
  "timestamp": 1727000000
}
```

---

### 2.3 Game State Machine (FSM) Design (Sprint 1 Deliverable)
- **State Transitions:** Detail state flow: `INIT` -> `WAITING_FOR_PLAYERS` -> `PLAYER_TURN` -> `GAME_END`.

---

## 3. Game Behavior & Server Concurrency Architecture (Sprint 2 Deliverable)

### 3.1 Server Concurrency Strategy
- **Architecture Choice:** [Multi-Threading (`threading.Thread`) OR Non-blocking I/O multiplexing (`select.select` / `selectors`)]
- **Synchronization Logic:** Explain how shared game state and client list are thread-safe (e.g. `threading.Lock`) to prevent race conditions during turn processing.

### 3.2 State & Score Synchronization Across Clients
- **Turn Enforcement:** Detail how the server validates active player ID before processing moves and broadcasts updated turn notifications to all clients.
- **Score & Board Synchronization:** Describe how state broadcasts keep client screens synchronized in real time.

---

## 4. Coding & AI Implementation Plan (Sprint 3)

- **Permitted AI Tools:** [e.g., GitHub Copilot, ChatGPT, Claude]
- **AI Prompting & Constraint Strategy:** Explain how you will constrain AI models to generate code (in Python or your chosen language) that adheres strictly to the protocol blueprint and FSM designed in Sprints 1 & 2.
I will design all of the architecture by hand using a specification document, then refine this into UML diagrams, then write pseudocode which implements the architecture plan, then attempt to hand-implement the actual code. I will only input segments of my own plan into AI, requesting advice on implementation if I am unsure of best practices for that specific block of code. AI will never make decisions about my architecture, only specific, locally scoped implementation details.
- **Implementation Risk Management:** Detail your plan to leverage past programming experience and manage time to ensure code completion on schedule.
I will implement this code in a modular fashion, starting with the core systems that are required for a round to progress, and gradually adding optional gameplay features like reverse or block cards. This way, I can have a viable first product early on, and focus on refinement for the remaining development time.

---

## 5. CML Multi-Subnet Topology & Wireshark Deployment Plan (Sprint 4 & 5 Deliverable)

> For now you can use the topology below. We may update this when we get to defining subnets.

### 5.1 Subnet & Router Design
- **Subnet A (Client 1):** `192.168.10.0/24` (Interface `Gi0/1` on Router R1)
- **Subnet B (Client 2):** `192.168.11.0/24` (Interface `Gi0/2` on Router R1)
- **Subnet C (Game Server):** `192.168.20.0/24` (Interface `Gi0/1` on Router R2)
- **Router Backbone:** `10.0.0.0/30` (Interface `Gi0/0` on R1 <-> `Gi0/0` on R2)

### 5.2 DHCP Pools & DNS Configuration Plan
- **Router R1 DHCP Pool 1 (`CLIENT1_POOL`):** Leases `192.168.10.10` - `192.168.10.50`, gateway `192.168.10.1`, DNS `10.0.0.2`.
- **Router R1 DHCP Pool 2 (`CLIENT2_POOL`):** Leases `192.168.11.10` - `192.168.11.50`, gateway `192.168.11.1`, DNS `10.0.0.2`.
- **Router R2 Authoritative DNS:** Configured with `ip dns server` and static host mapping `server.[yourlastname].edu` -> `192.168.20.100`.

### 5.3 Deployment Strategy & Wireshark Trace Capture
- **CML Deployment Strategy:** Deploy `server.py` onto Subnet C node (`192.168.20.100`) behind Router R2, and `client.py` onto Subnet A and Subnet B nodes behind Router R1.
- **Cisco Infrastructure Configuration:** Router R1 DHCP pools (`CLIENT1_POOL`, `CLIENT2_POOL`) and Router R2 authoritative DNS (`ip host server.[lastname].edu 192.168.20.100`).
- **Wireshark Trace Capture Plan:** Capture DHCP DORA exchange (`dhcp_negotiation.pcap`) and DNS query/response resolution (`dns_lookup.pcap`).
