# Repository for ss24.2.3/team136
This is the repository for you solution. You can modify this README file any way you see fit.

**Topic:** WS2324 Assignment 2.3: Wumpus Quest

# Assignment 2.3

This repository contains two implementations of the server protocol.
They require the `requests` library, which you can install with
```
python3 -m pip install requests
```
You simply have to implement the `agent_function`.

## Implementation 1: `client-simple-example`
This is a very minimal implementation,
which makes this useful if you want to do your own implementation in a different language
or modify the client implementation.
You can test your agent by running
```
python3 client_simple.py path/to/your/config.json
```
where `path/to/your/config.json` points to a configuration file with credentials for your client.
You should have configuration files for each environment in your repository.

## Implementation 2: `client-example`
This is a more complex and feature-rich implemetation that is under active development.
All the code for the server interaction is in `client.py` - you don't have to change anything there.
You can base your agent implementation on `example.py` and modify the `agent_function` in any way you see fit.
You can test your agent by running
```
python3 example.py path/to/your/config.json
```
where `path/to/your/config.json` points to a configuration file with credentials for your client.
You should have configuration files for each environment in your repository.


## Which client implementation should I use?
We recommend using the implementation from `client-example`.
It is more feature-rich, but just as easy to use.

    


