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

from thoughtforge_client.utils.sensor_motor_groups import (
    SensorGroup, MotorGroup, calc_sensor_range)


class BehaviorInterface:
    """ This class acts as an interface for composable behaviors for use with the
    ThoughtForge platform. Internalizes the specification of network topology and
    interfacing with the sensors and motors """

    def preprocess_specification(self, json_specification):
        """ This function takes the parameters from the 'preprocessor_specification'
        of the specification file, and uses it to generate an output json specification
        for a network topology and sensor/motor definitions """        
        preprocessor_specification = json_specification['preprocessor_specification']
        all_motor_specs = preprocessor_specification['motors']
        all_sensor_specs = preprocessor_specification['sensors']
        default_motor_params = preprocessor_specification['default_motor_params']     
        default_sensor_params = preprocessor_specification['default_sensor_params']

        ###############################
        # Setup sensor and motor groups
        self.sensor_groups = [
            SensorGroup(update_function=update_func, 
                        base_sensor_name=sensor_name)
            for sensor_name, update_func in self.sensor_update_definiton_dict.items()]
        self.motor_groups = [
            MotorGroup(base_motor_name)
            for base_motor_name in self.motor_names]

        motor_specs = [
            next(motor for motor in all_motor_specs if motor['name'] == motor_name)
            for motor_name in self.motor_names]
        motor_instantiation_info = self._build_full_motor_definitions(motor_specs, default_motor_params)
        
        sensor_specs = [
            next(sensor for sensor in all_sensor_specs if sensor['name'] == sensor_name)
            for sensor_name in self.sensor_names]
        sensor_instantiation_info = self._build_full_sensor_definitions(sensor_specs, default_sensor_params)

        return motor_instantiation_info, sensor_instantiation_info

    def update_sensor_values(self, obs, reset=False):
        """ This function takes in the observation space and returns a dictionary
        of sensor names and values calcluated from the observation space.
        If Reset is true, then this indicates an interruption in the temporal steam. 
        """
        raise NotImplementedError

    def get_motor_outputs(self, motor_dict):
        """ This function is intended to return an array of motor outputs
        but can be composed from seperate behaviors """
        raise NotImplementedError


    @staticmethod
    def  _build_full_sensor_definitions(sensor_specs, default_sensor_params):
        """ Utility function for building the full sensor specification from
        the raw preprocess specs """
        sensor_ranges_dict = {}
        for sensor_definition in sensor_specs:
            sensor_group_name = sensor_definition['name']
            sensor_min_range = sensor_definition['min_range']
            sensor_range_multiplier = sensor_definition['range_multiplier']
            sensor_range_length = sensor_definition['range_length']
            sensor_ranges_dict[sensor_group_name] = calc_sensor_range(sensor_min_range,  sensor_range_multiplier, sensor_range_length)

        sensor_block_params_dict = {
            'length': default_sensor_params['num_layers'],
            'width': default_sensor_params['base_size'], 
            'layer_stride': default_sensor_params['base_stride'], 
            'interlayer_stride': default_sensor_params['base_stride'],
            'outgoing_interblock_stride': default_sensor_params['base_size']
        }
        sensor_params_dict = {
            'category': default_sensor_params['type'], 
            'type': "MULTI"
            }
        sensor_param_dict_by_name = { 
            sensor_spec['name']: sensor_params_dict
            for sensor_spec in sensor_specs}
        # Note: The above dictionary is useful for customizing parameters
        #       for specific sensors, such as:
        # roll_sensor_params_dict = {
        #     'category': 'BETA', 
        #     'type': "MULTI",
        #     }
        # sensor_param_dict_by_name['upperarm_roll_angle'] = roll_sensor_params_dict
        # sensor_param_dict_by_name['forearm_roll_angle'] = roll_sensor_params_dict
        #     sensor_param_dict_by_name['right_gripper_distance'] = roll_sensor_params_dict
        #     sensor_param_dict_by_name['left_gripper_distance'] = roll_sensor_params_dict
        return sensor_ranges_dict, sensor_block_params_dict, sensor_param_dict_by_name

    @staticmethod
    def _build_full_motor_definitions(motor_specs, default_motor_params):
        """ Utility function for building the full motor specification from
        the raw preprocess specs """
        num_motors = int((default_motor_params['base_size'] + 1) / 2)
        motor_params_dict = {
            'category': [default_motor_params['type']] * num_motors,
            'type': "MULTI"
        }
        motor_param_dict_by_name = { 
            motor_spec['name']: motor_params_dict
            for motor_spec in motor_specs }
            
        motor_block_params_dict = {
            'length': default_motor_params['num_layers'], 
            'width': default_motor_params['base_size'], 
            'layer_stride': default_motor_params['base_stride'], 
            'interlayer_stride': default_motor_params['base_stride'], 
            'outgoing_interblock_stride': default_motor_params['base_size']
        }
        # Map which motors receive which sensors
        motor_sensor_instantiations = {motor_spec['name']: motor_spec['sensor_instantiations'] 
                                       for motor_spec in motor_specs}                                     

        return motor_block_params_dict, motor_param_dict_by_name, motor_sensor_instantiations

    @staticmethod
    def _add_motors_to_json(json_specification, 
                            motor_groups, motor_names, 
                            motor_sensor_instantiations, 
                            motor_param_dict_by_name, 
                            motor_block_params_dict):
        """ Add motor blocks to json based on the combined model parameters """
        for motor_group_name, motor_sensor_instantiation in motor_sensor_instantiations.items():
            for instantiation in motor_sensor_instantiation:
                # sensor_group_name = instantiation['name']
                num = instantiation['num']
                # sensor_group = self.sensor_groups[list(self.sensor_update_definiton_dict.keys()).index(sensor_group_name)]
                motor_group = motor_groups[motor_names.index(motor_group_name)]
                motor_group.increment_external_ref_count(num)
        for motor_group in motor_groups:
            motor_params = motor_param_dict_by_name[motor_group.base_motor_name]
            motor_group.add_to_json(json_specification, motor_params, motor_block_params_dict)
    
    @staticmethod
    def _add_sensors_to_json(json_specification,
                             sensor_groups, 
                             sensor_ranges_dict, 
                             motor_sensor_instantiations, 
                             sensor_param_dict_by_name, 
                             sensor_block_params_dict):
        """ Add sensor blocks to json based on the combined model parameters """
        sensor_num_dict = {}
        for motor_group_name, motor_sensor_instantiation in motor_sensor_instantiations.items():
            for instantiation in motor_sensor_instantiation:
                sensor_group_name = instantiation['name']
                num = instantiation['num']
                if sensor_group_name not in sensor_num_dict:
                    sensor_num_dict[sensor_group_name] = num
                else:
                    sensor_num_dict[sensor_group_name] += num
        for sensor_group in sensor_groups:
            sensor_params = sensor_param_dict_by_name[sensor_group.base_sensor_name]
            num = sensor_num_dict[sensor_group.base_sensor_name]
            sensors = sensor_ranges_dict[sensor_group.base_sensor_name]
            sensor_group.set_refcount(num)
            sensor_group.add_to_json(json_specification, sensor_params, sensor_block_params_dict, sensors)

    @staticmethod
    def _add_blocks_to_json(json_specification, 
                            motor_groups, motor_names, 
                            sensor_groups, sensor_names, 
                            motor_sensor_instantiations):
        """ Add internal blocks to json based on the combined model parameters """
        # Add block connections
        for motor_group_name, motor_sensor_instantiation in motor_sensor_instantiations.items():
            for instantiation in motor_sensor_instantiation:
                sensor_group_name = instantiation['name']
                num = instantiation['num']
                sensor_group = sensor_groups[sensor_names.index(sensor_group_name)]
                motor_group = motor_groups[motor_names.index(motor_group_name)]
                for i in range(num):
                    json_specification['connections'].append(
                        {'source': sensor_group.block_name, 
                        'dest': motor_group.block_name,
                        })
