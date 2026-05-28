import React, { useEffect, useRef, useState } from 'react';

export default function App() {
  const canvasRef = useRef(null);
  const [ws, setWs] = useState(null);
  const [gameState, setGameState] = useState(null);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/game');

    socket.onopen = () => console.log("Connected to Python Engine!");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setGameState(data);
    };

    setWs(socket);

    return () => socket.close();
  }, []);

  useEffect(() => {
    if (!canvasRef.current || !gameState) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState.lasers) {
      ctx.strokeStyle = 'cyan';
      ctx.lineWidth = 2;
      gameState.lasers.forEach(laser => {
        ctx.beginPath();
        ctx.moveTo(laser.startX, laser.startY);
        ctx.lineTo(laser.endX, laser.endY);
        ctx.stroke();
      });
    }

    const drawPolygon = (x, y, radius, sides) => {
      ctx.beginPath();
      for (let i = 0; i < sides; i++) {
        const angle = (i * 2 * Math.PI) / sides - (Math.PI / 2);
        const px = x + radius * Math.cos(angle);
        const py = y + radius * Math.sin(angle);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fill();
    };

    const sidesMap = {
      'triangle': 3,
      'square': 4,
      'pentagon': 5,
      'hexagon': 6,
      'heptagon': 7,
      'octagon': 8
    };

    ctx.fillStyle = '#ff3366';
    Object.values(gameState.enemies).forEach(enemy => {
      if (enemy.type === 'circle') {
        ctx.beginPath();
        ctx.arc(enemy.pos.x, enemy.pos.y, 15, 0, Math.PI * 2);
        ctx.fill();
      } else {
        drawPolygon(enemy.pos.x, enemy.pos.y, 15, sidesMap[enemy.type] || 8);
      }
    });

    ctx.fillStyle = '#0088ff';
    Object.values(gameState.towers).forEach(tower => {
      ctx.fillRect(tower.pos.x - 15, tower.pos.y - 15, 30, 30);
    });

  }, [gameState]);

  const placeTower = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        action: "place_tower",
        payload: { type: "square", x: 400, y: 300 }
      }));
    }
  };

  const startWave = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        action: "start_wave",
        payload: {}
      }));
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px', padding: '20px', backgroundColor: '#111', color: 'white', height: '100vh' }}>
      <div>
        <h2>Tower Defense</h2>
        <p>Lives: {gameState?.lives || 20} | Money: ${gameState?.money || 100}</p>
        <p>Wave: {gameState?.wave || 1}</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <button onClick={placeTower} style={{ padding: '10px', background: '#333', color: 'white', border: '1px solid #555', cursor: 'pointer' }}>
            Place Tower ($50)
          </button>
          <button onClick={startWave} style={{ padding: '10px', background: '#006600', color: 'white', border: '1px solid #00aa00', cursor: 'pointer' }}>
            Start Wave
          </button>
        </div>
      </div>

      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={{ border: '2px solid #444', backgroundColor: '#000' }}
      />
    </div>
  );
}