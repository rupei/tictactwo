import games  # module with games

# game = games.TenToZeroByOneOrTwo()
game = games.TicTacTwo()
analysis = {}
count = 0

def solve(position, symmetry_removal=False):
    # return of 1 is lose, 2 is win, 3 is a tie
    # `game` is any game object that follows the API spec of a game.
    # returns a tuple with semantics (value, remoteness)
    def memo_solve(position, memo):
        global count
        if symmetry_removal:
            symmetrical_positions = game.get_symmetric_positions(position)
            for pos in symmetrical_positions:
                if pos in memo:
                    return memo[pos]
        elif position in memo:
            return memo[position]
        if game.primitive_value(position):
            count += 1
            if count % 10000 == 0:
                print(count)
            val = game.primitive_value(position)
            memo[position] = (val, 0)
            analysis[0] = analysis.get(0, []) + [val]
            return game.primitive_value(position), 0
        tie = False
        win = False
        child_remoteness = []
        print(len(game.generate_moves(position)))
        return
        for move in game.generate_moves(position):
            value, remoteness = memo_solve(game.do_move(position, move), memo)
            if value == 1:
                win = True
            if value == 3:
                tie = True
            child_remoteness.append((value, remoteness))
        if win:
            memo[position] = (
                2,
                min([val[1] for val in child_remoteness if val[0] == 1]) + 1)
            analysis[memo[position][1]] = analysis.get(memo[position][1], []) + [2]
        elif tie:
            memo[position] = (
                3,
                max([val[1] for val in child_remoteness]) + 1)
            analysis[memo[position][1]] = analysis.get(memo[position][1], []) + [3]
        else:
            memo[position] = (
                1,
                max([val[1] for val in child_remoteness]) + 1)
            analysis[memo[position][1]] = analysis.get(memo[position][1], []) + [1]
        return memo[position]
    return memo_solve(position, memo={})


# starting_pos = 10
starting_pos = (-1, True, True, (((2, 2), (3, 3), (0, 0)), ((0, 0), (0, 0), (0, 0)), ((0, 0), (0, 0), (0, 0))))
solve(starting_pos, symmetry_removal=True)
print("Remote  Win     Lose    Tie     Total")
gap = "       "
total_wins = total_losses = total_ties = 0
for k in sorted(analysis.keys(), reverse=True):
    v = analysis[k]
    wins = losses = ties = 0
    for val in v:
        if val == 1:
            losses += 1
        elif val == 2:
            wins += 1
        elif val == 3:
            ties += 1
    total_wins += wins
    total_losses += losses
    total_ties += ties
    print(
        str(k) + gap + str(wins) + gap + str(losses) + gap + str(ties) +
        gap + str(wins + losses + ties))
print("Total   {}       {}       {}       {}".format(
    total_wins, total_losses, total_ties, total_wins + total_losses + total_ties))


