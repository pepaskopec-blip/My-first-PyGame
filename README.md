🚀 Space Evader

A simple 2D retro arcade game built with Python and the Pygame library. The goal is to control the red player square and dodge falling meteors for as long as possible.

🎮 About the Game

⚬ Player: Red square that can move freely around the screen.

⚬ Meteor: Yellow object falling from top to bottom at random X positions.

⚬ Score: You earn 1 point for every meteor you successfully dodge.

⚬ Game Over: Hitting a meteor immediately stops the game and displays your final score.

🛠 Requirements & Installation

You need Python 3.x and Pygame (or pygame-ce) installed.

1. Clone the repository:

[bash]
git clone https://github.com/pepaskopec-blip/My-first-PyGame.git
cd space-evader


2. Set up a virtual environment (optional):

[bash]
python -m venv .venv
source .venv/bin/activate  # On Linux / macOS
# .venv\Scripts\activate   # On Windows


3. Install dependencies:

[bash]
pip install pygame
# Or for Apple Silicon / newer Python versions:
# pip install pygame-ce


4. Run the game:

[bash]
python main.py


🕹 Controls

Key	Action
Left Arrow	Move Left
Right Arrow	Move Right
Up Arrow	Move Up
Down Arrow	Move Down

📝 License

This project is open-source and available under the GPL 3.0 License.
