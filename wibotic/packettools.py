#!/usr/bin/env python3
# coding=utf-8
""" WiBotic Websocket Network API Packet Tools

Tools for creating and interpreting binary packets sent over a Websocket
connection to a WiBotic charging system """

__copyright__ = "Copyright 2019 WiBotic Inc."
__version__ = "0.1"
__email__ = "info@wibotic.com"
__status__ = "Technology Preview"

import struct
from enum import IntEnum

_C_TYPE = {
    'uint32_t' : '<L',
    'uint16_t' : '<H',
    'uint8_t'  : '<B',
    'float'    : '<f'
}

class DeviceID(IntEnum):
    """ Device Address Identifiers """
    TX = 1
    RX_1 = 2
    
class ParamStatus(IntEnum):
    """ Response Codes """
    FAILURE = 0
    HARDWARE_FAIL = 1
    INVALID_INPUT = 2
    NON_CRITICAL_FAIL = 3
    READ_ONLY = 4
    SUCCESS = 5
    NOT_AUTHORIZED = 6
    PENDING = 7
    CLAMPED = 8
    
class ChargerState(IntEnum):
    """ State From Charger ADC Packet """
    IDLE = 0,
    RAMP_UP = 1,
    CC_CHARGE = 2,
    CV_CHARGE = 3,
    BATT_FULL = 4,
    STOPPING = 5,
    ALARM = 6,
    CHECK_VOLT = 7,
    RECOVERY = 8,
    FATAL = 9,
    POWER_SUPPLY = 10
    
class TransmitterState(IntEnum):
    """ State From Transmitter ADC Packet """
    OFF = 0,
    IDLE = 1,
    RAMP_UP = 2,
    CHARGING = 3,
    RX_NO_CHARGE = 4
    
class BatteryChemistry(IntEnum):
    """
    Battery Chemistry Identifiers. 
    You can use the Battery_Chemistry_Information dictionary to look up specific 
    values for each battery chemistry.
    """
    Unknown = 0
    LithiumIon = 1
    NiCad = 2
    LeadAcid = 3
    LiFePO4 = 4
    DJIMSeries = 5

Battery_Chemistry_Information = {
    BatteryChemistry.Unknown : {
        'min_voltage_per_cell': 500,
        'max_voltage_per_cell': 65535,
        'restart_per_cell': 65534,
        'overvolt_per_cell': 65535
    },
    BatteryChemistry.LithiumIon : {
        'min_voltage_per_cell': 3000,
        'max_voltage_per_cell': 4200,
        'restart_per_cell': 4075,
        'overvolt_per_cell': 4350
    },
    BatteryChemistry.NiCad : {
        'min_voltage_per_cell': 750,
        'max_voltage_per_cell': 1550,
        'restart_per_cell': 1400,
        'overvolt_per_cell': 1650
    },
    BatteryChemistry.LeadAcid : {
        'min_voltage_per_cell': 1930,
        'max_voltage_per_cell': 2440,
        'restart_per_cell': 2165,
        'overvolt_per_cell': 2540
    },
    BatteryChemistry.LiFePO4 : {
        'min_voltage_per_cell': 2500,
        'max_voltage_per_cell': 3650,
        'restart_per_cell': 3375,
        'overvolt_per_cell': 3800
    },
    BatteryChemistry.DJIMSeries : {
        'min_voltage_per_cell': 3000,
        'max_voltage_per_cell': 4350,
        'restart_per_cell': 4225,
        'overvolt_per_cell': 4450
    },
}

