import time
import pygame
import math
import random
import itertools

import arena_model
import arena_view
import roomba_model


def run_simulation(robot_params={}, room_params={}, stop_conditions={}, visual_feedback=True, draw_final_result=True):
    stats = []

    room_polygon = room_params["ROOM_POLYGON"]
    obstecles = room_params["OBSTECLES"]

    max_x = max(x[0] for x in room_polygon)
    max_y = max(x[1] for x in room_polygon)

    robot_size = robot_params["ROBOT_SIZE"]

    if visual_feedback:
        view = arena_view.ScreenView(robot_size, [max_x,max_y])
    room_model = arena_model.RoomModel(room_polygon,obstecles)

    if "INITIAL_POS" in robot_params:
        start_x,start_y,direction = robot_params["INITIAL_POS"]
    else:
        start_x,start_y=random.randint(0,max_x),random.randint(0,max_y)
        while not room_model.is_good_start_point((start_x,start_y),robot_size):
            start_x,start_y=random.randint(0,max_x),random.randint(0,max_y)
        direction = random.randint(0,360)*math.pi/180.
    roomba = roomba_model.RoombaModel((start_x,start_y), robot_size, robot_params["HEAD_SIZE"],
                                      direction, robot_params["SPEED"], room_model)

    done = False
    last_coverage = 0
    steps_with_no_improvement = 0
    min_coverage = None
    if "MIN_COVERAGE_TO_EXIT" in stop_conditions:
        min_coverage = stop_conditions["MIN_COVERAGE_TO_EXIT"]
    max_no_gain_steps = 0
    if "MAX_NO_GAIN_STEPS" in stop_conditions:
        max_no_gain_steps = stop_conditions["MAX_NO_GAIN_STEPS"]
    max_time = None
    if "MAX_TIME" in stop_conditions:
        max_time = stop_conditions["MAX_TIME"]
    for t in itertools.count():
        coverage = float(room_model.clean_count)/(room_model.clean_count + room_model.dirty_count)
        stats.append(coverage)
        if coverage == last_coverage and min_coverage != None and coverage > min_coverage:
            steps_with_no_improvement += 1
            if steps_with_no_improvement > max_no_gain_steps:
                done = True
        last_coverage = coverage
        if max_time != None and t > max_time:
            done = True

        if visual_feedback:
            view.clear_screen(room_model.state)
     
            for event in pygame.event.get(): # User did something
                #print "Got event",event,"type:",event.type
                if event.type == pygame.QUIT: # If user clicked close
                    done=True
        if done:
            break
        roomba.step()
        if visual_feedback:
            view.draw_roomba(*roomba.get_draw_info())
    if not visual_feedback and draw_final_result:
        view = arena_view.ScreenView(robot_size, [max_x,max_y])
        view.clear_screen(room_model.state)
        view.draw_roomba(*roomba.get_draw_info())
        view.clear_screen(room_model.state)
    return stats
