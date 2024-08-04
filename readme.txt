Detection of fire and foreign objects using Artifical Intelligence methods:

•	Developed an AI-driven bot capable of detecting fire or foreign objects in a ship using advanced algorithms like A* and maximum likelihood beliefs, enabling the bot to make intelligent and informed decisions.
•	Utilized PyTorch to build a predictive model based on an acquired dataset, enabling accurate predictions for fire and foreign objects across different ship layouts and enhancing the bot's movement decisions.

The bot is responsible for the safety and security of the ship while the crew is in deep hibernation. 
   
 Project 1 - Detection and Suppression of Fire 
 At a random open cell, a fire starts. Every time step, the fire has the ability to spread to adjacent open cells. The fire
 cannot spread to blocked cells. The fire spreads according to the following rules: 
 At each timestep, a non-burning cell catches on fire with the probability 1-(1-q)^K:
 q is a parameter between 0 and 1, de ning the flammability of the ship.
 K is the number of currently burning neighbors of this cell
 
 Bot Strategies:
 Bot 1- This bot plans the shortest path to the button, avoiding the initial fire cell, and then executes that
 plan. The spread of the fire is ignored by the bot.
 
 Bot 2- At every time step, the bot re-plans the shortest path to the button, avoiding the current fire cells,
 and then executes the next step in that plan.
 
 Bot 3- At every time step, the bot re-plans the shortest path to the button, avoiding the current fire cells
 and any cells adjacent to current fire cells, if possible, then executes the next step in that plan. If there is no
 such path, it plans the shortest path based only on current fire cells, then executes the next step in that plan.
 

   main.py takes in input parameters of the ship such as 'D' dimensions of the ship and can generate various ship layouts.
   It can also create random fire cell, bot cell and a button cell. The button triggers the fire suppression system. The goal is for the bot to get to the button as soon as possible and to turn off the fire. 
   
-----------------------------------------------------------------------------------------------------------------------
 Project 2 - Detection of a Stationary Mouse
 The ship can pick up a deep space mouse, it is the bot's responsibility to catch it and release it back into the wild.
  
 This use the same logic for ship layout. A random open position for bot and the mouse is allocated. The bot has a mouse sensor which can detect the mouse.  The nearer the bot is to the mouse, the more likely it is to give a beep. Note that if the bot stays in place, it may receive a beep at some timesteps, and not at others (because of the probabilistic nature). If the bot is d-distance from the mouse (manhattan distance), the probability of receiving a eep is e^(-alpha*(d-1)), for some alpha > 0. Note that if the bot is immediately next to the mouse, the probability of receiving a beep is 1.
  
 Bot Strategies:
 Bot 1: Move to the location with highest probability, sense.
 Bot 2: Move toward the location with highest probability, alternate moving and sensing
 
	bot_finds_mouse.py has the solutions for bot1 and bot2.
 
------------------------------------------------------------------------------------------------------------------------
 Project 3 - Extension to Project 2
 Build a model to tell the bot which action to take next - where to move or sense?
 
 Using PyTorch here to build a CNN model that:
 Input: The input data is some representation of the ship and the current state of knowledge/observations.
 Output: The output is some choice of movement (up/down/left/right/sensing) - multi-class classification 
 
 Training and test data set were acquired from project 2. bot_finds_mouse_dataset.py has the outline for gathering this dataset.
 
 The PyTorch solution for the trained model is in model_predict_bot_moves.ipynb.
 
 The trained model is 72% accurate on training data and 67% accurate of test data. 
	
	
 