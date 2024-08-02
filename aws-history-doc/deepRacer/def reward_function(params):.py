# https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html

# doordashguy v1
def reward_function(params):
    reward = 1e-3
    
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering_angle = abs(params['steering_angle'])  
    speed = params['speed']
    
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += -0.5 


    # high A high S
    if steering_angle > 20 and speed > 2.5:
        reward -= 2.0
    elif steering_angle > 12.5 and speed > 2.0:
        reward -= 1.0
    
    # high A low S
    if steering_angle > 15 and speed < 1.8:
        reward += 1.0


    # low A high S
    if steering_angle < 5 and speed > 2.5:
        reward += 2.0
    elif steering_angle < 12.5 and speed > 2.0:
        reward += 1.0

    # low A low S
    if steering_angle < 5 and speed < 1.0:
        reward -= 2.0

    return float(reward)


# doordashguy v2
def reward_function(params):
    reward = 1e-3
    
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering_angle = abs(params['steering_angle'])  
    speed = params['speed']
    
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += -0.5 

    # high A high S
    if steering_angle > 20 and speed > 2.5:
        reward -= 2.0
    elif steering_angle > 12.5 and speed > 2.0:
        reward -= 1.0
    
    # high A low S
    if steering_angle > 15 and speed < 2.2:
        reward += 1.0

    # low A high S
    if steering_angle < 5 and speed > 3:
        reward += 2.0
    elif steering_angle < 12.5 and speed > 2.5:
        reward += 1.0

    # low A low S
    if steering_angle < 5 and speed < 2.0:
        reward -= 2.0

    return float(reward)




# flash v1
import math
def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    objects_location = params['objects_location']
    agent_x = params['x']
    agent_y = params['y']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']
    # Initialize reward with a small number but not zero
    # because zero means off-track or crashed
    reward = 1e-3
    # Reward if the agent stays inside the two borders of the track
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward_lane = 1.0
    else:
        reward_lane = 1e-3
    # Penalize if the agent is too close to the next object
    reward_avoid = 1.0
    # Distance to the next object
    next_object_loc = objects_location[next_object_index]
    distance_closest_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)
    # Decide if the agent and the next object is on the same lane
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center
    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8:
            reward_avoid *= 0.5
        elif 0.3 <= distance_closest_object < 0.5:
            reward_avoid *= 0.2
        elif distance_closest_object < 0.3:
            reward_avoid = 1e-3  # Likely crashed
    # Calculate reward by putting different weights on
    # the two aspects above
    reward += 1.0 * reward_lane + 4.0 * reward_avoid
    return reward


# flash v2
import math
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    objects_location = params['objects_location']
    agent_x = params['x']
    agent_y = params['y']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])

    # Initialize reward
    reward = 1e-3

    # Encourage staying on the track
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward += 1.0

    reward += (1 - (distance_from_center / (track_width / 2))) * 0.5

    # Penalize if the agent is too close to the next object
    next_object_loc = objects_location[next_object_index]
    distance_closest_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center

    # avoid reward
    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8:
            reward = 0.8
        elif 0.3 <= distance_closest_object < 0.5:
            reward= 0.5
        elif distance_closest_object < 0.3:
            reward = 1e-3  

    # spped with angle reward
    if steering_angle < 15:  
        reward += speed * 0.5
    else:  
        reward += speed * 0.1

    return reward


# flash v3
import math
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    objects_location = params['objects_location']
    agent_x = params['x']
    agent_y = params['y']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])

    # Initialize reward
    reward = 1e-3

    # Encourage staying on the track
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward += 1.0

    reward += (1 - (distance_from_center / (track_width / 2))) * 0.5

    # Penalize if the agent is too close to the next object
    next_object_loc = objects_location[next_object_index]
    distance_closest_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center

    # avoid reward
    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8:
            reward = 0.8
        elif 0.3 <= distance_closest_object < 0.5:
            reward= 0.5
        elif distance_closest_object < 0.3:
            reward = 1e-3  

    # spped with angle reward
    if steering_angle < 15:  
        reward += speed * 0.5
    else:  
        reward += speed * 0.1


    #from previous reward
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += -0.5 

    # low A high S
    if steering_angle < 5 and speed > 2.5:
        reward += 2.0
    elif steering_angle < 12.5 and speed > 2.0:
        reward += 1.0

    # high A high S
    if steering_angle > 20 and speed > 2.5:
        reward -= 2.0
    elif steering_angle > 12.5 and speed > 2.0:
        reward -= 1.0
    
    # high A low S
    if steering_angle > 15 and speed < 1.8:
        reward += 1.0

    # low A low S
    if steering_angle < 5 and speed < 1.0:
        reward -= 2.0
    return reward