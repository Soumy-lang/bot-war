from flask import Flask, request, jsonify
from bot.decision import decide_action, get_bomb_type

app = Flask(__name__)

@app.route('/action', methods=['POST'])
def action():
    """
    Endpoint principal pour les décisions du bot.
    
    Accepte un état de jeu JSON et retourne :
    - move : Direction de mouvement (UP, DOWN, LEFT, RIGHT, STAY)
    - action : Type d'action (COLLECT, ATTACK, BOMB, NONE)
    - bombType : Type de bombe si action=BOMB (proximity, timer, static)
    """
    game_state = request.get_json(force=True)
    move, action = decide_action(game_state)
    
    response = {
        "move": move,
        "action": action
    }
    
    # Ajouter le type de bombe si l'action est BOMB
    if action == "BOMB":
        player_pos = game_state["player"]["position"]
        bomb_type = get_bomb_type(game_state, player_pos)
        response["bombType"] = bomb_type
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