class ParamID(IntEnum):
    """ Paramter Identifiers """
    ExampleId1 = 0
    ExampleId2 = 1
    ExampleId3 = 2
    Address = 3
    RadioChannel = 4
    ManualMode = 5
    DroppedPackets = 6
    TargetCtrl = 7
    TxGateDriverPot = 8
    TxPowerAmplifierPot = 9
    TxDdsPot = 10
    TxVicorEnable = 11
    TxGateDriverEnable = 12
    TxPowerEnable = 13
    TxBuck12VDisable = 14
    TxDdsFrequency = 15
    TxZMatchEnable = 16
    TxZFet1 = 17
    TxZFet2 = 18
    TxZFet3 = 19
    TxZFet4 = 20
    Fan1Enable = 21
    Fan2Enable = 22
    TxPowerLevel = 23
    TargetVrect = 24
    VrectTolerance = 25
    DigitalBoardVersion = 26
    RxBatteryConnect = 27
    RxBatteryChargerEnable = 28
    RxZIn1 = 29
    RxZIn2 = 30
    RxZOut1 = 31
    RxZOut2 = 32
    Fan3Enable = 33
    BatteryCurrentMax = 34
    ChargerCurrentLimit = 35
    MobileRxVoltageLimit = 36
    RxBatteryVoltageMin = 37
    BuildHash = 38
    TargetFirmwareId = 39
    TxPlvlMin = 40
    OtaMode = 41
    RxBatteryVoltage = 42
    RxBatteryCurrent = 43
    RxTemperature = 44
    EthIPAddr = 45
    EthNetMask = 46
    EthGateway = 47
    EthDNS = 48
    EthUseDHCP = 49
    EthUseLLA = 50
    DevMACOUI = 51
    DevMACSpecific = 52
    EthInterfacePort = 53
    EthMTU = 54
    EthICMPReply = 55
    EthTCPTTL = 56
    EthUDPTTL = 57
    EthUseDNS = 58
    EthTCPKeepAlive = 59
    ChargeEnable = 60
    I2cAddress = 61
    RxBatteryNumCells = 62
    RxBatterymVPerCell = 63
    TxPowerLimit = 64
    TxWirelessPowerLossLimit = 65
    MaxChargeTime = 66
    LogEnable = 67
    RxBatteryChemistry = 68
    RxWirelessTrackingGain = 69
    IgnoreBatteryCondition = 70
    PowerBoardVersion = 71
    TxDutyCycle = 72
    LEDPower12v = 73
    ModifyPowerLevel = 74
    UpdaterMode = 75
    RadioDebug = 76
    RSSIConnectThresh = 77
    AccessLevel = 78
    ConnectedDevices = 79
    LcdVersion = 80
    RadioConnectionRequest = 81
    CANMessageConfig = 82
    CANID = 83
    OtaCtrl = 84
    CoilCheckBaseStation = 85
    RecoveryChargeEnable = 86
    CANBitRate = 87
    BatteryRestartPerCell = 88
    MaxCVChargeTime = 89    
    
