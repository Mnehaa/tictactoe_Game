import streamlit as st # type: ignore

# Initialize session state for board and player
if "board" not in st.session_state:
    st.session_state.board = [['.' for _ in range(3)] for _ in range(3)]
if "current_player" not in st.session_state:
    st.session_state.current_player = 'X'
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None

def check_win(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '.':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '.':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '.':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '.':
        return board[0][2]
    for row in board:
        if '.' in row:
            return None
    return 'Tie'

def reset_game():
    st.session_state.board = [['.' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

st.title("Tic Tac Toe - Streamlit Edition")

if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        st.success("It's a Tie!")
    else:
        st.success(f"Player {st.session_state.winner} Wins! 🎉")
    if st.button("Play Again"):
        reset_game()
else:
    for r in range(3):
        cols = st.columns(3)
        for c in range(3):
            btn_label = st.session_state.board[r][c] if st.session_state.board[r][c] != '.' else " "
            if cols[c].button(btn_label, key=f"{r}-{c}", disabled=st.session_state.board[r][c] != '.' or st.session_state.game_over):
                st.session_state.board[r][c] = st.session_state.current_player
                winner = check_win(st.session_state.board)
                if winner:
                    st.session_state.winner = winner
                    st.session_state.game_over = True
                else:
                    st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
                st.experimental_rerun()
