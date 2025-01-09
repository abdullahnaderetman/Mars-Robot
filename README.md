## Features
- **Interactive Input:** Users define the robot's start and end positions and set the risk tolerance level.
- **Dynamic Environment:** The Mars map is randomly generated with three terrain types:
  - `H`: Hazards (-100 reward).
  - `R`: Rocky land (-10 reward).
  - `S`: Smooth land (-1 reward).
- **Reinforcement Learning:** The robot uses a Q-learning algorithm to explore and exploit its environment.

## Installation
1. Ensure you have Python 3.7 or later installed.
2. Install the required packages:
   ```bash
   pip install numpy matplotlib
   ```

## Running the Simulation
1. Run the Python script:
   ```bash
   python mars_project.py
   ```
2. Follow the prompts to:
   - Enter the starting (`x, y`) and goal (`x, y`) positions (range: 0 to 9).
   - Set the risk level (1-10), where 10 is high risk (favors speed) and 1 is low risk (favors safety).
3. The simulation will display the map, the robot's movements, and the chosen actions step by step.

## Simulation Parameters
- **Learning Rate (α):** 0.1 (Controls how much new information overrides old).
- **Discount Factor (γ):** 0.9 (Prioritizes future rewards).
- **Exploration Rate (ε):** Starts high but decays with each step to favor exploitation over exploration.
- **Hazard Penalty:** Dynamically adjusts based on the user's risk level.

## Code Structure
- **Map Generation:** Randomly assigns terrain types using predefined probabilities.
- **Q-Learning Algorithm:**
  - **Q-Table:** A matrix of dimensions `[map_size[0], map_size[1], 4]` to represent state-action pairs.
  - **Actions:** Up, Down, Left, Right.
- **Rewards Calculation:** Based on terrain and goal proximity.
- **Simulation Loop:** Robot iteratively chooses actions, updates the Q-table, and adjusts ε.

## Results
At the end of the simulation:
- The robot's path is displayed.
- A summary of steps taken and terrain traversed is printed:
  - Total steps.
  - Number of rocky, smooth, and hazardous steps.

## Customization
- Adjust the map size by modifying `map_size`.
- Change terrain probabilities in `np.random.choice()`.
- Tune learning parameters (`alpha`, `gamma`, `min_epsilon`, `epsilon_decay`) to modify robot behavior.

## Visualization
The simulation includes visual feedback:
- **Map Legend:**
  - `R`: Robot's current position.
  - `S, R, H`: Terrain types.
  - `Start`: Starting point.
  - `Goal`: Target point.

## Dependencies
- `numpy`: For numerical computations.
- `matplotlib`: (Optional) For future visualization of robot paths.

## Future Enhancements
- Implement a GUI for better interaction.
- Add obstacles that the robot cannot pass.
- Include more sophisticated pathfinding algorithms.