PARAM_TYPE_MAP = {
    ParamID.ExampleId1 : _C_TYPE.get('uint8_t'),
    ParamID.ExampleId2 : _C_TYPE.get('uint16_t'),
    ParamID.ExampleId3 : _C_TYPE.get('int32_t'),
    ParamID.Address : _C_TYPE.get('uint8_t'),
    ParamID.RadioChannel : _C_TYPE.get('uint8_t'),
    ParamID.ManualMode : _C_TYPE.get('uint8_t'),
    ParamID.DroppedPackets : _C_TYPE.get('uint8_t'),
    ParamID.TargetCtrl : _C_TYPE.get('uint32_t'),
    ParamID.TxGateDriverPot : _C_TYPE.get('uint16_t'),
    ParamID.TxPowerAmplifierPot : _C_TYPE.get('uint16_t'),
    ParamID.TxDdsPot : _C_TYPE.get('uint16_t'),
    ParamID.TxVicorEnable : _C_TYPE.get('uint8_t'),
    ParamID.TxGateDriverEnable : _C_TYPE.get('uint8_t'),
    ParamID.TxPowerEnable : _C_TYPE.get('uint8_t'),
    ParamID.TxBuck12VDisable : _C_TYPE.get('uint8_t'),
    ParamID.TxDdsFrequency : _C_TYPE.get('float'),
    ParamID.TxZMatchEnable : _C_TYPE.get('uint8_t'),
    ParamID.TxZFet1 : _C_TYPE.get('uint8_t'),
    ParamID.TxZFet2 : _C_TYPE.get('uint8_t'),
    ParamID.TxZFet3 : _C_TYPE.get('uint8_t'),
    ParamID.TxZFet4 : _C_TYPE.get('uint8_t'),
    ParamID.Fan1Enable : _C_TYPE.get('uint8_t'),
    ParamID.Fan2Enable : _C_TYPE.get('uint8_t'),
    ParamID.TxPowerLevel : _C_TYPE.get('uint16_t'),
    ParamID.TargetVrect : _C_TYPE.get('uint16_t'),
    ParamID.VrectTolerance : _C_TYPE.get('uint16_t'),
    ParamID.DigitalBoardVersion : _C_TYPE.get('uint8_t'),
    ParamID.RxBatteryConnect : _C_TYPE.get('uint8_t'),
    ParamID.RxBatteryChargerEnable : _C_TYPE.get('uint8_t'),
    ParamID.RxZIn1 : _C_TYPE.get('uint8_t'),
    ParamID.RxZIn2 : _C_TYPE.get('uint8_t'),
    ParamID.RxZOut1 : _C_TYPE.get('uint8_t'),
    ParamID.RxZOut2 : _C_TYPE.get('uint8_t'),
    ParamID.Fan3Enable : _C_TYPE.get('uint8_t'),
    ParamID.BatteryCurrentMax : _C_TYPE.get('uint16_t'),
    ParamID.ChargerCurrentLimit : _C_TYPE.get('uint16_t'),
    ParamID.MobileRxVoltageLimit : _C_TYPE.get('uint16_t'),
    ParamID.RxBatteryVoltageMin : _C_TYPE.get('uint16_t'),
    ParamID.BuildHash : _C_TYPE.get('uint32_t'),
    ParamID.TargetFirmwareId : _C_TYPE.get('uint32_t'),
    ParamID.TxPlvlMin : _C_TYPE.get('uint8_t'),
    ParamID.OtaMode : _C_TYPE.get('uint32_t'),
    ParamID.RxBatteryVoltage : _C_TYPE.get('uint32_t'),
    ParamID.RxBatteryCurrent : _C_TYPE.get('uint32_t'),
    ParamID.RxTemperature : _C_TYPE.get('uint32_t'),
    ParamID.EthIPAddr : _C_TYPE.get('uint32_t'),
    ParamID.EthNetMask : _C_TYPE.get('uint32_t'),
    ParamID.EthGateway : _C_TYPE.get('uint32_t'),
    ParamID.EthDNS : _C_TYPE.get('uint32_t'),
    ParamID.EthUseDHCP : _C_TYPE.get('uint8_t'),
    ParamID.EthUseLLA : _C_TYPE.get('uint8_t'),
    ParamID.DevMACOUI : _C_TYPE.get('uint32_t'),
    ParamID.DevMACSpecific : _C_TYPE.get('uint32_t'),
    ParamID.EthInterfacePort : _C_TYPE.get('uint16_t'),
    ParamID.EthMTU : _C_TYPE.get('uint32_t'),
    ParamID.EthICMPReply : _C_TYPE.get('uint8_t'),
    ParamID.EthTCPTTL : _C_TYPE.get('uint8_t'),
    ParamID.EthUDPTTL : _C_TYPE.get('uint8_t'),
    ParamID.EthUseDNS : _C_TYPE.get('uint8_t'),
    ParamID.EthTCPKeepAlive : _C_TYPE.get('uint8_t'),
    ParamID.ChargeEnable : _C_TYPE.get('uint8_t'),
    ParamID.I2cAddress : _C_TYPE.get('uint8_t'),
    ParamID.RxBatteryNumCells : _C_TYPE.get('uint8_t'),
    ParamID.RxBatterymVPerCell : _C_TYPE.get('uint16_t'),
    ParamID.TxPowerLimit : _C_TYPE.get('uint16_t'),
    ParamID.TxWirelessPowerLossLimit : _C_TYPE.get('uint16_t'),
    ParamID.MaxChargeTime : _C_TYPE.get('uint32_t'),
    ParamID.LogEnable : _C_TYPE.get('uint8_t'),
    ParamID.RxBatteryChemistry : _C_TYPE.get('uint8_t'),
    ParamID.RxWirelessTrackingGain : _C_TYPE.get('uint16_t'),
    ParamID.IgnoreBatteryCondition : _C_TYPE.get('uint8_t'),
    ParamID.PowerBoardVersion : _C_TYPE.get('uint8_t'),
    ParamID.TxDutyCycle : _C_TYPE.get('uint8_t'),
    ParamID.LEDPower12v : _C_TYPE.get('uint8_t'),
    ParamID.ModifyPowerLevel : _C_TYPE.get('int16_t'),
    ParamID.UpdaterMode : _C_TYPE.get('uint8_t'),
    ParamID.RadioDebug : _C_TYPE.get('uint8_t'),
    ParamID.RSSIConnectThresh : _C_TYPE.get('uint8_t'),
    ParamID.AccessLevel : _C_TYPE.get('uint8_t'),
    ParamID.ConnectedDevices : _C_TYPE.get('uint16_t'),
    ParamID.LcdVersion : _C_TYPE.get('uint8_t'),
    ParamID.RadioConnectionRequest : _C_TYPE.get('uint32_t'),
    ParamID.CANMessageConfig : _C_TYPE.get('uint8_t'),
    ParamID.CANID : _C_TYPE.get('uint8_t'),
    ParamID.OtaCtrl : _C_TYPE.get('uint8_t'),
    ParamID.CoilCheckBaseStation : _C_TYPE.get('uint32_t'),
    ParamID.RecoveryChargeEnable : _C_TYPE.get('uint8_t'),
    ParamID.CANBitRate : _C_TYPE.get('uint16_t'),
    ParamID.BatteryRestartPerCell : _C_TYPE.get('uint16_t'),
    ParamID.MaxCVChargeTime : _C_TYPE.get('uint32_t'),
}

