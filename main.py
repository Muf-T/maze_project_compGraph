import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time

# --- Configuration ---
R, C = 15, 15
CELL_SIZE = 2.0  # Scale for OpenGL coordinate system
OFFSET = (C * CELL_SIZE) / 2

class MazeApp:
    def __init__(self):
        # Arrays per assignment [cite: 13, 15, 17]
        self.northWall = [[1 for _ in range(C)] for _ in range(R + 1)] 
        self.eastWall = [[1 for _ in range(C + 1)] for _ in range(R)]
        self.visited = [[False for _ in range(C)] for _ in range(R)]
        
        # Solving state
        self.solve_stack = []
        self.solve_visited = set()
        self.dead_ends = set()
        self.path = []

    def init_gl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Set up a 2D orthographic view
        gluOrtho2D(-2, (C * CELL_SIZE) + 2, (R * CELL_SIZE) + 2, -2)
        glMatrixMode(GL_MODELVIEW)

    def draw_maze(self):
        glColor3f(0, 0, 0) # Black walls [cite: 67]
        glLineWidth(2)
        glBegin(GL_LINES)
        for r in range(R):
            for c in range(C):
                x, y = c * CELL_SIZE, r * CELL_SIZE
                # North Wall [cite: 15]
                if self.northWall[r][c]:
                    glVertex2f(x, y); glVertex2f(x + CELL_SIZE, y)
                # East Wall [cite: 12]
                if self.eastWall[r][c]:
                    glVertex2f(x + CELL_SIZE, y); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                
                # Bottom Edge (Phantom row) [cite: 16]
                if r == R - 1 and self.northWall[R][c]:
                    glVertex2f(x, y + CELL_SIZE); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                # Left Edge [cite: 17]
                if c == 0 and self.eastWall[r][C]: # Using index C for left boundary
                    glVertex2f(x, y); glVertex2f(x, y + CELL_SIZE)
        glEnd()

    def draw_dots(self):
        # Draw dead ends (Blue) [cite: 84, 102]
        glColor3f(0, 0, 1)
        glPointSize(8)
        glBegin(GL_POINTS)
        for (r, c) in self.dead_ends:
            glVertex2f(c * CELL_SIZE + CELL_SIZE/2, r * CELL_SIZE + CELL_SIZE/2)
        glEnd()

        # Draw current path (Red) [cite: 83, 102]
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for (r, c) in self.path:
            glVertex2f(c * CELL_SIZE + CELL_SIZE/2, r * CELL_SIZE + CELL_SIZE/2)
        glEnd()

    
    def render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.draw_maze()
        self.draw_dots()
        pygame.display.flip()
        pygame.time.wait(10)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Maze Generator & Solver")
    
    app = MazeApp()
    app.init_gl()
    
    # Process
    app.generate()
    time.sleep(1)
    app.solve()

    # Keep window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        app.render_frame()
    pygame.quit()

if __name__ == "__main__":
    main()