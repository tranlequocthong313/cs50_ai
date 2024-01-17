from flask import Flask, jsonify, request
from tic_tac_toe import TicTacToe
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
game = TicTacToe()


def convert(board):
    mapper = {"0": " ", "1": "X", "2": "O"}
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = mapper[str(board[i][j])]
    return board


@app.post("/choose/<box>")
def choose(box):
    try:
        board = convert(request.get_json()["board"])
        game = TicTacToe()
        state = game.choose(board, game.get_action_from_box(box))
        (best_action, value) = game.min_value(state)
        print(
            f"BEST MOVE FOR {game.player(state)}:",
            best_action,
            "Score: ",
            value,
        )
        if best_action:
            state = game.choose(state, best_action)
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 400
    print(state)
    return jsonify({"board": state, "gameOver": game.terminal(state)})


@app.post("/winner")
def winner():
    try:
        board = convert(request.get_json()["board"])
        return jsonify({"winner": game.utility(board)})
    except Exception as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
