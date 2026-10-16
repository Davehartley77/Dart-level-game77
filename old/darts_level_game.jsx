import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

const avatarColors = ["#F87171", "#60A5FA", "#34D399", "#FBBF24", "#A78BFA", "#FB7185"];
const avatarIcons = ["🎯", "🎲", "🏹", "🎮", "🧿", "🔥"];

const levelSettings = [
  { level: 1, min: 2, max: 40, even: true, points: 3, failTo: 1, penalty: 0 },
  { level: 2, min: 41, max: 60, points: 4, failTo: 1, penalty: 2 },
  { level: 3, min: 61, max: 80, points: 5, failTo: 2, penalty: 3 },
  { level: 4, min: 81, max: 100, points: 7, failTo: 3, penalty: 4 },
  { level: 5, min: 101, max: 170, points: 10, failTo: 4, penalty: 5 },
];

function getRandomTarget(level) {
  const { min, max, even } = levelSettings[level - 1];
  let target;
  do {
    target = Math.floor(Math.random() * (max - min + 1)) + min;
  } while (even && target % 2 !== 0);
  return target;
}

const successSound = new Audio("/sounds/success.mp3");
const failSound = new Audio("/sounds/fail.mp3");
const winSound = new Audio("/sounds/win.mp3");

export default function DartsLevelGame() {
  const [players, setPlayers] = useState([]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [inputScore, setInputScore] = useState(0);
  const [newPlayerName, setNewPlayerName] = useState("");
  const [selectedColor, setSelectedColor] = useState(avatarColors[0]);
  const [selectedIcon, setSelectedIcon] = useState(avatarIcons[0]);
  const [gameStarted, setGameStarted] = useState(false);
  const [rounds, setRounds] = useState([]);

  function addPlayer() {
    if (!newPlayerName.trim()) return;
    setPlayers((prev) => [
      ...prev,
      {
        name: newPlayerName,
        score: 0,
        level: 1,
        target: getRandomTarget(1),
        history: [],
        color: selectedColor,
        icon: selectedIcon,
      },
    ]);
    setNewPlayerName("");
  }

  function startGame() {
    if (players.length > 0) setGameStarted(true);
  }

  function handleScoreSubmit() {
    const newPlayers = [...players];
    const currentPlayer = newPlayers[currentPlayerIndex];
    const levelInfo = levelSettings[currentPlayer.level - 1];
    const isSuccess = inputScore === currentPlayer.target;

    if (isSuccess) {
      successSound.play();
      currentPlayer.score += levelInfo.points;
      currentPlayer.history.push(`✔️ Hit ${currentPlayer.target} (Level ${currentPlayer.level})`);
      if (currentPlayer.level < 5) {
        currentPlayer.level++;
        currentPlayer.target = getRandomTarget(currentPlayer.level);
      }
    } else {
      failSound.play();
      currentPlayer.score = Math.max(0, currentPlayer.score - levelInfo.penalty);
      currentPlayer.history.push(`❌ Missed ${currentPlayer.target} (Level ${currentPlayer.level})`);
      currentPlayer.level = levelInfo.failTo;
      currentPlayer.target = getRandomTarget(levelInfo.failTo);
    }

    const roundInfo = {
      player: currentPlayer.name,
      result: isSuccess ? "Success" : "Fail",
      level: currentPlayer.level,
      score: currentPlayer.score,
    };
    setRounds((prev) => [...prev, roundInfo]);

    setPlayers(newPlayers);
    setInputScore(0);
    setCurrentPlayerIndex((currentPlayerIndex + 1) % players.length);
  }

  const winner = players.find((p) => p.score >= 50);
  if (winner) winSound.play();

  if (!gameStarted) {
    return (
      <div className="p-4 sm:p-6 grid gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold">🎯 Setup Players</h1>
        <input
          type="text"
          className="border p-2 rounded w-full sm:w-64"
          placeholder="Player name"
          value={newPlayerName}
          onChange={(e) => setNewPlayerName(e.target.value)}
        />
        <div className="flex gap-2 mt-2">
          {avatarColors.map((color, idx) => (
            <div
              key={idx}
              className={`w-6 h-6 rounded-full border-2 cursor-pointer ${selectedColor === color ? 'border-black' : 'border-white'}`}
              style={{ backgroundColor: color }}
              onClick={() => setSelectedColor(color)}
            />
          ))}
        </div>
        <div className="flex gap-2 mt-2">
          {avatarIcons.map((icon, idx) => (
            <button
              key={idx}
              className={`text-xl p-1 rounded ${selectedIcon === icon ? 'bg-gray-300' : ''}`}
              onClick={() => setSelectedIcon(icon)}
            >
              {icon}
            </button>
          ))}
        </div>
        <Button onClick={addPlayer}>Add Player</Button>
        <div>
          <h2 className="mt-4 font-semibold">Players:</h2>
          {players.map((p, i) => (
            <p key={i} style={{ color: p.color }}>{p.icon} {p.name}</p>
          ))}
        </div>
        <Button onClick={startGame} disabled={players.length === 0} className="mt-4">
          Start Game
        </Button>
      </div>
    );
  }

  const currentPlayer = players[currentPlayerIndex];

  return (
    <div className="p-4 sm:p-6 grid gap-4">
      <h1 className="text-2xl sm:text-3xl font-bold">🎯 Darts Level Game</h1>

      <img src="/images/dartboard.png" alt="dartboard" className="mx-auto w-48 sm:w-64" />

      {players.map((p, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Card className="p-4">
            <CardContent>
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-full" style={{ backgroundColor: p.color }} />
                <p className="font-semibold" style={{ color: p.color }}>{p.icon} {p.name}</p>
              </div>
              <p>Level: {p.level}</p>
              <p>Score: {p.score}</p>
              <p>Target: {p.target}</p>
              <p className="text-sm mt-2 font-mono text-gray-600">History:</p>
              <ul className="text-sm list-disc list-inside">
                {p.history.map((entry, idx) => (
                  <li key={idx}>{entry}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      ))}

      <motion.div
        className="p-4 bg-gray-100 rounded-xl"
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <h2 className="text-xl font-semibold mb-2" style={{ color: currentPlayer.color }}>
          {currentPlayer.icon} {currentPlayer.name}'s Turn (Level {currentPlayer.level})
        </h2>
        <p className="mb-2">Target to hit: {currentPlayer.target}</p>
        <input
          type="number"
          className="border p-2 rounded w-full sm:w-48"
          value={inputScore}
          onChange={(e) => setInputScore(Number(e.target.value))}
        />
        <Button className="mt-2 sm:mt-0 sm:ml-2" onClick={handleScoreSubmit}>
          Submit Score
        </Button>
      </motion.div>

      <div className="p-4 bg-white rounded shadow">
        <h3 className="font-bold text-lg mb-2">📜 Round History</h3>
        <ul className="text-sm space-y-1 max-h-40 overflow-y-auto">
          {rounds.map((r, i) => (
            <li key={i}>
              <strong>{r.player}</strong>: {r.result} (Level {r.level}) — Score: {r.score}
            </li>
          ))}
        </ul>
      </div>

      {winner && (
        <motion.div
          className="bg-green-100 p-4 rounded-xl text-lg font-bold"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1.1 }}
          transition={{ yoyo: Infinity, duration: 0.6 }}
        >
          🎉 Winner: {winner.icon} {winner.name}!
        </motion.div>
      )}

      <div className="p-4 bg-blue-100 rounded shadow">
        <h3 className="font-bold text-lg mb-2">🏆 Scoreboard</h3>
        <ul className="text-sm space-y-1">
          {[...players].sort((a, b) => b.score - a.score).map((p, i) => (
            <li key={i}><strong>{i + 1}. {p.icon} {p.name}</strong>: {p.score} pts</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
