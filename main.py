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
        # Arrays to represent walls and visited cells
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
        gluOrtho2D(-2, (C * CELL_SIZE) + 2, (R * CELL_SIZE) + 2, -2)
        glMatrixMode(GL_MODELVIEW)

    def draw_maze(self):
        glColor3f(0, 0, 0) # Black walls
        glLineWidth(2)
        glBegin(GL_LINES)
        for r in range(R):
            for c in range(C):
                x, y = c * CELL_SIZE, r * CELL_SIZE
                # North Wall
                if self.northWall[r][c]:
                    glVertex2f(x, y); glVertex2f(x + CELL_SIZE, y)
                # East Wall
                if self.eastWall[r][c]:
                    glVertex2f(x + CELL_SIZE, y); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                
                # Bottom Edge (Phantom row)
                if r == R - 1 and self.northWall[R][c]:
                    glVertex2f(x, y + CELL_SIZE); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                # Left Edge
                if c == 0 and self.eastWall[r][C]: # Using index C for left boundary
                    glVertex2f(x, y); glVertex2f(x, y + CELL_SIZE)
        glEnd()

    def draw_dots(self):
        # Blue dead ends
        glColor3f(0, 0, 1)
        glPointSize(8)
        glBegin(GL_POINTS)
        for (r, c) in self.dead_ends:
            glVertex2f(c * CELL_SIZE + CELL_SIZE/2, r * CELL_SIZE + CELL_SIZE/2)
        glEnd()

        # Red for the path being explored
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for (r, c) in self.path:
            glVertex2f(c * CELL_SIZE + CELL_SIZE/2, r * CELL_SIZE + CELL_SIZE/2)
        glEnd()

    def generate(self):
        """Mouse 'eats' walls using stack-based DFS[cite: 68, 72]."""
        stack = []
        curr_r, curr_c = random.randint(0, R-1), random.randint(0, C-1)
        self.visited[curr_r][curr_c] = True
        visited_count = 1

        while visited_count < (R * C):
            neighbors = []
            # Check 4 neighbors
            dirs = [(-1,0,'N',(curr_r,curr_c)), (1,0,'N',(curr_r+1,curr_c)), 
                    (0,1,'E',(curr_r,curr_c)), (0,-1,'E',(curr_r,curr_c-1))]
            
            for dr, dc, w_type, (wr, wc) in dirs:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < R and 0 <= nc < C and not self.visited[nr][nc]:
                    neighbors.append((nr, nc, w_type, (wr, wc)))

            if neighbors:
                # 1. Choose randomly among unvisited neighbors
                next_r, next_c, w_type, (wr, wc) = random.choice(neighbors)
                
                # 2. Eat wall between current and chosen neighbor
                if w_type == 'N': self.northWall[wr][wc] = 0
                else: self.eastWall[wr][wc] = 0
                
                # Bonus: Randomly create loops to make maze less perfect
                if random.random() < 0.05:
                    self.northWall[random.randint(1, R-1)][random.randint(0, C-1)] = 0

                stack.append((curr_r, curr_c))
                curr_r, curr_c = next_r, next_c
                self.visited[curr_r][curr_c] = True
                visited_count += 1
                self.render_frame()
            elif stack:
                curr_r, curr_c = stack.pop() # 3. Pop if trapped 
        self.northWall[0][0] = 0
        self.northWall[R][C-1] = 0
        self.render_frame()

    def solve(self):
        """Backtracking solver[cite: 81]."""
        start, end = (0, 0), (R-1, C-1) # Arbitrary start/end
        self.solve_stack = [start]
        self.solve_visited.add(start)

        while self.solve_stack:
            r, c = self.solve_stack[-1]
            self.path = list(self.solve_stack)
            self.render_frame()
            
            if (r, c) == end: break

            # Check moves; No wall and unvisited 
            moves = []
            # North
            if r > 0 and self.northWall[r][c] == 0 and (r-1, c) not in self.solve_visited:
                moves.append((r-1, c))
            # South
            if r < R-1 and self.northWall[r+1][c] == 0 and (r+1, c) not in self.solve_visited:
                moves.append((r+1, c))
            # East
            if c < C-1 and self.eastWall[r][c] == 0 and (r, c+1) not in self.solve_visited:
                moves.append((r, c+1))
            # West
            if c > 0 and self.eastWall[r][c-1] == 0 and (r, c-1) not in self.solve_visited:
                moves.append((r, c-1))

            if moves:
                next_cell = random.choice(moves) 
                self.solve_visited.add(next_cell)
                self.solve_stack.append(next_cell)
            else:
                # Dead end
                self.dead_ends.add(self.solve_stack.pop())
            
            time.sleep(0.05)

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