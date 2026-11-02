"""
ASSIGNMENT 12

An autonomous delivery robot operates inside a warehouse represented by an R × C grid. The
robot must deliver a package from its starting position to a specified destination while managing
its limited battery capacity.
Each cell contains one of the following symbols:
Symbol Meaning
S Starting position
D Delivery destination
. Free cell
# Obstacle (cannot be entered)
B Battery charging station

The robot can move one cell up, down, left, or right, provided the destination cell is inside the
grid and is not an obstacle. Each move consumes one unit of battery. The battery has a
maximum capacity of K units and is initially fully charged. Whenever the robot enters a charging
station, its battery is instantly restored to full capacity at no additional movement cost. The
robot cannot make a move if its remaining battery is zero.

Your objective is to determine the minimum number of moves required to reach D. If the
destination cannot be reached, report that delivery is impossible.

A test data file with three cases is given to test your code.
The test data file has the following format.
R grid rows (one line) => using S D . # B
"""

class MinMovesinMaze:
    def __init__(self, filename):
        self.source_idx = (0, 0)
        self.grid = []
        self._read_grid(filename)

    def _read_grid(self, filename):
        """
        Read grid from the input file where the first line is battery capacity.
        """
        try:
            with open(filename, 'r') as file:
                self.K = int(file.readline().strip()[0])

                for line in file:
                    row = []
                    for char in line.strip():
                        if char == 'S':
                            self.source_idx = (len(self.grid), len(row))
                        row.append(char)
                    self.grid.append(row)

        except Exception as e:
            print(f"ERROR in parsing input file! Path: {filename}")
            print(e)
        
    def getminmoves(self):
        """
        Determine the minimum number of moves required to reach D. If the
        destination cannot be reached, report that delivery is impossible.
        """
        if len(self.grid) == 0 or len(self.grid[0]) == 0:           # empty grid
            return -1
        
        q = [(self.source_idx[0], self.source_idx[1], self.K)]      # initialize the BFS queue with start S 
        self.grid[self.source_idx[0]][self.source_idx[1]] = '#'     # block the cell to mark as visited

        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]             # 4-directional moves
        m, n = len(self.grid), len(self.grid[0])
        moves = 0

        while len(q) > 0:
            next = []   

            # process all the cells at the current BFS level
            for _ in range(len(q)):
                curr = q.pop(0)
                x, y, battery = curr

                if battery == 0:    # battery over
                    continue
                
                for dx, dy in directions:
                    next_x = x + dx
                    next_y = y + dy

                    # check if the next cell is reachable
                    if next_x >= 0 and next_x < m and next_y >= 0 and next_y < n and self.grid[next_x][next_y] != '#':
                        if self.grid[next_x][next_y] == 'D':
                            return moves + 1                    # reached the destination
                        if self.grid[next_x][next_y] == 'B':    
                            battery = self.K + 1                # battery charged (+1 to negate decrement)

                        self.grid[next_x][next_y] = '#'         # block the cell to mark as visited
                        next.append((next_x, next_y, battery - 1))

            # enqueue all the next level neighbor cells
            q.extend(next)
            moves += 1

        return -1   # destination is unreachable or not enough battery
    

if __name__ == "__main__":
    # Example: asgn-12-case-1.txt
    filename = input("Enter input file path: ")        
    mmm = MinMovesinMaze(filename)
    minmoves = mmm.getminmoves()

    if minmoves < 0:
        print("Delivery is impossible!")
    else:
        print("Min. moves to reach D:", minmoves)
    