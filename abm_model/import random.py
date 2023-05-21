import random
import numpy as np

import mesa
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class TeamAgent(mesa.Agent):
    """An agent in a team with a range of teamwork skill parameters"""

    def __init__(self, unique_id, model, problem_solving, communication, cps_level):
        super().__init__(unique_id, model)
        self.problem_solving = problem_solving # 1 to 2 # how good they are at solving problems
        self.cps_level = cps_level # 1 to 4 # how good they are at solving problems
        self.communication =  communication # 0.5 to 1.5 # how good they are at communicating
        self.working = False # By default the will not work on a task
        self.pos

    
    # A move function which will be used for the step function later on
    def move(self):
        if not self.working: # if they are not working on a task
            possible_moves = self.model.grid.get_neighborhood(  # retrieve neighborhood grids
                self.pos, moore=True, include_center=False 
            )
            new_position = random.choice(possible_moves) #
            self.model.grid.move_agent(self, new_position)

    def grid_problem_solving(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos]) # Retrieves a a list of all agents in the same cell
        self.team_problem_solving = 0
        if len(cellmates) > 1:
            for mate in cellmates:
                self.team_problem_solving += mate.problem_solving
        return self.team_problem_solving

    def evaluate(self):
        x, y = self.pos
        self.team_problem_solving = self.grid_problem_solving()
        if self.model.grid.accomplished[x][y] == True:
            self.working = False
        if self.problem_solving > self.model.grid.task_complexity[x][y]['task_complexity']:
            self.work_individually()
        elif self.team_problem_solving > self.model.grid.task_complexity[x][y]['task_complexity']:
            self.work_as_a_team()
        else:
            self.suggest_collaboration()
        
    def work_individually(self):
        self.working = True
        self.work()

    def work_as_a_team(self):
        self.working = True
        self.work()

    def suggest_collaboration(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )
        for neighbor in neighbors:
            if not neighbor.working and ( neighbor.problem_solving + self.problem_solving ) > self.model.grid.task_complexity[x][y]['task_complexity']:
                neighbor.model.grid.move_agent(neighbor, self.pos)

    def work(self):
        if self.working:
            x, y = self.pos
            self.model.grid.accomplished[x][y] = True
            
        
    
  #      for neighbor in self.model.grid.neighbor_iter(self.pos):
  #          if neighbor.problem_solving + self.problem_solving > task_complexity:
  #              similar += 1

    def step(self):
        self.evaluate()
        self.move()
        
# Custom grid build

class CustomGrid(MultiGrid):
    def __init__(self, width, height):
        super().__init__(width, height, torus=True)
        self.task_complexity = self.build_grid()
        self.accomplished = self.build_grid()

    def build_grid(self):
        grid = np.empty((self.width, self.height), dtype=object)
        for cell in self.empties:
            x, y = cell
            grid[x][y] = {
                'task_complexity': np.random.uniform(0, 2),
                'accomplished': False
            }
        return grid
    
    

# Create the model
class TeamworkModel(mesa.Model):
    """ A model with some number of agents."""
    
    def __init__(self, num_agents, width, height):
        self.num_agents = num_agents
        self.grid = CustomGrid(width, height)
        self.schedule = RandomActivation(self)

        def get_cps_level(problem_solving_value):
            if problem_solving_value >= 1.92 and problem_solving_value <= 2:
                return 4
            elif problem_solving_value >= 1.64 and problem_solving_value < 1.92:
                return 3
            elif problem_solving_value >= 1.29 and problem_solving_value < 1.64:
                return 2
            elif problem_solving_value >= 1 and problem_solving_value < 1.29:
                return 1
            else:
                return None

        # Create agents
        for i in range(self.num_agents):
            problem_solving = random.random() 
            communication = random.random() + 0.5
            cps_level = get_cps_level(problem_solving)
            agent = TeamAgent(i, self, problem_solving, communication, cps_level)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # create data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Task Completed": lambda model: np.sum(model.grid.accomplished),
                "Task Completed Individually": lambda model: np.sum(model.grid.accomplished) - np.sum(model.grid.collaborative),
                "Task Completed During Teamwork": lambda model: np.sum(model.grid.collaborative),
                "Agent Locations": lambda model: [agent.pos for agent in model.schedule.agents]
            }
        )

    def access_grid_values(self):
            for cell in self.grid.coord_iter():
                x, y = cell
                value = self.grid.task_complexity[x][y]
                accomplished = self.grid.accomplished[x][y]
                print(f"Cell ({x}, {y}) - Task Complexity: {value}, Accomplished: {accomplished}")


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


# Create the model and run the simulation
model = TeamworkModel(num_agents=10, width=10, height=10)
for i in range(10):
    model.step()

# Access the agent positions
for agent in model.schedule.agents:
    print(agent.pos)

