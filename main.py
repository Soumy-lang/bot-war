from flask import Flask, request, jsonify
from bot.decision import decide_action, get_bomb_type

app = Flask(__name__)

@app.route('/action', methods=['GET', 'POST'])
def action():
    if request.method == 'POST':
        game_state = request.get_json(force=True)

        # Garantir les clés attendues
        game_state.setdefault("enemies", [])
        game_state.setdefault("bombs", [])
        game_state.setdefault("map", {}).setdefault("objects", [])
    else:
        game_state = {
            "player": {"position": [5, 5], "score": 10},
            "map": {"width": 10, "height": 10, "center": [5, 5], "objects": []},
            "enemies": [],
            "bombs": []
        }

    move, action = decide_action(game_state)

    response = {
        "move": move,
        "action": action
    }

    if action == "BOMB":
        bomb_type = get_bomb_type(game_state, game_state["player"]["position"])
        response["bombType"] = bomb_type

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
