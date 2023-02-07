import pyb
import time
import utime
import motorDriver as Vroom
import encoder
import MotorControl


         

def MainCode():
    try:
        #Initiating the communication interface through UART
        ser= pyb.UART(2,baudrate= 115200)
        #Specifying the motor shield EN pin
        EN_PIN= 'PC1'
        #Specifyinng the In1 pin for the motor shield
        IN1= 'PA0'
        #Specifying the IN2 pin for the motor shield
        IN2= 'PA1'
        #SPecifying the Timer 
        TIMER=5;
        #Specifying the first encoder input pin
        ENC1= 'PC6'
        #Specifying the second encoder input pin
        ENC2= 'PC7'
        #Specifying the encoder Timer
        ENCT= 8
        #Specifying the Theta value that is wanted
        Theta_Want= 150000
        #Specifying the value for Kp
        #Kp=10
        Kp= .012
        #Creating the motor object
        Motor1= Vroom.MotorDriver(EN_PIN, IN1, IN2, TIMER)
        #Creating the encoder object for the motor
        Motor1E= encoder.Encoder(ENC1, ENC2, ENCT)
        #Setting the motor to 0. Off
        Motor1.set_duty_cycle(0)
        
        while True:
            #Creating the motor proprtional control object
            Motor1PC= MotorControl.PropControl(Kp, Theta_Want)
            #Input command specifies if instruction has received of not
            Input_Command=0
            #A continuous loop until a specific value is received
            while Input_Command ==0:
                utime.sleep_ms(10)
                if ser.any():
                    User_Input= ser.read(1)[0]
                    #The program is waiting for the ascii character d to be sent
                    if User_Input== 100:
                        #If d is received, the program can start
                        Input_Command=1
            #Initiating the Position List
            Position=[]
            #Initiating the Time List
            Time=[]
            #Creating the TimeMs Variable to store the time
            TimeMs= 0
            #Setting the instance that the code began running
            TimeOld= utime.ticks_ms()
            while True:
                  
                  
                
     
                 #Reading the current position of the motor
                 Theta_Count= Motor1E.read()
                 
                 
                 #Calculating the new PWM value depending on the current position of the motor
                 PWM = Motor1PC.run( Theta_Count, Theta_Want)
                 #Setting the PWM of the motor using the new value that was created
                 Motor1.set_duty_cycle(PWM)
                 #Receiving code was created to receive two different serial writes
                 #The count is sent first
                 ser.write(f"Count: {Theta_Count}\r\n")
                 #Right after, the time in ms is sent
                 ser.write(f"Time: {TimeMs}\r\n")
                 #The tine difference in calculated and then added to the old value of TimeMs
                 TimeMs+= utime.ticks_ms()-TimeOld
                 #TimeOld is specified as a new value
                 TimeOld= utime.ticks_ms()
                 #Position list gets appended with teh lated position value
                 Position.append(Theta_Count)
                 #Time list gets appended with the latest time value
                 Time.append(TimeMs)
                
                 utime.sleep_ms(6)
           
                 #After 5 seconds, the program is to stop
                 if TimeMs >= 5000:
                     #Sending Done to the host PC to signal that all teh data has been sent
                     ser.write(f"Done\r\n")
                     #Stopping the loop once a data has been sent
                     break
                    
            #this prints all the values that were collected 
            for Number in range(len(Position)):
                print(Time[Number],', ',Position[Number])
            #The motor is stopped since the trial has been completed
            Motor1.set_duty_cycle(0)
            #Resetting the home position of the motor to continue with testing of new input trials
            Motor1PC.ResetHome()
            Motor1E.zero()
            #A new value for Kp ois requested to continue with testing
            Kp= input('Enter New Kp')
            Kp= float(Kp)
            #A new value for wanted position is requested to continue with testing
            Theta_Want= input('Enter a new Position')
            Theta_Want=int(Theta_Want)
            
        
        
        
        
    except KeyboardInterrupt:
        print('that is all')
        Motor1.set_duty_cycle(0)
        
  
  
if __name__ == '__main__':
    MainCode()
