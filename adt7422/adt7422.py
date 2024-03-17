# The MIT License (MIT)
# Copyright (c) 2024 Ievgen Raievskiy
#
# For creation used Karl-Petter Lindegaard  smbus2.py
# https://github.com/kplindegaard/smbus2/blob/master/smbus2/smbus2.py
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import math
from smbus2 import SMBus
########################################################################################################################

TEMPERATURE_VALUE_MSB = 0x00                    # msb temperature register address
TEMPERATURE_VALUE_LSB = 0x01                    # lsb temperature register address
STATUS = 0x02                                   # status register address
CONFIGURATION = 0x03                            # configuration register address
T_HIGH_SETPOINT_MSB = 0x04                      # msb high temperature register address (default value is 64 C)
T_HIGH_SETPOINT_LSB = 0x05                      # lsb high temperature register address (default value is 64 C)
T_LOW_SETPOINT_MSB = 0x06                       # msb high temperature register address (default value is 10 C)
T_LOW_SETPOINT_LSB = 0x07                       # lsb high temperature register address (default value is 10 C)
T_CRIT_SETPOINT_MSB = 0x08                      # msb critical temperature register address (default value is 147 C)
T_CRIT_SETPOINT_LSB = 0x09                      # lsb critical temperature register address (default value is 147 C)
T_HYST_SETPOINT = 0x0A                          # hysteresis register address (default value is 5 C)
ID = 0x0B                                       # id register address (value is 0xCB)           
RESERVED_0 = 0x0C                               # reserved register address (default value 0xXX)
RESERVED_1 = 0x0D                               # reserved register address (default value 0xXX)
RESERVED_2 = 0x2E                               # reserved register address (default value 0xXX)
SOFTWARE_RESET = 0x2F                           # reset register address (default value 0xXX)                         

########################################################################################################################


