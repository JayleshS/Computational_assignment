from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pars as ps
import functions as fn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['axes.linewidth']  = 2
plt.rcParams['lines.linewidth'] = 2  # Create thicker lines in plots
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

current_date = np.datetime64('today')
c1= '#66c2a5'
c2= '#fc8d62'
c3= '#8da0cb'

def plot(all_info, zoom = 6):
    '''This function is an aid to plot the astroids, Jupiter and the stationary Sun as calulated by the simulation function.'''

    fig, (axes)= plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.* h)

    axes.scatter(0.0 , 0.0, s= 80, label="Sun",c=c2)
    axes.scatter((all_info['j_pos'][:,0]), (all_info['j_pos'][:,1]), s=20, label="Jupiter",c=c3)
    axes.scatter((all_info['a_pos'][:,0]), (all_info['a_pos'][:,1]), s=5, label="Astroids", c=c1)

    axes.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    axes.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    axes.set_xlim(-zoom, zoom)
    axes.set_ylim(-zoom, zoom)
    axes.axis('equal')

    axes.legend(prop={'size': 15},markerscale=1,fancybox=True,loc=2)
    plt.tight_layout()

    plt.show()

def plot_histo(all_info, nbins = 100) :
    ''' plot function for histogram '''

    fig, (axes)= plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.* h)

    axes.hist(all_info['d_astroid'], bins=nbins, label=str(nbins)+" bins", color = c1)
    axes.set_xlabel("Radial distance to Sun [AU]", fontsize=20)
    axes.set_ylabel("Number of asteroids", fontsize=20)

    axes.axvline(x=2.5  ,  color=c2, linestyle='dotted', linewidth=6)
    axes.axvline(x=2.8  ,  color=c2, linestyle='dotted', linewidth=6)
    axes.axvline(x=2.951,  color=c2, linestyle='dotted', linewidth=6)
    axes.axvline(x=3.375,  color=c2, linestyle='dotted', linewidth=6)
    axes.text(2.51  ,12.0,'3:1', fontsize=15)
    axes.text(2.81  ,12.0,'5:2', fontsize=15)
    axes.text(2.961 ,12.0,'7:3', fontsize=15)
    axes.text(3.385 ,12.0,'2:1', fontsize=15)

    plt.tight_layout()

    plt.show()

def load_files(time, h, number_of_astroids, extra_name=""):
    # all_info = np.load(str(extra_name) + "_date_2018-04-27_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".npz")
    all_info = np.load(str(extra_name) + "_date_" + str(current_date) +  "_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".npz")

    return all_info

'''choose total runtime, time stepsize and number of asteroids'''
total_years = 500
timestep = 0.5/365.25
number_of_astroids = 1000

'''perform the simulation '''
jupiter, astroids = fn.simulation(total_years, timestep, number_of_astroids, save=True)

''' load data and plot results'''
all_info = load_files(total_years, timestep, number_of_astroids)
plot(all_info)
plot_histo(all_info, nbins = 100)

print(" ====> end of code was reached <==== ")
