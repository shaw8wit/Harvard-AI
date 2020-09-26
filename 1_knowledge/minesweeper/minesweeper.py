import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        """
        Checks if the cell has a mine
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:

            # decreasing the mine count
            self.count -= 1

            # removing the cell from available cells
            self.cells.remove(cell)
            return 1

        return 0

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:

            # removing the cell from available cells
            self.cells.remove(cell)
            return 1

        return 0


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        count = 0
        self.mines.add(cell)
        for sentence in self.knowledge:
            count += sentence.mark_mine(cell)

        return count

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        count = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            count += sentence.mark_safe(cell)

        return count

    def update_state(self):
        """
        Iteratively pdates the state[safe/mine] of cells of the board at its current state
        """
        count = 1
        while count:
            count = 0
            for sentence in self.knowledge:

                # mark cell as safe if a sentence knows it to be safe
                for cell in sentence.known_safes():
                    self.mark_safe(cell)
                    count += 1

                # mark a cell as mine if a sentence knows it to be a mine
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
                    count += 1

            # if cell state is present in the current board mark it accordingly
            for cell in self.safes:
                count += self.mark_safe(cell)
            for cell in self.mines:
                count += self.mark_mine(cell)

    def get_inference(self):
        """
        returns the inference that can be made with the knowledge that is currently known
        """

        inferences = []
        to_remove = []

        for first_s in self.knowledge:

            # if the sentence is empty mark to remove
            if len(first_s.cells) == 0:
                to_remove.append(first_s)
                continue

            for second_s in self.knowledge:

                # if the sentence is empty mark to remove
                if len(second_s.cells) == 0:
                    to_remove.append(second_s)
                    continue

                if second_s != first_s:

                    # inference can be made if one sentence is a subset of another
                    if(second_s.cells.issubset(first_s.cells)):
                        new_cells = first_s.cells.difference(second_s.cells)
                        new_count = first_s.count - second_s.count
                        new_inference = Sentence(new_cells, new_count)

                        # add inference if its not already known
                        if new_inference not in self.knowledge:
                            inferences.append(new_inference)

        # apply the changes to the original knowledge
        self.knowledge = [x for x in self.knowledge if x not in to_remove]
        return inferences

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1 :
        self.moves_made.add(cell)

        # 2 :
        self.mark_safe(cell)
        i, j = cell

        # generate surrounding cells
        surrounding_cells = set()
        for row in range(max(i-1, 0), min(i+2, self.height)):
            for col in range(max(j-1, 0), min(j+2, self.width)):
                if (row, col) != (i, j):
                    surrounding_cells.add((row, col))

        # 3 :
        self.knowledge.append(Sentence(surrounding_cells, count))
        while True:

            # 4 :
            self.update_state()
            new_inferences = self.get_inference()

            # if no new inferences can be made then exit loop
            if len(new_inferences) == 0:
                break

            # 5 :
            for sentence in new_inferences:
                self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        invalid_moves = self.moves_made.union(self.mines)
        for move in self.safes:
            if move not in invalid_moves:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        invalid_moves = self.moves_made.union(self.mines)

        # getting random start positions
        row_traversal = range(self.height) if random.randint(
            0, 1) else range(self.height-1, -1, -1)
        col_traversal = range(self.width) if random.randint(
            0, 1) else range(self.width-1, -1, -1)
        for row in row_traversal:
            for col in col_traversal:
                move = (row, col)

                # if current move is not invalid then AI can make that move
                if move not in invalid_moves:
                    return move

        # if no moves are valid return none
        return None
