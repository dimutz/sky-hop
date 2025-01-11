# Sky Hop

Sky Hop is an arcade-style game application developed with Python, aimed at
providing an engaging and intuitive platform-hopping experience. Inspired by
classic vertical scrollers like Doodle Jump, Sky Hop challenges players to
reach new heights by controlling a character that must jump from platform to
platform and collect rewards to boost their score. This project integrates 
motion-based controls through MediaPipe's hand-tracking feature, creating an
unique gameplay experience where players can control the character's movement
and jumps through hand gestures captured via webcam, or by using the arrow keys.

#### Technologies used
- **Python 3.x** – The primary programming language used for developing the game.
- **Pygame** – A library used for creating the game engine and handling graphics.
- **OpenCV** – Utilized for video capture functionality, enabling webcam input
for the game.
- **MediaPipe** – A framework used for hand tracking, allowing motion-based
controls when using video input.

#### Instructions
- First, ***clone the repository*** from GitHub and ensure that ***the required
dependencies*** —pygame, opencv-python, and mediapipe— ***are installed***.
- Once the dependencies are set up, ***run the main file***, and the game menu
will appear. 
- By selecting the ***"How to Play" button***, you can learn how  to control the
character and understand the objective of the game. 
- ***The default control mode*** uses the ***keyboard arrows*** (left and right),
but you can switch to ***video mode*** and experience ***the hand-tracking feature***
provided by MediaPipe.
- *Start a new game and try to reach as many platforms as possible while
collecting rewards!* The challenge lies in surpassing your previous high 
score. *Be careful not to fall off the platforms*, as doing so will end the game.

#### Individual Contributions

##### Dămoc Mara

I worked on the **game_loop**, which determines the flow of the game and includes
the scoring system. I implemented the **game_over** window with options to resume
the *game* or *quit*, and I implemented **the Platform class** (which contains the
methods *create_initial_platform*, *generate_initial_platforms*, and
*update_platforms*) and **the Reward class** (which contains the methods
*is_collected* and *generate_rewards*). The difficulties I encountered were related
to understanding and learning how to use the GitHub platform in a collaborative
environment without creating errors.

##### Dima Alexandru

I worked on ***the video capture and processing module***. At first, I implemented
*a demo* in order *to show exactly how MediaPipe works*. The final version did not
show the frames on-screen, instead returning a value used later. I then added **a
method for handling video input in the Character class**, and this method is
called every time a new coordinate is returned by the frame handler function.
Finally, I added ***the toggle button in the game menu***, *offering the player the
choice between arrow keys input and video input*. I had difficulties finding the
MediaPipe documentation, ultimately relying on the library code. I also had trouble
trying to run the video component in WSL (I had chosen it because I like CLI git
commands more than PyCharm’s integrated VCS), before finding out that video support
is one of its limitations. I ended up moving everything on C: and using the Python
interpreter for Windows.

##### Ivașcu Andreea-Daria

I worked on **the Character class**, where I *created the character* and
*implemented its basic movement logic*. Therefore, *the character jumps
continuously* (like in the game Doodle Jump) and *by pressing the left or
right arrow keys*, the character will jump to the desired direction. I have
also implemented **the Game Menu and its buttons** that led to different
actions (like *the instructions page* for the **"How to Play" button** or
*the beginning of a new game* by pressing **the "Start Game" button**). I
have mostly worked with the **graphic interface**, in order to create *a more
attractive playing environment for the player*. This includes creating a
*sugestive game menu*, selecting *harmonious color schemes*, *incorporating
images* and choosing *fonts that evoke a retro arcade feel*. I have also added
a **"Back to Menu" button** on the *Game Over screen* that takes the player back
to the initial menu, if he wants to continue playing. I had some difficulties
making the character jump constantly and working with the jumping variables
(velocity, gravity, jumping force etc.), but in the end I managed to make it
jump correctly. Also, some difficulties appeared when adding the "Back to Menu"
button, because even though the queue of commands was emptied, the "Quit" button
on the Game Menu was pressed, because the two buttons were in the same
cooridinates on the screeen.
