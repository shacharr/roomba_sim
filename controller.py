import matplotlib.pyplot

from simulator import run_simulation

from helper_functions import *

#ROOM_POLYGON = [(0,0),(640,0),(640,480),(0,480)]
#ROOM_POLYGON = [(0,0),(640,0),(640,480),(320,480),(320,240),(0,240)]
ROOM_POLYGON = [(0,0),(640,0),(640,480),(320,480),(250,240),(0,240)]

SMALL_SQUARE = [(0,0),(10,0),(10,10),(0,10)]

OBSTECLES = [transpose_polygon(SMALL_SQUARE,(200,45)),
             transpose_polygon(SMALL_SQUARE,(270,45)),
             transpose_polygon(SMALL_SQUARE,(200,125)),
             transpose_polygon(SMALL_SQUARE,(270,125)),]

ROOMBA_SIZE = 20

MIN_COVERAGE_TO_EXIT = 0.988
MAX_NO_GAIN_STEPS = 3000


def main():

    robot_params = {"ROBOT_SIZE":ROOMBA_SIZE,
                    "HEAD_SIZE":1.9,
                    "SPEED":3}
    room_params = {"ROOM_POLYGON":ROOM_POLYGON,
                   "OBSTECLES":OBSTECLES}
    stop_conditions = {"MIN_COVERAGE_TO_EXIT":MIN_COVERAGE_TO_EXIT,
                       "MAX_NO_GAIN_STEPS":MAX_NO_GAIN_STEPS,
                       "MAX_TIME":9000}

    stats = run_simulation(robot_params, room_params,
                           stop_conditions, visual_feedback=True)

    matplotlib.pyplot.plot(stats)
    matplotlib.pyplot.show()

if __name__ == "__main__":
    main()
