class MarbleGame:
    def __init__(self, player_count, last_marble):
        self.player_count = player_count
        self.last_marble = last_marble
        self.current_marble = 0
        self.index = 0
        self.player = 0
        self.marbles = []
        self.scores = [0] * player_count
    
    def play_step(self):
        if self.current_marble != 0 and self.current_marble % 23 == 0:
            # Winner winner chicken dinner
            self.index = (self.index - 7) % len(self.marbles)
            # Take the marble out, and add it and the current marble to
            # the score
            value = self.marbles[self.index]
            self.marbles.remove(value)
            self.scores[self.player] += value + self.current_marble
            self.current_marble += 1
            if self.current_marble == self.last_marble:
                return True
        else:
            # Put the next marble in the right place
            self.update_index()
            if self.index == 0:
                self.marbles.append(self.current_marble)
                self.index = len(self.marbles) - 1
            else:
                self.marbles.insert(self.index, self.current_marble)
            self.current_marble += 1
            if self.current_marble == self.last_marble:
                return True

        # Pass turn to the next player
        self.player = (self.player + 1) % self.player_count

    def update_index(self):
        if self.marbles:
            self.index = (self.index + 2) % (len(self.marbles))

    def play_game(self):
        game_finished = False
        while not game_finished:
            game_finished = self.play_step()

    def highest_score(self):
        return max(self.scores)


def main():
    # Part 1
    game = MarbleGame(425, 70848)
    game.play_game()
    print(game.highest_score())


if __name__ == "__main__":
    main()