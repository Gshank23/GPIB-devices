# Python for Test and Measurement

# Example programs avaialable at 'ftp://ftp.keysight.com/callpub6/callpub6/MISC/Keysight_Python'
#
# SECTION 3a) Python and PyVISA - Video 13
#

# import python modules
import visa
import numpy as np
import matplotlib.pyplot as plt


def write(command):
     myinst.write(command)
     print "The command is %s" %command


preamble_key_map = {
        'ENC': 'Encoding_method',
        'YMU': 'vertical_scale_factor',
        'YOF':'Vertical_offset',
        'YZE':'Offset voltage',
        'YUN':'Vertical Units',
        'XZE':'Horizontal origin offset',
        'XUN':'horizontal Units',
        'XOF':'Horizontal Offset',
        'XIN':'Horizontal Sampling Interval',
        'WFI':'Curve Identifier',
        'PT_O':'trigger Position',
        'PT_F':'Formatsof Curve points',
        'NR_P':'Number of ponts in the curve',
        'CRV':'Preamble checksum of waveform points',
        'BYT_O':'Preamble byte order of waveform points',
        'BYT_N':'Preamble byte width of waveform points',
        'BN_F':'Preamble Binary Encoding Type',
        'BIT_N':'Preamble bit width of waveform points'
}


def process_preamble_data(preamble_response):
    print "Step0 %s " % preamble_response
    preamble_response=preamble_response[6:]
    print "Step1 %s " % preamble_response
    preamble_response=preamble_response.split(';' )
    print "Step2 %s " % preamble_response
    preamble={}
    print "step3"

    for item in preamble_response:
        key,value=item.split(" ",1)
        """
        if key == 'ENC':
            key='Encoding Method'
        elif key == 'YMU':
            key='vertical scale factor'
        elif key == 'YZE':
            key='Offset Voltage'
        elif key=='YOF':
            key='Vertical Offset'
        elif key=='XZE':
            key='Horizontal Origin Offset'
        """
        #print 'KEY = %s, they type of KEY = %s' % (key, type(key))
        """
        key = key.replace('ENC', 'encoding')
        key = key.replace('YMU', 'scale factor')
        """
        #if key == 'ENC' or key == 'YMU' or key == 'YOF':
        if key in preamble_key_map:
            key=preamble_key_map[key]

        """
        elif key == 'YMU':
            key=preamble_key_map[key]
        elif key == 'YZE':
            key=preamble_key_map[key]
        elif key=='YOF':
            key=preamble_key_map[key]
        elif key=='XZE':
            key=preamble_key_map[key]
        """
        
        preamble[key]=value
        print "%s : %s" % (key , value)
    return preamble
  

  
    
    


try:
    #Open Connection
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    #Connect to VISA Address
    #LAN - VXI-11 Connection:  'TCPIP0::xxx.xxx.xxx.xxx::inst0::INSTR'
    #LAN - HiSLIP Connection:  'TCPIP0::xxx.xxx.xxx.xxx::hislip0::INSTR'
    #USB Connection: 'USB0::xxxxxx::xxxxxx::xxxxxxxxxx::0::INSTR'
    #GPIB Connection:  'GPIP0::xx::INSTR'
    myinst = rm.open_resource("GPIB0::7::INSTR")
    
    #Set Timeout - 5 seconds
    myinst.timeout =  20000
    
    #*IDN? - Query Instrumnet ID
    write("*CLS")
    write("*IDN?")
    write("CH1:SCAle 500e-3")
    write("DATa:SOUrce CH1")
    write("DATa:SOUrce?")
    print myinst.read()
    write("DATa:ENCdg ASCIi")
    write("DATa:ENCdg?")
    print myinst.read()
    write("DATa:WIDth 2")
    write("DATa:WIDth?")
    print myinst.read()
    write("DATa:STARt 20")
    write("DATa:STARt?")
    print myinst.read()
    write("DATa:STOP")
    write("DATa:STOP?")
    print myinst.read()
    write("WFMPre?")
    
    preamble_response = myinst.read()
    preamble = process_preamble_data(preamble_response)
    print 'preamble_information: %s' % preamble
    
    write("CURVe?")
    m= myinst.read()
    m=m[6:]
    print m
  
    
    print "Curve  without :CURV"
    print m
    Curve_list=m.split(',' )
    print Curve_list
    print "The total acquierd data points = %d" % len(Curve_list)
#    print "Eliminating the CURV part"
#    print Curve_list[0]   
    
    print "Changing Curve_list to list of int values"
    Curve_list=[int(i) for i in Curve_list]
    print Curve_list
    Curve_list_new=[]
    for datapoint in Curve_list:
        Curve_list_new.append(datapoint*float(preamble['vertical_scale_factor']))
    
    Curve_array=np.array(Curve_list_new)
    plt.plot(Curve_array)
    plt.show()     
    
    #Close Connection
    myinst.close()
    print 'close instrument connection'

except Exception as err:
    print 'Exception: ' + str(err.message)
    
finally:
    #perform clean up operations
    print 'complete'
    

