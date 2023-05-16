import chess_lib as chess



starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
response_move = "a7a5"
# new_fen, move = chess.fen_and_move_to_next_move(starting_fen)

# 1. Shows best move based on given fen.
# 2. Performs the best move.
# 3. Lets the user decide the move of the other side.
# 4. Returns FEN resulting from two previous moves (each side once)

best_move_data = chess.best_move(starting_fen)
print("Best move:", best_move_data["move"])
new_fen = chess.respond_to_best_move(best_move_data["mid_fen"], best_move_data["controler"], response_move)

print()
print()
print("New fen:", new_fen)