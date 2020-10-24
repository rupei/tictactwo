import copy

class TenToZeroByOneOrTwo:

    def do_move(self, position, move):
        return position - move

    def generate_moves(self, position):
        if position == 0:
            return set()
        if position == 1:
            return {1}
        return {1, 2}

    def primitive_value(self, position):
        # 0 is not primitive, 1 is lose, 2 is win (N/A in this game)
        if position == 0:
            return 1
        return 0

class TwentyFiveToZeroByOneOrThreeOrFour:

    def do_move(self, position, move):
        return position - move

    def generate_moves(self, position):
        if position == 0:
            return set()
        if position < 3:
            return {1}
        if position < 4:
            return {1, 3}
        return {1, 3, 4}

    def primitive_value(self, position):
        # 0 is not primitive, 1 is lose, 2 is win (N/A in this game)
        if position == 0:
            return 1
        return 0

class TicTacToe:

    def _get_player_to_move(self, position):
        moves = 0
        for i in range(3):
            for j in range(3):
                moves += position[i][j]
        if moves == 1:
            return -1
        elif moves == 0:
            return 1
        else:
            raise ValueError("position is not valid")

    def do_move(self, position, move):
        """
        Args:
            position: a 2D tuple of shape (3, 3) that defines the board. 1 and -1
              define moves played by each player. Player '1' goes first. 0
              denotes an empty space.
            move: a tuple that denotes the coordinate of the move to be played.
        """
        position = list(list(r) for r in position)
        position[move[0]][move[1]] = self._get_player_to_move(position)
        return tuple(tuple(r) for r in position)

    def generate_moves(self, position):
        all_moves = set()
        for i in range(3):
            for j in range(3):
                if position[i][j] == 0:
                    all_moves.add((i, j))
        return all_moves

    def primitive_value(self, position):
        # 0 is not primitive, 1 is lose, 2 is win, 3 is tie
        rows = {}
        cols = {}
        zero_diag = 0  # diag that starts at (0, 0)
        two_diag = 0  # diag that starts at (0, 2)
        for i in range(3):
            for j in range(3):
                rows[i] = rows.get(i, 0) + position[i][j]
                cols[j] = cols.get(j, 0) + position[i][j]
                if i == j:
                    zero_diag += position[i][j]
                if i + j == 2:
                    two_diag += position[i][j]
        return self._check_for_win(
            self._get_player_to_move(position),
            len(self.generate_moves(position)),
            rows.values(), cols.values(), (zero_diag,), (two_diag,))

    def _check_for_win(self, parity, moves_left, *args):
        for arg in args:
            for val in arg:
                if val == parity * 3:
                    return 2
                elif val == -parity * 3:
                    return 1
        if moves_left == 0:
            return 3

    def get_symmetric_positions(self, position):
        all_positions = [position]
        cpy = list([r for r in position])
        cpy[0], cpy[2] = cpy[2], cpy[0]
        all_positions.append(tuple(tuple(r) for r in cpy))
        for _ in range(3):
            cpy = list([r for r in position])
            for r in range(3):
                cpy[r] = [position[i][r] for i in range(2, -1, -1)]
            all_positions.append(tuple(tuple(r) for r in cpy))
            position = copy.deepcopy(cpy)
            cpy[0], cpy[2] = cpy[2], cpy[0]
            all_positions.append(tuple(tuple(r) for r in cpy))
        return all_positions

