#################################################
# Programmed in 2024 by github.com/Aurora-Beta  #
# No copyright usage intended, use as you like! #
#################################################

# public modules
import argparse
import bottle
import json
from bottle import request  as bt_request
from bottle import response as bt_response
from pathlib import Path

# local modules
import chess
import chess.polyglot
import chess.pgn
import gamesdb

#
# Functions
#

def openingbook_lookup(given_fen: str) -> list:
    """Returns a list of dicts of possible moves for given FEN"""
    target_list = list()
    board = chess.Board(fen=given_fen)

    with chess.polyglot.open_reader(args.book) as reader:
        for entry in reader.find_all(board):
            target_list.append(
                {
                    "move": str(entry.move),
                    "whitewins":int(entry.weight),
                    "draws": int(entry.learn),
                    "blackwins":(100 - int(entry.weight) - int(entry.learn)),
                    "count": int(entry.n)
                }
            )

    return target_list


if __name__ == "__main__":

    # Argument parser
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--port",
        type=int,
        required=False,
        default=7777,
        help="Port to serve the HTTP-Server"
    )

    argument_parser.add_argument(
        "--host",
        type=str,
        required=False,
        default="0.0.0.0",
        help="IP address on which to serve."
    )

    argument_parser.add_argument(
        "--book",
        type=str,
        required=False,
        default="opening.data",
        help="File path to the opening book in polyglot format to be used."
    )

    argument_parser.add_argument(
        "--database",
        type=str,
        required=False,
        default="games.pgn.xz",
        help="File path to the games database in PGN format"
    )

    argument_parser.add_argument(
        "--indexfolder",
        type=str,
        required=False,
        default=".",
        help="Folder path containing the files index.w.csv.gz and index.b.csv.gz"
    )

    args = argument_parser.parse_args()

    for filename in [args.book, args.database, args.indexfolder]:
        if not Path(filename).exists():
            print(f"File or Folder '{filename}' does not exist!")
            exit(-1)

    gamesdb_obj = gamesdb.gamesdb(args.database, args.indexfolder)

    #
    # Bottle as HTTP-Server and Framework
    #

    bt = bottle.Bottle()


    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    }


    @bt.get("/")
    def get_index():
        # Set CORS-Headers
        for key, value in cors_headers.items():
            bt_response.set_header(key, value)

        return {"message": "Only valid endpoint is /query"}

    @bt.get("/query")
    def get_query():
        # Set CORS-Headers
        for key, value in cors_headers.items():
            bt_response.set_header(key, value)

        action = bt_request.query.action
        provided_fen = bt_request.query.fen

        if action == "get_book_moves" and provided_fen:
            result = openingbook_lookup(provided_fen)
            return json.dumps({"data": result})

        elif action == "get_games" and provided_fen:
            result = gamesdb_obj.lookup_games_by_fen(provided_fen)
            return json.dumps({"data": result})

        else:
            return {}

    bt.run(host=args.host, port=args.port)