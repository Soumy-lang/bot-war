const axios = require('axios');

const BASE_URL = process.env.BASE_URL || 'http://localhost:80';

describe('Bot War API Tests', () => {
  test('Player au centre - devrait retourner STAY', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('move');
    expect(response.data).toHaveProperty('action');
    expect(response.data.move).toBe('STAY');
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Player à gauche du centre - devrait retourner RIGHT', async () => {
    const gameState = {
      player: {
        position: [2, 5],
        score: 5
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.move).toBe('RIGHT');
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Player à droite du centre - devrait retourner LEFT', async () => {
    const gameState = {
      player: {
        position: [8, 5],
        score: 15
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.move).toBe('LEFT');
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Player au-dessus du centre - devrait retourner DOWN', async () => {
    const gameState = {
      player: {
        position: [5, 2],
        score: 8
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.move).toBe('DOWN');
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Player en-dessous du centre - devrait retourner UP', async () => {
    const gameState = {
      player: {
        position: [5, 8],
        score: 12
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.move).toBe('UP');
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Player avec collectible à proximité - devrait retourner COLLECT', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: [
          {
            type: "collectible",
            position: [5, 6]
          }
        ]
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.action).toBe('COLLECT');
  });

  test('Player avec ennemi adjacent - devrait retourner ATTACK', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      },
      enemies: [
        {
          position: [5, 6],
          score: 8
        }
      ]
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.action).toBe('ATTACK');
  });

  test('Smart bomber - devrait retourner BOMB avec type proximity', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      },
      enemies: [
        {
          position: [7, 5],
          score: 8
        },
        {
          position: [5, 7],
          score: 12
        }
      ],
      bombs: []
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.action).toBe('BOMB');
    expect(response.data).toHaveProperty('bombType');
    expect(response.data.bombType).toBe('proximity');
  });

  test('Trap setter - devrait retourner BOMB avec type timer', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: [
          {
            type: "collectible",
            position: [7, 7]
          }
        ]
      },
      bombs: []
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.action).toBe('BOMB');
    expect(response.data).toHaveProperty('bombType');
    expect(response.data.bombType).toBe('timer');
  });

  test('Player sans action spécifique - devrait retourner NONE', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      },
      enemies: [],
      bombs: []
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data.action).toBe('NONE');
  });

  test('Scénario complet - Mouvement + Action', async () => {
    const gameState = {
      player: {
        position: [2, 3],
        score: 7
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: [
          {
            type: "collectible",
            position: [2, 4]
          }
        ]
      },
      enemies: [
        {
          position: [3, 3],
          score: 8
        }
      ],
      bombs: []
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('move');
    expect(response.data).toHaveProperty('action');
    // Le joueur devrait se déplacer vers le centre (RIGHT ou DOWN)
    expect(['RIGHT', 'DOWN']).toContain(response.data.move);
    // Et devrait collecter le point à proximité
    expect(response.data.action).toBe('COLLECT');
  });

  test('Format de réponse correct avec toutes les actions', async () => {
    const gameState = {
      player: {
        position: [3, 3],
        score: 7
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      }
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('move');
    expect(response.data).toHaveProperty('action');
    expect(typeof response.data.move).toBe('string');
    expect(typeof response.data.action).toBe('string');
    expect(['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']).toContain(response.data.move);
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Bombe avec type static', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      },
      enemies: [
        {
          position: [7, 5],
          score: 8
        }
      ],
      bombs: [
        {
          type: "static",
          position: [6, 5]
        }
      ]
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    expect(['COLLECT', 'ATTACK', 'BOMB', 'NONE']).toContain(response.data.action);
  });

  test('Limite de bombes smart_bomber', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: []
      },
      enemies: [
        {
          position: [7, 5],
          score: 8
        },
        {
          position: [5, 7],
          score: 12
        }
      ],
      bombs: [
        {
          type: "proximity",
          position: [4, 5]
        },
        {
          type: "proximity",
          position: [6, 5]
        },
        {
          type: "proximity",
          position: [5, 4]
        }
      ]
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    // Ne devrait pas placer de bombe car limite atteinte
    expect(response.data.action).not.toBe('BOMB');
  });

  test('Priorité ATTACK > COLLECT', async () => {
    const gameState = {
      player: {
        position: [5, 5],
        score: 10
      },
      map: {
        width: 10,
        height: 10,
        center: [5, 5],
        objects: [
          {
            type: "collectible",
            position: [5, 6]
          }
        ]
      },
      enemies: [
        {
          position: [5, 6],
          score: 8
        }
      ]
    };

    const response = await axios.post(`${BASE_URL}/action`, gameState);
    
    expect(response.status).toBe(200);
    // ATTACK devrait avoir la priorité sur COLLECT
    expect(response.data.action).toBe('ATTACK');
  });
});
