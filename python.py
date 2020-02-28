import RPi.GPIO as GPIO
import time
import Adafruit_DHT as dht
from time import sleep
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

Motor1B = 26
Motor1E = 19
IR1 = 17
TRIG = 23 
ECHO = 24



GPIO.setup(Motor1B,GPIO.OUT)

GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(IR1,GPIO.IN)

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

def MAIN ():    
    count = 1
    while ( count != 0 ):       
        print " Do you want to start ? \n Press a for up \n Press b for down \n Press c for Temperature and Humidity measurement \n press d for terminating program "
        user = raw_input()
        if user == 'a':
            MOTOR1 ()
        if user == 'b':
            MOTOR2 ()
        if user == 'c':
            TEMP ()
        if user == 'd':
            print "TERMINATING PROGRAM"
            sleep (1)
            exit()
        else:
            print "INVALID INPUT"



MAIN ()

def ULTRA ():
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pass
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pass
        duration = time.time() - pulse_start

    distance = duration * 17150

    distance = round(distance, 2)

    print "Distance:",distance,"cm"

    return distance

def TEMP ():
    
    h,t = dht.read_retry(dht.DHT22, 18)
    
    print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h)
    
    MAIN ()
    

def MOTOR1 ():


    while (GPIO.input(17) == 0):

        count = 0
        
        print "Motor going to Start"

        GPIO.output(Motor1B,GPIO.LOW) # put it high to rotate motor in anti-clockwise direction

        GPIO.output(Motor1E,GPIO.HIGH) # Should be always high to start motor


        while (GPIO.input(17) == 0):  

            count = count + 1
        
        count = count/(120*5788.2)  
         
        print "Obstacle found at %s. th instant Stopping motor" % count

        

        GPIO.output(Motor1E,GPIO.LOW) 

        GPIO.output(Motor1B,GPIO.LOW)

        RESTART1 ()

       

def MOTOR2 ():
    count = 0
    x = 0

    x = ULTRA ()
    while (x > 10):
        
        x = ULTRA ()

        count = 0
        
        print "Motor going to Start"

        GPIO.output(Motor1B,GPIO.HIGH) # put it high to rotate motor in anti-clockwise direction

        GPIO.output(Motor1E,GPIO.LOW) # Should be always high to start motor

    while (x < 10): 


        print "Distance to obstacle is %s. cm: Stopping motor" % x

        GPIO.output(Motor1E,GPIO.LOW) # to stop the motor

        GPIO.output(Motor1B,GPIO.LOW)

        RESTART2 ()

def RESTART1 ():
    
        print " Do you want to bypass the obstacle and continue motion ? (y/n)"

        user = raw_input()

        if user == 'n':
             
            print "motor stopped"
         
            GPIO.output(Motor1E,GPIO.LOW) # to stop the motor
         
            GPIO.output(Motor1B,GPIO.LOW)
            
            MAIN ()
            
        if user == 'y':
            
             GPIO.output(Motor1B,GPIO.LOW) # put it high to rotate motor in anti-clockwise direction
             
             GPIO.output(Motor1E,GPIO.HIGH) # Should be always high to start motor#
             
             time.sleep(4)
             GPIO.output(Motor1E,GPIO.LOW) # to stop the motor
         
             GPIO.output(Motor1B,GPIO.LOW)

             MOTOR1()
            
       
def RESTART2 ():
        print " Do you want to bypass the obstacle and continue motion ? (y/n)"

        user = raw_input()
        if user == 'y':
             GPIO.output(Motor1B,GPIO.HIGH) # put it high to rotate motor in anti-clockwise direction
             
             GPIO.output(Motor1E,GPIO.LOW) # Should be always high to start motor#
             
             time.sleep(4)
             
             GPIO.output(Motor1E,GPIO.LOW) # to stop the motor
         
             GPIO.output(Motor1B,GPIO.LOW)

             MOTOR2()
             

        if user == 'n':
             print "motor stopped"
             
             GPIO.output(Motor1E,GPIO.LOW) # to stop the motor

             GPIO.output(Motor1B,GPIO.LOW)

             MAIN ()
        

    

