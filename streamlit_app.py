import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = ["."] * 9
    st.session_state.current_player = "X"
    st.session_state.mode = st.radio("Choose Mode", ["2P", "AI"])

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != ".":
            return board[a]
    if "." not in board:
        return "Tie"
    return None

def ai_move():
    available = [i for i, val in enumerate(st.session_state.board) if val == "."]
    if available:
        move = random.choice(available)
        st.session_state.board[move] = "O"
        st.session_state.current_player = "X"

def make_move(i):
    if st.session_state.board[i] == ".":
        st.session_state.board[i] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.success(f"{'Player' if winner in ['X','O'] else ''} {winner} wins!" if winner != "Tie" else "It's a tie!")
            st.button("Play Again", on_click=reset_game)
            return
        if st.session_state.mode == "AI" and st.session_state.current_player == "X":
            st.session_state.current_player = "O"
            ai_move()
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

def reset_game():
    st.session_state.board = ["."] * 9
    st.session_state.current_player = "X"

# Draw board
st.title("Tic Tac Toe")

cols = st.columns(3)
for i in range(9):
    if st.session_state.board[i] == ".":
        cols[i % 3].button(" ", key=i, on_click=make_move, args=(i,), help="Click to play")
    else:
        cols[i % 3].write(f"### {st.session_state.board[i]}")
