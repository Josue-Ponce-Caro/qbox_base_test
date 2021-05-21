# from socketIO_client import SocketIO
#from qbox_commands import *

import threading

import traceback
import time
from datetime import datetime

ENABLE_UPS = True
ODROID="BASE"
qbox_id = 4
# ************************* GLOBAL VARIABLES ************************************************************************************************************
# ------------------------------------------------------------------------------------------------------------------------------------------------------

from selenium import webdriver
    #import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
 
  

UPS_data_send_to_socket = {  #antes era RTD_S, ahora es UPS
    ## Todos los datos del UPS

        "qbox_id":qbox_id,
        'UPS_battery_bischarge_time' : -1,#ANTES NO CONSIDERADO
        "UPS_remaining_time_of_battery":"15:50:00",
        "UPS_remaining_capacity_of_battery":15.0,
        "UPS_battery_voltage":30.0,
        "UPS_input_voltage":5.0,
        'UPS_output_voltage' : -1,#ANTES NO CONSIDERADO
        'UPS_temperature' : -1,#ANTES NO CONSIDERADO
        "UPS_battery_voltage_low":1.0,
        "UPS_battery_testing":0,
        "UPS_battery_powered":1,
        "UPS_input_fault":0,
        "UPS_power_supply_mode":"Active",
        "UPS_bypass_fault":0,
        "UPS_type":"Normal",
        "UPS_over_temperature":0,
         "UPS_fault":0,
        "UPS_shutdown_active":0,
        "UPS_is_shutting_down":0,
        'UPS_IP_address' : -1  #ANTES NO CONSIDERADO
        }
