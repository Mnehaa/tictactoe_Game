import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = None
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "mode" not in st.session_state:
    st.session_state.mode = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False

def start_game(selected_mode):
    st.session_state.mode = selected_mode
    st.session_state.board = ["."] * 9
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.game_started = True

def reset_game():
    st.session_state.game_started = False
    st.session_state.mode = None

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
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            st.session_state.current_player = "X"

def make_move(i):
    if st.session_state.board[i] == "." and not st.session_state.game_over:
        st.session_state.board[i] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            if st.session_state.mode == "AI" and st.session_state.current_player == "X":
                st.session_state.current_player = "O"
                ai_move()
            else:
                st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

# UI: Title
st.title("🎮 Tic Tac Toe")

# Ask to choose mode if game not started
if not st.session_state.game_started:
    st.subheader("Select Game Mode")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play vs Player (2P)"):
            start_game("2P")
    with col2:
        if st.button("Play vs AI 🤖"):
            start_game("AI")

# If game started, show board
if st.session_state.game_started:
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if st.session_state.board[i] == ".":
                st.button(" ", key=i, on_click=make_move, args=(i,))
            else:
                st.markdown(f"### {st.session_state.board[i]}")

    # After game ends
    if st.session_state.game_over:
        winner = st.session_state.winner
        if winner == "Tie":
            st.success("It's a Tie!")
        else:
            st.success(f"Player {winner} Wins! 🎉")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play Again"):
                st.session_state.game_started = False
        with col2:
            if st.button("Exit Game"):
                reset_game()
