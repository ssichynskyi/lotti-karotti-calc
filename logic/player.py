# -*- coding: utf-8 -*-


class Rabbit:
    """
    Class describes player's chip
    """
    def __init__(self, number: int, player_id: int):
        """
        Initializes the rabbit with the given number (id)
        for a given player
        :param number: number / id of the rabbit
        :param player_id: object of Player class
        """
        self._number = number
        self._player_id = player_id

    @property
    def number(self) -> int:
        """
        Number / id of the rabbit
        :return: integer, the number/id of a rabbit
        """
        return self._number

    @property
    def player_id(self):
        """
        The player whom this rabbit belongs to
        :return: instance of the Player class
        """
        return self._player_id

    def __hash__(self):
        # required in order to use this object as a key in dict
        return hash((self._number, self._player_id))

    def __eq__(self, candidate):
        # required in order to use this object as a key in dict
        return (self._number, self._player_id) == (candidate.number, candidate.player_id)

    def __ne__(self, candidate):
        return not self == candidate


class NewPlayerGenerator:
    """
    Generator which is responsible for the creation of a new Players
    """
    def __init__(self, rabbits, max_index, starting_index=1):
        self._max_index = max_index
        self._index = starting_index
        self._rabbits = rabbits

    def __iter__(self):
        while self._index <= self._max_index:
            yield Player(self._index, self._rabbits)
            self._index += 1


class Player:
    """
    Describes a player
    """
    def __init__(self, player_id, rabbits, active_rabbits=0, lost_rabbits=0):
        """
        initializes the object of a Player class
        :param player_id: ID of the player (1...).
        :param rabbits: how many chips each player has
        :param active_rabbits: number of rabbits on the play field
        :param lost_rabbits: rabbits that were lost
        """
        if active_rabbits + lost_rabbits > rabbits:
            raise ValueError('rabbits param shall be >= active_rabbits + lost_rabbits params')
        self._id = player_id
        # player's rabbits that have been already lost in a game
        self._lost_rabbits = [
            Rabbit(rabbit_id, self._id)
            for rabbit_id in range(1, lost_rabbits + 1)
        ]
        # player's active rabbits are in a game
        self._active_rabbits = [
            Rabbit(i, self._id)
            for i in range(lost_rabbits + 1, lost_rabbits + active_rabbits + 1)
        ]
        # player's rabbits that are ready for a game
        self._ready_rabbits = [
            Rabbit(i, self._id)
            for i in range(lost_rabbits + active_rabbits + 1, rabbits + 1)
        ]

    @property
    def id(self):
        """
        Player's ID.
        :return: player's id / number.
        """
        return self._id

    @property
    def lost_rabbits(self) -> [Rabbit]:
        """
        Access to the player's lost rabbits (game chips)
        :return: list of objects of the Rabbit class
        """
        return self._lost_rabbits

    @property
    def active_rabbits(self) -> [Rabbit]:
        """
        Access to the player's active rabbits (game chips)
        :return: list of objects of the Rabbit class
        """
        return self._active_rabbits

    @property
    def ready_rabbits(self) -> [Rabbit]:
        """
        Access to the player's ready rabbits (game chips)
        :return: list of objects of the Rabbit class
        """
        return self._ready_rabbits

    @property
    def is_active(self) -> bool:
        """
        The activity status of the player. True - active,
        False - inactive. 'Inactive' means that player had already
        lost the current game
        :return: True if player is active, False in other case
        """
        return len(self._active_rabbits) + len(self._ready_rabbits) > 0

    def reset_condition(self) -> None:
        """
        Reset player's conditions to the default values:
        player status turns to active
        all rabbits
        :return: None
        """
        used_rabbits = self._lost_rabbits + self._active_rabbits
        while len(used_rabbits) > 0:
            self._ready_rabbits.insert(0, used_rabbits.pop())
            self._lost_rabbits = []
            self._active_rabbits = []

    def get_active_rabbit(self) -> Rabbit or None:
        """
        Gets active rabbit if there's one. If not, searches for
        rabbits that could be turned into the "active" state
        and returns the next one in the list
        :return: active Rabbit or None
        """
        if len(self._active_rabbits) > 0:
            return self._active_rabbits[0]
        if len(self._ready_rabbits) > 0:
            rabbit = self._ready_rabbits.pop(0)
            self._active_rabbits.append(rabbit)
            print(f'Player #{self._id} picks rabbit #{rabbit.number}')
            return rabbit
        return None

    def drop_active_rabbit(self) -> None:
        """
        Drops active rabbit. By default this happens when
        rabbit falls in the hole
        :return: None
        """
        rabbit = self._active_rabbits.pop()
        self._lost_rabbits.append(rabbit)
        print(f'Rabbit #{self._id}.{rabbit.number} falls into a hole!')
