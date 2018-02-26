"""Contains the parent class Interface."""


class Interface:
    """That class is a base class for the others interfaces."""

    def __init__(self):
        """Initialize the class."""
        self.go_to = ""
        self.name = NotImplemented

        self.connection = NotImplemented
        self.sprt = NotImplemented
        self.events = NotImplemented

        self._current_time = 0.0

    def start_events(self, event, mouse):
        """Call of event's module."""
        self._events.start(event, mouse)

    def update(self):
        """Update each sprite."""
        raise NotImplementedError

    def draw(self):
        """Draw the sprites."""
        raise NotImplementedError

    def transfer_datas(self, server_connection):
        """Collect and send datas from the server."""
        raise NotImplementedError

    def _secured_connection(transfer_datas):
        """Decorate and secure the datas transfers.

        If an OS error occure, go_to variable will be equal to 'main_menu',
        with -LosConnection's argument.
        """

        def wrapper(self):
            """Wrapp transfer_datas."""
            try:
                transfer_datas(self)
            except OSError as e:

                print(f"Failed connection.\nError: [e]")

                if self.name != 'main_menu':
                        self.go_to = 'main_menu -LostConnexion'

                self.connexion.close()

        return wrapper
    _secured_connection = staticmethod(_secured_connection)

    def _refresh_timer(self, set_zero=False):
        """Update the _current_time variable."""
        if set_zero:
            self._current_time = 0.0
            return

        self._current_time += 33.4

    def _is_timer_over(self, tenths_of_second):
        """Return True if _current_time is over tenths_of_seconds."""
        if self._current_time >= tenths_of_second:
            self.refresh_timer(set_zero=True)
            return True
        return False
