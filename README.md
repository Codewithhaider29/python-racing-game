# Ultimate Flying Car Racing Game

## Overview
**Ultimate Flying Car Racing Game** is an exciting 2D arcade-style racing game built with Python and Pygame. Control your flying car, avoid enemy cars, activate fly mode, and rack up the highest score possible.  

Features:
- Smooth lane-based car movement
- Three-lane road with dynamic road markings
- Multiple enemy cars with random colors and speeds
- Fly mode for temporary invincibility
- Leveling system that increases enemy speed
- Score and high score tracking
- Game Over and restart functionality

---

## Requirements
- Python 3.10+
- Pygame library

Install Pygame using:

```bash
pip install pygame
How to Run
Run the game script:

bash
Copy code
python flying_car_racer.py
Controls
Key	Action
Left Arrow	Move car to the left lane
Right Arrow	Move car to the right lane
Up Arrow	Activate FLY MODE (temporary invincibility)
Space	Start game / Restart after game over
Quit	Close game window

Gameplay Mechanics
Player Car
Lane-based movement with smooth transitions

Can activate Fly Mode to float above road and avoid collisions

Doors animate open during fly mode

Shadow appears when flying

Enemy Cars
Randomly spawned in lanes

Various colors

Increase in speed as player progresses through levels

Colliding with an enemy ends the game unless in fly mode

Road and Environment
Three-lane road with yellow edge lines

Moving road markings simulate motion

HUD shows score, high score, level, speed, and fly mode timer

Scoring and Levels
Score increases for each enemy car avoided

Levels increase every 10 points, boosting enemy speed

High score is saved during the session

Fly Mode
Activated with Up Arrow

Lasts for a limited time (default 5 seconds)

Player becomes invincible

Doors open and car rises

File Structure
bash
Copy code
flying_car_racer.py      # Main game script
No external assets are required. The game uses Pygame’s built-in drawing functions.

Notes
Game runs at 60 FPS

Collision detection is disabled during fly mode

Smooth lane movement improves gameplay feel

Start screen shows instructions and sample car

Game over screen displays score and high score

License
You are free to modify and distribute this game.

pgsql
Copy code

If you want, I can also create a **“Screenshots and GIF” section** for the README to make it GitHub-ready and visually appealing.  

Do you want me to add that?
