To use the algorithm Foe-Q[1] to find policies for players in a simple and classical general-sum two player Markov game. 
The game is like this: player A and player B started from the location below. Both of them try to reach the goal. If one of them reaches the goal, he gets +100 points and the other gets 0 points and the game ends. If both of them reach the goal simutanously, they get +50 points respectively. If they try to go across the barrier, 50% of the time they will go through and 50% of the time they end up sticking. If they try to reach a same location except the goal, only one of them can reach that location. 

![generalsum_game](https://user-images.githubusercontent.com/46943187/79052637-e5c82000-7c05-11ea-859d-6c7484dc1e07.png)





References:
[1]	M.Littman, “Friend or foe Q-learning in general-sum Markov games,” In Proceedings of the Eighteenth International Conference on Machine Learning, pages 322-328, June 2001.
