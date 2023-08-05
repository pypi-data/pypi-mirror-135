#############
# MIT License
#
# Copyright (C) 2020 ThoughtForge Inc.
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
#############

import copy
import math
import numpy as np


def calc_sensor_range(min_range, range_multiplier, range_length):
    sensor_range_list = [min_range * np.power(range_multiplier, i) for i in range(range_length)]
    # print("Generating sensor range:", sensor_range_list)
    return make_sensor_range(sensor_range_list)


def make_sensor_range(range_list):
    return [[-range_mag, range_mag] for range_mag in range_list]
    
class SensorGroup:
    """ This is a simple abstraction to consolidate handling for a simple sensor value
    with possibly multiple entrypoints into the network """

    def __init__(self, 
                 update_function,
                 base_sensor_name):
        self.update_function = update_function
        self.base_sensor_name = base_sensor_name
        self._base_block_name = self.base_sensor_name + '_block'
        self.refcount = 0

    def set_refcount(self, refcount):
        self.refcount = refcount

    def add_to_json(self, 
                    json_specification, 
                    sensor_params,
                    sensor_block_params_dict,
                    sensors):
        # if sensor isn't used, don't add to json
        if self.refcount > 0:
            # add sensor_definition
            local_params = copy.deepcopy(sensor_params)
            local_params['name'] = self.base_sensor_name
            local_params['sensor_range'] = sensors
            json_specification['sensors'].append(local_params)
            # add block specification for sensor block
            local_block_params = copy.deepcopy(sensor_block_params_dict)
            local_block_params['name'] = self._base_block_name
            # on outgoing sensor connections--make non-bi-directional?
            if local_params['type'] == 'MULTI':
                # for 'MULTI' sensors, scale length by sensor range
                sensors_per_layer = 1
                block_length = math.ceil(float(len(sensors)) / float(sensors_per_layer))
                local_block_params['length'] = block_length        
            json_specification['blocks'].append(local_block_params)
            self.block_name = self._base_block_name
            json_specification['connections'].append(
                {'source': self.base_sensor_name, 'dest': self.block_name})            

    def update_sensor_group(self, sensor_values_dict):
        """ Queries for updated sensor values and sets the sensor values appropriately """
        if self.refcount > 0:
            sensor_val = self.update_function()
            # print(self.base_sensor_name, ":", sensor_val)
            sensor_values_dict[self.base_sensor_name] = sensor_val


class MotorGroup:
    def __init__(self, 
                 base_motor_name):
        self.external_ref_count = 0
        self.base_motor_name = base_motor_name
        self.block_name = self.base_motor_name + '_block'

    def add_to_json(self, 
                    json_specification, 
                    motor_params,
                    motor_block_params_dict):
        # add motor definition
        local_params = copy.deepcopy(motor_params)
        local_params['name'] = self.base_motor_name
        added_nodes = json_specification['motor_added_nodes'] if 'motor_added_nodes' in json_specification else 0
        local_params['category'] = local_params['category'] * (self.external_ref_count)
        json_specification['motors'].append(local_params)
        # add block specification for motor block
        local_block_params = copy.deepcopy(motor_block_params_dict)
        local_block_params['name'] = self.block_name
        local_block_params['width'] = (motor_block_params_dict['width'] + added_nodes) * self.external_ref_count
        local_block_params['layer_stride'] = int(motor_block_params_dict['layer_stride'] * self.external_ref_count)
        local_block_params['interlayer_stride'] = int(motor_block_params_dict['interlayer_stride'] * self.external_ref_count)
        local_block_params['outgoing_interblock_stride'] = int(motor_block_params_dict['outgoing_interblock_stride'] * self.external_ref_count)
        json_specification['blocks'].append(local_block_params)
        # connect motors and blocks
        json_specification['connections'].append(
            {'source': self.base_motor_name, 'dest': self.block_name})            

    def increment_external_ref_count(self, num=1):
        self.external_ref_count += num

    def calc_motor_value_summed(self, motor_dict, motor_multiplier=1):
        value_list = motor_dict[self.base_motor_name]
        raw_value = sum(value_list)
        return raw_value * motor_multiplier

    def calc_motor_value_averaged(self, motor_dict, motor_multiplier=1):
        value_list = motor_dict[self.base_motor_name]
        raw_value = sum(value_list) / len(value_list)
        return raw_value * motor_multiplier
