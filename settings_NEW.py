#INDICA EL ID DEL QBOX
qbox_id = 4

# Seleccionar el Tipo de Dron con el que se va a trabajar ^^**********************************************************************************************
drone_type='HYBRID'
if drone_type=='COPTER':
    bat_volt='FS_BATT_VOLTAGE'
elif drone_type=='HYBRID':
    bat_volt='BATT_LOW_VOLT'

windows = 1

# Seleccionar la odroid a utilizar: odroid de la base u odrid de la estación ^^ **************************************************************************
ODROID = "BASE" #ESTACION
if ODROID=="BASE":
    #UPS online
    ENABLE_UPS=True
    ENABLE_NUCLEO_B= True    #VINCENT ^^
    #WIBOTIC (wireless charging system) online
    ENABLE_WIBOTIC=True
if ODROID=="ESTACION":
    # Datos del Decodificador de Datos del GPS (RTK) ^^
    RTK_PORT = '/dev/RTK_PORT'
    RTK_BAUDRATE = 115200
    ENABLE_RTK = True
    # COORDINATES_FILENAME="/home/odroid/qbox-python/coordinates.txt"
    COORDINATES_FILENAME="coordinates.txt"

    #VEHICLE_CONNECTION_STRING = 'udp:127.0.0.1:14551'
    #VEHICLE_CONNECTION_STRING = 'udp:192.168.10.104:14551'
    # Datalink connection string
    ##CONNECTION_STRING = 'COM4'
    # BBB connection string
    ##CONNECTION_STRING = '/dev/ttyO1'

    # Datos del DRON  ^^
    DRONE_PORT = '/dev/RFD900X_PORT'
    DRONE_BAUDRATE = 57600
    ENABLE_DRONE = True
    MIN_HEARTBEAT_INTERVAL = 2
    FLIGHT_END_ALT = 2

    # Datos de la núcleo ^^
    NUCLEO_PORT = '/dev/NUCLEO_PORT'
    NUCLEO_BAUDRATE = 115200
    ENABLE_NUCLEO = True
    DATA_HEADER='$'

## COMUNICACIÓN POR INTERNET ^^ *****************************************************************************************************************************
DEBUG = False # Para ELEGIR entre el servidor local donde se encuentre qairaOps o la página WEB
if DEBUG:
    #QUÉ TIPO DE COMUNICACIÓN USA EL QAIRA MAP ??????? EN TEORIÍA SE VA REEMPLAZAR LOS SOCKETS POR LA QUE USA QAIRA MAP
    SOCKET_URI = 'http://192.168.10.100' # UPDATE --- IP de la página ^^
    SOCKET_PORT = 8888
    SERVER_TIMEOUT = 0.1
else:
    SOCKET_URI = 'https://qairaopsnapi-dev.qairadrones.com' 
    SOCKET_PORT = 80
    SERVER_TIMEOUT = 2

BASE_URL = str(SOCKET_URI) + ':' + str(SOCKET_PORT)

#QBOX_NAME = 'Q001'#'Q002'
#ACCESS_CODE = '12345'#'YLUSA'


## TIPOS DE ERRORE **********************************************************************************************************************************************
RESPONSE_CODES = {
         'CONFLICT' : 409,
         'NOT_FOUND' : 404,
         'OK' : 200,
         'SERVER_ERROR' : 500,
         'UNAUTHORIZED' : 401}

## Datos que envía a la NÉCLEO (estados)*************************************************************************************************************************
qbox_data_send_to_nucleo = {
        "qbox_id" : qbox_id,
        'prepare_drone_launch' : 0, # VALOR = 1 : Baja la estación metereológica y abre la compuertas ^^
        'prepare_drone_land' : 0, # VALOR = 1 : Baja la estación meterológica, prende el IR-LOCK ^^
        # se debería anhadir una variable para indicar que el dron despegó para que suba la estación. A no ser que el qBox sepa de otra forma si el dron ya despegó ?????? ^^
        'close_qbox' : 0} # Cierra compuertas, sube la estación, cerrar y abrir el mecanismo de alineamiento
        # Si luego de enviar "prepare_drone_launch", en envía "close_qbox" sin enviar con anterioridad "prepare_drone_land", quiere decir que el dron ^^
        # aterrizó en otro lugar debido a que ocurrió algún error o fallo. ----- Opción de funcionamiento ^^
        ## Data enviada por el QBOX (ODROID de la estación) a la nube***************************************************************************************************************************
qbox_station_data_send_to_socket = {
        "qbox_id" : qbox_id,
        'temperature' : -1,# DATOS SENSADOR POR LA ESTACIÓN ^^ 
        'humidity': -1, 
        'rain' : -1,
        'wind_speed' : -1}

