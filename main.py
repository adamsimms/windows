import RPi.GPIO as GPIO
import time
import random
import requests
from bs4 import BeautifulSoup

# GET WEATHER DATA
def read_data():
    with open('data.txt', 'rt') as file:
        x = eval(file.read())
        return x


#SET VARIOUS MOVEMENTS OF MOTOR [main_sleep_time, step_val].
#main_sleep_time determines the time between pulses
#step_val determines how big should be a push in each pulse step
#high sleep_time recommended for high step_val, due to high distance.
sleep_vals = [[0.05, 0.4], [0.08, 0.5], [0.12, 0.6], [0.16, 0.8], [0.2, 1.0]]


servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 125)  # 125hz frequency

p.start(0)  # starting duty cycle ( it set the servo to 0 degree )

# GLOBAL VARIABLE TO HOLD PREV VALUES
x = 0
try:
    # defining random points between dutycycle 10 and 25
    for control_val in [10.0+random.random()*(25-10) for x in range(2000)]: #[25, 10, 20, 10, 15, 10]*2:
        # LATEST DATA INPUT
        print(read_data())
        
        # GET INPUT FOR FEATURES OF MOVEMENT. SPEED AND SMOOTHNES
        move_config = sleep_vals[random.randint(0, len(sleep_vals)-1)]
        main_sleep_time = move_config[0]
        step_val = move_config[1]
        
        # DESTINATION TO GO FROM CURRENT POSITION
        # USING GLOBAL x HERE
        print(control_val)
        if x > 0:
            prev_x = x
        else:
            prev_x = 10
        # INPUT FOR DEFINING THE MOVEMENT - WHERE AND HOW UNSLOW
        x_input = [control_val, main_sleep_time]#+random.random()*main_sleep_time]
        print(x_input)
                              
        # LIST CAN BE GIVEN TO CONTROL SPEED
        if type(x_input) == list:
            x = float(x_input[0])
            try:
                sleep_time = float(x_input[1])
            except:
                sleep_time = main_sleep_time
        else:
            x = float(x_input)
            sleep_time = main_sleep_time
        
        # DEFINING THE FLIGHT PATH OF THE MOTOR IN AN ARRAY FROM HERE TO THERE
        import decimal

        def float_range(start, stop, step):          
            val_list = [start]
            while val_list[-1] < stop:
                val_list.append(val_list[-1]+step)
            return val_list
    
    
        x_range = float_range(int(min(prev_x, x)), int(max(prev_x, x)), step_val)
        if x > 0:
            # MOVE THE MOTOR
            for val in (x_range if x>prev_x else reversed(x_range)):
                #print(val)
                GPIO.output(servoPIN, True)
                p.ChangeDutyCycle(val)
                time.sleep(sleep_time)
                GPIO.output(servoPIN, False)
                p.ChangeDutyCycle(0)
        else:
            p.ChangeDutyCycle(0)
            GPIO.output(servoPIN, False)

except KeyboardInterrupt:
    GPIO.cleanup()


