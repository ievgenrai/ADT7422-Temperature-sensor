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


from adt7422 import ADT7422
import time
import sys

sensor = ADT7422()


def start_test():
    set_smbus_i2c()
    sensor.open_smbus()
            

def set_smbus_i2c():
    """
    This function used to set smbus device and i2c adt7422 address and then open SMBus.
    """
    while True:
        print("Set SMBus (0 or 1)")
        smbus_device = int(input())
        if smbus_device == 0 or smbus_device == 1:
            break
        else:
            print("SMBus ERROR", smbus_device)

    while True:
        print("Set I2C device address (ADT7422 address), hex or dec: \n 0x48 (72 dec)")
        print("0x49 (73 dec) for Eval Board")
        print("0x4A (74 dec)")
        print("0x4B (75 dec)")
        i2c_device = int(input())
        if i2c_device != 0x48 and i2c_device != 0x49 and i2c_device != 0x4A and i2c_device != 0x4B:
            print("ADT7422 ADDRESS ERROR")
        else:
            break

    sensor.__init__(smbus_device, i2c_device)


def reset_test():
    """
    This function used to reset adt7422 sensor.
    Then reads and returns the values of all registers and checks them against the default values.
    """
    # read and check registers value after reset
    sensor.reset()
    time.sleep(0.1)

    sensor_id = sensor.get_id()
    if sensor_id == 0xCB:
        print('Sensor ID: passed', sensor_id)
    else:
        print('Sensor ID register reading test: error')

    sensor_status = sensor.get_status()
    if sensor_status == 128:
        print('Status register check: passed', sensor_status)
    else:
        print('Status register reading test: error')

    sensor_configuration = sensor.get_config()
    if sensor_configuration == 0:
        print('Default Configuration check: passed', sensor_configuration)
    else:
        print('Configuration register reading test: error')

    sensor_high_setpoint = sensor.get_high_setpoint()
    if sensor_high_setpoint == 64:
        print('Default High setpoint value check: passed', sensor_high_setpoint)
    else:
        print('High setpoint register reading test: error')

    sensor_low_setpoint = sensor.get_low_setpoint()
    if sensor_low_setpoint == 10:
        print('Default Low setpoint value check: passed', sensor_low_setpoint)
    else:
        print('Low setpoint register reading test: error')

    sensor_crit_setpoint = sensor.get_crit_setpoint()
    if sensor_crit_setpoint == 147:
        print('Default Crit setpoint value check: passed', sensor_crit_setpoint)
    else:
        print('Crit setpoint register reading test: error')

    sensor_hyst_setpoint = sensor.get_hyst_setpoint()
    if sensor_hyst_setpoint == 5:
        print('Default Hyst setpoint value check: passed', sensor_hyst_setpoint)
    else:
        print('Hyst setpoint register reading test: error')


def registers_test():
    """
    This function used to check that all sensor registers can be written correctly.
    """
    sensor.reset()
    time.sleep(0.1)

    sensor.set_config(0x80)
    if sensor.get_config() != 0x80:
        print('Configuration register writting: error')
    else:
        print('Configuration register writting test: passed')

    sensor.set_high_setpoint(4)
    if sensor.get_high_setpoint() != 4:
        print('High setpoint register writting: error')
    else:
        print('High setpoint register writting test: passed')

    sensor.set_low_setpoint(8)
    if sensor.get_low_setpoint() != 8:
        print('Low setpoint register writting: error')
    else:
        print('Low setpoint register writting test: passed')

    sensor.set_crit_setpoint(16)
    if sensor.get_crit_setpoint() != 16:
        print('Crit setpoint register writting: error')
    else:
        print('Crit setpoint register writting test: passed')

    sensor.set_hyst_setpoint(3)
    if sensor.get_hyst_setpoint() != 3:
        print('Hyst setpoint register writting: error')
    else:
        print('Hyst setpoint register writting test: passed')


def get_adc():
    """
    This function used to get temperature value.
    """
    time.sleep(0.5)
    if sensor.adc_complete():
        return sensor.get_temp()
    else:
        print('Read ADC result error')


