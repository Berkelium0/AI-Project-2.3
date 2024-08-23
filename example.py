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
import time

import numpy as np

# Define constants
N, S, E, W = 'NORTH', 'SOUTH', 'EAST', 'WEST'
ACTIONS = [N, S, E, W, 'FIGHT', 'TELEPORT', 'EXIT']
NUM_ROWS = 12
NUM_COLS = 14

EXIT_VALUE = 10
GOLD_VALUE = 10000
WALK_VALUE = 0.1
TELEPORT_VALUE = -10
PIT_VALUE = -10000
WUMPUS_VALUE = -50


def find_initial_position(cave):
    total_gold = 0
    start = set()
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if cave[r][c] == 'S':
                start = (r, c)
            if cave[r][c] == 'G':
                total_gold += 1
    return start, total_gold


def move_agent(state, action, cave, skill_alloc, collected_gold, beaten_wumpus):
    r, c = state
    if action == N:
        next_state = (r - 1, c) if r > 0 and cave[r - 1][c] != 'X' else state
    elif action == S:
        next_state = (r + 1, c) if r < NUM_ROWS - 1 and cave[r + 1][c] != 'X' else state
    elif action == E:
        next_state = (r, c + 1) if c < NUM_COLS - 1 and cave[r][c + 1] != 'X' else state
    elif action == W:
        next_state = (r, c - 1) if c > 0 and cave[r][c - 1] != 'X' else state

    # Example: Assign a reward and probability
    if cave[r][c] == 'G' and (r, c) not in collected_gold:
        reward = GOLD_VALUE
    elif cave[r][c] == 'W' and (r, c) not in beaten_wumpus:
        reward = WUMPUS_VALUE
    elif cave[r][c] == 'P':
        reward = PIT_VALUE
    else:
        reward = WALK_VALUE

    prob = 1 - (1 / skill_alloc["navigation"])

    return next_state, prob, reward


def fight_wumpus(state, skill_alloc):
    reward = 1

    prob = 1 - (1 / skill_alloc["fighting"])

    return state, prob, reward


def find_teleport_targets(state, cave):
    teleport_targets = []
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if cave[r][c] == 'T' and (r, c) != state:
                teleport_targets.append((r, c))

    return teleport_targets


def initialize_mdp(cave, skill_alloc, collected_gold, beaten_wumpus):
    states = []
    transition_probs = {}
    rewards = {}

    # Iterate over each cell in the cave
    for r in range(NUM_ROWS - 1):
        for c in range(NUM_COLS - 1):
            if cave[r][c] != 'X':  # Not a wall
                state = (r, c)  # State represented as (row, col)
                states.append(state)

                # Initialize transition probabilities and rewards for each action
                for action in ACTIONS:
                    transition_probs[(state, action)] = []
                    rewards[(state, action)] = []

                    if action in [N, S, E, W]:
                        # Calculate next position based on the action
                        next_state, prob, reward = move_agent(state, action, cave, skill_alloc, collected_gold,
                                                              beaten_wumpus)
                        transition_probs[(state, action)].append((next_state, prob))
                        rewards[(state, action)].append(reward)

                    elif action == 'FIGHT':
                        if cave[r][c] == 'W':  # Fight only if there's a Wumpus
                            next_state, prob, reward = fight_wumpus(state, skill_alloc)
                            transition_probs[(state, action)].append((next_state, prob))
                            rewards[(state, action)].append(reward)

                    elif action == 'TELEPORT':
                        if cave[r][c] == 'T':  # Teleport only if on a teleporter
                            teleport_states = find_teleport_targets(state, cave)
                            for ts in teleport_states:

                                prob = (1-(1/skill_alloc["navigation"])) / len(teleport_states)
                                transition_probs[(state, action)].append((ts, prob))
                                rewards[(state, action)].append(TELEPORT_VALUE)  # Example: -1 reward for risky teleport

                    elif action == 'EXIT':
                        if cave[r][c] == 'S':  # Exit only if at the stairs
                            transition_probs[(state, action)].append((None, 1))
                            rewards[(state, action)].append(EXIT_VALUE)

    return states, transition_probs, rewards


