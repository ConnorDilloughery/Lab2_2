'''
Connor Dilloughery
Lab 0x01: Reading CSV Files 
ME 405
'''
import matplotlib.pyplot as plt
import serial

def main():
    '''! The purpose of this code is to receive information regarding
         the time and position of the encoder. It spits out a list of
         the two values
         
    '''
    try:
        ## List to contain information about the time
        time_list = []
        ## List to contain information about the position
        count_list = []
        with serial.Serial ('/dev/tty.usbmodem142103', 115200) as s_port:
            s_port.write (b'd')      # Write bytes, not a string
            while True:
                ## reads the information on the serial port
                x = str(s_port.readline())
                print(x)
                ## adds information regarding count
                if 'Count' in x:
                    count = int(''.join(c for c in x if c.isdigit() or c =='.' or c =='-'))
                    count_list.append(count)
                ## adds information regarding time
                elif 'Time' in x:
                    time = int(''.join(t for t in x if t.isdigit() or t =='.' or t =='-'))
                    time_list.append(time)
                ## checks to see if the code is done
                else:
                    print('Break')
                    break
            print(time_list)
            print(count_list)
        ## prints the motor time versus encoder position using pyplot
        plt.plot(time_list, count_list)
        plt.ylabel('Position, Encoder')
        plt.xlabel('Times, ms')
        plt.show()

    ## prevents code from crashing if serial is bugging
    except serial.SerialException:
        serial.Serial('/dev/tty.usbmodem142103', 115200).close()
        serial.Serial('/dev/tty.usbmodem142103', 115200)

         
if __name__ == '__main__':
    main()