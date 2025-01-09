import numpy as np
import matplotlib.pyplot as plt

# Define the Mars map grid
map_size = (10, 10)  # Bigger Mars map
mars_map = np.random.choice(['H', 'R', 'S'], size=map_size, p=[0.1, 0.3, 0.6])  # Hazards, Rocky, Smooth

# Function to initialize the environment based on user input
def initialize_simulation():
    print("Hello, I am Mars Robot with you!")

    # Get the start and goal positions from the user
    start_x = int(input("Where should I start? Please enter x-position (0 to 9): "))
    start_y = int(input("Where should I start? Please enter y-position (0 to 9): "))
    goal_x = int(input("Where should I end? Please enter x-position (0 to 9): "))
    goal_y = int(input("Where should I end? Please enter y-position (0 to 9): "))

    # Get the risk level from the user (from 1 to 10)
    risk_level = int(input("How much should I take risks for the sake of speed (from 1 to 10)? Note: I might die for it. "))

    # Set the starting and goal positions
    mars_map[start_x][start_y] = 'Start'
    mars_map[goal_x][goal_y] = 'Goal'

    # Adjust epsilon and hazard penalties based on risk level
    epsilon = max(0.1, min(0.9, 0.1 * (11 - risk_level)))  # Higher risk leads to higher epsilon
    hazard_penalty = -100 * (1 - 0.05 * (risk_level - 1))  # Lower hazard penalty with higher risk

    return (start_x, start_y), (goal_x, goal_y), epsilon, hazard_penalty

# Define rewards
rewards = {
    'H': -100,  # Hazards
    'R': -10,   # Rocky land
    'S': -1,    # Smooth land
    'Start': 0, # Starting position
    'Goal': 100 # Goal position
}

# Handle edge case for goal representation
def get_reward(cell, hazard_penalty):
    if cell == 'Goal':
        return rewards['Goal']
    elif cell == 'H':
        return hazard_penalty  # Use dynamic hazard penalty based on risk level
    return rewards.get(cell, -1)  # Default penalty for other cells

# Initialize Q-table
q_table = np.zeros((map_size[0], map_size[1], 4))  # Four actions: up, down, left, right

# Actions (up, down, left, right)
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_position(pos):
    """Check if a position is valid on the map."""
    x, y = pos
    return 0 <= x < map_size[0] and 0 <= y < map_size[1] and mars_map[x][y] != 'H'

# Simulation parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
min_epsilon = 0.1  # Minimum exploration rate
epsilon_decay = 0.99  # Decay rate for epsilon

# Step counters
total_steps = 0
rocky_steps = 0
smooth_steps = 0
hazard_steps = 0

def choose_action(state, epsilon):
    """Choose an action based on epsilon-greedy policy."""
    if np.random.rand() < epsilon:
        return np.random.choice(range(4))  # Explore
    else:
        return np.argmax(q_table[state[0], state[1]])  # Exploit

def update_q_table(state, action, reward, next_state):
    """Update the Q-value using the Q-learning formula."""
    current_q = q_table[state[0], state[1], action]
    max_next_q = np.max(q_table[next_state[0], next_state[1]])
    q_table[state[0], state[1], action] = current_q + alpha * (reward + gamma * max_next_q - current_q)

# Start the simulation based on user input
start_position, goal_position, epsilon, hazard_penalty = initialize_simulation()

# Starting position
robot_position = start_position

# Simulation loop
while robot_position != goal_position:
    print("\nCurrent Mars Map:")
    for i in range(map_size[0]):
        row = ''
        for j in range(map_size[1]):
            if (i, j) == robot_position:
                row += 'R '  # Robot position
            else:
                row += mars_map[i][j][0] + ' '
        print(row)

    current_state = robot_position
    action = choose_action(current_state, epsilon)
    next_position = (current_state[0] + actions[action][0], current_state[1] + actions[action][1])

    if not is_valid_position(next_position):
        reward = hazard_penalty  # Penalty for invalid moves
        next_position = current_state  # Stay in place
    else:
        reward = get_reward(mars_map[next_position[0]][next_position[1]], hazard_penalty)

    # Update Q-table and move to the next position
    update_q_table(current_state, action, reward, next_position)
    robot_position = next_position

    # Count steps for each type of terrain
    if mars_map[robot_position[0]][robot_position[1]] == 'R':
        rocky_steps += 1
    elif mars_map[robot_position[0]][robot_position[1]] == 'S':
        smooth_steps += 1
    elif mars_map[robot_position[0]][robot_position[1]] == 'H':
        hazard_steps += 1

    # Increment total steps
    total_steps += 1

    # Check if the goal is reached, and stop if so
    if robot_position == goal_position:
        print(f"Robot's current position: {robot_position}")
        print(f"Goal Reached!")
        break

    print(f"Robot's current position: {robot_position}")
    print(f"Action taken: {['Up', 'Down', 'Left', 'Right'][action]}")
    print(f"Reward received: {reward}")

    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# Print the final report after reaching the goal
print("\nFinal Report:")
print(f"Total steps taken to reach the goal: {total_steps}")
print(f"Rocky steps: {rocky_steps}")
print(f"Smooth steps: {smooth_steps}")
print(f"Hazard steps: {hazard_steps}")