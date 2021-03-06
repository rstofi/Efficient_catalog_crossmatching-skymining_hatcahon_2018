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

from position_model import *;
from sky_model import *;

#=================================================
#LOGGING
#=================================================
import logging;

log = logging.getLogger();
log.setLevel(logging.INFO);

#=================================================
#SUPPORT FUNCTIONS
#=================================================
def add_galaxy_model(initial_sky_model,model_galaxy):
    """Add an observed galaxy position to the model
    
    :param initial_sky_model: The sky model
    :param model_galaxy: The model of a 'real galaxy' consist a bunch of observations
    """
    initial_sky_model.galax_model_list.append(model_galaxy);
    
    return initial_sky_model;

def create_initial_sky_model(epoch_ID, epoch):
    """Create an initial sky model using a given epoch

    :param epoch_ID: The ID (time) of a given epoch
    :param epoch: given epoch in a numpy array, already readed from .csv
    """
    
    sm = sky_model();
    
    observed_galaxy_ID = epoch[:,0];
    
    for i in observed_galaxy_ID:
        observed_galaxy = observed_galaxy_position(epoch=epoch_ID, obs=galaxy_obs(epoch, i));
        
        galaxy_model = model_galaxy();
        
        add_observation(galaxy_model,observed_galaxy);
    
        add_galaxy_model(sm,galaxy_model);
    
    return sm;

def distance(a,b):
    """Approx distance of two points in the sky
    
    :param a,b: the two points, both tuple
    """
    
    dist = np.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]));

    return dist;

def compute_cost_matrix(sm,observed_epoch,epoch_ID):
    """Compute the cost matrix for the Hungarian algorithm
    
    :param sm: Sky model
    :param observed_epoch: given epoch in a numpy array, already readed from .csv
    :param epoch_ID: The ID pf the observed epoch
    """
    #Create cost matrix
    assert observed_epoch.shape[0] == len(sm.galax_model_list), "Discrepancy model- and observed galaxy number"

    cost_matrix = np.zeros((observed_epoch.shape[0],len(sm.galax_model_list)));#Rows are observations, columns are models
    
    j = 0;
    observed_galaxy_ID = observed_epoch[:,0];
    for galaxy_model in sm.galax_model_list:
        i = 0;
        for g_id in observed_galaxy_ID:
            
            """Possible spped up ==> but it make the algorith worst
            if distance(galaxy_model.sky_position,
                    (observed_galaxy_position(epoch=epoch_ID, obs=galaxy_obs(observed_epoch, g_id)).RA, observed_galaxy_position(epoch=epoch_ID,\
                    obs=galaxy_obs(observed_epoch, g_id)).Dec)) > 6 * galaxy_model.sky_radial_sigma:
                cost_matrix[i,j] = 0.000001;
            else:
                cost_matrix[i,j] = p_value_of_observation(galaxy_model,observed_galaxy_position(epoch=epoch_ID, obs=galaxy_obs(observed_epoch, g_id)));
            """
           
            cost_matrix[i,j] = p_value_of_observation(galaxy_model,observed_galaxy_position(epoch=epoch_ID, obs=galaxy_obs(observed_epoch, g_id)));
           
            i += 1;
            
            log.info('Cost matrix row computed');
            
        j += 1;
            
    return cost_matrix;

#=================================================
#MAIN
#=================================================
if __name__ == '__main__':
    """Test
    """
    initial_epoch = np.genfromtxt('./Small_simulated_data/test_epoch00.csv',  dtype=float, delimiter=',',  skip_header=0);
    initial_epoch_ID =0;
    
    #observed_epoch = np.genfromtxt('../Data/epoch01.csv',  dtype=float, delimiter=',',  skip_header=0);
    observed_epoch = np.genfromtxt('./Small_simulated_data/test_epoch10.csv',  dtype=float, delimiter=',',  skip_header=0); 
    epoch_ID = 1;    
    
    sm = create_initial_sky_model(initial_epoch_ID, initial_epoch);

    cm = compute_cost_matrix(sm,observed_epoch,epoch_ID);

    print(cm);

#    print(len(sm.galax_model_list));
#    print(len(sm.galax_model_list[0].obs_list));