class AdcID(IntEnum):
    """ ADC Identifiers """
    PacketCount = 0
    Timestamp = 1
    ChargeState = 2
    Flags = 3
    PowerLevel = 4
    VMon3v3 = 5
    VMon5v = 6
    IMon5v = 7
    VMon12v = 8
    IMon12v = 9
    VMonGateDriver = 10
    IMonGateDriver = 11
    VMonPa = 12
    IMonPa = 13
    TMonPa = 14
    VMonBatt = 15
    VMonCharger = 16
    VRect = 17
    TBoard = 18
    ICharger = 19
    IBattery = 20
    TargetIBatt = 21
    ISingleCharger1 = 22
    ISingleCharger2 = 23
    ISingleCharger3 = 24
    RfSense = 25
    VMon48v = 26
    IMon48v = 27
    TMonAmb = 28
    
ADC_TYPE_MAP = {
    AdcID.PacketCount : _C_TYPE.get('uint16_t'),
    AdcID.Timestamp : _C_TYPE.get('uint32_t'),
    AdcID.ChargeState : _C_TYPE.get('uint8_t'),
    AdcID.Flags : _C_TYPE.get('uint16_t'),
    AdcID.PowerLevel : _C_TYPE.get('uint16_t'),
    AdcID.VMon3v3 : _C_TYPE.get('float'),
    AdcID.VMon5v : _C_TYPE.get('float'),
    AdcID.IMon5v : _C_TYPE.get('float'),
    AdcID.VMon12v : _C_TYPE.get('float'),
    AdcID.IMon12v : _C_TYPE.get('float'),
    AdcID.VMonGateDriver : _C_TYPE.get('float'),
    AdcID.IMonGateDriver : _C_TYPE.get('float'),
    AdcID.VMonPa : _C_TYPE.get('float'),
    AdcID.IMonPa : _C_TYPE.get('float'),
    AdcID.TMonPa : _C_TYPE.get('float'),
    AdcID.VMonBatt : _C_TYPE.get('float'),
    AdcID.VMonCharger : _C_TYPE.get('float'),
    AdcID.VRect : _C_TYPE.get('float'),
    AdcID.TBoard : _C_TYPE.get('float'),
    AdcID.ICharger : _C_TYPE.get('float'),
    AdcID.IBattery : _C_TYPE.get('float'),
    AdcID.TargetIBatt : _C_TYPE.get('float'),
    AdcID.ISingleCharger1 : _C_TYPE.get('float'),
    AdcID.ISingleCharger2 : _C_TYPE.get('float'),
    AdcID.ISingleCharger3 : _C_TYPE.get('float'),
    AdcID.RfSense : _C_TYPE.get('float'),
    AdcID.VMon48v : _C_TYPE.get('float'),
    AdcID.IMon48v : _C_TYPE.get('float'),
    AdcID.TMonAmb : _C_TYPE.get('float'),
}

