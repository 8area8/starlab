"""Game initiator."""

from f_roboc.interface import Interface
import constants.find as fd


class GameInitiator(Interface):
    """Initialize the game."""

    def __init__(self, connection, _map=None, nb_players=0, hote=False):
        """Initialize the class."""
        super().__init__()

        # CONNECTIONS VARIABLES
        self.connection = connection
        self.hote = hote
        self._orders = ""

        # PLAYERS INFORMATION
        self.active_turn = 0
        self.player_digit = 0
        self.nb_players = nb_players
        self.players = []

        # PROGRESS VARIABLE
        self.__step = 1

        # GAME'S MAP
        self._map = _map

    @property
    def _step(self):
        """Unused 'get' property."""
        return self.__step

    @_step.setter
    def _step(self, value):
        """Just a print who advertise me when self.__step changes."""
        self.__step = value
        print("step is now ", self._step)

    def start_events(self, event, mouse):
        """Start the events."""
        pass

    @Interface._secured_connection
    def transfer_datas(self):
        """Data communication."""
        if self._step == 1:
            self._get_or_send_map_and_nb_players()

        elif self._step == 2:
            self._wait_for_all_players()

        elif self._step == 3:
            self._define_players()

        elif self._step == 4:
            self.go_to = 'game'

    def update(self):
        """Update the sprites."""
        pass

    def draw(self):
        """Draw the sprites."""
        pass

    def _get_or_send_map_and_nb_players(self):
        """Get or send the map and the number of players.

        if you are the hote, you will send these informations.
        Else, you will wait for these.
        """
        if self.hote:
            self._send_map_and_nb_players()
        else:
            self._wait_map_and_nb_players()

    def _send_map_and_nb_players(self):
        """Send the map content and the number of players."""
        string_map = 'Q'.join(["".join(line) for line in self._map])

        msg = f"nb_players:{self.nb_players} map:{string_map}"

        self.connection.send(msg)
        self._step = 2

    def _wait_map_and_nb_players(self):
        """Wait for the map and the number of players."""
        msg = self.connection.receive()

        if 'map:' not in msg:
            self.connection.send('need_map')

        else:
            # convert the map string into a valid map list.
            self._map = fd.find_text_after('map:', msg).split("Q")
            self._map = [list(line) for line in self._map]

            print('Game informations received.')
            print('map received:\n', self._map)
            self._step = 2

    def _wait_for_all_players(self):
        """Wait for new game's connections.

        when the server has all its players, it send:
        - the player's number
        - the active turn
        - the number of players.
        """
        msg = self.connection.receive()

        if "players_infos_ok:" in msg:
            self.player_digit = fd.find_number_after('player_digit:', msg)
            self.active_turn = fd.find_number_after("active_turn:", msg)
            self.nb_players = fd.find_number_after("nb_players:", msg)

            self.connection.send('synchro_ok')
            self._step = 3

        else:
            self.connection.send('players_informations?')

    def _define_players(self):
        """Define the players lists if 'players_list in msg.

        We create one list per player, who contains his:
        - digit
        - name (and type)
        - membership
        - spawn
        """
        msg = self.connection.receive()

        if 'players_list:' not in msg:
            return

        for i in range(self.nb_players):
            i += 1

            is_yours = True if self.player_digit == i else False
            name = 'superstar' if i == 1 else 'superalien'

            spawn = fd.find_and_get_coords_after(f"player{i}_place:", msg)
            print("dans g_i. spawn du joueur: ", spawn)

            self.players.append([i, name, is_yours, spawn])

        self._step = 4