qbox_data_send_to_socket = {

         "qbox_id":qbox_id,
         # COMPUERTA ^^
         'gate1' : -1,# antes door1_state
         'gate2' : -1, # antes door2_state
         # MASTIL DE LA ESTACIÓN METEREOLÓGICA^^
         'station': -1, # antes mastil
         # MECANISMO DE ALINEAMIENTO ^^
         'mechanism_v' : -1, #VERTICAL # HORIZONTAL # antes a_mechanism_1_state
         'mechanism_h' : -1, #HORIZONTAL#  antes a_mechanism_2_state
          #'a_mechanism_3_state' : -1, # ANTES ERES
          #'a_mechanism_4_state' : -1, # ANTES ERA
          # RESPUESTA A "prepare_drone_launch", SI TODO ESTÁ "OK" (los datos sensados son idóneos, la estación se bajó y se abrió las compuertas)
          # "launch_ready" se vuelve "1", lo que indica a la página que todo está listo para que el dron despegue
         'launch_ready' : -1,
          # RESPUESTA A "prepare_drone_land", SI TODO ESTÁ "OK" (los datos sensados son idóneos, la estación se bajó, se prendió el IR-lock, etc)
          # "land_ready" se vuelve "1", lo que le indica a la página que todo está listo para que el dron aterrice
          'land_ready' : -1,
          # INDICA CADA COSA QUE HIZO CAMBIANDO EL VALOR DE LA VARIABLE "sequence_state", POR EJEMPLO: Bajó estación (1), abrió compuerta (3), despegó el dron (4), etc
         'status' : -1, # antes era sequence_state modificado 19-04-2021
         'reset': -1, # anñadido 19-04-2021
          # Indica si IR-LOCK está encendido o apagado
         'irlock_beacon' : -1
           # Variables para enviar datos generados por el RTK, SU PRESICIÓN y su estado
            #      'latitud' : -1,
            #     'longitud' : -1,
            #      'altitud' : -1,
            #     'accuracy' : -1,
            #    'rtk_state' : -1
        }
           ## ODROID DE LA BASE, DATOS QUE SE ENVÍA A LA NUBE *******************************************************************************************************
RTK_data_send_to_socket = {
             'qbox_id' :qbox_id,
             'latitud' : -1,
             'longitud' : -1,
             'altitud' : -1,
             'accuracy' : -1,
             'rtk_state' : -1    
}
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
        
       




            #        'UPS Battery Discharge Time' : -1,
            #     'UPS_Remaining_Time_of_Battery' : -1,
            # 'UPS_Remaining_Capacity_of_Battery' : -1,
            #               'UPS_Battery_Voltage' : -1,
            #                 'UPS_Input_Voltage' : -1,
            #               'UPS Input Frequency' : -1,
            #                'UPS Output Voltage' : -1,
            #                   'UPS Output Load' : -1,
            #              'UPS Bypass Frequency' : -1,
            #                'UPS Bypass Voltage' : -1,
            #                   'UPS_Temperature' : -1,
            #           'UPS_Battery_Voltage_Low' : -1,
            #               'UPS_Battery_Testing' : -1,
            #               'UPS_Battery_Powered' : -1,
            #                   'UPS_Input_Fault' : -1,
            #             'UPS_Power_Supply_Mode' : -1,
            #                  'UPS_Bypass_Fault' : -1,
            #                          'UPS_Type' : -1,
            #               'UPS_OverTemperature' : -1,
            #                         'UPS_Fault' : -1,
            #               'UPS_Shutdown_Active' : -1,
            #              'UPS_is_Shutting_Down' : -1,
            #                    'UPS IP Address' : -1  
                   }
  # Todos los datos del CARGADOR DE BATERÍAS
DRONE_CHARGER_data_send_to_socket = { #antes era parte de RTD_S (actual ups)
                "qbox_id":qbox_id, #INCLUIDO
                "device_id":-1,
                "warning_messages":-1, # ANTES'ChargeState' : -1, 
                "power_level":-1,
                "IMON_5v":-1,
                "VMON_gate_driver":-1,
                "IMON_gate_driver":-1,
                "VMON_Pa":-1,
                "IMON_Pa":-1,
                "TMON_Pa":-1,
                "RF_sense":-1,
                "VMON_48v":-1,      
                "TMON_Amb":-1
                #  'IMon48v' : -1,  #HABIDO EN CODIGO MAS NO EN SERVIDOR, POR ELLO SE COMENTO ESTA VARIABLE
                }

			    #          'DeviceID' : -1,
		        #       'ChargeState' : -1, 
	          	#        'PowerLevel' : -1, 
                #            'IMon5v' : -1, 
                #    'VMonGateDriver' : -1, 
                #    'IMonGateDriver' : -1, 
                #            'VMonPa' : -1, 
                #            'IMonPa' : -1, 
                #            'TMonPa' : -1, 
                #           'RfSense' : -1, 
                #           'VMon48v' : -1, 
                #           'IMon48v' : -1, 
                #           'TMonAmb' : -1}





