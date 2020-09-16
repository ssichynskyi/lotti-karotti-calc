# -*- coding: utf-8 -*-


class PlayFieldCell:
    """
    A cell of a play field. Represents a node of a singly linked list
    """
    def __init__(self, number: int, is_hole=False, is_winning_cell=False):
        self.number = number
        self._is_hole = is_hole
        self._is_winning_cell = is_winning_cell
        self._next = None

    @property
    def next(self):
        """
        Access to the next cell on a play field
        """
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    @property
    def is_hole(self) -> bool:
        """
        :return: True if cell is a hole, False in other case
        """
        return self._is_hole

    @is_hole.setter
    def is_hole(self, value: bool):
        self._is_hole = value

    @property
    def is_winning_cell(self) -> bool:
        """
        :return: True if cell is winning cell, False in other case
        note: there's only one winning cell, the last one
        """
        return self._is_winning_cell

    @is_winning_cell.setter
    def is_winning_cell(self, value: bool):
        self._is_winning_cell = value


class PlayField:
    """
    Represents a play field of the game which consists of a given
    number of PlayFieldCells
    """
    def __init__(self, number_of_cells: int, holes: [int]):
        """
        PlayField class constructor
        :param number_of_cells: total number of cells on play field,
        excluding the default 0-field.
        The last field automatically becomes a winning cell
        :param holes: array of cell numbers that represent possible
        holes. 0-element of this array becomes an active hole at the
        beginning of the game.
        """
        self._initial_holes_list = holes
        self._holes = holes
        # play field cell with number 0 is a starting point, out of the field
        self._cell_list = []
        self._create_cells(number_of_cells)
        # last cell on a play field is always a winning one
        self._cell_list[-1].is_winning_cell = True
        # set first active hole
        self._set_hole(self._holes[0])

    def _create_cells(self, number_of_cells: int) -> None:
        """
        Creates list of cells for a play field
        :param number_of_cells: number of cells on a play field.
        0th element is a starting position out of the play field
        :return: None
        """
        last_cell = None
        for i in range(number_of_cells + 1):
            new_cell = PlayFieldCell(i)
            self._cell_list.append(new_cell)
            if last_cell:
                last_cell.next = new_cell
            last_cell = new_cell

    @property
    def cells(self) -> [PlayFieldCell]:
        """
        All cells on a play field. Fast access to a linked list
        :return: list of play field cells
        """
        return self._cell_list

    @property
    def holes(self) -> [int]:
        """
        All possible holes on a play field
        :return: list of holes
        """
        return self._holes

    @property
    def starting_cell(self) -> PlayFieldCell:
        """
        Access to a starting cell (default out-of-the-play field location)
        :return: PlayFieldCell which is the starting position
        """
        return self._cell_list[0]

    @property
    def winning_cell(self) -> PlayFieldCell:
        """
        Access to a winning cell
        :return: PlayFieldCell which is last cell on a play field
        """
        return self._cell_list[-1]

    def reset_condition(self) -> None:
        """
        Resets condition of a play field to a default
        :return: None
        """
        for cell in self.cells:
            cell.is_hole = False
        self._holes = self._initial_holes_list
        self._set_hole(self._holes[0])

    def _set_hole(self, cell_number: int) -> None:
        """
        makes a hole in a play field
        :param cell_number: number of cell to turn into a hole
        :return: None
        """
        for cell in self.cells:
            cell.is_hole = False
        try:
            cell_to_become_hole = self._cell_list[cell_number]
        except IndexError:
            # handle the case when there're no holes on a play field
            return
        cell_to_become_hole.is_hole = True
        print(f'Cell #{cell_to_become_hole.number} turns into a hole!')

    def rotate_carrot(self, shift: int) -> None:
        """
        Changes the position of holes "shift" times
        :return: None
        """
        for _ in range(shift):
            self._holes = self._holes[1:] + self._holes[:1]
            self._set_hole(self._holes[0])
