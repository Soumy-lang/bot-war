# Bot War API

Une API Flask pour le jeu Bot War qui prend des décisions de mouvement et d'action basées sur l'état du jeu.

## 🎯 Objectif

Créer une API avec une route `/action` qui :
- Reçoit l'état du jeu (JSON)
- Répond avec `{"move": "UP", "action": "ATTACK", "bombType": "proximity"}`
- Implémente la logique de décision du bot avec nouvelles actions
- **Exécute automatiquement des actions toutes les 10 secondes**
- Inclut des tests avec pytest
- Utilise un Dockerfile fonctionnel
- Se déploie automatiquement avec GitHub Actions

## 🚀 Fonctionnalités

- **Route `/action`** : Endpoint principal pour les décisions du bot
- **Logique de mouvement** : Le bot se dirige vers le centre de la carte
- **Nouvelles actions** : COLLECT, ATTACK, BOMB, NONE
- **Types de bombes** : proximity, timer, static
- **Stratégies avancées** : smart_bomber, trap_setter
- **Exécution automatique** : Actions toutes les 10 secondes en arrière-plan
- **Tests complets** : Tests pytest pour tous les scénarios
- **Containerisation** : Dockerfile pour déploiement facile
- **CI/CD** : Déploiement automatique avec GitHub Actions

## 📋 Prérequis

- Python 3.11+
- Docker (optionnel)

## 🛠️ Installation

### Installation locale

1. **Cloner le repository**
```bash
git clone <your-repo-url>
cd bot-war
```

2. **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

3. **Démarrer l'API**
```bash
python main.py
```

L'API sera disponible sur `http://localhost:5000`

**⚠️ Note importante :** L'API démarre automatiquement l'exécution d'actions toutes les 10 secondes en arrière-plan.

### Avec Docker

```bash
# Construire l'image
docker build -t bot-war .

# Lancer le container
docker run -p 5000:5000 bot-war
```

## 🧪 Tests

### Tests pytest
```bash
# Exécuter tous les tests
python -m pytest test_api.py -v

# Ou avec npm (si package.json configuré)
npm test
```

### Tests avec Postman
Importez le fichier `postman_collection.json` dans Postman pour tester manuellement.

## 📡 Utilisation de l'API

### Endpoint : `/action`

**Méthodes :** GET, POST  
**Content-Type :** application/json (pour POST)

#### Exemple de requête POST :
```json
{
  "player": {
    "position": [2, 3],
    "score": 5
  },
  "map": {
    "width": 10,
    "height": 10,
    "center": [5, 5],
    "objects": [
      {
        "type": "collectible",
        "position": [2, 4]
      }
    ]
  },
  "enemies": [
    {
      "position": [3, 3],
      "score": 8
    }
  ],
  "bombs": []
}
```

#### Exemple de réponse :
```json
{
  "move": "RIGHT",
  "action": "COLLECT"
}
```

#### Exemple de réponse avec bombe :
```json
{
  "move": "STAY",
  "action": "BOMB",
  "bombType": "proximity"
}
```

### Valeurs possibles pour `move` :
- `"UP"` : Se déplacer vers le haut
- `"DOWN"` : Se déplacer vers le bas
- `"LEFT"` : Se déplacer vers la gauche
- `"RIGHT"` : Se déplacer vers la droite
- `"STAY"` : Rester sur place

### Valeurs possibles pour `action` :
- `"COLLECT"` : Collecter un point à proximité
- `"ATTACK"` : Attaquer un bot ennemi adjacent
- `"BOMB"` : Placer une bombe
- `"NONE"` : Aucune action

### Types de bombes (`bombType`) :
- `"proximity"` : Explose quand un bot ennemi passe à côté (défaut)
- `"timer"` : Explose après 2 tours
- `"static"` : Ne bouge jamais, obstacle permanent

## ⏰ Exécution automatique

L'API exécute automatiquement des actions toutes les 10 secondes en arrière-plan :

### **Au démarrage :**
- L'exécution automatique démarre automatiquement
- Un thread en arrière-plan prend des décisions toutes les 10 secondes
- Les actions sont affichées dans les logs de l'API

### **État de jeu par défaut pour l'auto-exécution :**
```json
{
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
```