def value_iteration(states, transition_probs, rewards, cave, collected_gold, total_gold, beaten_wumpus, gamma=0.9,
                    theta=0.001):
    V = {state: 0 for state in states}  # Initialize value of all states to 0
    policy = {}

    while True:
        delta = 0
        for state in states:
            # print("state", state)
            v = V[state]
            r, c = state  # Extract row and column from the state
            max_value = float('-inf')
            best_action = None

            valid_actions = []
            if cave[r][c] == 'W' and (r, c) not in beaten_wumpus:
                valid_actions.append('FIGHT')
            else:
                if r > 0 and cave[r - 1][c] != 'X':  # Check if NORTH is a valid action
                    valid_actions.append('NORTH')
                if r < NUM_ROWS - 1 and cave[r + 1][c] != 'X':  # Check if SOUTH is a valid action
                    valid_actions.append('SOUTH')
                if c > 0 and cave[r][c - 1] != 'X':  # Check if WEST is a valid action
                    valid_actions.append('WEST')
                if c < NUM_COLS - 1 and cave[r][c + 1] != 'X':  # Check if EAST is a valid action
                    valid_actions.append('EAST')
                if cave[r][c] == 'T':
                    valid_actions.append('TELEPORT')
                if cave[r][c] == 'S':
                    valid_actions.append('EXIT')

            for action in valid_actions:
                total = 0
                for next_state, prob in transition_probs[(state, action)]:
                    if next_state is None:  # Handle the EXIT action
                        total += prob * rewards[(state, action)][0]
                    else:
                        total += prob * (rewards[(state, action)][0] + gamma * V[next_state])

                if total > max_value:
                    max_value = total
                    best_action = action

            V[state] = max_value
            policy[state] = best_action
            delta = max(delta, abs(v - V[state]))

        if delta < theta:
            break

    return policy, V


def print_pretty_cave(cave):
    print("Cave Layout:")
    # Print column numbers
    col_numbers = "   " + " ".join([str(i % 10) for i in range(len(cave[0]))])
    print(col_numbers)
    print("  " + "-" * (len(col_numbers) - 2))

    # Print each row with its row number
    for r, row in enumerate(cave):
        row_str = " ".join(row)
        print(f"{r % 10} | {row_str} |")
    print("  " + "-" * (len(col_numbers) - 2))


def agent_function(request_data, request_info):
    print('I got the following request:')
    print(request_data)

    global total_gold
    total_gold = 0

    cave = [list(row) for row in request_data['map'].split('\n')]
    initial_position, total_gold = find_initial_position(cave)
    print_pretty_cave(cave)

    if 'skill-points' not in request_data:
        print("in")
        skill_alloc = {'navigation': 12, 'fighting': 8}
        return skill_alloc
    print("here")
    try:
        collected_gold = []
        beaten_wumpus = []
        for entry in request_data['history']:
            if 'collected-gold-at' in entry['outcome']:
                gold_position = tuple(entry['outcome']['collected-gold-at'])
                collected_gold.append(gold_position[::-1])
            if 'killed-wumpus-at' in entry['outcome']:
                wumpus_position = tuple(entry['outcome']['killed-wumpus-at'])
                beaten_wumpus.append(wumpus_position[::-1])

    except:
        collected_gold = []
        beaten_wumpus = []
    # Initialize MDP
    states, transition_probs, rewards = initialize_mdp(cave, request_data['skill-points'], collected_gold,
                                                       beaten_wumpus)
    policy, _ = value_iteration(states, transition_probs, rewards, cave, collected_gold, total_gold, beaten_wumpus)
    print("policy", policy)
    # print(request_data)
    # return "EXIT"
    try:
        print("trying")
        if request_data['history'][-1]['action'] == "FIGHT":
            feedback_position = tuple(request_data['history'][-1]['outcome']['killed-wumpus-at'])
        else:
            feedback_position = tuple(request_data['history'][-1]['outcome']['position'])
        position = (feedback_position[1], feedback_position[0])
        # Swap to (row, col) format
    except:
        print("excepting")
        position = initial_position

    print("position", position)
    print("beaten_wumpus", beaten_wumpus)
    print("collected gold", collected_gold, "total gold", total_gold)
    # time.sleep(10)
    # print("policy.get", policy.get(position, 'EXIT'))
    # Follow the policy
    action = policy.get(position)
    if action == 'EXIT':  # Default to EXIT if no policy found
        collected_gold.clear()
        beaten_wumpus.clear()
    return action


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
