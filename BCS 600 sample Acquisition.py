import pyvisa
import time 

try:
    #List all available VISA resources
    rm = pyvisa.ResourceManager()
    li = rm.list_resources()
    choice = ''
    while(choice == ''):
        for index in range(len(li)):
            print(str(index)+" - "+li[index])
        choice = input("Select DUT: ")
        try: 
            if(int(choice) > len(li) - 1 or int(choice) < 0):
                choice = ''
                print("Invalid Input\n")
        except:
            print("Invalid Input\n")
            choice = ''

except:
    # could not connect
    print('Could not establish communication with resource. Exiting')
    inst.exit()
    inst.close()

inst = rm.open_resource(li[int(choice)]) 

print('Instrument Connected: ' + li[int(choice)] + "\n")

def instrumentInit():
    # initialize instrument parameters and query ID
    inst.timeout = 5000 # 5s
    inst.chunk_size = 10400
    inst.read_termination = '\n'
    inst.write_termination = '\n'

    #inst.write("*RST")
    #time.sleep(.25)
    inst.write("*CLS")
    time.sleep(.25)
    ID = inst.query("*IDN?")
    print("Instrument ID = " + ID + "\n")
    errorquery()
    return;

def errorquery():
    #Query error bus
    time.sleep(.05)
    err = inst.query("SYST:ERR?")
    print("reported error = " + err + "\n")
    time.sleep(.05) 
    return;

def ConfigSample():
    #Configure samples per measurement to 600
    inst.write("SENS:SWE:POIN 600")
    return;

def ReadBuffer():
    Buffer = inst.query("FETC:ARR:VOLT?")
    print(Buffer + "\n")
    errorquery()


def main():

    instrumentInit()
    ConfigSample()
    ReadBuffer()
    inst.close()
    

if __name__ == '__main__': 
    proc = main()
