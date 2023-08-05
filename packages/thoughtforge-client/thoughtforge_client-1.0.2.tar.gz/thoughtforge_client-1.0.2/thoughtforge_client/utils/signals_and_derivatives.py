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

from thoughtforge_client.utils.value_delta import ValueDelta


class SignalAndDerivatives():
    """ Utility class for simple tracking of derivatives of sensor signal values """

    def __init__(self, num_derivatives):
        # this class is not intended to handle very long derivative chains.
        assert(num_derivatives >= 0 and num_derivatives < 10)
        self.num_derivatives = num_derivatives
        # note: we allocate one additional tracker just in case, which provides
        # easy access for the last state of the previous derivative
        self.deriv_trackers = [ValueDelta() for i in range(num_derivatives+1)]
    
    def update(self, new_value):
        """ Update the derivative value chain """
        last_delta_value = new_value
        for deriv_tracker in self.deriv_trackers:
            last_delta_value = deriv_tracker.update_and_get_delta(last_delta_value)

    def reset(self, new_signal_value=0):
        """ Reset derivative trackers to zero """
        for deriv_tracker in self.deriv_trackers:
            if new_signal_value != 0:
                deriv_tracker.reset(new_signal_value)
                new_signal_value = 0
            else:
                deriv_tracker.reset()

    def get_value(self, deriv=0):
        """ Returns the current value for the requested derivative """
        assert(deriv <= self.num_derivatives)
        return self.deriv_trackers[deriv].last_value
