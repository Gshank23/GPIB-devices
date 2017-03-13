# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 09:50:18 2017

@author: gshankar
"""


import visa


#def write_signal_generator(command):
#     signal_generator.write(command)
#     print "The command is %s" %command
#    
#     
#def write_power_meter(command):
#     power_meter.write(command)
#     print "The command is %s" %command
#    
     
def write_device(device,command):
    device.write(command)
    print "The command is %s" %command


def read_device(device):
    response= device.read()
    print "The response is %s" %response
    return response

def ask_device(device,command):
    write_device(device,command)
    response=read_device(device)
    return response
    
try:
    #Open Connection
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')

    signal_generator = rm.open_resource("GPIB0::5::INSTR")
       #Set Timeout - 10 seconds
    signal_generator.timeout =  10000
    
    #*IDN? - Query Instrumnet ID
    write_device(signal_generator,"*CLS")
    write_device(signal_generator,"*IDN?")
    
    print "The details of signal generator are as follows"
    read_device(signal_generator)
    
    
    signal_generator.close()
    print 'close instrument connection'

    print ""
    print ""
    
    power_meter = rm.open_resource("GPIB0::13::INSTR")
    #Set Timeout - 10 seconds
    power_meter.timeout =  10000
    print"The detials of power meter are as follows"
    #*IDN? - Query Instrumnet ID
    write_device(power_meter,"*CLS")
    write_device(power_meter,"*IDN?")
    read_device(power_meter)
#    write_device(power_meter,"MEASure?")
#    power_level= read_device(power_meter)
#    
#    print type(power_level)
#    print "The Measured power level from the power meter is %f dBm" %float(power_level)
    response=ask_device(power_meter,"MEASure?")
    print "The Measured power level from the power meter is %f dBm" %float(response)
    #Close Connection
    power_meter.close()
    print 'close instrument connection'

except Exception as err:
    print 'Exception: ' + str(err.message)
    
finally:
    #perform clean up operations
    print 'complete'
    

