![pi_version](https://img.shields.io/badge/python%20-version%7C%203.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C-blue
)
# ADT7422 Temperature sensor quick start with Raspberry Pi

**adt7422.py** - contains methods for initializing the temperature sensor, reading and writing registers, as well as register addresses.

**selftest.py** - test program to fully verify the functionality of the sensor.

## Introduction

### adt7422.py currently supported features are:
- __init__
- open_smbus
- close_smbus
- get_register
- set_register
- reset
- adc_complete
- get_temp
- get_flags
- get_status
- set_config
- get_config
- get_high_setpoint
- set_high_setpoint
- get_low_setpoint
- set_low_setpoint
- get_crit_setpoint
- set_crit_setpoint
- get_hyst_setpoint
- set_hyst_setpoint
- get_id
______________________________________________________________________________

## Code examples

### Example 1: Init smbus and adt7422 I2C address
Use this method to change SMBus device and adt7422 I2C address. 
The temperature sensor can have one of four addresses as i2c device (0x48, 0x49, 0x4A or 0x4B).
Rasberry Pi computers has SMBus 0 or SMBus 1.
Calling this method set current adt7422 sensor i2c address and SMBus device.
This method uses EV-TempSense-ARDZ address (0x49) by default.
  
    # set SMBus device 0 and i2c address 0x48      
    __init__(0, 0x48)
       
### Example 2: Open SMBus
Use this method to open SMBus and check that adt7422 i2c address set correctly (See Example 1 for details).
The method returns error messages:
    'SMBus ERROR' (SMBus device not equal 0 or 1)
    'ADT7422 ADDRESS ERROR' (i2c address not equal 0x48, 0x49, 0x4A or 0x4B)
The method returns established message:
    SMBus opened

    # example 1
    # SMBus = 1, EV-TempSense-ARDZ address = 0x49
    # open SMBus    
    open_smbus()
    # SMBus opened

### Example 3: Close SMBus
Use this method to close SMBUS. SMBus device defined in init function (see Example 1).

    # close current SMBus  
    close_smbus()
    # SMBus closed

### Example 4: Read ADT7422 register
Use this method use to read adt7422 registers. 

    # read id register
    get_register(0x0B)
    # 203
        
### Example 5: Write ADT7422 register
Use this method use to write adt7422 registers. 

    # write 0x10 value into configuration register 
    set_register(0x03, 0x10)

### Example 6: Reset ADT7422
Use this method to reset ADT7422.
To reset the ADT7422 without having to reset the entire I2C bus, an explicit reset command is provided.
This command uses a particular address pointer word as a command word to reset the device and upload all
default settings. Reset method returns reset_flag = True if reset process completed successfully or False if reset process not completed successfully
  
    # reset ADT7422 temperature sensor
    reset()
    # True   

### Example 7: Read status ADT7422
Use this method for reading and returning STATUS (address 0x00) register value.
The default setting for the status register is 0x00.

    # read status register value 
    get_status()
    # 0

### Example 8: Check ADC complete 
Use this method to check bit 7 (RDY) of the STATUS register. 
This method returns True if when the temperature conversion result is written into the temperature value register.
This method returns False if the temperature conversion result is not written into the temperature value register.

    # check adc complete
    adc_complete()
    # True

### Example 9: Read temperature
This method return 16 bit or 13 bit result of analog to digital conversation.
The method reads bit 7 of the CONFIGURATION (address 0x03) register to determine the resolution of the data from the ADC.
The method selects the algorithm for converting binary data from the ADC into a decimal floating point value.
    
    # get adc result
    def get_temp()
    # 22.3125

### Example 10: Read flags
Use this method for reading and returning boolean flags values from TEMPERATURE_VALUE_MSB (address 0x00) register.
Reading Bit 0 to Bit 2 that are event alarm flags for the TLOW, THIGH, and TCRIT setpoint most significant byte
registers and least significant byte registers. The default setting for the alarm flags 0.
This method returns True or False for each flag.

    # read flags 
    get_flags()
    # (False, False, True)
    # TLOW flag is False, THIGH flag is False, TCRIT flag is True 

### Example 11: Write ADT7422 configuration 
Use this method for writing CONFIGURATION (address 0x03) register value.
This 8-bit write register stores various configuration modes for the ADT7422, including shutdown mode,
overtemperature and undertemperature interrupts, one shot mode, continuous conversion mode, 
interrupt pins polarity, and overtemperature fault queues.

    # write configuration register with 0x10 value
    set_config(0x10)

### Example 12: Read ADT7422 configuration
Use this method for reading and returning CONFIGURATION (address 0x03) register value.
This method returns configuration register value in decimal. The default setting for the configuration register is 0x00.

    # read confuguration register
    get_config()
    # 16 dec is equal 0x10 hex
    
### Example 13: Read high setpoint value 
Use this method for reading, converting and returning T_HIGH_SETPOINT_MSB (address 0x04) and T_HIGH_SETPOINT_LSB (address 0x05) registers
values in decimal. The default setting for the high setpoint value is 64°C.

    # read high setpoint value
    get_high_setpoint()
    # 64.0

