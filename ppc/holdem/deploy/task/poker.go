package task

import (
	"fmt"
	"math/rand/v2"
	"slices"
)

type PokerCombination uint

const (
	HighCard PokerCombination = iota
	OnePair
	TwoPair
	ThreeOfAKind
	Straight
	Flush
	FullHouse
	FourOfAKind
	StraightFlush
	RoyalFlush
)

func (d PokerCombination) String() string {
	if d > 9 {
		panic(fmt.Sprintf("invalid poker combination: %d", d))
	}
	return [...]string{
		"HIGH CARD", "ONE PAIR", "TWO PAIR", "THREE OF A KIND",
		"STRAIGHT", "FLUSH", "FULL HOUSE",
		"FOUR OF A KIND", "STRAIGHT FLUSH", "ROYAL FLUSH",
	}[d]
}

type CardRank uint

const (
	One CardRank = iota + 1
	Two
	Three
	Four
	Five
	Six
	Seven
	Eight
	Nine
	Ten
	Jack
	Queen
	King
	Ace
)

func (r CardRank) String() string {
	if r < 1 || r > 14 {
		panic(fmt.Sprintf("invalid card rank: %d", r))
	}

	return [...]string{"1", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"}[r-1]
}

func (r CardRank) NextRank() CardRank {
	if r == Ace {
		return One
	}

	return r + 1
}

type CardSuit uint

const (
	Hearts CardSuit = iota
	Diamonds
	Clubs
	Spades
)

func (s CardSuit) String() string {
	if s > 3 {
		panic(fmt.Sprintf("invalid card suit: %d", s))
	}

	return [...]string{"h", "d", "c", "s"}[s]
}

type Card struct {
	Rank CardRank
	Suit CardSuit
}

func (c Card) String() string {
	return fmt.Sprintf("%s%s", c.Rank, c.Suit)
}

func GenerateCardCombination(baseComb PokerCombination) []Card {
	switch baseComb {
	case HighCard:
		return generateHighCard()
	case OnePair:
		return generateOnePair()
	case TwoPair:
		return generateTwoPair()
	case ThreeOfAKind:
		return generateThreeOfAKind()
	case Straight:
		return generateStraight()
	case Flush:
		return generateFlush()
	case FullHouse:
		return generateFullHouse()
	case FourOfAKind:
		return generateFourOfAKind()
	case StraightFlush:
		return generateStraightFlush()
	case RoyalFlush:
		return generateRoyalFlush()
	default:
		return []Card{}
	}
}

func generateRandomCard() Card {
	return Card{
		Rank: CardRank(rand.IntN(13) + 1),
		Suit: CardSuit(rand.IntN(4)),
	}
}

func generateHighCard() []Card {
	cards := make([]Card, 5)
	usedRanks := make(map[CardRank]bool)

	for i := 0; i < 5; i++ {
		for {
			card := generateRandomCard()
			if !usedRanks[card.Rank] {
				usedRanks[card.Rank] = true
				cards[i] = card
				break
			}
		}
	}
	return cards
}

func generateOnePair() []Card {
	pairRank := CardRank(rand.IntN(13) + 1)
	cards := []Card{
		{Rank: pairRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pairRank, Suit: CardSuit(rand.IntN(4))},
	}

	usedRanks := map[CardRank]bool{pairRank: true}
	for i := 0; i < 3; i++ {
		for {
			card := generateRandomCard()
			if !usedRanks[card.Rank] {
				usedRanks[card.Rank] = true
				cards = append(cards, card)
				break
			}
		}
	}
	return cards
}

func generateTwoPair() []Card {
	pair1Rank := CardRank(rand.IntN(13) + 1)
	pair2Rank := CardRank(rand.IntN(13) + 1)
	for pair2Rank == pair1Rank {
		pair2Rank = CardRank(rand.IntN(13) + 1)
	}

	cards := []Card{
		{Rank: pair1Rank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pair1Rank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pair2Rank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pair2Rank, Suit: CardSuit(rand.IntN(4))},
	}

	usedRanks := map[CardRank]bool{pair1Rank: true, pair2Rank: true}
	for {
		card := generateRandomCard()
		if !usedRanks[card.Rank] {
			cards = append(cards, card)
			break
		}
	}
	return cards
}

func generateThreeOfAKind() []Card {
	tripletRank := CardRank(rand.IntN(13) + 1)
	cards := []Card{
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
	}

	usedRanks := map[CardRank]bool{tripletRank: true}
	for i := 0; i < 2; i++ {
		for {
			card := generateRandomCard()
			if !usedRanks[card.Rank] {
				usedRanks[card.Rank] = true
				cards = append(cards, card)
				break
			}
		}
	}
	return cards
}

func generateStraight() []Card {
	startRank := CardRank(rand.IntN(10) + 1)
	cards := make([]Card, 5)

	for i := 0; i < 5; i++ {
		rank := startRank + CardRank(i)
		if rank > Ace {
			rank = One
		}
		cards[i] = Card{
			Rank: rank,
			Suit: CardSuit(rand.IntN(4)),
		}
	}
	return cards
}

func generateFlush() []Card {
	suit := CardSuit(rand.IntN(4))
	cards := make([]Card, 5)
	usedRanks := make(map[CardRank]bool)

	for i := 0; i < 5; i++ {
		for {
			card := Card{
				Rank: CardRank(rand.IntN(13) + 1),
				Suit: suit,
			}
			if !usedRanks[card.Rank] {
				usedRanks[card.Rank] = true
				cards[i] = card
				break
			}
		}
	}
	return cards
}

func generateFullHouse() []Card {
	tripletRank := CardRank(rand.IntN(13) + 1)
	pairRank := CardRank(rand.IntN(13) + 1)
	for pairRank == tripletRank {
		pairRank = CardRank(rand.IntN(13) + 1)
	}

	return []Card{
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: tripletRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pairRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: pairRank, Suit: CardSuit(rand.IntN(4))},
	}
}

