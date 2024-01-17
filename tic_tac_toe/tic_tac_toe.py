import sys


class TicTacToe:
    def __init__(self):
        self.actions_mapping = {
            "1": (0, 0),
            "2": (0, 1),
            "3": (0, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "7": (2, 0),
            "8": (2, 1),
            "9": (2, 2),
        }

    def get_action_from_box(self, box):
        return self.actions_mapping[box]

    def player(self, state):
        x_count = 0
        o_count = 0
        for r in state:
            for c in r:
                if c == "X":
                    x_count += 1
                if c == "O":
                    o_count += 1
        return "X" if x_count == o_count else "O"

    def actions(self, state):
        candidates = [
            (0, 1),
            (2, 1),
            (1, 0),
            (1, 2),
            (0, 0),
            (0, 2),
            (2, 0),
            (2, 2),
            (1, 1),
        ]

        result = []
        for r, c in candidates:
            if state[r][c] == " ":
                result.append((r, c))
        return result

    def result(self, state, action):
        import copy

        copied_state = copy.deepcopy(state)
        (r, c) = action
        copied_state[r][c] = self.player(state)
        return copied_state

    def terminal(self, state):
        has_empty = False
        for r in state:
            if " " in r:
                has_empty = True
            for i in range(len(r)):
                if (
                    " " != state[i][0] == state[i][1] == state[i][2]
                    or " " != state[0][i] == state[1][i] == state[2][i]
                ):
                    return True
        return (
            state[1][1] != " "
            and (
                state[0][0] == state[1][1] == state[2][2]
                or state[0][2] == state[1][1] == state[2][0]
            )
        ) or not has_empty

    def utility(self, state):
        for r in state:
            for i in range(len(r)):
                if " " != state[i][0] == state[i][1] == state[i][2]:
                    return 1 if state[i][0] == "X" else -1
                if " " != state[0][i] == state[1][i] == state[2][i]:
                    return 1 if state[0][i] == "X" else -1
        return (
            (1 if state[1][1] == "X" else -1)
            if state[1][1] != " "
            and (
                (
                    state[0][0] == state[1][1] == state[2][2]
                    or state[0][2] == state[1][1] == state[2][0]
                )
            )
            else 0
        )

    def max_value(self, state):
        if self.terminal(state):
            return (None, self.utility(state))
        value = -sys.maxsize - 1
        best_action = None
        for action in self.actions(state):
            min_value = self.min_value(self.result(state, action))[1]
            if value <= min_value:
                best_action = action
                value = min_value
            if value == 1:
                break
        return (best_action, value)

    def min_value(self, state):
        if self.terminal(state):
            return (None, self.utility(state))
        value = sys.maxsize
        for action in self.actions(state):
            max_value = self.max_value(self.result(state, action))[1]
            if value >= max_value:
                best_action = action
                value = max_value
            if value == -1:
                break
        return (best_action, value)

    def print(self, state):
        v1 = state[0][0]
        v2 = state[0][1]
        v3 = state[0][2]
        v4 = state[1][0]
        v5 = state[1][1]
        v6 = state[1][2]
        v7 = state[2][0]
        v8 = state[2][1]
        v9 = state[2][2]
        board = f"|{v1}|{v2}|{v3}|\n" f"|{v4}|{v5}|{v6}|\n" f"|{v7}|{v8}|{v9}|"
        print(board)

    def choose(self, state, action):
        if action not in self.actions(state):
            raise Exception("your box has been chosen or it is out of the boundaries.")
        else:
            return self.result(state, action)

    def board_is_empty(self, state):
        for r in state:
            if "X" in r or "O" in r:
                return False
        return True


if __name__ == "__main__":
    import random

    game = TicTacToe()
    while True:
        print("===== TIC TAC TOE =====")
        print("1> Play\n2> BvB\n3> Quit")
        choice = int(input("Your choice: "))
        if choice == 3:
            break
        elif choice not in (1, 2):
            print("You choice is invalid. Please choose again.")
            continue
        else:
            state = [[" "] * 3 for _ in range(3)]
            while game.terminal(state) is False:
                game.print(state)
                if choice == 1 and game.player(state) == "X":
                    box = input(f"Your turn. Which box (1-9)? : ")
                    try:
                        state = game.choose(state, game.get_action_from_box(box))
                    except Exception as e:
                        print(e)
                        continue
                else:
                    if choice == 2 and game.player(state) == "X":
                        if game.board_is_empty(state):
                            result = ((random.randint(0, 2), random.randint(0, 2)), 0)
                        else:
                            result = game.max_value(state)
                    else:
                        result = game.min_value(state)
                    (best_action, value) = result
                    print(
                        f"BEST MOVE FOR {game.player(state)}:",
                        best_action,
                        "Score: ",
                        value,
                    )
                    if best_action:
                        try:
                            state = game.choose(state, best_action)
                        except Exception as e:
                            print(e)
                            continue
            game.print(state)
            try:
                winner = game.utility(state)
                if winner in (1, -1):
                    print(f"Winner is {"X" if winner == 1 else "O"}!")
                else:
                    print(f"No one won!")
            except Exception as e:
                print(e)
            print("===========================")
