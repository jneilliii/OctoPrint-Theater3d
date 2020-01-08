'''

Author : Princton C. Brennan
Creation Date : December 23, 2019

The Servo Controller module was created with the intention to be used
in conjuction with octoprint. Due to the low power nature of the Raspberry Pi, 
servos are a good solution to use for different controls related to the 
3d printer. This code is compatible w/ python 2.7 through python 3.7, and 
utilizes the RPi library for Pi GPIO control to send PWM (Pulse Width Modulation)
signals to the respective servos.  

Be mindful to only wire the servos to PWM capable pins on the Pi; this code was tested
with the Pi3 B+ which has the following PWM pins: 32 & 33
The code is written such that the pins must be assigned by the user.

'''

from time import sleep
import sys, os
cd = os.getcwd()
paths=[cd+'/static/python','/usr/lib/python2.7', '/usr/lib/python2.7/plat-arm-linux-gnueabihf', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/home/pi/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages']
for path in paths:
       sys.path.append(path)
import RPi.GPIO as GPIO


try:
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)		# This sets the pin references for the PI to the numbered mode
	GPIO.cleanup()	# Clear any previous settings for the GPIO pins, in case they weren't cleared previously
except Exception:
	print("All pins ready for assignment")
	pass	#if there's nothing to cleanup, the GPIO.cleanup() will be skipped.
class PanTilt_Ctrlr:
	pan_pin = 32			# Use this variable to assign the pan servo's signal (pwm) pin
	tlt_pin = 33			# Use this variable to assign the pan servo's signal (pwm) pin
	led_pin = 29			# Use this variable to assign the pan/tilt led digital pin
	dutyCycle_stop = 0	# Default Duty Cycle value to stop the servo movement is 0
	delay_time = 0.025	# Default servo turn delay value is 50 milliseconds
	pan_servo = None	# This variable will be used as a placeholder for the pan servo object
	tlt_servo = None	# This variable will be used as a placeholder for the tilt servo object
        pan_ccw_val = 12
        pan_cw_val = 3
	tlt_ccw_val = 12
	tlt_cw_val = 3

	# The method below assigns the servos to their respective positions based on your pin variable definitions
	def assignServos(self):
		# If the pan or tilt signal pins are not assigned, the servo's cannot be assigned
		if (self.pan_pin != 0):
			try:
				GPIO.setup(self.led_pin,GPIO.OUT, initial=0) # Sets LED signal pin assignment [parameter must be set]
				GPIO.setup(self.pan_pin,GPIO.OUT)  # Sets Pan-Servo signal pin assignment [parameter must be set]
				self.pan_servo = GPIO.PWM(self.pan_pin, 50)     # Sets Pan-Servo signal pin as a PWM pin
				self.pan_servo.start(0)               # Starts running PWM on the Pan-Servo signal pin and sets it to 0
				GPIO.setup(self.tlt_pin,GPIO.OUT)  
				self.tlt_servo = GPIO.PWM(self.tlt_pin, 50)     
				self.tlt_servo.start(0) 
			except Exception:
				self.stop_ServoSession()
				GPIO.setmode(GPIO.BOARD)		# This sets the pin references for the PI to the numbered mode
				GPIO.setup(self.led_pin,GPIO.OUT, initial=0) # Sets LED signal pin assignment [parameter must be set]
				GPIO.setup(self.pan_pin,GPIO.OUT)  # Sets Pan-Servo signal pin assignment [parameter must be set]
				self.pan_servo = GPIO.PWM(self.pan_pin, 50)     # Sets Pan-Servo signal pin as a PWM pin
				self.pan_servo.start(0)               # Starts running PWM on the Pan-Servo signal pin and sets it to 0
				GPIO.setup(self.tlt_pin,GPIO.OUT)  
				self.tlt_servo = GPIO.PWM(self.tlt_pin, 50)     
				self.tlt_servo.start(0) 

		else:
			print("Error: Please provide pan & tile servo pins before assigning Servos.")

	# If the commands you provide seem to be controlling the incorrect servo, you can run the method below to swap them
	def swap_ServoAssignments(self):
		self.stop_ServoSession()
		# The servo swap cannot occur it there are no initial servo assignments 
		if (self.pan_servo != None):
			self.pan_servo = GPIO.PWM(self.tlt_pin, 50)     
			self.pan_servo.start(0)   
			self.tlt_servo = GPIO.PWM(self.pan_pin, 50)     
			self.tlt_servo.start(0)               
		else:
			print("Error: The servos were never initialized.")

	def swap_pan_rotations(self):
		if (self.pan_ccw_val == 12):
			self.pan_ccw_val = 3
			self.pan_cw_val = 12
		else:
                        self.pan_ccw_val = 12
                        self.pan_cw_val = 3

	def swap_tlt_rotations(self):
                if (self.tlt_ccw_val == 12):
                        self.tlt_ccw_val = 3
                        self.tlt_cw_val = 12
                else:
                        self.tlt_ccw_val = 12
                        self.tlt_cw_val = 3

        def swap_rotations(self):
		self.swap_pan_rotations()
		self.swap_tlt_rotations

	def swap_all(self):
                self.swap_pan_rotations()
                self.swap_tlt_rotations
		self.swap_ServoAssignments()

	def pan_left(self):
		self.pan_servo.ChangeDutyCycle(self.pan_ccw_val)
		sleep(self.delay_time)
		self.pan_servo.ChangeDutyCycle(0)

	def pan_right(self):
		self.pan_servo.ChangeDutyCycle(self.pan_cw_val)
		sleep(self.delay_time)
		self.pan_servo.ChangeDutyCycle(0)

	def tilt_down(self):
		self.tlt_servo.ChangeDutyCycle(self.tlt_ccw_val)
		sleep(self.delay_time)
		self.tlt_servo.ChangeDutyCycle(0)

	def tilt_up(self):
		self.tlt_servo.ChangeDutyCycle(self.tlt_cw_val)
		sleep(self.delay_time)
		self.tlt_servo.ChangeDutyCycle(0)

	def lights_on(self):
		GPIO.output(self.led_pin,1)

	def lights_off(self):
		GPIO.output(self.led_pin,0)

	# Kills the servo control to release the PWM control and pin configuration
	def stop_ServoSession(self):
		try:
			self.pan_servo.ChangeDutyCycle(0)
			self.tlt_servo.ChangeDutyCycle(0)
		except Exception:
			print("no initial servo assignment.")
		GPIO.cleanup()

	def reset_Servos(self):
		self.stop_ServoSession()
		GPIO.setmode(GPIO.BOARD)
		self.assignServos()

	def __init__(self):
		self.assignServos()
	sleep(1)




