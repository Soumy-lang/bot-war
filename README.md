# Bot War API

Une API Flask pour le jeu Bot War qui prend des décisions de mouvement et d'action basées sur l'état du jeu.

## 🎯 Objectif

Créer une API avec une route `/action` qui :
- Reçoit l'état du jeu (JSON)
- Répond avec `{"move": "UP", "action": "ATTACK", "bombType": "proximity"}`
- Implémente la logique de décision du bot avec nouvelles actions
- Inclut des tests avec Jest
- Utilise un Dockerfile fonctionnel
- Se déploie automatiquement avec GitHub Actions

## 🚀 Fonctionnalités

- **Route `/action`** : Endpoint principal pour les décisions du bot
- **Logique de mouvement** : Le bot se dirige vers le centre de la carte
- **Nouvelles actions** : COLLECT, ATTACK, BOMB, NONE
- **Types de bombes** : proximity, timer, static
- **Stratégies avancées** : smart_bomber, trap_setter
- **Tests complets** : Tests Jest pour tous les scénarios
- **Containerisation** : Dockerfile pour déploiement facile
- **CI/CD** : Déploiement automatique avec GitHub Actions

## 📋 Prérequis

- Python 3.11+
- Node.js 18+ (pour les tests)
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

3. **Installer les dépendances Node.js (pour les tests)**
```bash
npm install
```

4. **Démarrer l'API**
```bash
python main.py
```

L'API sera disponible sur `http://localhost:80`

### Avec Docker

```bash
# Construire l'image
docker build -t bot-war .

# Lancer le container
docker run -p 80:80 bot-war
```

## 🧪 Tests

### Tests Jest
```bash
npm test
```

### Tests avec Postman
Importez le fichier `postman_collection.json` dans Postman pour tester manuellement.

## 📡 Utilisation de l'API

### Endpoint : `/action`

**Méthode :** POST  
**Content-Type :** application/json

#### Exemple de requête :
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
- `BASE_URL` : URL de base pour les tests (défaut: `http://localhost:80`)

### Ports
- **Port par défaut** : 80
- **Host** : 0.0.0.0 (accessible depuis l'extérieur)

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
├── main.py                 # Point d'entrée de l'API
├── bot/
│   ├── __init__.py
│   ├── decision.py         # Logique de décision du bot
│   └── game_state.py       # Gestion de l'état du jeu
├── tests/
│   ├── api.test.js         # Tests Jest
│   └── mock_game_state.json # Données de test
├── requirements.txt         # Dépendances Python
├── package.json            # Configuration Node.js
├── Dockerfile              # Configuration Docker
├── postman_collection.json # Tests Postman
└── .github/workflows/      # GitHub Actions
    └── deploy.yml
```

## 🔄 Développement

### Ajouter de nouvelles fonctionnalités

1. **Modifier la logique** : Éditez `bot/decision.py`
2. **Ajouter des tests** : Créez de nouveaux tests dans `tests/api.test.js`
3. **Tester localement** : `npm test`
4. **Pousser les changements** : Le déploiement se fait automatiquement

### Améliorations possibles

- [x] Ajouter la logique d'attaque
- [x] Implémenter la détection d'ennemis
- [x] Ajouter la gestion des objets collectables
- [x] Implémenter les stratégies smart_bomber et trap_setter
- [ ] Optimiser les algorithmes de pathfinding
- [ ] Ajouter des métriques et monitoring
- [ ] Implémenter des stratégies plus avancées
- [ ] Ajouter la gestion des équipes

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs de l'API
2. Exécutez les tests : `npm test`
3. Consultez la documentation de l'API
4. Ouvrez une issue sur GitHub

---

**URL publique de l'API :** `https://your-deployment-url.com/action`

*Note : Remplacez `your-deployment-url.com` par votre URL de déploiement réelle.*