import Card as Card
import copy

class ResultCalculator:

    result_rank = ["JUMBO Five Gong", "Niu Dong Gu", "Pair Ace", "Pair King", "Pair Queen", "Pair Jack", 
                   "Pair 10", "Pair 9", "Pair 8", "Pair 7", "Pair 6", "Pair 5", "Pair 4", "Pair 3", "Pair 2", 
                   "Niu 10", "Niu 9", "Niu 8", "Niu 7", "Niu 6", "Niu 5", "Niu 4", "Niu 3", "Niu 2", "Niu 1", "No Niu found"]

    def calculate_result(self, cards):
        # now the 3 and 6 can interchange
        # generate all possible combinations of the cards
        original_result, threeCardIndex, twoCardIndex = self.calculate(cards)

        other_possible_combinations = self.generate_combinations(cards)
        best_result = original_result
        bestThreeCard = [cards[i] for i in threeCardIndex]
        bestTwoCard = [cards[i] for i in twoCardIndex]
        ## only consider other result when it is worse than Niu 10
        if self.result_rank.index(original_result) <= self.result_rank.index("Niu 10"):
            return best_result, bestThreeCard, bestTwoCard
        
        bestThreeCardIndex, bestTwoCardIndex = threeCardIndex, twoCardIndex
        for combination in other_possible_combinations:
            result, threeCardIndex, twoCardIndex = self.calculate(combination)
            if self.result_rank.index(result) < self.result_rank.index(best_result):
                best_result, bestThreeCardIndex, bestTwoCardIndex = result, threeCardIndex, twoCardIndex
                bestThreeCard = [combination[i] for i in bestThreeCardIndex]
                bestTwoCard = [combination[i] for i in bestTwoCardIndex]
        return best_result, bestThreeCard, bestTwoCard


    def generate_combinations(self, cards):
        def helper(cards, index, current_combination, results):
            # Generate all possible combinations of the cards
            if current_combination is None:
                current_combination = copy.copy(cards)  # Start with the original combination
            # Ensure current combination is sorted before converting to tuple for results
            sorted_combination = sorted(current_combination)
            # print(sorted_combination)
            results.add(tuple(sorted_combination))

            for i in range(index, len(cards)):
                # Only swap if the current card is a 3 or a 6
                if cards[i].value() in (3, 6):
                    swapped_rank = Card.Card('6', cards[i].suit) if cards[i].value() == 3 else Card.Card('3', cards[i].suit)
                    # Create a new combination for this specific swap
                    new_combination = current_combination.copy()
                    new_combination[i] = swapped_rank
                    # Recurse with the new combination
                    helper(cards, i + 1, new_combination, results)

        # Initial call to helper with empty results set
        results = set()
        helper(cards, 0, None, results)

        # Convert each tuple in results back to a sorted list
        return [list(combination) for combination in sorted(results)]
        
    def calculate(self, cards):
        # Return the calculated result
        # Assume that there are 5 cards
        result = ""

        # if all 5 cards are high cards, return JUMBO Five Gong!
        if all(card.rank in ['Jack', 'Queen', 'King'] for card in cards):
            return "JUMBO Five Gong", [0, 1, 2, 3, 4], []

        # check if the Ace of Spades is in the hand
        hasAcespades = False
        #high cards means Jack, Queen, King
        hasJQK = False
        for card in cards:
            if card.rank == 'Ace' and card.suit == 'Spades':
                hasAcespades = True
        if any(card.rank in ['Jack', 'Queen', 'King'] for card in cards):
            hasJQK = True
        values = [card.value() for card in cards]
        print(values)
        # check if any sum of 3 cards is 10, 20 or 30
        isValidNiu = False
        possiblethreeCardSum = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    if values[i] + values[j] + values[k] in [10, 20, 30]:
                        possiblethreeCardSum.append([i, j, k])
                        isValidNiu = True
        bestThreeCardIndex = []
        if isValidNiu:
            # find the remaining 2 cards
            best_score = 0
            for threeCardSum in possiblethreeCardSum:
                twoCards = [values[i] for i in range(5) if i not in threeCardSum]
                twoCardsRank = [cards[i].rank for i in range(5) if i not in threeCardSum]

                # Niu Dong Gu means one card is highCard and the other is Ace of Spades
                # print(hasAcespades, hasHighCard, twoCards)
                if hasAcespades and hasJQK and 1 in twoCards and 10 in twoCards:
                    bestThreeCardIndex = threeCardSum
                    result = "Niu Dong Gu"
                    break

                # check if twoCards has the same rank, return Pair x
                if len(set(twoCardsRank)) == 1:
                    bestThreeCardIndex = threeCardSum
                    result = f"Pair {twoCardsRank[0]}"
                    break
                
                # find the best score
                score = sum(twoCards) % 10
                if score % 10 == 0:
                    best_score = 10
                best_score = max(best_score, score)
                bestThreeCardIndex = threeCardSum
                result = f"Niu {best_score}"
        else:
            result = "No Niu found"
        bestTwoCardIndex = [i for i in range(5) if i not in bestThreeCardIndex]
        return (result, bestThreeCardIndex, bestTwoCardIndex)
    
#Testing the ResultCalculator
# cards1 = [Card.Card('Ace', 'Spades'), Card.Card('Jack', 'Hearts'), Card.Card('3', 'Clubs'), Card.Card('4', 'Diamonds'), Card.Card('3', 'Spades')]
# print(ResultCalculator().calculate_result(cards1))  # Expected output: Niu Dong gu

# cards2 = [Card.Card('Ace', 'Spades'), Card.Card('King', 'Hearts'), Card.Card('Ace', 'Club'), Card.Card('9', 'Diamonds'), Card.Card('10', 'Spades')]
# print(ResultCalculator().calculate_result(cards2))  # Expected output: Niu Dong gu




cards3 = [Card.Card('6', 'Spades'), 
          Card.Card('4', 'Hearts'), 
          Card.Card('3', 'Club'), 
          Card.Card('10', 'Diamonds'), 
          Card.Card('Jack', 'Spades')]
print(ResultCalculator().calculate_result(cards3))  # Expected output: Niu Dong gu