import os
import random
import math

class BuildBoard():
    
    def __init__(self, m, n):
        self.maze= []
        self.generate_board(m,n) 
    
    def generate_board(self, m, n):
        legal_char = "X_"
        
        for i in range(m):
            row = []

            for j in range(n):
                if i == 0 or j == 0 or (i == m - 1) or (j == n - 1) :
                    row.append("X")
                else:
                    row.append(random.choice(legal_char))
            
            self.maze.append(row)
        
        start_x = random.randint(1, m-2)
        start_y = random.randint(1, n-2)
        goal_x = random.randint(1, m-2)
        goal_y = random.randint(1, n-2)

        self.maze[start_x][start_y] = "S"
        self.maze[goal_x][goal_y] = "G"
        self.clear_path(start_x, start_y, goal_x, goal_y)
    
    def clear_path(self, start_x, start_y, goal_x, goal_y):
        x_distance = abs(start_x - goal_x)
        y_distance = abs(start_y - goal_y)
        
        x_direction = 1 if (start_x - goal_x < 0) else -1
        y_direction = 1 if (start_y - goal_y < 0) else -1

        curr_x = start_x
        curr_y = start_y

        while (curr_x != goal_x or curr_y != goal_y):
            if (curr_x != goal_x):
                curr_x += x_direction
            if (curr_y != goal_y):
                curr_y += y_direction
            if (curr_x != goal_x or curr_y != goal_y):
                self.maze[curr_x][curr_y] = "_"

