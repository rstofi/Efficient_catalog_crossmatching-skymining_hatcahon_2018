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

#=================================================
#PLOT FUNCTIONS
#=================================================

def plot_epoch_sky(epoch):
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
    
    plt.show();

def plot_two_epoch_sky(epoch1, epoch2):
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
    
    plt.show();

#=================================================
#MAIN
#=================================================
if __name__ == "__main__":
    """Testing
    """
    epoch_0 = np.genfromtxt('../Data/epoch00.csv',  dtype=float, delimiter=',',  skip_header=1);
    epoch_1 = np.genfromtxt('../Data/epoch01.csv',  dtype=float, delimiter=',',  skip_header=1);

    plot_epoch_sky(epoch_0);

    plot_two_epoch_sky(epoch_0, epoch_1)
