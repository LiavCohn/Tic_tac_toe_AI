# Tic_tac_toe_AI
This game demonstrates the Minimax algorithm using the classic Tic-Tac-Toe game. The player,'O',plays against the computer, 'X'.
Minimax in a nutt shell-
there are 2 players- the maximizer and the minimizer.
the computer plays as the maximizer, and always try to get the higher score.
the scores are:
if the computer wins: +1
if the player wins: -1
if its a tie: 0
we go through all the empty spots, and recurisly checking what is the end score.
if that score is higher than the one we have, we choose that move, because that is the best move that the computer can make at that point.
