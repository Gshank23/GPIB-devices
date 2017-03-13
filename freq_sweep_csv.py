# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:57:49 2017

@author: gshankar
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:27:16 2017

@author: gshankar
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 09:50:18 2017

@author: gshankar
"""


import visa
import time
import csv



     
def write_device(device,command):
    device.write(command)
    print "The command is %s" %command


def read_device(device):
    response= device.read()
    print "The response is %s" %response
    return response

def ask_device(device,command):
    write_device(device,command)
    ask_response=read_device(device)
    return ask_response
 
def sweep_and_measure(start_freq,stop_freq,step_freq):  
    set_freq_list=[]
    measured_power_list=[]
#    sweep_and_measure_dict={}
    
    for freq in range(start_freq,stop_freq,step_freq):
        
        write_device(signal_generator,":FREQ:CW %sGHZ" %(freq /1000.0))
        time.sleep(1)
        set_freq=ask_device(signal_generator,":FREQ:CW?")
        print"The set_freq is %s"  %(set_freq)
        set_freq_list.append(float(set_freq)/1000000000.0)
        
        print ""
        print ""
        
        measured_power=ask_device(power_meter,"MEASure?")
        print "The Measured power level from the power meter is %f dBm" %float(measured_power)
        measured_power_list.append(float(measured_power))
 
    return (set_freq_list, measured_power_list)

    

try:
    #Open Connection
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    signal_generator = rm.open_resource("GPIB0::5::INSTR")
       #Set Timeout - 10 seconds
    signal_generator.timeout =  100000
    print "The details of signal generator are as follows"
    #*IDN? - Query Instrumnet ID
    write_device(signal_generator,"*CLS")
    IDN= ask_device(signal_generator,"*IDN?")
    print "The IDN of the device is %s" %IDN 

    power_meter = rm.open_resource("GPIB0::13::INSTR")
    #Set Timeout - 10 seconds
    power_meter.timeout =  100000
    print"The detials of power meter are as follows"
    #*IDN? - Query Instrumnet ID
    write_device(power_meter,"*CLS")
    write_device(power_meter,"*IDN?")
    read_device(power_meter)
   
#    power_meter.close()
#    print 'close instrument connection'
    (set_freq,measured_power)=sweep_and_measure(1000,5000,500)
    print "The freq set is ", set_freq
    print "the power measured is " , measured_power
    
    with open('freq_sweep2.csv','wb') as f:
        writer=csv.writer(f)
        writer.writerow(["Output file name is freq_sweep2.csv"])
        for row in range (1,6):
            writer.writerow(["User comment %d: " %row]) 
        writer.writerow(["Relay state 1 to set: SS1 1|0"])
        writer.writerow(["Relay state 2 to set: SS1 2|0"])
        writer.writerow(["Relay state 3 to set: SS1 3|0"])
        writer.writerow(["Attenuator under calibartion : Atten 1|2"])
        writer.writerow(["Start Frequency :  Hz"])
        writer.writerow(["Stop Frequency : Hz"])
        writer.writerow(["Step Frequency : Hz"])
        writer.writerow(["Start Attenuation : dB"])
        writer.writerow(["Stop Attenuation : dB"])
        writer.writerow(["Step Attenuation : dB"])
        writer.writerow([" Fixed Attenuation of Atten 1|2 : dB"])
        writer.writerow(["Wait time between frequency for power reading : mS"])
        writer.writerow(["Wait time between attenuation for power reading : mS"])
        writer.writerow([" "])  
        set_freq=["F[MHz]"] + set_freq
        measured_power=[" "] + measured_power
        writer.writerow(set_freq)
        writer.writerow(measured_power)
    
    
    signal_generator.close()
    print 'closed signal_generator instrument connection'
    power_meter.close()
    print 'closed power meter instrument connection'
    

# this execption block will give not give us the actual error message 
#except Exception, err:
#    print 'Exception: ' + str(err)
    
finally:
    #perform clean up operations
    print 'complete'
    

