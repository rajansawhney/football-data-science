# Football data science

Based on tutorials by [Friends of tracking](https://github.com/Friends-of-Tracking-Data-FoTD)

## Tutorial 1
- Incorporate metric coordinates into events data - to measure speed in m/s and goal distance in m, etc.
- Plot players, passes and shots
  
  `1. Kick off`
  
  ![Kick off](analysis-with-tracking-data/plots/player-pos-at-kick-off.png)
  
  `2. Defenders movement trace during first minute of the game`
  
  ![Defenders movement trace during first minute of the game](analysis-with-tracking-data/plots/defenders-during-first-min.png)
  
  `3. Player postions at instance of goal by player 9`
  
  ![Player postions at instance of goal by player 9](analysis-with-tracking-data/plots/all-player-pos-at-player9-goal.png)
  
  `4. Passes leading up to player9's goal`
  
  ![Passes leading up to player9's goal](analysis-with-tracking-data/plots/passing-run-to-goal-with-annotations.png)
  
  
## Tutorial 2
- Calculate player velocities, minutes played, distance covered for each player using tracking data
  
  `Player velocities`
  
  ![Player velocities](analysis-with-tracking-data/plots/frame-10000-with-player-velocities.png)
- Classify distance covered amongst walking, jogging, running, sprinting - plot clustered bar chart
  
  `Distance covered at different speeds`
  
  ![Distance covered at different speeds](analysis-with-tracking-data/plots/distance-covered-at-diff-speeds-bar.png)

- How many sprints? What directions? - plot trajectories

  `Sprints by player 10`
  
  ![Sprints by player 10](analysis-with-tracking-data/plots/player-10-sprint-plot.png)
  
- Extra:
  1. Plot passes and shots leading up to the second and and third goal
  
  `1. Second goal with passes`
  
  ![1. Second goal with passes](analysis-with-tracking-data/plots/second-goal-w-passes.png)
  
  `2. Third goal with passes`
  
  ![2. Third goal with passes](analysis-with-tracking-data/plots/third-goal-w-passes.png)
  
  2. Plot all player9 shots for home team. Visually differentiate goal and no-goal shots
  
  `Shots attempted by player9`
  
  ![Shots attempted by player9](analysis-with-tracking-data/plots/home-player9-shots.png)
  
  3. Plot postitions of all players at player10's goal using tracking data
  
  `Player postions at time of goal`
  
  ![Player postions at time of goal](analysis-with-tracking-data/plots/all-player-pos-at-player9-goal.png)
  
  4. Display distance covered using a bar chart
  
  `1. Distance covered by home and away team players`
  
  ![Distance covered by home team players](analysis-with-tracking-data/plots/distance-covered-home.png)
  ![Distance covered by home team players](analysis-with-tracking-data/plots/distance-covered-away.png)

 
## Tutorial 3
 - Create a pitch control model using parameters `{ frame index, events, tracking_home, tracking_away, static_default_params_dict, GK_numbers, field_dim}` 
    where `static_default_params_dict` includes max_player_speed, max_player_acceleration, average_ball_speed, reaction_time  etc default observed values
 - Plot pitch control for 3 passes leading up to the second goal of the game
 
 `1. Pitch control when player21 passes`
 
 ![Pitch control when player21 passes](analysis-with-tracking-data/plots/t3-pc-at-player21-pass.png)
 
 `2. Pitch control when player19 passes`
 
 ![Pitch control when player19 passes](analysis-with-tracking-data/plots/t3-pc-at-player19-pass.png)
  
 `3. Pitch control when player23 passes`
  
 ![Pitch control when player23 passes](analysis-with-tracking-data/plots/t3-pc-at-player23-pass.png)
   
 - Calculate and plot pass probablity for every successful pass by the home team
 
 `Pass probablity for home team's succesful passes`
 
 ![Pass probablity for home team's succesful passes](analysis-with-tracking-data/plots/t3-pass-attempted-vs-pass-prob.png)
 
 - Plot risky passes - successful passes with low probability
 
 `Risky passes`
 
 ![Risky passes](analysis-with-tracking-data/plots/t3-risky-passes.png)
   
    