class ADT7422:

    def __init__(self, smbus=1, device=0x49):
        self.smbus = smbus
        self.device = device
        self.bus = 0
        
    def __del__(self):
        pass
       
    def open_smbus(self):
        """
        This method used to check SMBus number, available adt7422 addresses to open SMBus.
        The method returns boolean value (true if SMBus is opened or false if SMBus closed) and errors text message.
        """
        
        error = False
        if self.smbus != 0 and self.smbus != 1:
            error = True
            print("SMBus ERROR")
        if self.device != 0x48 and self.device != 0x49 and self.device != 0x4A and self.device != 0x4B:
            error = True
            print("ADT7422 ADDRESS ERROR") 
        if not error:
            self.bus = SMBus(self.smbus)        
            self.bus.open(self.smbus)           
            print("SMBus opened")
            
    def close_smbus(self):
        """
        This method used to close SMBus
        """
        
        SMBus(self.smbus).close()
        return "SMBus closed"
        
    def read_register(self, address):
        """
        This method used to read register with the specified address
        """
        
        self.bus.write_byte(self.device, 0x00)
        return self.bus.read_byte_data(self.device, address)
        
    def write_register(self, address, data):
        """
        This method used to write data into register with the specified address
        """

        self.bus.write_word_data(self.device, address, data)
        return     
        
    def reset(self):
        """
        This method used to reset ADT7422.
        To reset the ADT7422 without having to reset the entire I2 C bus, an explicit reset command is provided.
        This command uses a particular address pointer word as a command word to reset the device and upload all
        default settings.
        """

        bus = self.bus
        device = self.device
        reset_flag = False
        bus.write_byte(device, 0x00)
        bus.read_byte_data(device, SOFTWARE_RESET, 0x00)
        time.sleep(0.1)
        data = bus.read_byte_data(device, CONFIGURATION)
        if data == 0:
            reset_flag = True
        return reset_flag

    def adc_complete(self):
        """
        This method used to check STATUS register (RDY bit) and determinate end of A/D conversation.
        STATUS REGISTER bit 7 goes low when the temperature conversion result is written into the
        temperature value register.
        """
        
        self.bus.write_byte(self.device, 0x00)
        data = self.bus.read_byte_data(self.device, STATUS)
        if data & 0x80 == 0x00:
            return True
        return False

    def get_temp(self):
        """
        This method used to obtain temperature measurement data.
        This function checks the Configuration register to determine the width of data to be read.  
        """
        
        self.bus.write_byte(self.device, 0x00)
        resolution = self.bus.read_byte_data(self.device, CONFIGURATION)
        self.bus.write_byte(self.device, 0x00)
        temperature_msb = self.device.read_byte_data(self.device, TEMPERATURE_VALUE_MSB)
        self.bus.write_byte(self.device, 0x00)
        temperature_lsb = self.bus.read_byte_data(self.device, TEMPERATURE_VALUE_LSB)
        temperature = (temperature_msb << 8) | temperature_lsb
        if (resolution & 0x80) == 0x80:
            if temperature_msb & 0x8000 == 0x0000:
                temperature = temperature / 128
            else:
                temperature &= 0x7FFF
                temperature = -(temperature / 128)
        else:
            if temperature & 0x8000 == 0x0000:
                temperature = temperature >> 3
                temperature = temperature / 16
            else:
                temperature &= 0x7FFF
                temperature = temperature >> 3
                temperature = -(temperature / 16)
        return temperature
    
    def get_flags(self):
        """
        This method used to read and return boolean flags values from TEMPERATURE_VALUE_MSB register.
        Reading Bit 0 to Bit 2 that are event alarm flags for the TLOW, THIGH, and TCRIT setpoint most significant byte
        registers and least significant byte registers. The default setting for the alarm flags 0.
        """
        
        t_low_flag = False
        t_high_flag = False
        t_crit_flag = False
        data = self.bus.read_word_data(self.device, TEMPERATURE_VALUE_MSB)
        data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        if data & 0x0001 == 0x0001:
            t_low_flag = True
        if data & 0x0002 == 0x0002:
            t_high_flag = True
        if data & 0x0004 == 0x0004:
            t_crit_flag = True
        return t_low_flag, t_high_flag, t_crit_flag

    def get_status(self):
        """
        This method used to read and return STATUS register value.
        The default setting for the status register is 0x00.
        """
        
        self.bus.write_byte(self.device, 0x00)
        status = self.bus.read_byte_data(self.device, STATUS)
        return status 

    def set_config(self, data):
        """
        This method used to write and return CONFIGURATION register value.
        This 8-bit write register stores various configuration modes for the ADT7422, including shutdown mode,
        overtemperature and undertemperature interrupts, one shot mode, continuous conversion mode, 
        interrupt pins polarity, and overtemperature fault queues.
        """
    
        self.bus.write_byte_data(self.device, CONFIGURATION, data)
        return

    def get_config(self):
        """
        This method used to read and return CONFIGURATION register value.
        This 8-bit write register stores various configuration modes for the ADT7422, including shutdown mode,
        overtemperature and undertemperature interrupts, one shot mode, continuous conversion mode, 
        interrupt pins polarity, and overtemperature fault queues.
        The default setting for the configuration register is 0x00.
        """
        
        self.bus.write_byte(self.device, 0x00)
        configuration_word = self.bus.read_byte_data(self.device, CONFIGURATION)
        return configuration_word

    def get_high_setpoint(self):
        """
        This method used to read, convert and return T_HIGH_SETPOINT_MSB and T_HIGH_SETPOINT_LSB registers
        values in degrees. The default setting for the THIGH setpoint register is 64°C.
        """
        
        data = self.bus.read_word_data(self.device, T_HIGH_SETPOINT_MSB)
        data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        if data & 0x8000 == 0x0000:
            high_setpoint = data / 128
        else:
            data &= 0x7FFF
            high_setpoint = -(data / 128)
        return high_setpoint

    def set_high_setpoint(self, data):
        """
        This method used to convert (from decimal), write and return T_HIGH_SETPOINT_MSB and
        T_HIGH_SETPOINT_LSB registers.
        """
        
        if (data > 125) | (data < -40):
            msg = "Value out of range"
            return msg
        if data > 0:
            data = int(data * 128)
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        else:
            data = (-(int(data * 128))) | 0x8000
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
    
        self.bus.write_word_data(self.device, T_HIGH_SETPOINT_MSB, data)
        return

    def get_low_setpoint(self):
        """
        This method used to read, convert and return T_LOW_SETPOINT_MSB and T_LOW_SETPOINT_LSB registers
        values in degrees. The default setting for the TLOW setpoint register is 10°C.
        """
        
        data = self.bus.read_word_data(self.device, T_LOW_SETPOINT_MSB)
        data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        if data & 0x8000 == 0x0000:
            low_setpoint = data / 128
        else:
            data &= 0x7FFF
            low_setpoint = -(data / 128)
        return low_setpoint

    def set_low_setpoint(self, data):
        """
        This method used to convert (from decimal), write and return T_LOW_SETPOINT_MSB and
        T_LOW_SETPOINT_LSB registers.
        """
        
        if (data > 125) | (data < -40):
            msg = "Value out of range"
            return msg
        if data > 0:
            data = int(data * 128)
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        else:
            data = (-(int(data * 128))) | 0x8000
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
    
        self.bus.write_word_data(self.device, T_LOW_SETPOINT_MSB, data)
        return

    def get_crit_setpoint(self):
        """
        This method used to read, convert and return T_CRIT_SETPOINT_MSB and T_CRIT_SETPOINT_LSB registers
        values in degrees. The default setting for the TCRIT setpoint register is 147°C.
        """
        
        data = self.bus.read_word_data(self.device, T_CRIT_SETPOINT_MSB)
        data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        if data & 0x8000 == 0x0000:
            crit_setpoint = data / 128
        else:
            data &= 0x7FFF
            crit_setpoint = -(data / 128)
        return crit_setpoint

    def set_crit_setpoint(self, data):
        """
        This method used to convert (from decimal), write and return T_CRIT_SETPOINT_MSB and
        T_CRIT_SETPOINT_LSB registers.
        """
        
        if (data > 125) | (data < -40):
            msg = "Value out of range"
            return msg
        if data > 0:
            data = int(data * 128)
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
        else:
            data = (-(int(data * 128))) | 0x8000
            data = ((data & 0x00FF) << 8) | ((data & 0xFF00) >> 8)
    
        self.bus.write_word_data(self.device, T_CRIT_SETPOINT_MSB, data)
        return

    def get_hyst_setpoint(self):
        """
        This function used to read, convert and return 8 bit T_HYST_SETPOINT register value in degrees.
        The default setting for the THIST setpoint register is 5°C.
        """
        
        self.bus.write_byte(self.device, 0x00)
        hyst_setpoint = self.bus.read_byte_data(self.device, T_HYST_SETPOINT)
        return hyst_setpoint

    def set_hyst_setpoint(self, data):
        """
        This function used to convert (from decimal), write and return T_HYST_SETPOINT register.
        """
        
        if (data > 15) | (data < 0):
            msg = "Value out of range"
            return msg
        if math.modf(data)[0] != 0:
            print("Error. Set an integer value")
            return
        self.bus.write_word_data(self.device, T_HYST_SETPOINT, data)
        return 
    
    def get_id(self):
        """
        This function used to reading and return ID register value. ID register value is 0xCB.
        This 8-bit read only register stores the manufacture ID in Bit 3 to Bit 7 and the silicon revision in
        Bit 0 to Bit 2. The default setting for the ID register is 0xCB.
        """
        
        self.bus.write_byte(self.device, 0x00)
        return self.bus.read_byte_data(self.device, ID)
