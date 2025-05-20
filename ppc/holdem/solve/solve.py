from pwn import *

rank_mapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

class Card:
    def __init__(self, rank: str, suit: str):
        if rank.isnumeric():
            self.rank = int(rank)
        else:
            self.rank = rank_mapping[rank]

        self.suit = suit

def is_royal_flush(cards: list[Card]) -> bool:
    return cards[-1].rank == 14 and is_straight_flush(cards)

def is_straight_flush(cards: list[Card]) -> bool:
    return is_straight(cards) and is_flush(cards)

def is_four_of_a_kind(cards: list[Card]) -> bool:
    rank_counts = {}
    for card in cards:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        if rank_counts[card.rank] >= 4:
            return True
    return False

def is_full_house(cards: list[Card]) -> bool:
    rank_counts = {}
    for card in cards:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

    has_three = False
    has_pair = False
    for count in rank_counts.values():
        if count == 3:
            has_three = True
        elif count == 2:
            has_pair = True
    return has_three and has_pair

def is_flush(cards: list[Card]) -> bool:
    suit = cards[0].suit
    return all(card.suit == suit for card in cards[1:])

def is_straight(cards: list[Card]) -> bool:
    sorted_cards = sorted(cards, key=lambda c: c.rank)
    ranks = [card.rank for card in sorted_cards]

    # Handle Ace-low straight case
    if ranks[-1] == 14:
        ranks.insert(0, 1)

    serial_count = 0
    for i in range(len(ranks)-1):
        if ranks[i] + 1 == ranks[i+1]:
            serial_count += 1
        else:
            serial_count = 0
        if serial_count >= 4:
            return True
    return False

def is_three_of_a_kind(cards: list[Card]) -> bool:
    rank_counts = {}
    for card in cards:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        if rank_counts[card.rank] >= 3:
            return True
    return False

def is_two_pair(cards: list[Card]) -> bool:
    rank_counts = {}
    for card in cards:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

    pairs = 0
    for count in rank_counts.values():
        if count == 2:
            pairs += 1
            if pairs >= 2:
                return True
    return False

def is_one_pair(cards: list[Card]) -> bool:
    seen_ranks = set()
    for card in cards:
        if card.rank in seen_ranks:
            return True
        seen_ranks.add(card.rank)
    return False


def solve(r: tube):
    while True:
        print(r.recvuntil(b"[").decode('utf-8'), end="")
        print(r.recvline().decode('utf-8'), end="")

        r.recvuntil(b"Flop:")
        flop = r.recvline().decode('utf-8').strip().split(" ")

        r.recvuntil(b"Turn:")
        turn = r.recvline().decode('utf-8').strip()

        r.recvuntil(b"River:")
        river = r.recvline().decode('utf-8').strip()

        print(f"Flop: {flop}\nTurn: {turn}\nRiver: {river}")

        cards = [Card(c[0], c[1]) for c in flop + [turn,] + [river,]]

        comb = b"HIGH CARD"
        if is_royal_flush(cards):
            comb = b"ROYAL FLUSH"
        elif is_straight_flush(cards):
            comb = b"STRAIGHT FLUSH"
        elif is_four_of_a_kind(cards):
            comb = b"FOUR OF A KIND"
        elif is_full_house(cards):
            comb = b"FULL HOUSE"
        elif is_flush(cards):
            comb = b"FLUSH"
        elif is_straight(cards):
            comb = b"STRAIGHT"
        elif is_three_of_a_kind(cards):
            comb = b"THREE OF A KIND"
        elif is_two_pair(cards):
            comb = b"TWO PAIR"
        elif is_one_pair(cards):
            comb = b"ONE PAIR"


        print(comb.decode('utf-8'))
        r.sendline(comb)


if __name__ == "__main__":
    cli = remote("localhost", 10315)

    try:
        with cli:
            solve(cli)
    except Exception as e:
        print("error:", e.__class__.__name__, e)
    finally:
        cli.interactive()
