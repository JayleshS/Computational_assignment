from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pars as ps
import functions as fn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# mpl.rcdefaults()
# mpl.rcParams.update(mpl.rcParamsDefault)


# mpl.rcParams['axes.linewidth']  = 2
# plt.rcParams['lines.linewidth'] = 2  # Create thicker lines in plots
#
# plt.rcParams['xtick.labelsize'] = 12
# plt.rcParams['ytick.labelsize'] = 12

current_date = np.datetime64('today')
c1= '#66c2a5'
c2= '#fc8d62'
c3= '#8da0cb'

def plot(all_info, zoom = 6, save=''):
    '''This function is an aid to plot the astroids, Jupiter and the stationary Sun as calulated by the simulation function.
    Depending on the method used to save the data the plot is generated in two different ways.'''

    fig, (axes)= plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.* h)

    if save == 'np':
        axes.scatter(0.0 , 0.0, s= 80, label="Sun",c=c2)
        axes.scatter((all_info['j_pos'][:,0]), (all_info['j_pos'][:,1]), s=20, label="Jupiter",c=c3)
        axes.scatter((all_info['a_pos'][:,0]), (all_info['a_pos'][:,1]), s=5, label="Astroids", c=c1)

    else:
        #plt.scatter((all_info[:,0])           , (all_info[:,1])           , label="astroids"             , c=c1, s=5)
        plt.scatter((all_info[:,0][-300*100:]), (all_info[:,1][-300*100:]), label="Last year of Astroids", c=c2, s=5)


    axes.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    axes.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    axes.set_xlim(-zoom, zoom)
    axes.set_ylim(-zoom, zoom)
    axes.axis('equal')

    axes.legend(prop={'size': 15},markerscale=1,fancybox=True,loc=2)
    plt.tight_layout()

    plt.show()

def plot_histo(all_info, nbins = 100, save='') :
    '''Plot function for histogram
    Depending on the method used to save the data the plot is generated in two different ways.'''

    fig, (axes)= plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.* h)

    if save == 'np':
        axes.hist(all_info['d_astroid'], bins=nbins, label=str(nbins)+" bins", color = c1)
    else:
        axes.hist(np.sqrt((all_info[:,0])**2 + (all_info[:,1])**2), bins=nbins, label=str(nbins)+" bins", color = c1)

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
    # axes.set_yscale('Log')

    plt.tight_layout()

    plt.show()

def plot_convergence(p_1,p_2,p_3, zoom=3):

    plt.plot( p_1[:,0], p_1[:,1], '-', label="planet 1", c=c1)
    plt.plot( p_2[:,0], p_2[:,1], 's', label="planet 2", c=c2)
    plt.plot( p_3[:,0], p_3[:,1], '^', label="planet 3", c=c3)

    plt.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    plt.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    plt.set_xlim(-zoom, zoom)
    plt.set_ylim(-zoom, zoom)

    plt.legend(prop={'size': 15},markerscale=1,fancybox=True,loc=2)
    plt.tight_layout()
    axes.axis('equal')
    plt.show()

def load_files(time, h, number_of_astroids, extra_name=""):
    #astroid_pos = np.loadtxt("astroid_pos_"+str(extra_name) + "_date_" + str(current_date) +  "_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat")
    #astroid_vel = np.loadtxt("astroid_vel_"+str(extra_name) + "_date_" + str(current_date) +  "_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat")
    all_info = np.load(str(extra_name) + "_date_" + str(current_date) +  "_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".npz")
    return all_info
    #return astroid_pos, astroid_vel

def load_convergence_file(time,h,extra_name=''):
    p_1 = np.loadtxt("p_1_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    p_2 = np.loadtxt("p_2_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    p_3 = np.loadtxt("p_3_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")

    return p_1, p_2, p_3


'''choose total runtime, time stepsize and number of asteroids'''
total_years = 25
timestep = 1e-3
number_of_saves = total_years/timestep/100
number_of_astroids = 1000

'''perform the simulation '''
fn.simulation(total_years, timestep, number_of_astroids, save=True, number_of_saves=number_of_saves)

# print (number_of_saves)


''' load data and plot results'''
astroid_pos = load_files(total_years, timestep, number_of_astroids)
plot(astroid_pos, save='np')
plot_histo(astroid_pos, save='np', nbins = 100)

# '''convergence test'''
# p_1,p_2,p_3 = fn.convergence_test(3, 1e-3,save=False)
# p_1,p_2,p_3 = load_convergence_file(1e-1,1e-3)
# plot_convergence(p_1,p_2,p_3)
