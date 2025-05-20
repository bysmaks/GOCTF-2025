package task

import (
	"context"
	"fmt"
	"holdem/config"
	"holdem/log"
	"holdem/timeoutrw"
	"math/rand/v2"
	"strings"
)

const newLine = '\n'

func Task(ctx context.Context, rw *timeoutrw.TimeoutReadWriter) error {
	logger := log.Logger(ctx)
	cfg := config.GetConfig()

	if _, err := rw.WriteString(welcomeMessage()); err != nil {
		return fmt.Errorf("failed to write welcome message: %v", err)
	}

	loose := false
	for lvl := 1; lvl <= cfg.Levels; lvl++ {
		cards := GenerateCardCombination(PokerCombination(rand.IntN(10)))
		rand.Shuffle(len(cards), func(i, j int) {
			cards[i], cards[j] = cards[j], cards[i]
		})

		highestComb := GetHighestCombination(cards)

		flop := cards[:3]
		turn := cards[3]
		river := cards[4]

		if _, err := rw.WriteStringf(taskBody(lvl, flop, turn, river)); err != nil {
			return fmt.Errorf("failed to write task content: %v", err)
		}

		answ, err := rw.ReadString(newLine)
		if err != nil {
			return fmt.Errorf("failed to read answer from client: %v", err)
		}

		if strings.TrimSpace(answ) == highestComb.String() {
			if _, err := rw.WriteString("Correct!\n\n"); err != nil {
				return fmt.Errorf("failed to write task result: %v", err)
			}
		} else {
			if _, err := rw.WriteStringf("Wrong! Highest comb was %s.\n\n", highestComb); err != nil {
				return fmt.Errorf("failed to write task result: %v", err)
			}
			loose = true
			break
		}
	}

	if loose {
		logger.Info("lost")
		if _, err := rw.WriteString("You lost! But you can try again\n"); err != nil {
			return fmt.Errorf("failed to write task flag: %v", err)
		}
	} else {
		logger.Info("won")
		if _, err := rw.WriteStringf("Gratz! Your flag: %s\n", cfg.Flag); err != nil {
			return fmt.Errorf("failed to write task flag: %v", err)
		}
	}

	return nil
}

const welcomeTemplate = "Give me name of the highest combination.\nCombinations names:\n%s\n\n"

func welcomeMessage() string {
	combinationsNames := make([]string, 0, RoyalFlush-HighCard+1)
	for comb := HighCard; comb <= RoyalFlush; comb++ {
		combinationsNames = append(combinationsNames, "- "+comb.String())
	}

	return fmt.Sprintf(welcomeTemplate, strings.Join(combinationsNames, "\n"))
}

const taskTemplate = "[Combination #%d]\nFlop: %s\nTurn: %s\nRiver: %s\n\nHighest combination: "

func taskBody(level int, flop []Card, turn Card, river Card) string {
	flopS := ""
	for i, card := range flop {
		flopS += card.String()
		if i != len(flop)-1 {
			flopS += " "
		}
	}

	return fmt.Sprintf(taskTemplate, level, flopS, turn, river)
}
