"""
    To use this implementation, you simply have to implement `agent_function` such that it returns a legal action.
    You can then let your agent compete on the server by calling
        python3 example.py path/to/your/config.json
    
    You can interrupt the script at any time.
    The server will remember the actions you have sent.

    Note:
        By default the client bundles multiple requests for efficiency.
        This can complicate debugging.
        You can disable it by setting `parallel_runs=False` in the last line.
"""


def initialize_mdp(cave):
    states = []  # Generate all possible states
    transition_probs = {}  # Transition probabilities
    rewards = {}  # Rewards for transitions
    for r, row in enumerate(cave):
        for c, cell in enumerate(row):
            if cell != 'X':  # If not a wall
                state = (r, c)  # Example state representation
                states.append(state)
                # Define transition probabilities and rewards here
                # E.g., for each state-action pair
                # transition_probs[state, action, next_state] = probability
                # rewards[state, action, next_state] = reward_value
    return states, transition_probs, rewards


def agent_function(request_data, request_info):
    # TODO: Implement this function in a better way.
    # The request_data contains all the relevant information (map, history, ...).
    # You can ignore request_info.
    print('I got the following request:')
    print(request_data)

    cave = request_data['map']
    initialize_mdp(cave)

    if not 'skill-points' in request_data:
        # allocate all skill points to navigation
        return {'navigation': request_data['free-skill-points'], 'fighting': 0}
    else:
        return 'EXIT'  # a very risk-averse strategy


if __name__ == '__main__':
    import sys, logging
    from client import run

    # You can set the logging level to logging.WARNING or logging.ERROR for less output.
    logging.basicConfig(level=logging.INFO)

    run(
        agent_function=agent_function,
        agent_config_file=sys.argv[1],
        parallel_runs=False,  # Set it to False for debugging.
        run_limit=1,  # Stop after 1000 runs. Set to 1 for debugging.
    )
