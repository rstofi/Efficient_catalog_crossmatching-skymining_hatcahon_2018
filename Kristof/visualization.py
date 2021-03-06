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

Visualization for Hachastron

"""

#=================================================
#IMPORTS
#=================================================
import numpy as np;
from matplotlib import pylab;
from matplotlib import pyplot as plt;
import glob;
import random;

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

def get_data_colums(epoch):
    """Return the data columns of a given epoch
    
    :param epoch: given epoch in a numpy array, already readed from .csv
    """
    
    ID = epoch[:,0];
    RA = epoch[:,1];
    RA_err = epoch[:,2];
    Dec = epoch[:,3];
    Dec_err = epoch[:,4];
    Flux = epoch[:,5];
    Flux_err = epoch[:,6];

    return ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err;

def get_position_model_colums(gal_model):
    """Return the data columns of a galaxy position model
    
    :param gal_model: One galaxy model from output of the sky model, already readed from .csv
    """
    
    ID = gal_model[:,0];
    RA = gal_model[:,1];
    RA_err = gal_model[:,2];
    Dec = gal_model[:,3];
    Dec_err = gal_model[:,4];
    Flux = gal_model[:,5];
    Flux_err = gal_model[:,6];
    Epoch = gal_model[:,7];

    return ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Epoch;

#=================================================
#PLOT FUNCTIONS
#=================================================

def plot_epoch_sky(epoch,save=False):
    """Plot the observed galaxy positions in the sky
    
    :param epoch: given epoch in a numpy array, already readed from .csv 
    """

    ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err = get_data_colums(epoch);

    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Sources on the sky', size=24);
        
    plt.errorbar(RA, Dec, xerr=RA_err, yerr=Dec_err, fmt='o');

    pylab.xlabel('RA [deg]', fontsize = 24);
    pylab.ylabel('Dec [deg]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    if save == True:
        plt.savefig('./Figures/initial_sky_model.png');
    else:
        plt.show();

def plot_two_epoch_sky(epoch1, epoch2,save=False):
    """Plot the observed galaxy positions in the sky
    
    :param epoch1: The firs given epoch in a numpy array, already readed from .csv
    :param epoch2: The second given epoch in a numpy array, already readed from .csv
    """

    ID_1, RA_1, RA_err_1, Dec_1, Dec_err_1, Flux_1, Flux_err_1 = get_data_colums(epoch1);
    ID_2, RA_2, RA_err_2, Dec_2, Dec_err_2, Flux_2, Flux_err_2 = get_data_colums(epoch2);

    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Sources on the sky', size=24);
        
    plt.errorbar(RA_1, Dec_1, xerr=RA_err_1, yerr=Dec_err_1, fmt='o', color='blue', alpha=0.5);
    plt.errorbar(RA_2, Dec_2, xerr=RA_err_2, yerr=Dec_err_2, fmt='o', color='red', alpha=0.5);

    pylab.xlabel('RA [deg]', fontsize = 24);
    pylab.ylabel('Dec [deg]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    if save == True:
        plt.savefig('./Figures/sky_model_update.png');
    else:
        plt.show();

def plot_test_data(folder=None):
    """Plot the test data I created
    
    :param folder: The folder where the data is
    """
    #========
    #Sky map
    #========
    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Sources on the sky', size=24);
    
    c = ['blue','red','green','orange','black','gray','yellow','purple', 'cyan', 'maroon'];
    
    if folder == None:
        folder = './Small_simulated_data/';
 
    epoch_data_list = sorted(glob.glob("%s/*.csv" %folder));
    
    ep = 0;
    for epoch in epoch_data_list:
        epoch = np.genfromtxt(epoch,  dtype=float, delimiter=',');
        for i in range(0,3):
            observed_galaxy = observed_galaxy_position(epoch=ep, obs=galaxy_obs(epoch, i));
            
            plt.errorbar(observed_galaxy.RA, observed_galaxy.Dec,
                        xerr=observed_galaxy.RA_err, yerr=observed_galaxy.Dec_err,
                        fmt='o', color=c[i], alpha=0.5);
            
        ep += 1;
            
    pylab.xlabel('RA [deg]', fontsize = 24);
    pylab.ylabel('Dec [deg]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    plt.show();

    #========
    #Flux vs time
    #========
    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Flux vs time', size=24);

    ep = 0;
    for epoch in epoch_data_list:
        epoch = np.genfromtxt(epoch,  dtype=float, delimiter=',');
        for i in range(0,3):
            observed_galaxy = observed_galaxy_position(epoch=ep, obs=galaxy_obs(epoch, i));
            
            plt.errorbar(ep, observed_galaxy.Flux, yerr=observed_galaxy.Flux_err,
                        fmt='o', color=c[i], alpha=0.5);
            
        ep += 1;    

    pylab.xlabel('Time [epoch number]', fontsize = 24);
    pylab.ylabel('Flux [mJy]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    plt.show();

def plot_test_solution(folder=None, initial_dataset=None):
    """Plot the test matching results

    :param folder: The folder where the data is
    :param initial_dataset: The dataset path (&name) which define the initial sky model
    """
    
    if folder == None:
        folder = './Small_simulated_data/';
    if initial_dataset == None:
        initial_dataset = './Small_simulated_data/test_epoch00.csv';
    
    #Solve the problem
    sm = tinder_for_galaxy_positions(folder, initial_dataset);
    final_sky_model = human_readable_sky_model(sm);
    
    #Plot   
    
    #========
    #Sky map
    #========
    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Sources on the sky', size=24);
    
    c = ['blue','red','green','orange','black','gray','yellow','purple', 'cyan', 'maroon'];
    
    for i in range(0,len(final_sky_model)):
        #ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Eopch = get_model_columns(final_sky_model,i);
        ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Eopch = get_model_columns(final_sky_model,i);
        
        plt.errorbar(RA, Dec, xerr=RA_err, yerr=Dec_err,
                    fmt='o', color=c[i], alpha=0.5);
            
    pylab.xlabel('RA [deg]', fontsize = 24);
    pylab.ylabel('Dec [deg]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    plt.show();

    #========
    #Flux vs time
    #========
    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Flux vs time', size=24);

    for i in range(0,len(final_sky_model)):
        ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Epoch = get_model_columns(final_sky_model,i);
                
        plt.errorbar(Epoch, Flux, yerr=Flux_err,
                    fmt='o', color=c[i], alpha=0.5);

    pylab.xlabel('Time [epoch number]', fontsize = 24);
    pylab.ylabel('Flux [mJy]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    plt.show();

def plot_galaxy_positon_model(galaxy_model_file=None):
    """Plot a galaxy position model from a final sky model output dataset
    
    :param galaxy_model_file: The path to the galaxy model position file
    """
    
    if galaxy_model_file == None:
        galaxy_model_file = './Final_sky_model/Galaxy_position_model00.csv'
    
    galaxy_position_model = np.genfromtxt(galaxy_model_file,  dtype=float, delimiter=',');
    
    ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Epoch = get_position_model_colums(galaxy_position_model);
    
    
def different_color_plot_of_model_galaxies(folder=None,save=False):
    """Plot each model galaxy in a given folder with different color
    
    :param folder: The folder where the data is
    """
    if folder == None:
        folder = './Final_sky_model/';
 
    galaxy_position_model_data_list = sorted(glob.glob("%s/*.csv" %folder));
    
    fig=plt.figure(figsize=(12,12));
    plt.clf();
    plt.title('Matched sources on the sky', size=24);
      
    color_for_three = ['blue','red','green'];
   
    i = 0;
    for galaxy_position_model in galaxy_position_model_data_list:
        epoch = np.genfromtxt(galaxy_position_model,  dtype=float, delimiter=',');
        
        ID, RA, RA_err, Dec, Dec_err, Flux, Flux_err, Epoch = get_position_model_colums(epoch);
        
        r = lambda: random.randint(0,255);
        c = '#%02X%02X%02X' % (r(),r(),r());
        
        plt.errorbar(RA, Dec, xerr=RA_err, yerr=Dec_err,
                    fmt='o', color=c, alpha=0.5);
                    
        i += 1;

    pylab.xlabel('RA [deg]', fontsize = 24);
    pylab.ylabel('Dec [deg]', fontsize = 24);
    plt.tick_params(labelsize=18);

    plt.tight_layout();
    
    if save == True:
        plt.savefig('./Figures/final_sky_model.png');
    else:
        plt.show();

#=================================================
#MAIN
#=================================================
if __name__ == "__main__":
    """Testing
    """
    #epoch_0 = np.genfromtxt('../Small/epoch00.csv',  dtype=float, delimiter=',',  skip_header=1);
    #epoch_1 = np.genfromtxt('../Small/epoch01.csv',  dtype=float, delimiter=',',  skip_header=1);
    
    #epoch_0 = np.genfromtxt('../Data/epoch00.csv',  dtype=float, delimiter=',',  skip_header=1);
    #epoch_1 = np.genfromtxt('../Data/epoch01.csv',  dtype=float, delimiter=',',  skip_header=1);

    #plot_epoch_sky(epoch_0,save=True);
    #plot_two_epoch_sky(epoch_0, epoch_1,save=True);

    #different_color_plot_of_model_galaxies();
    
    plot_test_data();
    plot_test_solution();
    #plot_test_data(folder='./Subdatacube');
    #plot_test_solution(folder='./Subdatacube/', initial_dataset='./Subdatacube/test_epoch00.csv');

    #different_color_plot_of_model_galaxies(folder='./Small_solution/',save=False);
