import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Grid size
grid_size = 5;
measurements=[2,2,1,1,2]; 
# Define the color map
cmap = sns.color_palette("coolwarm", as_cmap=True)

def prob_to_log_odds(p):
    return np.log(p / (1.0 - p))

def log_odds_to_prob(l):
    return 1.0 / (1 + np.exp(-l))

class OccupancyGrid:
    def __init__(self, grid_size, prior=0.5):
        self.grid = np.ones((grid_size, grid_size)) * prob_to_log_odds(prior)  # Initialize in log odds
        self.grid_size = grid_size
        self.prior_log_odds = prob_to_log_odds(prior)
          
    def update_grid(self, cell_number, heading, z_t):
        i, j = divmod(cell_number - 1, self.grid_size)
        
        if heading == 'Up':
            cells = [(x, j) for x in range(i-1, -1, -1)]
        elif heading == 'Down':
            cells = [(x, j) for x in range(i+1, self.grid_size)]
        elif heading == 'Left':
            cells = [(i, y) for y in range(j-1, -1, -1)]
        elif heading == 'Right':
            cells = [(i, y) for y in range(j+1, self.grid_size)]
        
        if z_t == 0 and cells:  # By default next cell occupied if there is an adjacent cell
            x, y = cells[0]
            self.grid[x, y] += prob_to_log_odds(0.8) - self.prior_log_odds
            return
        for k, (x, y) in enumerate(cells):
            if k < z_t:  # Free
                self.grid[x, y] += prob_to_log_odds(0.1) - self.prior_log_odds
            elif k == z_t:  # Occupied
                self.grid[x, y] += prob_to_log_odds(0.8) - self.prior_log_odds
            else:  # Unknown
                self.grid[x, y] += prob_to_log_odds(0.5) - self.prior_log_odds
                    
    def visualize_grid(self):
        prob_grid = log_odds_to_prob(self.grid)  # Convert to probabilities for visualization
        plt.figure(figsize=(self.grid_size, self.grid_size))
        sns.heatmap(prob_grid, annot=True, fmt=".2f", cmap=cmap, cbar=False, square=True, linewidths=0.5,
                    linecolor='black', annot_kws={"size": 20, "weight": "bold", "color": "black"})
        plt.title("Occupancy Grid", fontsize=20)
        plt.show()

# Initialize the occupancy grid
occupancy_grid = OccupancyGrid(grid_size)

occupancy_grid.update_grid(1, 'Right', measurements[0])
occupancy_grid.update_grid(2, 'Down', measurements[1])
occupancy_grid.update_grid(7, 'Down', measurements[2])
occupancy_grid.update_grid(8, 'Down', measurements[3])
occupancy_grid.update_grid(9, 'Down', measurements[4])
#occupancy_grid.update_grid(5, 'Right', math.floor(measurements[5]/grid_cell_width))
#occupancy_grid.update_grid(6, 'Down', 0)
#occupancy_grid.update_grid(6, 'Up', 0)
#occupancy_grid.update_grid(6, 'Left', 2)
#occupancy_grid.update_grid(5, 'Down', 0)
# Visualize the occupancy grid
occupancy_grid.visualize_grid()