class _ResponseType(IntEnum):
    PARAM_UPDATE = 0x80
    PARAM_RESPONSE = 0x81
    ADC_UPDATE = 0x82
    CONNECTION_STATUS = 0x85
    INCOMING_MESSAGE = 0x86
    RX_ASSOCIATION = 0x87
    GENERAL_DATA_READ = 0x89
    
class AuxiliaryReadType(IntEnum):
    FILENAME_READ = 0x01

class ADCUpdate:
    """ Contains new ADC values that are sent periodically """
    def __init__(self, device, values):
        self.device = device
        self.values = values
        
    def __repr__(self):
        output = "{\nADC Update\n%s\n" % str(self.device)
        for pid, pval in self.values.items():
            output += "%s = %s\n" % (str(pid), str(pval))
        output += "\n}"
        return output
        
class ParamUpdate:
    """ Contains a response to a request to read a value from a parameter """
    def __init__(self, device, param, value):
        self.device = device
        self.param = param
        self.value = value
        
    def __repr__(self):
        output = "{\nParameter Update\nDevice:%s, Parameter:%s = %s\n}"\
         % (str(self.device), str(self.param), str(self.value))
        return output
    
class ParamResponse:
    """ Contains a response to a parameter update request """
    def __init__(self, device, param, status):
        self.device = device
        self.param = param
        self.status = status
        
    def __repr__(self):
        output = "{\nParameter Response\nDevice:%s, Parameter:%s, Status:%s\n}"\
         % (str(self.device), str(self.param), str(self.status))
        return output

class ConnectedDevices:
    """ Contains the current devices available from the current connection """
    def __init__(self, device_list):
        self.devices = device_list

    def __repr__(self):
        return str(self.devices)
        
class IncomingMessage:
    """ Contains a human readable message from a WiBotic device """
    def __init__(self, device, level, message):
        self.device = device
        self.level = level
        self.message = message
        
    def __repr__(self):
        output = "[%s]: %s"\
         % (str(self.device), str(self.message))
        return output

class AuxiliaryDataReadResponse:
    """ Contains a response to an auxiliary data read """
    def __init__(self, device_id, type, data):
        self.type = type
        self.data = data
        self.device_id = device_id #ADDED
    def __repr__(self):
        if self.type == AuxiliaryReadType.FILENAME_READ: # Filename Read
            output = 'syslog.txt\n'
            num_files = int(''.join(str(x) for x in self.data[3:7]))
            log_file = int(''.join(str(x) for x in self.data[7:11]))
            for file_num in range(num_files + 1):
                if file_num == log_file:
                    output += 'RX_' + file_num.zfill(4) + '.csv\n'
                    output += 'TX_' + file_num.zfill(4) + '.csv\n'
        else:
            return 'Unknown data read'
    
class IncomingAssociation:
    """ Contains information about a device that requested association """
    def __init__(self, rssi, mac):
        self.rssi = rssi
        self.mac = mac
    
    def __repr__(self):
        output = "{\nMAC: %s\nRSSI: %s\n}" % (hex(self.mac), str(self.rssi))
        return output
    
