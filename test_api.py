import pytest
import requests
import json
from main import app

class TestBotWarAPI:
    """Tests pour l'API Bot War"""
    
    @pytest.fixture
    def client(self):
        """Client de test Flask"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_action_get_method(self, client):
        """Test de l'endpoint /action avec méthode GET"""
        response = client.get('/action')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'move' in data
        assert 'action' in data
        assert data['move'] in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']
        assert data['action'] in ['COLLECT', 'ATTACK', 'BOMB', 'NONE']
    
    def test_action_post_method(self, client):
        """Test de l'endpoint /action avec méthode POST"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'move' in data
        assert 'action' in data
        assert data['move'] == 'STAY'  # Au centre
        assert data['action'] in ['COLLECT', 'ATTACK', 'BOMB', 'NONE']
    
    def test_player_left_of_center(self, client):
        """Test: joueur à gauche du centre -> RIGHT"""
        game_state = {
            "player": {
                "position": [2, 5],
                "score": 5
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['move'] == 'RIGHT'
    
    def test_player_right_of_center(self, client):
        """Test: joueur à droite du centre -> LEFT"""
        game_state = {
            "player": {
                "position": [8, 5],
                "score": 15
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['move'] == 'LEFT'
    
    def test_player_above_center(self, client):
        """Test: joueur au-dessus du centre -> DOWN"""
        game_state = {
            "player": {
                "position": [5, 2],
                "score": 8
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['move'] == 'DOWN'
    
    def test_player_below_center(self, client):
        """Test: joueur en-dessous du centre -> UP"""
        game_state = {
            "player": {
                "position": [5, 8],
                "score": 12
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['move'] == 'UP'
    
    def test_collect_action(self, client):
        """Test: action COLLECT quand collectible à proximité"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": [
                    {
                        "type": "collectible",
                        "position": [5, 6]
                    }
                ]
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'COLLECT'
    
    def test_attack_action(self, client):
        """Test: action ATTACK quand ennemi adjacent"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            },
            "enemies": [
                {
                    "position": [5, 6],
                    "score": 8
                }
            ]
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'ATTACK'
    
    def test_smart_bomber_action(self, client):
        """Test: action BOMB avec type proximity (smart bomber)"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            },
            "enemies": [
                {
                    "position": [7, 5],
                    "score": 8
                },
                {
                    "position": [5, 7],
                    "score": 12
                }
            ],
            "bombs": []
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'BOMB'
        assert 'bombType' in data
        assert data['bombType'] == 'proximity'
    
    def test_trap_setter_action(self, client):
        """Test: action BOMB avec type timer (trap setter)"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": [
                    {
                        "type": "collectible",
                        "position": [7, 7]
                    }
                ]
            },
            "bombs": []
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'BOMB'
        assert 'bombType' in data
        assert data['bombType'] == 'timer'
    
    def test_none_action(self, client):
        """Test: action NONE quand aucune action spécifique"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            },
            "enemies": [],
            "bombs": []
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'NONE'
    
    def test_attack_priority_over_collect(self, client):
        """Test: priorité ATTACK > COLLECT"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": [
                    {
                        "type": "collectible",
                        "position": [5, 6]
                    }
                ]
            },
            "enemies": [
                {
                    "position": [5, 6],
                    "score": 8
                }
            ]
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] == 'ATTACK'  # ATTACK devrait avoir la priorité
    
    def test_bomb_limit_smart_bomber(self, client):
        """Test: limite de bombes smart_bomber"""
        game_state = {
            "player": {
                "position": [5, 5],
                "score": 10
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            },
            "enemies": [
                {
                    "position": [7, 5],
                    "score": 8
                },
                {
                    "position": [5, 7],
                    "score": 12
                }
            ],
            "bombs": [
                {
                    "type": "proximity",
                    "position": [4, 5]
                },
                {
                    "type": "proximity",
                    "position": [6, 5]
                },
                {
                    "type": "proximity",
                    "position": [5, 4]
                }
            ]
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['action'] != 'BOMB'  # Ne devrait pas placer de bombe
    
    def test_response_format(self, client):
        """Test: format de réponse correct"""
        game_state = {
            "player": {
                "position": [3, 3],
                "score": 7
            },
            "map": {
                "width": 10,
                "height": 10,
                "center": [5, 5],
                "objects": []
            }
        }
        
        response = client.post('/action', 
                             data=json.dumps(game_state),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Vérifier la structure de la réponse
        assert 'move' in data
        assert 'action' in data
        assert isinstance(data['move'], str)
        assert isinstance(data['action'], str)
        
        # Vérifier les valeurs possibles
        assert data['move'] in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']
        assert data['action'] in ['COLLECT', 'ATTACK', 'BOMB', 'NONE']
        
        # Si c'est une bombe, vérifier bombType
        if data['action'] == 'BOMB':
            assert 'bombType' in data
            assert data['bombType'] in ['proximity', 'timer', 'static']

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 