class TicTacTwo:

    def __init__(self):
        self.all_possible_moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    def _get_player_to_move(self, position):
        return position[0]

    def do_move(self, position, move):
        """
        Args:
            position: a 2D tuple of shape (3, 3) that defines the board. 1 and -1
              define moves played by each player. Player '1' goes first. 0
              denotes an empty space.
            move: a tuple of a tuple that denotes the coordinate of the move, a int representing how many
        """
        board = position[3]
        board = list(list(r) for r in board)
        to_move = self._get_player_to_move(position)
        for m in move:
            old_val = board[m[0]][m[1]]
            board[m[0]][m[1]] = (old_val[0] + to_move, old_val[1] + 1)
        new_board = tuple(tuple(r) for r in board)
        if to_move == -1:
            return -1 * position[0], len(move) != 2 and position[1], position[2], new_board
        else:
            return -1 * position[0], position[1], len(move) != 2 and position[2], new_board

    def generate_moves(self, position):
        all_moves = set()
        board = position[3]
        player = position[0]
        if position[0] == -1:
            double_left = position[1]
        else:
            double_left = position[2]
        for i, j in self.all_possible_moves:
            # single move
            if board[i][j][1] < 3 and abs(board[i][j][0]) < 2:
                all_moves.add(((i, j),))
            # double moves in same position
            if double_left:
                if (board[i][j][0] == 0 or board[i][j][0] == player * -1) and board[i][j][1] < 2:
                    all_moves.add(((i, j),(i, j)))
        if not double_left:
            return all_moves
        for k, (a, b) in enumerate(self.all_possible_moves):
            for l, (c, d) in enumerate(self.all_possible_moves):
                # double moves that aren't in the same position
                if k < l:
                    if abs(board[a][b][0]) < 2 and board[a][b][1] < 3 and abs(board[c][d][0]) < 2 and board[c][d][1] < 3:
                        all_moves.add(((a, b), (c, d)))
        return all_moves
        '''                # double move
                        if ((i, j), (l, k)) in all_moves or ((l, k), (i, j)) in all_moves:
                            continue
                        if i == l and j == k:
                            if 
                if double_left:
                    if board[i][j][1] < 2:
                        all_moves.add(((i, j), (i, j)))
                    # this is incorrect
                    for l in range(3):
                        for k in range(3):
                            if j == k and i == l:
                                continue
                            if board[i][j][1] < 3 and board[l][k][1] < 3:
                                if ((i, j), (l, k)) not in all_moves and ((l, k), (i, j)) not in all_moves:
                                    all_moves.add(((i, j), (l, k)))

        return all_moves'''

    def primitive_value(self, position):
        # 0 is not primitive, 1 is lose, 2 is win, 3 is tie
        rows = {}
        cols = {}
        zero_diag = 0  # diag that starts at (0, 0)
        two_diag = 0  # diag that starts at (0, 2)
        board = position[3]
        for i in range(3):
            for j in range(3):
                rows[i] = rows.get(i, 0) + self._check_owner(board[i][j])
                cols[j] = cols.get(j, 0) + self._check_owner(board[i][j])
                if i == j:
                    zero_diag += self._check_owner(board[i][j])
                if i + j == 2:
                    two_diag += self._check_owner(board[i][j])
        return self._check_for_win(
            self._get_player_to_move(position),
            len(self.generate_moves(position)),
            rows.values(), cols.values(), (zero_diag,), (two_diag,))

    def _check_owner(self, pos):
        if pos[0] == 2:
            return 1
        elif pos[0] == -2:
            return -1
        if pos[1] == 3:
            return 1 if pos[0] > 0 else -1
        return 0

    def _check_for_win(self, parity, moves_left, *args):
        # return of 1 is lose, 2 is win, 3 is a tie
        for arg in args:
            for val in arg:
                if val == parity * 3:
                    return 2
                elif val == -parity * 3:
                    return 1
        if moves_left == 0:
            return 3

    def get_symmetric_positions(self, position):
        board = position[3]
        all_boards = [board]
        cpy = list([r for r in board])
        cpy[0], cpy[2] = cpy[2], cpy[0]
        all_boards.append(tuple(tuple(r) for r in cpy))
        for _ in range(3):
            cpy = list([r for r in board])
            for r in range(3):
                cpy[r] = [board[i][r] for i in range(2, -1, -1)]
            all_boards.append(tuple(tuple(r) for r in cpy))
            board = copy.deepcopy(cpy)
            cpy[0], cpy[2] = cpy[2], cpy[0]
            all_boards.append(tuple(tuple(r) for r in cpy))
        return all_boards