import numpy as np
import pygame
import json



CORRIDOR_CODE = 0
WALL_CODE = -1
POSITION_CODE = -5
END_CODE = -10
VISITED_CODE = 1


class Maze():
    def __init__(self, layout_filepath):
        self.load_maze(layout_filepath)
        self.agent_position = self.start_pos


    def get_layout(self):
        return self.layout


    def get_start_position(self):
        return self.start_pos


    def get_end_position(self):
        return self.end_pos


    def get_agent_position(self):
        return self.agent_position


    def set_agent_position(self, new_position):
        row, col = self.agent_position
        self.layout[row][col] = VISITED_CODE

        self.agent_position = new_position
        new_row, new_col = new_position
        self.layout[new_row][new_col] = POSITION_CODE

        return (self.agent_position==self.end_pos).all()


    def load_maze(self, filepath):
        '''
        Loads a maze from a text file containing
        ASCII characters - . for floor, # for wall
        S for start position and F for end position
        '''
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
        for row_idx in range(rows):
            for column_idx in range(columns):
                char = maze[row_idx][column_idx]
                if char == '.':
                    maze_board[row_idx][column_idx] = CORRIDOR_CODE
                elif char =='#':
                    maze_board[row_idx][column_idx] = WALL_CODE
                elif char == 'S':
                    maze_board[row_idx][column_idx] = POSITION_CODE
                    self.start_pos = np.array([row_idx, column_idx])
                elif char == 'F':
                    maze_board[row_idx][column_idx] = END_CODE
                    self.end_pos = np.array([row_idx, column_idx])
        self.layout = maze_board


    def get_actions(self):
        '''
        Agent can move up, down, left and right.
        It cannot pass through walls or leave the grid
        '''
        max_row, max_col = self.layout.shape
        row, col = self.agent_position
        available_positions = []
        for offset in [-1, 1]:
            if row + offset >= 0 and row + offset < max_row and self.layout[row + offset][col] != WALL_CODE:
                available_positions.append([row + offset, col])
            if col + offset >= 0 and col + offset <max_col and self.layout[row, col + offset] != WALL_CODE:
                available_positions.append([row, col + offset])

        return np.array(available_positions)


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




if __name__ == "__main__":
    pass
