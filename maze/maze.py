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

    def remove_smallest_node(self, calculate):
        if self.empty():
            raise Exception("empty frontier")
        else:
            smallest_node_index = 0
            for i, node in enumerate(self.frontier):
                if calculate(node.state) < calculate(
                    self.frontier[smallest_node_index].state
                ):
                    smallest_node_index = i
            node = self.frontier[smallest_node_index]
            self.frontier = (
                self.frontier[:smallest_node_index]
                + self.frontier[smallest_node_index + 1 :]
            )
            return node

    def sort(self, compare):
        for i in range(len(self.frontier)):
            for j in range(i + 1, len(self.frontier)):
                if compare(self.frontier[i].state, self.frontier[j].state) > 0:
                    self.frontier[i], self.frontier[j] = (
                        self.frontier[j],
                        self.frontier[i],
                    )


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self, filename, show_image, verbose, bfs, gbfs, a_star, show_mahattan):
        self.filename = filename
        self.show_image = show_image
        self.verbose = verbose
        self.bfs = bfs
        self.gbfs = gbfs
        self.a_star = a_star
        self.show_mahattan = show_mahattan

        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        self.map = contents.splitlines()
        self.height = len(self.map)
        self.width = max(len(line) for line in self.map)

        for r in range(self.height):
            for c in range(self.width):
                try:
                    if self.map[r][c] == "A":
                        self.start = (r, c)
                    elif self.map[r][c] == "B":
                        self.goal = (r, c)
                except IndexError:
                    pass

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for r, row in enumerate(self.map):
            for c, col in enumerate(row):
                if (
                    (r, c) != self.start
                    and (r, c) != self.goal
                    and solution is not None
                    and (r, c) in solution
                ):
                    print("*", end="")
                else:
                    print(self.map[r][c], end="")
            print()
        print("States explored", self.num_explored)

    def display_image(self):
        from PIL import Image, ImageDraw, ImageFont
        import math

        if not self.show_image:
            return
        solution = self.solution[1] if self.solution is not None else None
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
        for r, row in enumerate(self.map):
            for c, _ in enumerate(row):
                fill = colors[self.map[r][c]]
                if (
                    self.verbose
                    and (r, c) != self.start
                    and (r, c) != self.goal
                    and self.explored is not None
                    and (r, c) in self.explored
                ):
                    fill = (196, 76, 74)
                if (
                    (r, c) != self.start
                    and (r, c) != self.goal
                    and solution is not None
                    and (r, c) in solution
                ):
                    fill = (255, 255, 0)
                canvas.rectangle(
                    [
                        (c * self.square_size, r * self.square_size),
                        (
                            c * self.square_size + self.square_size,
                            r * self.square_size + self.square_size,
                        ),
                    ],
                    fill=fill,
                    outline=(0, 0, 0),
                    width=3,
                )
                if self.show_mahattan and self.map[r][c] != "#":
                    font_size = self.square_size // 2
                    mahattan = str(abs(self.goal[1] - c) + abs(self.goal[0] - r))
                    if self.a_star:
                        font_size /= 2
                        if (r, c) in self.costs:
                            mahattan = str(self.costs[(r, c)]) + "+" + mahattan
                    if self.map[r][c] != " ":
                        mahattan = self.map[r][c]
                    canvas.text(
                        (
                            c * self.square_size + self.square_size // 2,
                            r * self.square_size + self.square_size // 2,
                        ),
                        mahattan,
                        font=ImageFont.truetype("arial.ttf", font_size),
                        fill=(0, 0, 0),
                        anchor="mm",
                        stroke_width=1,
                        stroke_fill="black",
                    )
        img.show()
        img.save("maze.png", "PNG")

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if (
                    r >= 0
                    and c >= 0
                    and r < self.height
                    and c < self.width
                    and not self.map[r][c] == "#"
                ):
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier() if self.gbfs or self.bfs else StackFrontier()
        frontier.add(start)

        self.explored = set()
        self.costs = {self.start: 0}

        while True:
            if frontier.empty():
                raise Exception("no solution")

            if self.a_star:
                node = frontier.remove_smallest_node(
                    lambda state: self.__heuristic(state=state) + self.costs[state]
                )
                print(node.action)
            elif self.gbfs:
                node = frontier.remove_smallest_node(self.__heuristic)
            else:
                node = frontier.remove()
            self.num_explored += 1

            if self.goal == node.state:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if self.__valid_state(frontier=frontier, state=state):
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    self.costs[state] = self.costs[child.parent.state] + 1

    def __valid_state(self, frontier, state):
        return not frontier.contains_state(state) and state not in self.explored

    def __heuristic(self, state):
        (r, c) = state
        return abs(self.goal[1] - c) + abs(self.goal[0] - r)


if __name__ == "__main__":
    import sys

    if "--help" in sys.argv:
        print("Usage:", "python maze.py [FILEPATH] [OPTIONS]")
        print("Options:")
        print("--show-image:", "show image of the maze")
        print(
            "--bfs:",
            "use breadth-first search, default algorithm is depth-first search",
        )
        print(
            "--gbfs:",
            "use greedy breadth-first search, default algorithm is depth-first search",
        )
        print(
            "--astar:",
            "use A* algorithm, default algorithm is depth-first search",
        )
        print("--verbose:", "show all explored path when --show-image option is true")
        print(
            "--show-mahattan:",
            "show Mahattan distance when --show-image option is true",
        )
    else:
        print('Type "--help" for more information.')
        if len(sys.argv) <= 1 or not sys.argv[1].endswith(".txt"):
            raise Exception("must provide a text file")
        filename = sys.argv[1]
        show_image = "--show-image" in sys.argv
        verbose = "--verbose" in sys.argv
        bfs = "--bfs" in sys.argv
        gbfs = "--gbfs" in sys.argv
        a_star = "--astar" in sys.argv
        show_mahattan = "--show-mahattan" in sys.argv
        if bfs and gbfs and a_star:
            raise Exception("can only choose one algorithm")

        maze = Maze(
            filename=filename,
            show_image=show_image,
            verbose=verbose,
            bfs=bfs,
            gbfs=gbfs,
            a_star=a_star,
            show_mahattan=show_mahattan,
        )
        maze.solve()
        maze.print()
        maze.display_image()
