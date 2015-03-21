Roomba Simulator
----------------

This is a small pygame based roomba simulator.

To run, "python controller.py".

You will need to have matplotlib and pygame (1.8) installed.

It assumes a roomba with 2 modes - random direction switching upon hitting a wall or wall following

The roomba is placed in a polygon shaped room, and let loose.

A nice animation shows what the roomba managed to clean (blue) and what is still dirty (green). The roomba itself is drawn as a red circle, with an arrow showing where it is heading.

Currently, there is no support for obstacles in the room.

Code is arranged in a classical MVC form.

The arena_model module contains the Roomba and the Room models. The roomba has location, direction and parameters, as well as roomba navigation logic state. The room keeps a pygame surface indicating what area was cleaned already, as well as a polygon of the room to indicate where the walls are. It also keeps count of the clean vs. dirty pixels for statistics.

The arena_view module contains the major pygame interaction - drawing the roomba and the room, cleaning the screen, etc.

The controller module is tying the view with the model. It is running the main game loop. It is also collects statistics as for the progress of the cleaning effort over time. Once the room is mostly clean, and no new progress is achieved for a while, the simulation will end and a graph of cleanliness over time will be shown.

TODO:
-----

- Support for configuration which is not hard coded in the code

- Support for obstacles in the room

- Nicer graphics

- Support for collecting statistics without showing the graphics

- Support for random placement of the roomba in the room

- Add the spiral cleaning mode that roomba is using in the beginning of cleaning in a room

- Smarter mode switching logic?

- Auto tuning of parameters (i.e. when to switch to what mode of cleaning) depending on room size?

- Neato (Lidar scan, mapping, plan a route for cleaning) model for comparison of performance?