### **Logs d'exécution automatique :**
```
🚀 Bot War API démarrée sur http://localhost:5000
📡 Endpoint disponible: GET/POST /action
⏰ L'exécution automatique effectue des actions toutes les 10 secondes
🚀 Exécution automatique démarrée - actions toutes les 10 secondes
Auto-execution: {'move': 'STAY', 'action': 'NONE'}
Auto-execution: {'move': 'STAY', 'action': 'NONE'}
Auto-execution: {'move': 'STAY', 'action': 'NONE'}
```

## 🧠 Logique de décision

### Mouvement
Le bot utilise une logique simple pour se diriger vers le centre :
1. **Calcul de la position** : Détermine sa position actuelle
2. **Calcul du centre** : Identifie le centre de la carte
3. **Décision de mouvement** :
   - Si à gauche du centre → `RIGHT`
   - Si à droite du centre → `LEFT`
   - Si au-dessus du centre → `DOWN`
   - Si en-dessous du centre → `UP`
   - Si au centre → `STAY`

### Actions
Priorité des actions (dans l'ordre) :
1. **COLLECT** : Si un objet collectable est à proximité (distance ≤ 1)
2. **ATTACK** : Si un ennemi est adjacent (distance = 1)
3. **BOMB** : Selon les stratégies smart_bomber ou trap_setter
4. **NONE** : Aucune action spécifique

### Stratégies

#### Smart Bomber
- **Objectif** : Placer des bombes de proximité intelligentes
- **Condition** : 2+ ennemis à distance 2-3 et moins de 3 bombes existantes
- **Type de bombe** : `proximity`

#### Trap Setter
- **Objectif** : Placer des pièges près des points collectables
- **Condition** : Point collectable à distance 1-2 et pas de bombe timer existante
- **Type de bombe** : `timer`

## 🔧 Configuration

### Variables d'environnement
- `BASE_URL` : URL de base pour les tests (défaut: `http://localhost:5000`)

### Ports
- **Port par défaut** : 5000
- **Host** : 0.0.0.0 (accessible depuis l'extérieur)

### Timing
- **Intervalle d'exécution automatique** : 10 secondes
- **Thread daemon** : S'arrête automatiquement quand l'API s'arrête

## 🚀 Déploiement

### GitHub Actions

Le projet inclut un workflow GitHub Actions qui :
1. **Exécute les tests** sur chaque push/PR
2. **Construit l'image Docker** si les tests passent
3. **Pousse l'image** vers Docker Hub
4. **Déploie automatiquement** sur la branche main

### Configuration requise

Ajoutez ces secrets dans votre repository GitHub :
- `DOCKER_USERNAME` : Votre nom d'utilisateur Docker Hub
- `DOCKER_PASSWORD` : Votre token Docker Hub

## 📁 Structure du projet

```
bot-war/
├── main.py                 # Point d'entrée de l'API avec auto-exécution
├── bot/
│   ├── __init__.py
│   ├── decision.py         # Logique de décision du bot
│   └── game_state.py       # Gestion de l'état du jeu
├── tests/
│   └── mock_game_state.json # Données de test
├── test_api.py             # Tests pytest
├── requirements.txt         # Dépendances Python
├── package.json            # Configuration npm (optionnel)
├── Dockerfile              # Configuration Docker
├── postman_collection.json # Tests Postman
└── .github/workflows/      # GitHub Actions
    └── deploy.yml
```

## 🔄 Développement

### Ajouter de nouvelles fonctionnalités

1. **Modifier la logique** : Éditez `bot/decision.py`
2. **Ajouter des tests** : Créez de nouveaux tests dans `test_api.py`
3. **Tester localement** : `python -m pytest test_api.py -v`
4. **Pousser les changements** : Le déploiement se fait automatiquement

### Améliorations possibles

- [x] Ajouter la logique d'attaque
- [x] Implémenter la détection d'ennemis
- [x] Ajouter la gestion des objets collectables
- [x] Implémenter les stratégies smart_bomber et trap_setter
- [x] Ajouter l'exécution automatique toutes les 10 secondes
- [x] Remplacer les tests Jest par pytest
- [ ] Optimiser les algorithmes de pathfinding
- [ ] Ajouter des métriques et monitoring
- [ ] Implémenter des stratégies plus avancées
- [ ] Ajouter la gestion des équipes

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs de l'API
2. Exécutez les tests : `python -m pytest test_api.py -v`
3. Consultez la documentation de l'API
4. Ouvrez une issue sur GitHub

---

**URL publique de l'API :** `https://your-deployment-url.com/action`

*Note : Remplacez `your-deployment-url.com` par votre URL de déploiement réelle.*