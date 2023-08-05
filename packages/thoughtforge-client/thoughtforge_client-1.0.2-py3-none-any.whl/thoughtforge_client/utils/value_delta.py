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


class ValueDelta:
    """ ValueDelta is a utility class for tracking the change in a value over time.
    This is commonly used in sensor definitions to get the derivative of a changing
    continuous value """
    def __init__(self, last_value=0):
        self.last_value = last_value

    def reset(self, reset_value=0):
        """ Indicates an interruption in the data stream """
        self.last_value = reset_value

    def update_and_get_delta(self, new_value):
        """ Updates the current value of the value stream and returns the delta from 
        last value """
        delta = self.last_value - new_value
        self.last_value = new_value
        return delta
