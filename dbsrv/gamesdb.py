#################################################
# Programmed in 2024 by github.com/Aurora-Beta  #
# No copyright usage intended, use as you like! #
#################################################

import chess
import lzma
import subprocess
from pathlib import Path


class gamesdb:
    """
    This class replaces the old tcscid stack by reading in a PGN file
    and CSV index files containing FENs with an offset in the PGN file.
    """
    initial_board_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    initial_board_offsets = [865, 1400, 2043, 3027, 3671]

    def __init__(self, pgn_filepath: str, index_folderpath: str) -> None:
        if Path(pgn_filepath).suffix == ".xz":
            self.pgn = lzma.open(pgn_filepath, "rt")
        else:
            self.pgn = open(pgn_filepath, "rt")

        self.index_white_path = Path(index_folderpath + "/" + "index.w.csv.gz")
        self.index_black_path = Path(index_folderpath + "/" + "index.b.csv.gz")
        self.grep_command = "zgrep"
        self.exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)

        self._reset_and_activate_search()

    def _reset_and_activate_search(self) -> None:
        print("Initial board positions. Resetting states for new game.")
        self.possible_game_offsets = []
        self.given_fens = []
        self.search_active = True

    def get_offsets_for_fen(self, given_fen: str) -> list:
        """Lookup the offsets for given FEN in the index."""

        # Chose the correct index per color
        color = given_fen.split(" ")[1]
        match color:
            case "w":
                index_filepath = self.index_white_path
            case "b":
                index_filepath = self.index_black_path

        # Do the index lookup
        p = subprocess.run(
            f"{self.grep_command} -F '{given_fen}' {index_filepath} | cut -d ';' -f2",
            capture_output=True, shell=True
        )

        # Output of subprocess has at least one line
        if len(p.stdout) > 0:
            # Read in the list
            result = eval(p.stdout.decode())
            if type(result) == list:
                return result

        # Fallback when incorrect or unknown FEN
        return []

    def get_pgn_for_index_nr(self, given_offset: int):
        self.pgn.seek(given_offset)
        return chess.pgn.read_game(self.pgn)


    def lookup_games_by_fen(self, given_fen: str) -> list:
        """
            Returns a list of five dicts containing infos and PGN of games
            matching the moves of the current game.
        """

        # New game as the given FEN before the first move of white
        # on a new board.
        if given_fen == self.initial_board_fen:
            self._reset_and_activate_search()

        # Append the given FEN
        self.given_fens.append(given_fen)

        # Retrieve the offsets for given FEN
        if self.search_active:
            retrieved_offsets = self.get_offsets_for_fen(given_fen)

            # Performance optimization for the initial board
            if len(self.given_fens) == 1:
                retrieved_offsets = self.initial_board_offsets

        else:
            retrieved_offsets = []

        # Deactivate the search and processing of retrieved offsets
        # until a new game has been started.
        if not retrieved_offsets:
            self.search_active = False

        # Search for five games that contain the movements
        # of the current game
        if self.search_active:
            if len(self.given_fens) in [1, 2]:
                # Set initial offsets after the first move of white
                self.possible_game_offsets = retrieved_offsets
            else:
                # Filter out offsets not associated with current FEN
                new_offsets = []
                for element in retrieved_offsets:
                    if element in self.possible_game_offsets:
                        new_offsets.append()
                self.possible_game_offsets = new_offsets

        target_list = []

        for offset in self.possible_game_offsets[:5]:
            target_dict = {}
            game = self.get_pgn_for_index_nr(offset)

            name_white = game.headers.get("White", "")
            name_black = game.headers.get("Black", "")
            elo_white = game.headers.get("WhiteElo", "")
            elo_black = game.headers.get("BlackElo", "")
            event = game.headers.get("Event", "")
            year = str(game.headers.get("Date", "")).split(".")[0]

            field_white = f"{name_white} ({elo_white})"
            field_black = f"{name_black} ({elo_black})"
            field_event = f"{year}, {event}"

            target_dict = {
                "white": field_white,
                "black": field_black,
                "result": game.headers.get("Result", ""),
                "event": field_event,
                "pgn": str(game.accept(self.exporter))
            }

            target_list.append(target_dict)

        return target_list