func generateFourOfAKind() []Card {
	quadRank := CardRank(rand.IntN(13) + 1)
	cards := []Card{
		{Rank: quadRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: quadRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: quadRank, Suit: CardSuit(rand.IntN(4))},
		{Rank: quadRank, Suit: CardSuit(rand.IntN(4))},
	}

	for {
		card := generateRandomCard()
		if card.Rank != quadRank {
			cards = append(cards, card)
			break
		}
	}
	return cards
}

func generateStraightFlush() []Card {
	startRank := CardRank(rand.IntN(10) + 1)
	suit := CardSuit(rand.IntN(4))
	cards := make([]Card, 5)

	for i := 0; i < 5; i++ {
		rank := startRank + CardRank(i)
		if rank > Ace {
			rank = One
		}
		cards[i] = Card{
			Rank: rank,
			Suit: suit,
		}
	}
	return cards
}

func generateRoyalFlush() []Card {
	suit := CardSuit(rand.IntN(4))
	return []Card{
		{Rank: Ten, Suit: suit},
		{Rank: Jack, Suit: suit},
		{Rank: Queen, Suit: suit},
		{Rank: King, Suit: suit},
		{Rank: Ace, Suit: suit},
	}
}

func GetHighestCombination(cards []Card) PokerCombination {
	highestCombination := HighCard

	if isOnePair(cards) {
		highestCombination = OnePair
	}

	if isTwoPair(cards) {
		highestCombination = TwoPair
	}

	if isThreeOfAKind(cards) {
		highestCombination = ThreeOfAKind
	}

	if isStraight(cards) {
		highestCombination = Straight
	}

	if IsFlush(cards) {
		highestCombination = Flush
	}

	if isFullHouse(cards) {
		highestCombination = FullHouse
	}

	if isFourOfAKind(cards) {
		highestCombination = FourOfAKind
	}

	if isStraightFlush(cards) {
		highestCombination = StraightFlush
	}

	if isRoyalFlush(cards) {
		highestCombination = RoyalFlush
	}

	return highestCombination
}

func isRoyalFlush(cards []Card) bool {
	return cards[len(cards)-1].Rank == Ace && isStraightFlush(cards)
}

func isStraightFlush(cards []Card) bool {
	return isStraight(cards) && IsFlush(cards)
}

func isFourOfAKind(cards []Card) bool {
	ranksCountMap := make(map[CardRank]int, len(cards))
	for _, card := range cards {
		if _, ok := ranksCountMap[card.Rank]; !ok {
			ranksCountMap[card.Rank] = 0
		}
		ranksCountMap[card.Rank]++

		if ranksCountMap[card.Rank] >= 4 {
			return true
		}
	}
	return false
}

func isFullHouse(cards []Card) bool {
	ranksCountMap := make(map[CardRank]int, len(cards))
	for _, card := range cards {
		if _, ok := ranksCountMap[card.Rank]; !ok {
			ranksCountMap[card.Rank] = 0
		}
		ranksCountMap[card.Rank]++
	}

	threeOfAKind := false
	pair := false
	for _, rankCount := range ranksCountMap {
		if rankCount == 2 {
			pair = true
		}

		if rankCount == 3 {
			threeOfAKind = true
		}
	}
	return threeOfAKind && pair
}

func IsFlush(cards []Card) bool {
	allSameSuit := true
	suit := cards[0].Suit
	for _, card := range cards[1:] {
		if card.Suit != suit {
			allSameSuit = false
			break
		}
	}
	return allSameSuit
}

func isStraight(cards []Card) bool {
	slices.SortFunc(cards, func(a, b Card) int {
		return int(a.Rank - b.Rank)
	})

	if cards[len(cards)-1].Rank == Ace {
		cards = append([]Card{cards[len(cards)-1]}, cards...)
	}

	serialCount := 0
	for i := 0; i < len(cards)-1; i++ {
		if cards[i].Rank.NextRank() == cards[i+1].Rank {
			serialCount++
		} else {
			serialCount = 0
		}
	}

	return serialCount >= 4
}

func isThreeOfAKind(cards []Card) bool {
	ranksCountMap := make(map[CardRank]int, len(cards))
	for _, card := range cards {
		if _, ok := ranksCountMap[card.Rank]; !ok {
			ranksCountMap[card.Rank] = 0
		}
		ranksCountMap[card.Rank]++

		if ranksCountMap[card.Rank] >= 3 {
			return true
		}
	}
	return false
}

func isTwoPair(cards []Card) bool {
	ranksCountMap := make(map[CardRank]int, len(cards))
	for _, card := range cards {
		if _, ok := ranksCountMap[card.Rank]; !ok {
			ranksCountMap[card.Rank] = 0
		}
		ranksCountMap[card.Rank]++
	}

	pairs := 0
	for _, rankCount := range ranksCountMap {
		if rankCount == 2 {
			pairs++
		}
		if pairs >= 2 {
			return true
		}
	}
	return false
}

func isOnePair(cards []Card) bool {
	ranksMap := make(map[CardRank]struct{}, len(cards))
	for _, card := range cards {
		if _, ok := ranksMap[card.Rank]; ok {
			return true
		}
		ranksMap[card.Rank] = struct{}{}
	}
	return false
}
