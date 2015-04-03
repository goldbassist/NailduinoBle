#####################################################################
# Aldo Vargas
# 
#
# Purpose:
#   Connects a Raspberry Pi to the MultiWii Flight Controller. Based on 
#   the work made by Drew Brandsen.
#   Using MutliWii Serial Protocol (MSP), requests flight telemetry
#   data. Attitude and RC input values coming from the RX/TX with the
#   purpose to do systems identification, or just act as a data logger.
#   
#
########################################################################


import sys      # for user input
import time     # for wait commands
import datetime # for current time
import struct
import timeit
import random

from btle import UUID, Peripheral

class HM10(Peripheral):
    _ctrlUUID=UUID("00001800-0000-1000-8000-00805f9b34fb")
    _dataUUID=UUID("0000ffe0-0000-1000-8000-00805f9b34fb")
    
    def __init__(self, addr):
        Peripheral.__init__(self,addr)
        self.discoverServices()
        for cUUID in self.services:
            print("== %s =="%str(cUUID))
            print(self.getServiceByUUID(cUUID).getCharacteristics())
                
        self.ctrl_SRV=self.getServiceByUUID(self._ctrlUUID)
        self.data_SRV=self.getServiceByUUID(self._dataUUID)

        self.data = self.data_SRV.getCharacteristics()[0]
        
        #print("== CTRL ==")
        #print(self.ctrl_SRV.getCharacteristics())
        self.ctrl = self.ctrl_SRV.getCharacteristics()[0]

cHM10 = HM10("7C:66:9D:9B:20:F6")
cHM10.ctrl.write(struct.pack("B", 0xff))

###############################
# Initialize Global Variables
###############################
latitude = 0.0

#####################################################################
###################### MultiWii Serial Protocol######################
#####################################################################
#  The following define the hex values required
#  to make various MSP requests
################################################

BASIC="\x24\x4d\x3c\x00"        #MSG Send Header (to MultiWii)
MSP_ATTITUDE=BASIC+"\x6C\x6C"   #MSG ID: 108

CMD2CODE = {
'MSP_ATTITUDE':108
}

################################################
# ALTITUDE(msp)
#   receives: msp altitude message
#   outputs:  prints data in nice format
#   returns:  Angle in X, Y and heading
################################################
def ATTITUDE(msp):
    global angx
    global angy
    global heading
    if str(msp) == "":
        #print("Header: " + msp_hex[:6])
        #payload = int(msp_hex[6:8])
        #print("Payload: " + msp_hex[6:8])
        #print("Code: " + msp_hex[8:10])
        #print("RC data unavailable")
        return
    else:
        print("msp:"+msp[0:4])


#############################################################
# askATT()
#   receives: nothing
#   outputs:  nothing
#   function: Do everything to ask the MW for data and save it on globals 
#   returns:  nothing
#############################################################
def askATT():

    cHM10.data.write(MSP_ATTITUDE)  # sends MSP request
    time.sleep(1) # gives adaquate time between MSP TX & RX
    response=cHM10.data.read()  # reads MSP response
    ATTITUDE(response)  # sends to ATTITUDE to parse and update global variables


####################################################################
####################### MAIN #######################################
####################################################################
# main()
#   receives: -
#   function: opens serial port
#        loops msp commands
####################################################################
def main():
    global beginFlag

    print ("Beginning in 3 seconds...")
    
    if True:
        try:
            while True:
                #askATT()
                response=cHM10.data.read()  # reads MSP response
                ATTITUDE(response)  # sends to ATTITUDE to parse and update global variables


            cHM10.disconnect()
        
        except Exception,e1:    # Catches any errors in the serial communication
            print("Error on main: "+str(e1))
    else:
        print("Cannot open serial port")

#-----------------------------------------------------------------------
if __name__=="__main__":
    main()