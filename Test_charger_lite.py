# from socketIO_client import SocketIO
#from qbox_commands import *
import requests
import threading
import sys
import asyncio
import traceback
import time
from datetime import datetime
import websockets
from wibotic import packettools
ENABLE_WIBOTIC = True
ODROID="BASE"
qbox_id = 4
# ************************* GLOBAL VARIABLES ************************************************************************************************************
# ------------------------------------------------------------------------------------------------------------------------------------------------------



    #import pandas as pd

Send_Telemetry_Drone_Battery = {  #antes era RTD_S, ahora es UPS
    ## Todos los datos del char

        "qbox_id"	:4,
        "VMON_gate_driver"	:1.0,
        "IMON_5v"	:1.3,
        "VMON_Pa"	:1.5,
        "IMON_Pa"	:1.1,
        "power_level"	:1.2,
        "IMON_gate_driver"	:1.0,
        "device_id"	:1,
        "RF_sense"	:1.3,
        "TMON_Amb"	:0.9,
        "TMON_Pa"	:1.0,
        "VMON_48v"	:1.0,
        "warning_messages"	:"Low battery"
        }


class NetApi:
    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        pass

    async def connect(self):
        async with websockets.connect(self.websocket_url, subprotocols=['wibotic']) as websocket:
            consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
            producer_task = asyncio.ensure_future(self.producer_handler(websocket))
            done, pending = await asyncio.wait(
                [consumer_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
                
    async def consumer_handler(self, websocket):
        while True:
            message = await websocket.recv()
            await self.consumer(message)
            
    async def producer_handler(self, websocket):
        while True:
            message = await self.producer()
            await websocket.send(message)
            
    async def consumer(self, data):
        # Print all ADC packets and Parameter Updates to the console window
        #print(packettools.process_data(data))
        try:
            # Print all ADC packets and Parameter Updates to the console window
            wibotic_data=str(packettools.process_data(data)).splitlines()
            #print(wibotic_data)
        
            #print(len(wibotic_data))
            Send_Telemetry_Drone_Battery["qbox_id"]=wibotic_data[2].split('.')[1]
            #charge_state=wibotic_data[5].split('=')
            #print(charge_state[1])
            Send_Telemetry_Drone_Battery["warning_messages"]=wibotic_data[5].split(' = ')[1] 
            Send_Telemetry_Drone_Battery["power_level"]=wibotic_data[6].split(' = ')[1]
            Send_Telemetry_Drone_Battery["IMON_5v"]=str(round(float(wibotic_data[7].split(' = ')[1]),3))  
            Send_Telemetry_Drone_Battery["VMON_gate_driver"]=wibotic_data[8].split(' = ')[1] 
            Send_Telemetry_Drone_Battery["IMON_gate_driver"]=wibotic_data[9].split(' = ')[1] 
            Send_Telemetry_Drone_Battery["VMON_Pa"]=str(round(float(wibotic_data[10].split(' = ')[1]),3)) 
            Send_Telemetry_Drone_Battery["IMON_Pa"]=str(round(float(wibotic_data[11].split(' = ')[1]),3))  
            Send_Telemetry_Drone_Battery["TMON_Pa"]=str(round(float(wibotic_data[12].split(' = ')[1]),3))  
            Send_Telemetry_Drone_Battery["RF_sense"]=wibotic_data[13].split(' = ')[1]  
            Send_Telemetry_Drone_Battery["VMON_48v"]=str(round(float(wibotic_data[14].split(' = ')[1]),3))
            #Send_Telemetry_Drone_Battery["IMon48v"]=str(round(float(wibotic_data[15].split(' = ')[1]),3))
            Send_Telemetry_Drone_Battery["TMON_Amb"]=str(round(float(wibotic_data[16].split(' = ')[1]),3))
            print("____________________________________________________________________________")
            print(Send_Telemetry_Drone_Battery)
            print("____________________________________________________________________________")
            time.sleep(10)
        except Exception as err:
            print(err)
            print('Wibotic Exception ignored. Code must not break')
            traceback_msg = traceback.format_exc() 
            pass
        except Exception as e:
            print(e)
        
    async def producer(self):
        await asyncio.sleep(1)
        
        # Send commands to the charger
        print("Changing a parameter...")
        request = packettools.ParamWriteRequest(
            packettools.DeviceID.TX, 
            packettools.ParamID.ChargeEnable,
            True
        );

	       # Example of requesting a parameter value
        #print("Request a parameter value...")
        #request = packettools.ParamReadRequest(
        #    packettools.DeviceID.TX, 
        #    packettools.ParamID.ChargeEnable
        #);
        
        # Return the request as bytes to get sent out
        return bytes(request.as_packet())

    
def WIBOTICThread():
    global Send_Telemetry_Drone_Battery,ENABLE_WIBOTIC
    if stop_all_threads:
        print('WIBOTIC thread stopped')
        return  
    #try:
    #if True: 
    if ENABLE_WIBOTIC:
        print("Entrando al hilo de WIBOTIC......")
        WIBOTIC_CHARGER_WS_URL = "ws://192.168.2.20/ws"
        test = NetApi(WIBOTIC_CHARGER_WS_URL)
            #asyncio.get_event_loop().run_until_complete(
            #    test.connect()
            #)
        loop=asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(test.connect())
        loop.close()
        print("Disconnected")          
    #except Exception as err:
    #    print('Exception ignored. Code must not break')
    #    traceback_msg = traceback.format_exc()
    #    if ENABLE_DRONE:
    #        sendStatusMessage(token_drone, traceback_msg)
    #    pass
    #except Exception as e:
    #    print(e)
#------------------------------------------------------------
if ODROID=="BASE":
      if ENABLE_WIBOTIC:
       #print("Entrando al hilo de WIBOTIC......")
        WIBOTIC_CHARGER_WS_URL = "ws://192.168.2.20/ws"
       # test = NetApi(WIBOTIC_CHARGER_WS_URL)
        #asyncio.get_event_loop().run_until_complete(
        #        test.connect()
        #        )                                                                                                                       
        print("Disconnected") 
        #t6 = threading.Thread(target = WIBOTICThread)
        #t6.setDaemon(True)
        #loop = asyncio.new_event_loop()
        #t6 = threading.Thread(target=WIBOTICThread, args=(loop,), daemon=True)
        t6 = threading.Thread(target=WIBOTICThread, daemon=True)
        t6.start()
        t6.join()
print("OUT")