### Example 14: Write high setpoint value
This method used for converting data (from decimal to binary), writing and returning T_HIGH_SETPOINT_MSB (address 0x04) and T_HIGH_SETPOINT_LSB (address 0x05) registers.
High setpoint may be integer or float and must be in range from -40 to 150.

    # example 1
    # write high setpoint value 35
    set_high_setpoint(35)

    # example 2
    # write float high setpoint value 25.625
    set_high_setpoint(25.625)

    # example 3
    # write high setpoint value 200
    set_high_setpoint(200)
    # 'Value out of range'

### Example 15: Read low setpoint value
This method used for reading, converting and returning T_LOW_SETPOINT_MSB (address 0x06) and T_LOW_SETPOINT_LSB (address 0x06) registers values in decimal.
The default setting for the low setpoint value is 10°C.

    # read low setpoint value 
    get_low_setpoint()
    # 10

### Example 16: Write low setpoint value
This method used for converting (from decimal), writing and returning T_LOW_SETPOINT_MSB (address 0x06) and T_LOW_SETPOINT_LSB (address 0x07) registers.
Low setpoint may be integer or float and must be in range from -40 to 150.
    
    # example 1
    # write low setpoint value -20
    set_low_setpoint(-20)

    #example 2
    # write float low setpoint value -2.9
    set_low_setpoint(-2.9)

    # example 3
    # write low setpoint value -150
    set_high_setpoint(-150)
    # 'Value out of range'

### Example 17: Read critical setpoint value
This method used for reading, converting and returning T_CRIT_SETPOINT_MSB (address 0x08) and T_CRIT_SETPOINT_LSB (address 0x09) registers values in decimal.
The default setting for the critical setpoint value is 147°C.
    
    # read critical setpoint value
    get_crit_setpoint()
    # 147

### Example 18: Write critical setpoint value
This method used for converting (from decimal), writing and returning T_CRIT_SETPOINT_MSB (address 0x08) and T_CRIT_SETPOINT_LSB (address 0x09) registers.
Critical setpoint may be integer or float and must be in range from -40 to 150.

    # example 1
    # write critical setpoint value 125
    set_crit_setpoint(125)

    # example 2
    # write float critical setpoint value 125.5
    set_crit_setpoint(125.5)

### Example 19: Read hysteresis setpoint value
This method used for reading, converting and returning 8 bit T_HYST_SETPOINT (0x0A) register value in decimal.
The default setting for the hysteresis setpoint value is 5°C.
    
    # Read hysteresis setpoint value
    get_hyst_setpoint()

### Example 20: Write hysteresis setpoint value
This method used for converting (from decimal), writing and returning T_HYST_SETPOINT (address 0x0A) register.

    # example 1
    # write integer setpoint value from 0 to 15 degrees (Celcius)
    # write integer setpoint value 3
    set_hyst_setpoint(3)

    # example 2
    # write out of range integer setpoint value 25
    set_hyst_setpoint(25)
    # 'Value out of range'

    # example 3
    # write float setpoint value 4.5 (Celcius)
    set_hyst_setpoint(4.5)
    # 'Error. Set an integer value'

### Example 21: Read ID register
This method used for reading and returning ID register value. ID register value is 0xCB.
This 8-bit read only register stores the manufacture ID in Bit 3 to Bit 7 and the silicon revision in Bit 0 to Bit 2.
The default setting for the ID register is 0xCB.

    # read id register
    get_id()
    # 203
______________________________________________________________________________

## ADT7422 testing program selftest.py currently supported features are:

- reset_test()

    This function used to reset adt7422 sensor.
    Then reads and returns the values of all registers and checks them against the default values.


- registers_test()
    
    This function used to check that all sensor registers can be written correctly.


- get_adc()

    This function used to get temperature value.


- ctmode_test()

    This function used to test overtemperature, undertemperature and critical temperature events.


- continuous_mode()

    This function used to test continuous mode.


- one_shot_mode()

    This function is used to test one shot mode.


- one_sps_mode()

    This function is used to test 1 SPS mode.


- shutdown()

    This function is used to test shutdown mode.
______________________________________________________________________________
## Software installation

- Install smbus2 package
```pyton
sudo pip3 install smbus2
```

- Install adt7422 package
```pyton
sudo pip3 install adt7422
```

## Hardware installation
This example of hardware installation using [Raspberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) or other Raspberry Pi and [EV-TempSense-ARDZ](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/EV-TempSense-ARDZ.html) 
- Connect ground wire for [EV-TempSense-ARDZ](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/EV-TempSense-ARDZ.html) 
- Connect 3.3V power supply for [EV-TempSense-ARDZ](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/EV-TempSense-ARDZ.html)
- Connect Raspberry Board to ADT7422 using I2C interface (using [Raspberry Pi 3 Model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/))
  - I2C serial Data to GPIO2 
  - I2C serial Clock to GPIO3
- Plug power cord to Raspberry Board

### Errors
- Errors may appear due to lack of power and I2C bus signals.
- Check supply, ground, serial clock and data wires connection.