"""
------------------------------
MIT License

Copyright (c) 2018 Hachastron

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
------------------------------

Cost matrix for the Hungarian algorithm

"""

#=================================================
#IMPORTS
#=================================================
import numpy as np;
from scipy import stats;
import glob;

from position_model import *;
from matching_algorithm import *;

#=================================================
#LOGGING
#=================================================
import logging;

log = logging.getLogger();
log.setLevel(logging.INFO);

#=================================================
#SUPPORT FUNCTIONS
#=================================================
def get_parameter(kwargs, key, default=None):
    """ Get a specified named value for this (calling) function

    The parameter is searched for in kwargs

    :param kwargs: Parameter dictionary
    :param key: Key e.g. 'loop_gain'
    :param default: Default value
    :return: result
    """

    if kwargs is None:
        return default;

    value = default;
    if key in kwargs.keys():
        value = kwargs[key];
    return value;

def add_noise(source, **kwargs):
    """ Add noise to source from the 'standard normal' distribution, but optionally the distribution mu and sigma can be changed
    
    :param source: Source true position on the sky
    :return: source with noise
    """
    sigma = get_parameter(kwargs, "sigma", None);#tuple of the sigma of the real and the imaginary part
    if sigma is None:
        sigma = 1;

    mu = get_parameter(kwargs, "mu", None);#tuple of the mu of the real and the imaginary part
    if mu is None:
        mu = 0;

    epoch_index = source[0];
    source_with_err = source + (mu + sigma * np.random.randn(len(source)));
    
    source_with_err[0] = epoch_index;
    
    for i in [2,4,6]:
        source_with_err[i] = np.fabs(source_with_err[i]);
    
    return source_with_err;


def firts_rows_from_actual_dataset(N):
    """Returns the first N row from the acrtual dataset for each epoch and saves it into a folder
    
    :param N: The number of rows used
    """
    
    epoch_data_list = sorted(glob.glob("../Data/*.csv"));
    
    i = 0;
    for epoch in epoch_data_list:
        epoch = np.genfromtxt(epoch,  dtype=float, delimiter=',', skip_header=1);
        
        sub_epoch = epoch[0:N,:];
        
        #save
        if i <= 9:
            np.savetxt('./Subdatacube/test_epoch0%s.csv' %i, sub_epoch, delimiter=',');
        else:
            np.savetxt('./Subdatacube/test_epoch%s.csv' %i, sub_epoch, delimiter=',');
        
        i += 1;

#=================================================
#MAIN
#=================================================
if __name__ == '__main__':
    """Create test data
    """
    
    firts_rows_from_actual_dataset(N=10);
    
    exit();
    
    #Sources
    source1 = [0,20,0,20,0,20,0];
    source2 = [1,22,0,20,0,19,0];
    source3 = [2,21,0,21,0,22,0];

    #Generate random data
    for i in range(0,50):
        source1_observed = add_noise(source1, sigma=0.5);
        source2_observed = add_noise(source2, sigma=0.5);
        source3_observed = add_noise(source3, sigma=0.5);
        
        observation_set = np.column_stack((source1_observed,source2_observed,source3_observed));
        observation_set = np.transpose(observation_set);

        #save
        if i <= 9:
            np.savetxt('./Small_simulated_data/test_epoch0%s.csv' %i, observation_set, delimiter=',');
        else:
            np.savetxt('./Small_simulated_data/test_epoch%s.csv' %i, observation_set, delimiter=',');

