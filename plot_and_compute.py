from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pars as ps
import functions as fn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#

mpl.rcParams['axes.linewidth'] = 2


current_date = np.datetime64('today')



'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
'''%%% running the simulation '''
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''



def load_files(time, h, number_of_astroids, extra_name=""):

    a_pos = np.loadtxt(str(extra_name) + "_date_" + str(current_date) + "_astroid_positions_m=1_abound=3.3_3.4_time_"  +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    a_vel = np.loadtxt(str(extra_name) + "_date_" + str(current_date) + "_astroid_velocities_m=1_abound=3.3_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    j_pos = np.loadtxt(str(extra_name) + "_date_" + str(current_date) + "_jupiter_positions_m=1_abound=3.3_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    j_vel = np.loadtxt(str(extra_name) + "_date_" + str(current_date) + "_jupiter_velocities_m=1_abound=3.3_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    distance_astroid = np.loadtxt(str(extra_name) + "_date_" + str(current_date) + "_distance_astroids_m=1_abound=3.3_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")

    return a_pos, a_vel, j_pos, j_vel, distance_astroid





total_years = 10
timestep = 0.5/365.25
number_of_astroids = 10000

jupiter, astroids = fn.simulation(total_years, timestep, number_of_astroids)
# a_pos, a_vel, j_pos, j_vel, distance_astroid = load_files(total_years, timestep, number_of_astroids, extra_name='troep')
# print (a_pos)


#convergence_test(10,0.01)


def plot_planets(planet_one, planet_two, planet_three, nbins=250, zoom=6):
    '''This function is an aid to plot the planets investigated in the convergence_test function.'''
    fig, axes = plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.4* h)

    axes.scatter((planet_one[:,0]), (planet_one[:,1]), s=20, label="planet one", c=c1)
    axes.scatter((planet_two[:,0]), (planet_two[:,1]), s=20, label="planet two", c=c2)
    axes.scatter((planet_three[:,0]), (planet_three[:,1]), s=20, label="planet three", c=c3)
    axes.scatter(0.0 , 0.0, s= 50,c='y')

    axes.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    axes.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    axes.set_title("Trajectory of Jupiter and Asteriods",fontsize=20)
    axes.tick_params (axis='both',labelsize=20, length=20,width=2)
    axes.legend (prop={'size': 25},markerscale=1,fancybox=True,loc=2)
    axes.set_xlim(-zoom, zoom)
    axes.set_ylim(-zoom, zoom)
    plt.show()

#plot_planets(planet_one, planet_two, planet_three)



def plot_data(astroid_position, jupiter_position, distance, nbins=250, zoom=6):
    '''This function is an aid to plot the astroids, Jupiter and the stationary Sun as calulated by the simulation function.'''

    fig, (axes,axes2)= plt.subplots(nrows=2, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(2.2 * w, 5.* h)

    axes.scatter(0.0 , 0.0, s= 80, label="Sun",c=c2)
    axes.scatter((jupiter_position[:,0]), (jupiter_position[:,1] ), s=20, label="Jupiters orbit",c=c3)
    axes.scatter((astroid_position[:,0]), (astroid_position[:,1]), s=5, label="bound Astroids", c=c1)
    axes2.hist(distance, bins=nbins,  color=c1)
    axes2.set_xlabel("radial distance to sun (AU)", fontsize=20)
    axes2.set_ylabel("number of bound asteroids", fontsize=20)

    # axes2.axvline(x=2.5,  color=c2, linestyle='dotted', linewidth=6)
    # axes2.axvline(x=2.8,  color=c2, linestyle='dotted', linewidth=6)
    # axes2.axvline(x=2.951,  color=c2, linestyle='dotted', linewidth=6)
    # axes2.axvline(x=3.375,  color=c2, linestyle='dotted', linewidth=6)
    # axes2.text(2.51  ,12.0,'3:1', fontsize=15)
    # axes2.text(2.81  ,12.0,'5:2', fontsize=15)
    # axes2.text(2.961 ,12.0,'7:3', fontsize=15)
    # axes2.text(3.385 ,12.0,'2:1', fontsize=15)

    axes.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    axes.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    axes.set_title("Trajectory of Jupiter and Asteriods",fontsize=20)
    # axes.tick_params (axis='both',labelsize=20, length=20,width=2)
    # axes2.tick_params(axis='both',labelsize=20, length=20,width=2)
    axes.legend (prop={'size': 15},markerscale=1,fancybox=True,loc=2)
    axes.set_xlim(-zoom, zoom)
    axes.set_ylim(-zoom, zoom)
    axes.axis('equal')
    plt.tight_layout()

    plt.show()

c1= '#66c2a5'
c2= '#fc8d62'
c3= '#8da0cb'

# plot_data(a_pos, j_pos, distance_astroid, nbins=25, zoom=6)
