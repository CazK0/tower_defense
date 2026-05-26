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

    ctx.fillStyle = 'red';
    Object.values(gameState.enemies).forEach(enemy => {
      ctx.beginPath();
      ctx.arc(enemy.pos.x, enemy.pos.y, 15, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.fillStyle = 'blue';
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

  return (
    <div style={{ display: 'flex', gap: '20px', padding: '20px', backgroundColor: '#111', color: 'white', height: '100vh' }}>
      <div>
        <h2>Tower Defense</h2>