def ctmode_test():
    """
    This function used to test overtemperature, undertemperature and critical temperature events.
    """
    sensor.reset()
    time.sleep(0.1)
    sensor.set_config(0x10)
    if sensor.get_config() != 0x10:
        print('Comrarator mode setting: error')
    else:
        print('Comrarator mode is set: passed')

    sensor.set_hyst_setpoint(1)
    print('Hyst setpoint:', sensor.get_hyst_setpoint())

    time.sleep(0.5)
    if sensor.adc_complete():
        adc_result = sensor.get_temp()
        if 149 < adc_result < -38:
            print('Current temperature out of range')
        print('Current temperature:', adc_result)
        test_setpoint = round(adc_result, 0)
        sensor.set_crit_setpoint(test_setpoint - 2)
        sensor.set_high_setpoint(test_setpoint - 3)
        sensor.set_low_setpoint(test_setpoint + 1)
    else:
        print('Get adc result error')

    time.sleep(0.5)
    print('CRIT setpoint value:', sensor.get_crit_setpoint())
    if sensor.get_flags()[2]:
        print('TCRIT flag test: passed')
    else:
        print('TCRIT flag test: error')

    print('High setpoint value:', sensor.get_high_setpoint())
    if sensor.get_flags()[1]:
        print('THIGH flag test: passed')
    else:
        print('THIGH flag test: error')

    print('LOW setpoint value:', sensor.get_low_setpoint())
    if sensor.get_flags()[0]:
        print('TLOW flag test: passed')
    else:
        print('TLOW flag test: error')


def continuous_mode():
    """
    This function used to test continuous mode.
    """
    sensor.reset()
    time.sleep(0.1)
    sensor.set_config(0x10)
    if sensor.get_config() == 0x10:
        print('Continuous mode setting: passed')
    else:
        print('Continuous mode setting: error')
        return

    print('Wait 10 samples:')
    time.sleep(0.5)
    counter = 10
    adc_counter = 10
    while counter != 0:
        if sensor.adc_complete():
            print('Current temperature value:', sensor.get_temp())
            adc_counter -= 1
            time.sleep(0.3)
        counter -= 1
    if adc_counter == 0:
        print('Continuous mode test: passed')
    else:
        print('Continuous mode test: error')


def one_shot_mode():
    """
    This function is used to test one shot mode.
    """
    sensor.reset()
    time.sleep(0.1)
    sensor.set_config(0x20)
    if sensor.get_config() == 0x20:
        print('One shot mode setting: passed')
    else:
        print('One shot mode setting: error')
        return

    time.sleep(0.5)
    if sensor.adc_complete():
        print('Current temperature value:', sensor.get_temp())
    else:
        print('One shot mode test: error')
        return

    if sensor.get_config() == 0x60:
        print('One shot mode test: passed')
    else:
        print('One shot mode test: error')


def one_sps_mode():
    """
    This function is used to test 1 SPS mode.
    """
    sensor.reset()
    time.sleep(0.1)
    sensor.set_config(0x40)
    if sensor.get_config() == 0x40:
        print('1 SPS mode setting: passed')
    else:
        print('1 SPS mode setting: error')
        return

    print('Wait 10 samples:')
    time.sleep(0.5)
    counter = 10
    while counter != 0:
        time.sleep(1)
        if sensor.adc_complete():
            print('Current temperature value:', sensor.get_temp())
        else:
            print('1 SPS mode test: error')
            return
        counter -= 1

    print('1 SPS mode test: passed')


def shutdown():
    """
    This function is used to test shutdown mode.
    """
    sensor.reset()
    time.sleep(0.1)
    sensor.set_config(0x60)
    if sensor.get_config() == 0x60:
        print('Shutdown mode setting: passed')
    else:
        print('Shutdown mode setting: error')
        return


def full_test():
    """
    This function is used to test all functions of the adt7422
    """
    start_test()

    print("\nReset test:")
    registers_test()

    print("\nCurrent temperature test:")
    sensor.reset()
    print('13 bit temperature value (degree):', get_adc())

    print("\nRegisters test:")
    registers_test()

    print("\nCurrent temperature test:")
    print('16 bit temperature value (degree):', get_adc())

    print("\nCT Mode test:")
    ctmode_test()

    print("\nContinuous Mode test:")
    continuous_mode()

    print("\nOne shot Mode test:")
    one_shot_mode()

    print("\n1 SPS Mode test:")
    one_sps_mode()

    print("\nShutdown test:")
    shutdown()


try:
    full_test()
except OSError:
    print("OSError. Check ADT7422 I2C address adn SDA/SCL connection")

sys.exit()