def UPSThread():
    global UPS_data_send_to_socket,ENABLE_UPS, options, driver0, driver1, driver2
    # global RTD_S,ENABLE_UPS, qbox_data_send_to_socket_base,options, driver0, driver1, driver2
    while True:
 
        try: 
            if ENABLE_UPS:
                start_time = time.time()
                print("Entrando al hilo del UPS......")
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                # driver0 = webdriver.Chrome(r"chromedriver", options = options)
                time.sleep(2)
                driver0 = webdriver.Chrome(r"C:\Users\H P\Desktop\qAIRA\qbox-python_NEW\chromedriver.exe", options = options)
                time.sleep(1)
                driver0.get("http://admin:admin@192.168.1.9/User_26")
                time.sleep(1)
                RTD_1 = driver0.find_element_by_xpath("//*[@id='Bat1']") #Battery Discharge Time(s)
                RTD_2 = driver0.find_element_by_xpath("//*[@id='Bat2']") #Remaining Time of Battery(min)
                RTD_3 = driver0.find_element_by_xpath("//*[@id='Bat3']") #Remaining Capacity of Battery(%)
                RTD_4 = driver0.find_element_by_xpath("//*[@id='Bat4']") #Battery Voltage(V)
                RTD_5 = driver0.find_element_by_xpath("//*[@id='input2']") #Input Voltage(V)
                RTD_6 = driver0.find_element_by_xpath("//*[@id='input8']") #Input Frequency(Hz)
                RTD_7 = driver0.find_element_by_xpath("//*[@id='output3']") #Output Voltage(V)
                RTD_8 = driver0.find_element_by_xpath("//*[@id='output12']") #Output Load(%)
                RTD_9 = driver0.find_element_by_xpath("//*[@id='byp0']") #Bypass Frequency(Hz)
                RTD_10 = driver0.find_element_by_xpath("//*[@id='byp2']") #Bypass Voltage(V)
                RTD_11 = driver0.find_element_by_xpath("//*[@id='Bat6']") #Temperature(°C)
                RTD_1C = RTD_1.get_attribute('innerHTML')
                RTD_2C = RTD_2.get_attribute('innerHTML')
                RTD_3C = RTD_3.get_attribute('innerHTML')
                RTD_4C = RTD_4.get_attribute('innerHTML')
                RTD_5C = RTD_5.get_attribute('innerHTML')
                RTD_6C = RTD_6.get_attribute('innerHTML')
                RTD_7C = RTD_7.get_attribute('innerHTML')
                RTD_8C = RTD_8.get_attribute('innerHTML')
                RTD_9C = RTD_9.get_attribute('innerHTML')
                RTD_10C = RTD_10.get_attribute('innerHTML')
                RTD_11C = RTD_11.get_attribute('innerHTML')
                driver0.close()
                time.sleep(2)
                print("...............................DRIVER 0 OUR ...........................")
                # driver1 = webdriver.Chrome(r'chromedriver', options = options)
                driver1 = webdriver.Chrome(r"C:\Users\H P\Desktop\qAIRA\qbox-python_NEW\chromedriver.exe", options = options)
                time.sleep(1)
                driver1.get("http://admin:admin@192.168.1.9/User_47")
                time.sleep(1)
                RTD_12 = driver1.find_element_by_xpath("//*[@id='dis_y0_0']") #Battery Voltage Low
                RTD_13 = driver1.find_element_by_xpath("//*[@id='dis_y0_1']") #Battery Testing
                RTD_14 = driver1.find_element_by_xpath("//*[@id='dis_y0_2']") #Battery Powered
                RTD_15 = driver1.find_element_by_xpath("//*[@id='dis_y0_3']") #Input Fault
                RTD_16 = driver1.find_element_by_xpath("//*[@id='dis_n2']") #Power Supply Mode
                RTD_17 = driver1.find_element_by_xpath("//*[@id='dis_y0_8']") #Bypass Fault
                RTD_18 = driver1.find_element_by_xpath("//*[@id='dis_n3']") #UPS Type
                RTD_19 = driver1.find_element_by_xpath("//*[@id='dis_y0_4']") #OverTemperature
                RTD_20 = driver1.find_element_by_xpath("//*[@id='dis_y0_4']") #UPS Fault
                RTD_21 = driver1.find_element_by_xpath("//*[@id='dis_y0_6']") #UPS Shutdown Active	
                RTD_22 = driver1.find_element_by_xpath("//*[@id='dis_y0_7']") #UPS is Shutting Down	
                RTD_12C = RTD_12.get_attribute('innerHTML')
                RTD_13C = RTD_13.get_attribute('innerHTML')
                RTD_14C = RTD_14.get_attribute('innerHTML')
                RTD_15C = RTD_15.get_attribute('innerHTML')
                RTD_16C = RTD_16.get_attribute('innerHTML')
                RTD_17C = RTD_17.get_attribute('innerHTML')
                RTD_18C = RTD_18.get_attribute('innerHTML')
                RTD_19C = RTD_19.get_attribute('innerHTML')
                RTD_20C = RTD_20.get_attribute('innerHTML')
                RTD_21C = RTD_21.get_attribute('innerHTML')
                RTD_22C = RTD_22.get_attribute('innerHTML')
                driver1.close()
                time.sleep(2)
                print("...............................DRIVER 1 OUR ...........................")
                driver2 = webdriver.Chrome(r"C:\Users\H P\Desktop\qAIRA\qbox-python_NEW\chromedriver.exe", options = options)
                time.sleep(1)
                # driver2 = webdriver.Chrome(r'chromedriver', options = options)        
                driver2.get("http://admin:admin@192.168.1.9/User_15")
                time.sleep(1)
                RTD_23 = driver2.find_element_by_xpath("//*[@id='config_ip']") #IP Address
                RTD_23C = RTD_23.get_attribute('value')
                RTD = RTD_1C+ ','+RTD_2C+ ','+RTD_3C + ','+RTD_4C + ','+RTD_5C + ','+RTD_6C + ','+ RTD_7C + ','+ RTD_8C + ','+ RTD_9C + ','+RTD_10C + ','+RTD_11C + ','+RTD_12C + ',' + RTD_13C + ',' + RTD_14C + ',' + RTD_15C + ',' + RTD_16C + ',' + RTD_17C + ',' +RTD_18C + ','+ RTD_19C+ ','+RTD_20C + ','+RTD_21C
                print("Data leida: "+RTD) 
                #UPS_data_send_to_socket antes era RTD_S
                UPS_data_send_to_socket["UPS_battery_bischarge_time"] = str(RTD_1C)#ANTES NO CONSIDERADO
                UPS_data_send_to_socket["UPS_remaining_time_of_battery"] = str(RTD_2C)
                UPS_data_send_to_socket["UPS_remaining_capacity_of_battery"] = str(RTD_3C)
                UPS_data_send_to_socket["UPS_battery_voltage"] = str(RTD_4C)
                UPS_data_send_to_socket["UPS_input_voltage"] = str(RTD_5C)
                # UPS_data_send_to_socket["UPS Input Frequency"] = str(RTD_6C)
                UPS_data_send_to_socket["UPS_output_voltage"] = str(RTD_7C) #ANTES NO CONSIDERADO
                # UPS_data_send_to_socket["UPS Output Load"] = str(RTD_8C)
                # UPS_data_send_to_socket["UPS Bypass Frequency"] = str(RTD_9C)
                # UPS_data_send_to_socket["UPS Bypass Voltage"] = str(RTD_10C)
                UPS_data_send_to_socket["UPS_temperature"] = str(RTD_11C)#ANTES NO CONSIDERADO
                UPS_data_send_to_socket["UPS_battery_voltage_low"] = str(RTD_12C)
                UPS_data_send_to_socket["UPS_battery_testing"] = str(RTD_13C)
                UPS_data_send_to_socket["UPS_battery_powered"] = str(RTD_14C)
                UPS_data_send_to_socket["UPS_input_fault"] = str(RTD_15C)
                UPS_data_send_to_socket["UPS_power_supply_mode"] = str(RTD_16C)
                UPS_data_send_to_socket["UPS_bypass_fault"] = str(RTD_17C)
                UPS_data_send_to_socket["UPS_type"] = str(RTD_18C)
                UPS_data_send_to_socket["UPS_over_temperature"] = str(RTD_19C)
                UPS_data_send_to_socket["UPS_fault"] = str(RTD_20C)
                UPS_data_send_to_socket["UPS_shutdown_active"] = str(RTD_21C)
                UPS_data_send_to_socket["UPS_is_shutting_down"] = str(RTD_22C)
                UPS_data_send_to_socket["UPS_IP_address"] = str(RTD_23C)#ANTES NO CONSIDERADO
                print("LEIDO...............")
                print(UPS_data_send_to_socket)
                driver2.close()
                time.sleep(2)
                print("...............................DRIVER 2 OUR ...........................")
                
                # time.sleep(5)
                print("-------------------------OUT OF READING---------------------------------")
        except Exception as err:
            print(err)
            print('UPS exception ignored. Code must not break')
            traceback_msg = traceback.format_exc()
            # if ENABLE_DRONE:
            #     sendStatusMessage(token_drone, traceback_msg)
            # pass
        except Exception as e:
            print(e)
        
        time.sleep(2)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("_________________________________NEW READINGGG_____________________________________")

if ODROID=="BASE":
    if ENABLE_UPS:
        t5 = threading.Thread(target = UPSThread)
        t5.setDaemon(True)
        t5.start()
        t5.join()
print("OUT")