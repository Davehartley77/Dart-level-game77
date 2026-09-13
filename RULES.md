# Saved by the Bull — Game Rules

Recovered from the June 2025 code (the version that became the Replit app "PlayerQuestTracker").

## The idea
A darts checkout game for 1 or more players. Each player climbs through five
levels. At every level the game gives you a random checkout number to hit.
Hit it and you go up a level and gain points. Miss it and you drop back and lose points.
First player to 50 points wins.

## Setup
- Add any number of players. Each player picks a name, a colour and an icon.
- Everyone starts on Level 1 with 0 points.
- Play goes round the players in the order they were added, one turn each.

## The levels
| Level | Target is a random number between | Points for a hit | Points lost for a miss | Miss sends you back to |
|-------|-----------------------------------|------------------|------------------------|------------------------|
| 1     | 2 and 40 (even numbers only)      | +3               | 0                      | Level 1 (stay)         |
| 2     | 41 and 60                         | +4               | -2                     | Level 1               |
| 3     | 61 and 80                         | +5               | -3                     | Level 2               |
| 4     | 81 and 100                        | +7               | -4                     | Level 3               |
| 5     | 101 and 170                       | +10              | -5                     | Level 4               |

## A turn
1. The screen shows the player's current level and their target number.
2. The player throws three darts, then presses HIT or MISSED.
3. On a HIT:
   - add the level's points to the player's score
   - move up one level (Level 5 players stay on Level 5)
   - a new target is drawn for the new level
4. On a MISS:
   - take the level's penalty off the score, but a score never goes below 0
   - drop back to the level shown in the table (Level 1 players stay on Level 1)
   - a new target is drawn for that level
5. The turn passes to the next player.

## Winning
- The first player whose score reaches 50 or more wins, and a winner banner shows.

## What the screen shows
- A card per player: name, colour, icon, current level, score, current target, and
  that player's own hit/miss history.
- A "whose turn" box with the target and a number entry field.
- A round-by-round history of every turn taken.
- A scoreboard sorted highest score first.
- Sounds on hit, miss and win.

## Older versions (for reference only)
The March 2025 version had SIX levels (level 5 was 101-120, level 6 was 121-170),
hit points of 3/4/6/8/10/12, miss penalties of 0/2/5/6/8/8, a miss always dropped
exactly one level, and there was no 50-point win: you played rounds until you chose
to stop and the highest score won. The June 2025 rules above replaced it.

# 501 mode (added 2026-09-13)

- Choose a start of 301, 501 or 701 and how many legs win the match. The starter alternates each leg.
- Each turn, enter the total of the three darts (or say it into the microphone where the browser allows).
- Standard double-out: the last dart must be a double or the bull. Going below zero, leaving 1, or a
  finish that isn't possible is a BUST and the score stays as it was.
- When a finish is on (170 or less, not a bogey number) the standard checkout route is shown and read out.
  When it isn't, the game suggests what to score to leave a good finish, e.g. "Score 180 to leave 141".
- On a checkout the player says how many darts it took, for the three-dart average.
- The caller voice (browser speech) announces scores, "you require", and the suggested checkout. Toggle it in the header.
