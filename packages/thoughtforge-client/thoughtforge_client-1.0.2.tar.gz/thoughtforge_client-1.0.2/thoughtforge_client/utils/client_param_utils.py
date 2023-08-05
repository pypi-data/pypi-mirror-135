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

import json
import os
from collections import namedtuple
from typing import List


CURRENT_CLIENT_PARAMS_VERSION = 1


def safe_dict_get(dict, keyName, default):
    """ Utility function for accessing dictionary values """
    return dict[keyName] if keyName in dict.keys() else default


def _load_enforced_type(file_name, enforced_types, use_named_tuple=False):
    print('load', file_name, enforced_types)
    def mapJSONToObject(dict):
        return namedtuple('X', dict.keys())(*dict.values())
    config = {}
    file_extension = os.path.splitext(file_name)[1]
    if(file_extension in enforced_types):
      with open(file_name) as f:
          if(use_named_tuple):
              config = json.load(f, object_hook=mapJSONToObject)
          else:
              config = json.load(f) #, object_hook=mapJSONToObject
    else:
      raise 'config files must be of type' + enforced_types + ' got ' + file_name
    return config  


def load_client_params(file_name):
    """ return json client configuration from the given filename """
    return _load_enforced_type(file_name, ['.params', '.spec'])
