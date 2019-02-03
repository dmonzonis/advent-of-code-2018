#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"

typedef struct Marble
{
    int value;
    struct Marble *previous, *next;
} Marble;

typedef struct MarbleGame
{
    int size;
    int currentPlayer, currentMarble;
    int playerCount, lastMarble, marbleCount;
    Marble *marble;  // Marbles are stored in a doubly linked list
    unsigned long *scores;
} MarbleGame;

void removeMarble(Marble *marble)
{
    // Remove the marble from the list
    Marble *prev, *next;
    prev = marble->previous;
    next = marble->next;

    if (prev)
        prev->next = next;
    if (next)
        next->previous = prev;
    free(marble);
}

void initGame(MarbleGame *game, int playerCount, int lastMarble)
{
    // Initialize the struct for a new game
    game->size = 0;
    game->playerCount = playerCount;
    game->scores = (unsigned long *)calloc(playerCount, sizeof(unsigned long));
    game->marble = NULL;
    game->lastMarble = lastMarble;
    game->currentMarble = game->marbleCount = game->currentPlayer = 0;
}

bool playStep(MarbleGame *game)
{
    Marble *aux, *newMarble;
    if (game->currentMarble % 23 == 0) // Winner winner chicken dinner
    {
        // Take the marble 7 positions ccw
        for(size_t i = 0; i < 7; i++)
            game->marble = game->marble->previous;
        // Add its value to the current player's score
        game->scores[game->currentPlayer] += game->marble->value + game->currentMarble;
        // Remove it from the circle and make the next one the current marble
        aux = game->marble->next;
        removeMarble(game->marble);
        game->size--;
        game->marble = aux;
    }
    else
    {
        // Insert the marble into the circle
        game->marble = game->marble->next;
        aux = game->marble->next;
        newMarble = (Marble *)malloc(sizeof(Marble));
        newMarble->value = game->currentMarble;
        newMarble->previous = game->marble;
        newMarble->next = aux;
        game->marble->next = newMarble;
        aux->previous = newMarble;
        game->marble = newMarble;
        game->size++;
    }

    game->currentMarble++;
    game->currentPlayer = (game->currentPlayer + 1) % game->playerCount;
    
    return game->currentMarble == game->lastMarble;
}

void playGame(MarbleGame *game, int playerCount, int lastMarble)
{
    initGame(game, playerCount, lastMarble);

    // First play
    Marble *marble;
    marble = (Marble *)malloc(sizeof(Marble));
    marble->value = game->currentMarble;
    marble->previous = marble->next = marble; // Next and previous is itself
    game->marble = marble;
    game->currentPlayer++;
    game->currentMarble++;

    // Rest of plays
    while (!playStep(game));

    // Free memory
    for(size_t i = 0; i < game->size; i++)
    {
        marble = game->marble->next;
        free(game->marble);
        game->marble = marble;
    }
}

int highestScore(MarbleGame *game)
{
    int i;
    unsigned long max = 0;
    for(int i = 0; i < game->playerCount; i++)
    {
        if (game->scores[i] > max)
            max = game->scores[i];
    }
    return max;
}

int main(int argc, char const *argv[])
{
    int playerCount = 425;
    // int lastMarble = 70848;
    int lastMarble = 70848 * 100;

    MarbleGame game;
    playGame(&game, playerCount, lastMarble);
    printf("Highest score: %lu", highestScore(&game));

    free(game.scores);

    return 0;
}
