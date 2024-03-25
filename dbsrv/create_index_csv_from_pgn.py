import chess
import chess.pgn
import lzma

from pathlib import Path

# 526882 games in db

all_games_count = 526882

pgn_filename = "games.pgn.xz"
target_filename = "index.csv"

target_dict = {}

with lzma.open(pgn_filename, "rt") as pgn:
    for i in range(0, all_games_count):
        game = chess.pgn.read_game(pgn)
        board = game.board()
        for move in game.mainline_moves():
            fen = board.fen()
            offset = pgn.tell()
            if fen not in target_dict.keys():
                target_dict[fen] = [offset]
            else:
                target_dict[fen].append(offset)
            board.push(move)
        if i % 200 == 0:
            percent = i/all_games_count*100
            print(f"Already {i} games converted. Current offset at {offset}. {percent}% done.")

number_fens = len(target_dict.keys())

print(f"Generated {number_fens} FENs.")
print(f"Writing to file '{target_filename}' now ...")

with open(target_filename, "wt") as csvfile:
    for key in target_dict.keys():
        csvfile.write(f"{key};{target_dict[key]}\n")
