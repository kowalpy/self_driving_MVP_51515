from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import random
import math
import time


class AutonomousCar:
    def __init__(self, settings):
        self.settings = settings
        self.go_ahead = True
        self.turn = False
        self.turn_angle = 30
        if bool(random.getrandbits(1)):
            self.turn_angle *= -1
        self.initiate_objects()
        if settings['run_test']:
            self.test_function()
        else:
            self.calibrate()
            self.the_loop()

    def initiate_objects(self):
        self.hub = MSHub()
        self.hub.status_light.on('orange')
        self.motor_front = Motor(self.settings['motor_front_port'])
        self.motor_rear = Motor(self.settings['motor_rear_port'])
        self.dist_sens = DistanceSensor(self.settings['dist_sens_port'])

    def calibrate(self):
        self.motor_front.run_to_position(self.settings['motor_front_angle'])

    def test_function(self):
        self.hub.light_matrix.show_image('PACMAN')
        sounds_and_colors = [(65, "blue"), (70, "azure"), (60, "cyan")]
        for i in sounds_and_colors:
            self.hub.speaker.beep(i[0], 0.3)
            self.hub.status_light.on(i[1])
        self.hub.light_matrix.off()

    def end_turn(self):
        self.turn = False
        self.motor_front.run_for_degrees(self.turn_angle * -1)

    def the_loop(self):
        self.hub.light_matrix.write('GO')
        self.hub.status_light.on('green')
        loop_time_diff = 0
        loop_start_time = time.time()
        turn_time_diff = 0
        turn_start_time = None
        while loop_time_diff < self.settings['how_long_run']:
            how_far = self.dist_sens.get_distance_cm()
            rear_speed = self.settings.get('motor_rear_speed')
            if self.turn:
                self.hub.status_light.on('yellow')     
                turn_time_control = time.time()
                turn_time_diff = turn_time_control - turn_start_time
                if isinstance(how_far, int) and how_far <= self.settings['dist_threshold_low']:
                    self.go_ahead = False
                    self.end_turn()
                elif turn_time_diff >= self.settings['turn_in_seconds']:
                    self.end_turn()
            elif self.go_ahead:
                self.hub.status_light.on('green')
                rear_speed = rear_speed * -1
                if isinstance(how_far, int) and how_far <= self.settings['dist_threshold_low']:
                    self.go_ahead = False
            else: 
                self.hub.status_light.on('blue')     
                if isinstance(how_far, int) and how_far >= self.settings['dist_threshold_high']:   
                    self.turn = True  
                    turn_start_time = time.time()
                    self.motor_front.run_for_degrees(self.turn_angle)
                    self.go_ahead = True 
            self.motor_rear.start(rear_speed)
            wait_for_seconds(0.25)
            loop_time_control = time.time()
            loop_time_diff = loop_time_control - loop_start_time
        self.motor_rear.stop()
        self.calibrate()
        self.hub.light_matrix.write('STOP')


settings = {
    'run_test': False,            # only test function to be executed if True
    'motor_front_port': 'A',      # port to which front motor is connected
    'motor_front_angle': 110,     # angle to which front engine should be calibrated when program starts 
                                   # angle depends on motor initial setting - if MVP assembled according to manual should be probably 0
                                   # however there seem to be a play in steering "wheel" so it is better to set some other value than 0
    'turn_angle': 30,             # turn angle
    'turn_in_seconds': 3,         # how long should turn
    'motor_rear_port': 'B',       # port to which rear motor is connected
    'motor_rear_speed': 50,       # absolute basic speed of rear motor in scale 0..100 
    'dist_sens_port': 'F',        # port to which distance sensor is connected
    'dist_threshold_low': 40,     # distance threshold in centimeters
    'dist_threshold_high': 60,    # distance threshold in centimeters
    'how_long_run': 120           # how long should program run in seconds
}

AutonomousCar(settings)
