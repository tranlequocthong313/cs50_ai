class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self, filename, show_image, verbose, bfs):
        self.filename = filename
        self.show_image = show_image
        self.verbose = verbose
        self.bfs = bfs

        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        self.map = contents.splitlines()
        self.height = len(self.map)
        self.width = max(len(line) for line in self.map)

        for i in range(self.height):
            for j in range(self.width):
                try:
                    if self.map[i][j] == "A":
                        self.start = (i, j)
                    elif self.map[i][j] == "B":
                        self.goal = (i, j)
                except IndexError:
                    pass

        self.solution = None

    def print(self):
        print()
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if (
                    (i, j) != self.start
                    and (i, j) != self.goal
                    and self.solution is not None
                    and (i, j) in self.solution
                ):
                    print("*", end="")
                else:
                    print(self.map[i][j], end="")
            print()
        print("Moved steps", self.moved_steps)

    def display_image(self):
        from PIL import Image, ImageDraw

        if not self.show_image:
            return
        self.square_size = 200
        img = Image.new(
            "RGB", (self.width * self.square_size, self.height * self.square_size)
        )
        canvas = ImageDraw.Draw(img)
        colors = {
            "A": (255, 0, 0),
            "B": (0, 255, 0),
            "#": (27, 27, 27),
            " ": (255, 255, 255),
        }
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                fill = colors[self.map[i][j]]
                if (
                    self.verbose
                    and (i, j) != self.start
                    and (i, j) != self.goal
                    and self.visited is not None
                    and (i, j) in self.visited
                ):
                    fill = (196, 76, 74)
                if (
                    (i, j) != self.start
                    and (i, j) != self.goal
                    and self.solution is not None
                    and (i, j) in self.solution
                ):
                    fill = (255, 255, 0)
                canvas.rectangle(
                    [
                        (j * self.square_size, i * self.square_size),
                        (
                            j * self.square_size + self.square_size,
                            i * self.square_size + self.square_size,
                        ),
                    ],
                    fill=fill,
                    outline=(0, 0, 0),
                    width=3,
                )
        img.show()
        img.save("maze.png", "PNG")

    def solve(self):
        self.moved_steps = 0
        self.frontier = QueueFrontier() if self.bfs else StackFrontier()
        self.visited = set(self.start)
        node = Node(state=self.start, parent=None, action=None)
        self.frontier.add(node)
        while not self.frontier.empty():
            node = self.frontier.remove()
            self.visited.add(node.state)
            self.moved_steps += 1

            if self.goal == node.state:
                self.solution = []
                while node:
                    self.solution.append(node.state)
                    node = node.parent
                break

            (i, j) = node.state
            down = Node(state=(i + 1, j), parent=node, action=None)
            up = Node(state=(i - 1, j), parent=node, action=None)
            right = Node(state=(i, j + 1), parent=node, action=None)
            left = Node(state=(i, j - 1), parent=node, action=None)
            if self.__valid_state(node=down):
                self.frontier.add(down)
            if self.__valid_state(node=up):
                self.frontier.add(up)
            if self.__valid_state(node=left):
                self.frontier.add(left)
            if self.__valid_state(node=right):
                self.frontier.add(right)

        self.display_image()

    def __solve_helper(self, node):
        if node == None:
            return
        if self.goal == node.state:
            self.solution = []
            while node:
                self.solution.append(node.state)
                node = node.parent
            return
        if not self.__valid_state(node=node):
            return

        self.moved_steps += 1
        self.visited.add(node.state)

        (i, j) = node.state
        self.__solve_helper(node=(Node(state=(i + 1, j), parent=node, action=None)))
        self.__solve_helper(node=(Node(state=(i - 1, j), parent=node, action=None)))
        self.__solve_helper(node=(Node(state=(i, j + 1), parent=node, action=None)))
        self.__solve_helper(node=(Node(state=(i, j - 1), parent=node, action=None)))

    def __valid_state(self, node):
        (i, j) = node.state
        return (
            i >= 0
            and i < self.height
            and j >= 0
            and j < self.width
            and (i, j) not in self.visited
            and self.map[i][j] != "#"
        )


if __name__ == "__main__":
    import sys

    if "--help" in sys.argv:
        print("Usage:", "python maze.py [FILEPATH] [OPTIONS]")
        print("Options:")
        print("--show-image:", "show image of the maze")
        print(
            "--bfs:",
            "use breadth first search, default algorithm is depth first search",
        )
        print("--verbose:", "show all explored path when --show-image option is true")
    else:
        print('Type "--help" for more information.')
        if len(sys.argv) <= 1 or not sys.argv[1].endswith(".txt"):
            raise Exception("must provide a text file")
        filename = sys.argv[1]
        show_image = "--show-image" in sys.argv
        verbose = "--verbose" in sys.argv
        bfs = "--bfs" in sys.argv

        maze = Maze(filename, show_image, verbose, bfs)
        maze.solve()
        maze.print()
