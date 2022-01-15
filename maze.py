import numpy as np
import pygame
import json
from copy import copy, deepcopy

# layout coding
CORRIDOR_CODE = 0
WALL_CODE = -1
POSITION_CODE = -5
END_CODE = -10
VISITED_CODE = 1

# actions coding
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


class Maze():
    def __init__(self, layout_filepath):
        self.load_maze(layout_filepath)
        self.agent_position = self.start_pos


    def load_maze(self, filepath):
        maze = []
        rows = 0
        with open(filepath, 'r') as fh:
            for line in fh:
                row = [character for character in line if character != '\n']
                if row:
                    rows +=1
                maze.append(row)
        columns = len(maze[0])
        maze_board = np.zeros((rows, columns))
        self.states = {}
        states_count = 0
        for row_idx in range(rows):
            for column_idx in range(columns):
                char = maze[row_idx][column_idx]
                if char == '.':
                    maze_board[row_idx][column_idx] = CORRIDOR_CODE
                    self.states[(row_idx, column_idx)] = states_count
                    states_count += 1
                elif char =='#':
                    maze_board[row_idx][column_idx] = WALL_CODE
                elif char == 'S':
                    maze_board[row_idx][column_idx] = POSITION_CODE
                    self.start_pos = np.array([row_idx, column_idx])
                    self.states[(row_idx, column_idx)] = states_count
                    states_count += 1
                elif char == 'F':
                    maze_board[row_idx][column_idx] = END_CODE
                    self.end_pos = np.array([row_idx, column_idx])
                    self.states[(row_idx, column_idx)] = states_count
                    states_count += 1
        self.original_layout = maze_board
        self.layout = deepcopy(self.original_layout)


    def init_Q_table(self):
        q_rows = len(self.states.keys())
        q_cols = 4
        Q_table = np.zeros((q_rows, q_cols))

        for state, code in self.states.items():
            actions = self.get_actions_code(state)
            for action in range(4):
                if action not in actions:
                    Q_table[code][action] = -float('inf')

        return Q_table


    def get_states(self):
        return self.states


    def step(self, action):

        row, col = self.agent_position
        if action == UP:
            row -= 1
        elif action == LEFT:
            col -= 1
        elif action == DOWN:
            row += 1
        elif action == RIGHT:
            col += 1
        # print(self.agent_position, row, col)
        new_position = np.array([row, col])
        self.set_agent_position(new_position)

        done = (new_position==self.end_pos).all()
        if done:
            reward = 1000
        else:
            reward = -1

        return self.states[tuple(self.agent_position.tolist())], reward, done


    def reset(self):
        self.layout = deepcopy(self.original_layout)
        self.set_agent_position(self.start_pos)
        self.layout[self.end_pos[0]][self.end_pos[1]] = END_CODE
        return self.states[tuple(self.start_pos.tolist())]


    def get_actions(self):
        max_row, max_col = self.layout.shape
        row, col = self.agent_position
        available_positions = []
        for offset in [-1, 1]:
            if row + offset >= 0 and row + offset < max_row and self.layout[row + offset][col] != WALL_CODE:
                available_positions.append([row + offset, col])
            if col + offset >= 0 and col + offset <max_col and self.layout[row, col + offset] != WALL_CODE:
                available_positions.append([row, col + offset])

        return np.array(available_positions)

    def get_actions_code(self, state):
        max_row, max_col = self.layout.shape
        actions = []
        row, col = state
        if row - 1 >= 0 and self.layout[row-1][col] != WALL_CODE:
            actions.append(UP)
        if col - 1 >= 0 and self.layout[row][col-1] != WALL_CODE:
            actions.append(LEFT)
        if row + 1 < max_row and self.layout[row+1][col] != WALL_CODE:
            actions.append(DOWN)
        if col + 1 < max_col and self.layout[row][col+1] != WALL_CODE:
            actions.append(RIGHT)
        return actions


    def set_agent_position(self, new_position):
        row, col = self.agent_position
        self.layout[row][col] = VISITED_CODE

        self.agent_position = new_position
        new_row, new_col = new_position
        self.layout[new_row][new_col] = POSITION_CODE


    def load_color_theme(self, filepath, theme_name):
        with open(filepath) as fh:
            themes = json.load(fh)
        self.theme = themes[theme_name][0]


    def prepare_window(self, square_size, caption='Maze'):
        pygame.init()
        self.square = square_size
        self.default_caption = caption
        rows, columns = self.layout.shape
        height = rows * self.square
        width = columns * self.square
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.default_caption)
        self.window.fill(self.theme['corridor_color'])


    def render(self, caption=None):
        self.window.fill(self.theme['corridor_color'])
        for row in range(self.layout.shape[0]):
            for col in range(self.layout.shape[1]):
                square = self.layout[row][col]
                if square:
                    points = [
                        (col * self.square, row * self.square),
                        (col * self.square + self.square, row * self.square),
                        (col * self.square + self.square, row * self.square + self.square),
                        (col * self.square, row * self.square + self.square),
                    ]
                    if square == WALL_CODE:
                        square_color = self.theme['wall_color']
                    elif square == POSITION_CODE:
                        square_color = self.theme['position_color']
                    elif square == END_CODE:
                        square_color = self.theme['end_color']
                    elif square == VISITED_CODE:
                        square_color = self.theme['visited_color']
                    pygame.draw.polygon(self.window, square_color, points)
        if caption:
            pygame.display.set_caption(caption)

        pygame.display.update()
