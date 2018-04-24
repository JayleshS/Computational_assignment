from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime

mpl.rcParams['axes.linewidth'] = 2


a = 5.2044             # semi major axis (units of AU)
e = 0.0489          # eccentricity
G = 4*(np.pi**2)    # gravitational constant (units of M_sun, AU and year)
M_sun = 1.          # solar mass
M_jup = (1.0/1047)*M_sun  # fraction of M_sun


''' Date of today!!!!!
'''
# current = np.datetime64(datetime.datetime.now())


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
'''%%% running the simulation '''
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

def load_files(time, h, number_of_astroids, extra_name=""):

    a_pos = np.loadtxt(str(extra_name) + "astroid_positions_m=1_abound=2.4_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    a_vel = np.loadtxt(str(extra_name) + "astroid_velocities_m=1_abound=2.4_3.4_time_"+str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    j_pos = np.loadtxt(str(extra_name) + "jupiter_positions__m=1_abound=2.4_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    j_vel = np.loadtxt(str(extra_name) + "jupiter_velocities_m=1_abound=2.4_3.4_time_"+str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")
    distance_astroid = np.loadtxt(str(extra_name) + "distance_astroids_m=1_abound=2.4_3.4_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids)+".dat", "a")

    return a_pos, a_vel, j_pos, j_vel, distance_astroid





total_years = 200000
timestep = 0.5/365.25
number_of_astroids = 10000
#jupiter, astroids = simulation(total_years, timestep, number_of_astroids)


#part_of_filename = '_time_7feb_20000_h_0.00136892539357_n_10000'


#j_pos = np.loadtxt('jupiter_positions'+str(part_of_filename)+'.dat')
#as_pos = np.loadtxt('astroid_positions'+str(part_of_filename)+'.dat')
#distance_astroid = np.loadtxt( 'distance_astroids_7feb_time_m=1_20000_h_0.00136892539357_n_10000.dat')



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

    axes2.axvline(x=2.5,  color=c2, linestyle='dotted', linewidth=6)
    axes2.axvline(x=2.8,  color=c2, linestyle='dotted', linewidth=6)
    axes2.axvline(x=2.951,  color=c2, linestyle='dotted', linewidth=6)
    axes2.axvline(x=3.375,  color=c2, linestyle='dotted', linewidth=6)
    axes2.text(2.51  ,12.0,'3:1', fontsize=15)
    axes2.text(2.81  ,12.0,'5:2', fontsize=15)
    axes2.text(2.961 ,12.0,'7:3', fontsize=15)
    axes2.text(3.385 ,12.0,'2:1', fontsize=15)

    axes.set_xlabel("x$_{position}$ [AU]", fontsize=20)
    axes.set_ylabel("y$_{position}$ [AU]", fontsize=20)
    axes.set_title("Trajectory of Jupiter and Asteriods",fontsize=20)
    axes.tick_params (axis='both',labelsize=20, length=20,width=2)
    axes2.tick_params(axis='both',labelsize=20, length=20,width=2)
    axes.legend (prop={'size': 15},markerscale=1,fancybox=True,loc=2)
    axes.set_xlim(-zoom, zoom)
    axes.set_ylim(-zoom, zoom)
    axes.axis('equal')
    plt.tight_layout()

    plt.show()

c1= '#66c2a5'
c2= '#fc8d62'
c3= '#8da0cb'

plot_data(a_pos[-400:], j_pos, d_astroid[-400:], nbins=25, zoom=6)
