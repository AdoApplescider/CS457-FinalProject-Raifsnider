# AI Prompting Strategy

## The Plan
While I do not plan to use AI tools for much of this project, when implementing AI into my workflow I will use prompts such as the following in order to ensure the AI agent follows my specifications. All AI-generated code would also be carefully reviewed and tested for coherency before implementing into the overall architecture.
## Protocol Implementation Prompt

The following prompt would be provided to an AI coding assistant before
generating networking code:

> You are implementing the networking layer for a multiplayer UNO game.
> You MUST follow the protocol defined in protocol_blueprint.md exactly.
>
> Transport:
> - Use TCP.
> - Use UTF-8 encoded JSON.
> - Every JSON message must be terminated by a newline character (`\n`).
> - The receiver must buffer incoming TCP data because TCP does not preserve
>   application message boundaries.
>
> Message types:
> - CONNECT
> - LOBBY_WAIT
> - START_GAME
> - GAME_START
> - DRAW
> - DEAL
> - PLACE
> - STATE_UPDATE
> - ERROR
> - GAME_OVER
> - FORFEIT
>
> Do not invent additional message types.
> Do not rename message types.
> Do not add or remove required fields.
> Do not change field names or data types.
> Do not use a different serialization or framing mechanism.
>
> If the protocol specification is ambiguous or missing information,
> do not invent a solution. Identify the ambiguity and ask for
> clarification instead.
>
> All generated networking code must validate incoming messages against
> the protocol before modifying game state.

