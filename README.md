# Repository for AI Project 2.3

**Assignment:** [Monster Quest](https://kwarc.info/teaching/AISysProj/SS24/assignment-2.3.pdf)

# Monster World Agent

This repository contains an implementation of a Monster World agent that navigates a cave, collects gold, fights
Monsters, and exits safely. The agent uses a Markov Decision Process (MDP) and value iteration to decide on the best
actions to take based on its surroundings and objectives.

## Dependencies

This project is written in Python and requires the following dependencies:

- **Python**: Version 3.7 or higher
- **NumPy**: Used for numerical operations and data handling.

To install the required Python packages, run:

```bash
pip install numpy
```

## Function Details

### - agent_function()

The main component of this project is the `agent_function`, which is responsible for determining the actions of the
agent based on the state of the cave. It processes incoming requests containing the state of the game environment and
the agent's history of actions and outcomes. Based on this information, it determines
the next action to take using a policy derived from value iteration on a Markov Decision Process (MDP).

#### **Key Steps in `agent_function`:**

1. **Parse Request Data**: Reads the current state of the cave and the agent's history.
2. **Initial Skill Allocation**: If the agent has not yet been initialized, it allocates skill points to `navigation`
   and `fighting`.
3. **MDP Initialization**: Sets up states, transition probabilities, and rewards based on the current cave layout and
   agent's history.
4. **Value Iteration**: Computes the optimal policy for the agent using the value iteration algorithm.
5. **Determine Next Action**: Uses the computed policy to select the best action given the current state.
6. **Return Action**: Sends the selected action back to the server.

### - find_initial_position()

This function iterates over each cell in the cave to identify the starting position 'S' and count the number of
gold pieces 'G'.

- **Parameters**:
    - `cave`: A 2D list representing the cave layout.
- **Returns**:
    - `start`: The starting position `(row, col)` of the agent.
    - `total_gold`: Total number of gold pieces in the cave.

### - move_agent()

This function determines the outcome of a move in the specified direction, fighting, teleporting, or exiting based
on the cave layout and current agent state.

- **Parameters**:
    - `state`: Current position `(row, col)` of the agent.
    - `action`: Action to be taken (`'NORTH'`, `'SOUTH'`, `'EAST'`, `'WEST'`, `'FIGHT'`, `'TELEPORT'`, `'EXIT'`).
    - `cave`: 2D list representing the cave layout.
    - `skill_alloc`: Dictionary containing skill points allocated for `navigation` and `fighting`.
    - `collected_gold`: List of positions where gold has been collected.
    - `beaten_monster`: List of positions where Monsteres have been defeated.
    - `total_gold`: Total number of gold pieces in the cave.
- **Returns**:
    - `next_state`: The agent's next state after the action.
    - `prob`: The probability of successfully transitioning to `next_state`.
    - `reward`: The reward for taking the action from the current state.

### - fight_monster()

This function computes the success probability and reward of fighting a Monster based on the agent's fighting
skills.

- **Parameters**:
    - `state`: Current position `(row, col)` of the agent.
    - `skill_alloc`: Dictionary containing skill points allocated for `navigation` and `fighting`.
- **Returns**:
    - `state`: The state remains the same if the fight occurs at the agent's current location.
    - `prob`: Probability of winning the fight.
    - `reward`: The reward for fighting a Monster.

### - find_teleport_targets()

This function scans the cave layout for cells marked as 'T' (teleporters) excluding the agent's current position.

- **Parameters**:
    - `state`: Current position `(row, col)` of the agent.
    - `cave`: 2D list representing the cave layout.
- **Returns**:
    - `teleport_targets`: List of positions `(row, col)` that are valid teleportation destinations.

### - initialize_mdp()

This function sets up the MDP by iterating over each cell in the cave and computing possible actions, resulting
states, probabilities, and rewards for each state.

- **Parameters**:
    - `cave`: 2D list representing the cave layout.
    - `skill_alloc`: Dictionary containing skill points allocated for `navigation` and `fighting`.
    - `collected_gold`: List of positions where gold has been collected.
    - `beaten_monster`: List of positions where Monsteres have been defeated.
    - `total_gold`: Total number of gold pieces in the cave.
- **Returns**:
    - `states`: List of all possible states `(row, col)` in the cave.
    - `transition_probs`: Dictionary mapping `(state, action)` pairs to their possible next states and probabilities.
    - `rewards`: Dictionary mapping `(state, action)` pairs to their respective rewards.

### - value_iteration()

This function iteratively updates the value of each state until the values converge within a specified threshold.
The policy is derived from the state-action values.

- **Parameters**:
    - `states`: List of all possible states `(row, col)` in the cave.
    - `transition_probs`: Dictionary mapping `(state, action)` pairs to their possible next states and probabilities.
    - `rewards`: Dictionary mapping `(state, action)` pairs to their respective rewards.
    - `cave`: 2D list representing the cave layout.
    - `collected_gold`: List of positions where gold has been collected.
    - `total_gold`: Total number of gold pieces in the cave.
    - `beaten_monster`: List of positions where Monsteres have been defeated.
    - `gamma`: Discount factor (default is 0.9).
    - `theta`: Convergence threshold (default is 0.001).
- **Returns**:
    - `policy`: Optimal policy mapping each state to the best action.
    - `V`: Value function mapping each state to its value.

### - print_pretty_cave()

This function formats and prints the cave to the console with row and column numbers for easier interpretation.

- **Parameters**:
    - `cave`: 2D list representing the cave layout.
- **Returns**: None