def process_data(data):
    """ Takes binary data and processes it into an object that can be 
    easily parsed """
    def param_update(data):
        device_id, param_id, param_value = struct.unpack_from("<BLL", data, 1)
        return ParamUpdate(
                DeviceID(device_id), 
                ParamID(param_id), 
                param_value
               )
        
    def param_response(data):
        device_id, param_id, param_status = struct.unpack_from("<BLB", data, 1)
        return ParamResponse(
                DeviceID(device_id), 
                ParamID(param_id), 
                ParamStatus(param_status)
               )
        
    def adc_update(data):
        device_id = DeviceID(struct.unpack_from("<B", data, 1)[0])
        number_adc_data = (len(data)-2)//6
        adc_values = {}
        for x in range(0, number_adc_data):
            data_location = 2+(x*6)
            adc_id = AdcID(struct.unpack_from("<H", data, data_location)[0])
            adc_convert_as = ADC_TYPE_MAP.get(adc_id)
            adc_data = struct.unpack_from(adc_convert_as, data, data_location + 2)
            adc_values[adc_id] = adc_data[0]
        return ADCUpdate(device_id, adc_values)
        
    def connection_status(data):
        device_as_bit = struct.unpack_from("<H", data, 1)[0]
        parsed_devices = []
        for bit_position in range(0, 15):
            if ((device_as_bit >> bit_position) & 0x01):
                parsed_devices.append(DeviceID(bit_position + 1))
        return ConnectedDevices(parsed_devices)
    
    def incoming_message(data):
        device_id, message_level = struct.unpack_from("<BB", data, 1)
        return IncomingMessage(
                DeviceID(device_id),
                message_level,
                data[3:].decode("utf-8")
               )
    
    def auxiliary_data_read(data):
        device_id = struct.unpack_from("<B", data, 1)[0]
        read_type = struct.unpack_from("<B", data, 2)[0]
        
        return AuxiliaryDataReadResponse(
                DeviceID(device_id),
                AuxiliaryReadType(read_type),
                data[3:] 
               )
    
    def association_read(data):
        device_id, rssi, mac = struct.unpack_from("<BB6s", data, 1)
        
        return IncomingAssociation(
                rssi,
                int.from_bytes(mac, byteorder="little", signed=False)
               )

    event = {
        _ResponseType.PARAM_UPDATE: param_update,
        _ResponseType.PARAM_RESPONSE: param_response,
        _ResponseType.ADC_UPDATE: adc_update,
        _ResponseType.CONNECTION_STATUS: connection_status,
        _ResponseType.INCOMING_MESSAGE: incoming_message,
        _ResponseType.GENERAL_DATA_READ: auxiliary_data_read,
        _ResponseType.RX_ASSOCIATION: association_read
    }
    response_type = _ResponseType(data[0])
    return event[response_type](data)
        
class RequestConnectionStatus:
    """ Builds a binary packet containing a request to send
    which devices are currently connected to the WiBotic system """
    def as_packet(self):
        ACTION_REQ_CONNECTION_STATUS = 0x06
        return bytearray([ACTION_REQ_CONNECTION_STATUS])

class RequestAuxiliaryDataRead:
    """ Builds a binary packet containing a request to send
    a general data read"""
    def __init__(self, read_type):
        self.type = read_type

    def as_packet(self):
        ACTION_REQ_DATA_READ = 0x07
        packed_data = struct.pack(
            ">BB",
            ACTION_REQ_DATA_READ,
            self.type
        )
        return bytearray(packed_data)
        
class ParamReadRequest:
    """ Builds a binary packet containing a request to read a parameter 
    from the WiBotic system """
    def __init__(self, destination_device, parameter):
        self.dest = destination_device
        self.param = parameter
        
    def as_packet(self):
        ACTION_READ_PARAMETER = 0x01
        packed_data = struct.pack(
            ">BBL", 
            ACTION_READ_PARAMETER, 
            self.dest, 
            self.param
        )
        return bytearray(packed_data)
    
class ParamWriteRequest:
    """ Builds a binary packet containing a request to write a new 
    value to a parameter on the WiBotic system """
    def __init__(self, destination_device, parameter, new_value):
        self.dest = destination_device
        self.param = parameter
        self.value = new_value
        
    def as_packet(self):
        ACTION_WRITE_PARAMETER = 0x03
        packed_data = struct.pack(
            ">BBLL", 
            ACTION_WRITE_PARAMETER, 
            self.dest, 
            self.param,
            self.value
        )
        return bytearray(packed_data)
        
class SubscribeRequest:
    """Builds a binary packet containing a request to subscribe to a topic
    in the WiBotic system"""
    def __init__(self, topic):
        self.topic = topic
    
    def as_packet(self):
        ACTION_SUBSCRIBE = 0x11
        packed_data = struct.pack(
          ">BB",
          ACTION_SUBSCRIBE,
          self.topic          
        )
        return bytearray(packed_data)

class UnsubscribeRequest:
    """Builds a binary packet containing a request to unsubscribe from a topic
    in the WiBotic system"""
    def __init__(self, topic):
        self.topic = topic
    
    def as_packet(self):
        ACTION_UNSUBSCRIBE = 0x12
        packed_data = struct.pack(
          ">BB",
          ACTION_UNSUBSCRIBE,
          self.topic          
        )
        return bytearray(packed_data)