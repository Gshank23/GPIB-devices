# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:57:49 2017

@author: gshankar
"""


import visa
import time
import csv
import ConfigParser
import telnetlib
import os
    
     
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
 
def atten_loop(start_atten,stop_atten,step_atten,start_freq,stop_freq,step_freq):
    set_atten=[]
    set_freq_full=[]
    measured_power_full=[]
    read_atten_list=[]
    stop_atten=stop_atten+step_atten
    stop_freq=stop_freq+step_freq
    response = os.system("ping "+ "10.16.77.203")
    print response
    HOST = "10.16.77.203"
    tn = telnetlib.Telnet(HOST,"2001")
    
    for atten in range (start_atten,stop_atten,step_atten):
        
        atten=float(atten)/1000.000
        
        print "the set_atten value is %f" %atten
        tn.write("sa2 20\r")
        tn.write("sa1 %.3f\r" %atten)
        print "wrote: "+ "sa2 " + str(atten)
        read_atten = tn.read_until('\r')
        print 'read: ' + read_atten
        (set_freq,measured_power)=sweep_and_measure(start_freq,stop_freq,step_freq)
        set_atten.append(atten)
        read_atten_list.append(read_atten)
        set_freq_full.append(start_freq)
        measured_power_full.append(measured_power)
    return (set_freq,measured_power_full,set_atten,read_atten_list)

def sweep_and_measure(start_freq,stop_freq,step_freq):  
    set_freq_list=[]
    measured_power_list=[]

    
    for freq in range(start_freq,stop_freq,step_freq):
        freq=float(freq)/1000.000
        write_device(signal_generator,":FREQ:CW %sGHZ" %(freq /1000.0))
        time.sleep(1)
        set_freq=ask_device(signal_generator,":FREQ:CW?")
        print"The set_freq is %s"  %(set_freq)
        set_freq_list.append(float(set_freq)/1000000.0)
        
        print ""
        print ""
        
        measured_power=ask_device(power_meter,"MEASure?")
        print "The Measured power level from the power meter is %f dBm" %float(measured_power)
        measured_power_list.append(float(measured_power))
 
    return (set_freq_list, measured_power_list)

def read_user_data_from_ini(filename):
    user_data=ConfigParser.ConfigParser()

    with open (filename,'rb') as fi:
        user_data.readfp(fi)
        
    general_information = dict(user_data.items('general_information'))
    frequency_details=dict(user_data.items('frequency_details'))
    attenuation_details=dict(user_data.items('attenuation_details'))
    relay_state_details=dict(user_data.items('relay_state_details'))
    return (general_information,frequency_details,attenuation_details,relay_state_details)


def write_user_data_to_csv(filename):
        writer.writerow(["output_file_name", general_information["output_file_name"]])
        for row in range (1,6): writer.writerow(["user_comment_%s" % row, general_information["user_comment_%s" %row]])
        writer.writerow([" "])
        writer.writerow(["relay_state_1_to_set",relay_state_details["relay_state_1_to_set"]])
        writer.writerow(["relay_state_2_to_set",relay_state_details["relay_state_2_to_set"]])
        writer.writerow(["relay_state_3_to_set",relay_state_details["relay_state_3_to_set"]])
        writer.writerow([" "])
        writer.writerow(["start_attenuation_dB",attenuation_details["start_attenuation_db"]])
        writer.writerow(["stop_attenuation_dB",attenuation_details["stop_attenuation_db"]])
        writer.writerow(["step_attenuation_dB",attenuation_details["step_attenuation_db"]])
        writer.writerow(["attenuator_under_calibration",attenuation_details["attenuator_under_calibration"]])
        writer.writerow(["attenuator_not_under_calibration",attenuation_details["attenuator_not_under_calibration"]])
        writer.writerow(["fixed_attenuation_value_for attenuator_not_under_calibration",attenuation_details["fixed_attenuation_value_for attenuator_not_under_calibration"]])
        writer.writerow(["wait_time_between_change_in_attenuation_and_power_measurement",attenuation_details["wait_time_between_change_in_attenuation_and_power_measurement"]])
        writer.writerow([" "])
        writer.writerow(["start_frequency_MHz",frequency_details["start_frequency_mhz"]])
        writer.writerow(["stop_frequency_MHz",frequency_details["stop_frequency_mhz"]])
        writer.writerow(["step_frequency_MHz",frequency_details["step_frequency_mhz"]])
        writer.writerow(["wait_time_between_change_in_frequency_and_power_measurement",frequency_details["wait_time_between_change_in_frequency_and_power_measurement"]])
        writer.writerow([" "])
        writer.writerow([" "])

    

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
    
    
    
    general_information,frequency_details,attenuation_details,relay_state_details=read_user_data_from_ini('example.ini')
    
    print "general_information =", general_information
    print "frequency_details = ", frequency_details
    print "attenuation_details = ", attenuation_details
    print "relay_state_details = ", relay_state_details
    
    attenuation_details["start_attenuation_db"]=float(attenuation_details["start_attenuation_db"])*1000.000
    attenuation_details["stop_attenuation_db"]=float(attenuation_details["stop_attenuation_db"])*1000.000            
    attenuation_details["step_attenuation_db"]=float(attenuation_details["step_attenuation_db"])*1000.000  
    start_atten= int(attenuation_details["start_attenuation_db"])
    stop_atten = int(attenuation_details["stop_attenuation_db"])
    step_atten = int(attenuation_details["step_attenuation_db"])
    frequency_details["start_frequency_mhz"]=float(frequency_details["start_frequency_mhz"])*1000.000
    frequency_details["stop_frequency_mhz"]=float(frequency_details["stop_frequency_mhz"])*1000.000            
    frequency_details["step_frequency_mhz"]=float(frequency_details["step_frequency_mhz"])*1000.000  
    start_freq= int(frequency_details["start_frequency_mhz"])
    stop_freq = int(frequency_details["stop_frequency_mhz"])
    step_freq = int(frequency_details["step_frequency_mhz"])
                 

    (set_freq_full,measured_power_full,set_atten,read_atten_list)=atten_loop(start_atten,stop_atten,step_atten,start_freq,stop_freq,step_freq)
    print "The freq set is ", set_freq_full
    print "the power measured is " , measured_power_full
    print "the set atten list is ", set_atten
    print "the read atten list is ", read_atten_list
    

         
    
  
    with open(general_information["output_file_name"],'wb') as f:
        writer=csv.writer(f)
        write_user_data_to_csv(general_information["output_file_name"])
        writer.writerow([" "])  
        set_freq_full=["F[MHz]"] + set_freq_full
        writer.writerow(set_freq_full)
        for i,atten in enumerate(set_atten):
            measured_power= [atten] + measured_power_full[i]
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
    

