import random

class DartsGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.player_scores = [0] * num_players
        self.player_levels = [1] * num_players
        self.current_targets = [0] * num_players
        self.level_ranges = [
            (2, 40, 2),   # Level 1: range 2-40 (even), +3 points
            (41, 60, 1),  # Level 2: range 41-60, +4/-2 points
            (61, 80, 1),  # Level 3: range 61-80, +6/-5 points
            (81, 100, 1), # Level 4: range 81-100, +8/-6 points
            (101, 120, 1),# Level 5: range 101-120, +10/-8 points
            (121, 170, 1) # Level 6: range 121-170, +12/-8 points
        ]
        self.level_rewards = [3, 4, 6, 8, 10, 12]
        self.level_penalties = [0, 2, 5, 6, 8, 8]

    def generate_target(self, level):
        min_val, max_val, step = self.level_ranges[level - 1]
        if level == 1:
            # Ensure even number for level 1
            target = random.randrange(min_val, max_val + 1, step)
            return target if target % 2 == 0 else target + 1
        return random.randint(min_val, max_val)

    def check_hit(self, player_num):
        self.current_targets[player_num] = self.generate_target(self.player_levels[player_num])
        print(f"\nPlayer {player_num + 1}: Level {self.player_levels[player_num]}")
        print(f"Target number: {self.current_targets[player_num]}")
        
        while True:
            try:
                hit = int(input("Enter the number you hit (or any number to simulate): "))
                break
            except ValueError:
                print("Please enter a valid number!")
        
        if hit == self.current_targets[player_num]:
            self.handle_hit(player_num)
        else:
            self.handle_miss(player_num)

    def handle_hit(self, player_num):
        level = self.player_levels[player_num]
        points = self.level_rewards[level - 1]
        self.player_scores[player_num] += points
        print(f"Hit! Player {player_num + 1} gains {points} points. Total: {self.player_scores[player_num]}")
        
        # Move to next level if not at max
        if level < len(self.level_ranges):
            self.player_levels[player_num] += 1
            print(f"Player {player_num + 1} advances to Level {self.player_levels[player_num]}")
        else:
            print(f"Player {player_num + 1} is already at max level!")

    def handle_miss(self, player_num):
        level = self.player_levels[player_num]
        if level == 1:
            print("Miss! No points lost at Level 1.")
            return
        
        penalty = self.level_penalties[level - 1]
        self.player_scores[player_num] = max(0, self.player_scores[player_num] - penalty)
        print(f"Miss! Player {player_num + 1} loses {penalty} points. Total: {self.player_scores[player_num]}")
        
        # Go back one level if not at level 1
        self.player_levels[player_num] = max(1, level - 1)
        print(f"Player {player_num + 1} drops to Level {self.player_levels[player_num]}")

    def play_game(self):
        print("Welcome to Multiplayer Darts Scoring Game!")
        round_num = 1
        
        while True:
            print(f"\n=== Round {round_num} ===")
            for player in range(self.num_players):
                print(f"\nPlayer {player + 1}'s turn (Score: {self.player_scores[player]})")
                self.check_hit(player)
            
            # Display scores
            print("\nCurrent Scores:")
            for i in range(self.num_players):
                print(f"Player {i + 1}: {self.player_scores[i]} points (Level {self.player_levels[i]})")
            
            # Check if players want to continue
            play_again = input("\nPlay another round? (y/n): ").lower()
            if play_again != 'y':
                break
            round_num += 1
        
        print("\nFinal Scores:")
        for i in range(self.num_players):
            print(f"Player {i + 1}: {self.player_scores[i]} points")
        
        # Determine winner
        max_score = max(self.player_scores)
        winners = [i + 1 for i, score in enumerate(self.player_scores) if score == max_score]
        if len(winners) == 1:
            print(f"\nPlayer {winners[0]} wins with {max_score} points!")
        else:
            print(f"\nIt's a tie between Players {', '.join(map(str, winners))} with {max_score} points!")

def main():
    while True:
        try:
            num_players = int(input("Enter the number of players (1-4): "))
            if 1 <= num_players <= 4:
                break
            print("Please enter a number between 1 and 4!")
        except ValueError:
            print("Please enter a valid number!")
    
    game = DartsGame(num_players)
    game.play_game()

if __name__ == "__main__":
    main()
