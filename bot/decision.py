def decide_action(game_state):
    """
    Décide de l'action du bot basée sur l'état du jeu.
    
    Actions possibles :
    - COLLECT : Collecter un point
    - ATTACK : Attaquer un bot adjacent
    - BOMB : Placer une bombe
    - NONE : Aucune action
    
    Types de bombes :
    - proximity : Explose quand un bot ennemi passe à côté (défaut)
    - timer : Explose après 2 tours
    - static : Ne bouge jamais, obstacle permanent
    
    Stratégies :
    - smart_bomber : Pose des bombes de proximité intelligentes
    - trap_setter : Place des pièges près des points
    """
    
    player = game_state["player"]
    x, y = player["position"]
    
    center = game_state["map"]["center"]
    cx, cy = center
    
    # Décision de mouvement (logique existante)
    move = "STAY"
    if x < cx:
        move = "RIGHT"
    elif x > cx:
        move = "LEFT"
    elif y < cy:
        move = "DOWN"
    elif y > cy:
        move = "UP"
    
    # Nouvelle logique pour les actions
    action = decide_action_type(game_state, player)
    
    return move, action

def decide_action_type(game_state, player):
    """
    Décide du type d'action à effectuer.
    """
    player_pos = player["position"]
    map_data = game_state["map"]
    
    # Vérifier s'il y a des ennemis à attaquer (priorité la plus haute)
    if has_enemy_adjacent(player_pos, game_state):
        return "ATTACK"
    
    # Vérifier s'il y a des points à collecter à proximité
    if has_collectible_nearby(player_pos, map_data):
        return "COLLECT"
    
    # Stratégie smart_bomber : placer des bombes de proximité intelligentes
    if should_place_smart_bomb(player_pos, game_state):
        return "BOMB"
    
    # Stratégie trap_setter : placer des pièges près des points
    if should_place_trap(player_pos, game_state):
        return "BOMB"
    
    # Par défaut, aucune action
    return "NONE"

def has_collectible_nearby(player_pos, map_data):
    """
    Vérifie s'il y a des objets collectables à proximité.
    """
    x, y = player_pos
    objects = map_data.get("objects", [])
    
    for obj in objects:
        if obj.get("type") == "collectible":
            obj_x, obj_y = obj["position"]
            # Distance de Manhattan <= 1
            if abs(x - obj_x) + abs(y - obj_y) <= 1:
                return True
    
    return False

def has_enemy_adjacent(player_pos, game_state):
    """
    Vérifie s'il y a des ennemis adjacents à attaquer.
    """
    x, y = player_pos
    enemies = game_state.get("enemies", [])
    
    for enemy in enemies:
        enemy_x, enemy_y = enemy["position"]
        # Distance de Manhattan = 1 (adjacent)
        if abs(x - enemy_x) + abs(y - enemy_y) == 1:
            return True
    
    return False

def should_place_smart_bomb(player_pos, game_state):
    """
    Stratégie smart_bomber : place des bombes de proximité intelligentes.
    """
    x, y = player_pos
    enemies = game_state.get("enemies", [])
    bombs = game_state.get("bombs", [])
    
    # Vérifier s'il y a des ennemis à proximité (distance 2-3)
    nearby_enemies = 0
    for enemy in enemies:
        enemy_x, enemy_y = enemy["position"]
        distance = abs(x - enemy_x) + abs(y - enemy_y)
        if 2 <= distance <= 3:
            nearby_enemies += 1
    
    # Vérifier qu'il n'y a pas déjà trop de bombes
    existing_bombs = len([b for b in bombs if b.get("type") == "proximity"])
    
    # Placer une bombe si 2+ ennemis à proximité et pas trop de bombes existantes
    return nearby_enemies >= 2 and existing_bombs < 3

def should_place_trap(player_pos, game_state):
    """
    Stratégie trap_setter : place des pièges près des points collectables.
    """
    x, y = player_pos
    objects = game_state["map"].get("objects", [])
    bombs = game_state.get("bombs", [])
    
    # Chercher des points collectables
    collectibles = [obj for obj in objects if obj.get("type") == "collectible"]
    
    # S'il y a des collectibles sur la carte
    if collectibles:
        # Vérifier qu'il n'y a pas déjà trop de bombes timer
        existing_timer_bombs = len([b for b in bombs if b.get("type") == "timer"])
        
        # Placer une bombe timer si pas trop de bombes timer existantes
        return existing_timer_bombs < 2
    
    return False

def get_bomb_type(game_state, player_pos):
    """
    Détermine le type de bombe à placer selon la stratégie.
    """
    # Pour smart_bomber : utiliser des bombes de proximité
    if should_place_smart_bomb(player_pos, game_state):
        return "proximity"
    
    # Pour trap_setter : utiliser des bombes timer
    if should_place_trap(player_pos, game_state):
        return "timer"
    
    # Par défaut : bombe de proximité
    return "proximity"
