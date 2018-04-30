from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pars as ps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

current_date = np.datetime64('today')
c1= '#66c2a5'
c2= '#fc8d62'
c3= '#8da0cb'

def simulation(time, h, number_of_astroids, save=False, extra_name=""):
    '''This function uses the Euler-Cromer method to solve N times 3-body problems.'''

    '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
    '''%%% creation and initialization of jupiter and astroids '''
    '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

    '''jupiter, take sun = (0,0,0) '''
    jupiter = np.array([[ [0.0,ps.a*(1.-ps.e),0.0] , [-np.sqrt( (ps.G/ps.a) * (1.+ps.e)/(1-ps.e) ),0.0,0.0] ]])

    '''create multidimensional array for all astroids'''
    astroids = np.zeros((number_of_astroids, 2, 3)) # nr astr., pos. and vel. vector, spatial dimension

    '''array for radius and angle for starting position'''
    radius0 = np.random.uniform(2.0, 3.5, number_of_astroids)
    theta0  = np.random.uniform(0.0, 2*np.pi, number_of_astroids)

    '''x = r cos theta'''
    astroids[:,0][:,0] = radius0*np.cos(theta0)

    '''y = r sin theta'''
    astroids[:,0][:,1] = radius0*np.sin(theta0)

    '''z = small'''
    astroids[:,0][:,2] = 1/100*radius0*np.sin(theta0)


    '''vx and vy are random '''
    astroids[:,1][:,0] = + radius0 * np.sin(theta0)

    astroids[:,1][:,1] = - radius0 * np.cos(theta0)

    '''vz = small'''
    astroids[:,1][:,2] = np.random.uniform(-1e-4, 1e-4, (number_of_astroids))

    '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
    '''%%% time for loop '''
    '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

    n = int(time/h) #number of timesteps
    print("number of timesteps: " + str(n))
    for t in range(n-1):

        if t % 10000 == 0 :
            '''prints current timestep, number of total timesteps and current year'''
            print("simulation reached time step " + str(t) + " of " + str(n) + ". Year = " + str(t*h))

        '''distance sun to jupiter'''
        d_sun_jup = np.sqrt(  jupiter[:,0][:,0]**2
                            + jupiter[:,0][:,1]**2
                            + jupiter[:,0][:,2]**2
                            )[:,None]

        '''distance sun to astroids'''
        d_sun_ast = np.sqrt(  astroids[:,0][:,0]**2
                            + astroids[:,0][:,1]**2
                            + astroids[:,0][:,2]**2
                            )[:,None]
        '''distance jupiter to astroids'''
        d_jup_ast = np.sqrt(  (astroids[:,0][:,0]-jupiter[:,0][:,0])**2
                            + (astroids[:,0][:,1]-jupiter[:,0][:,1])**2
                            + (astroids[:,0][:,2]-jupiter[:,0][:,2])**2
                            )[:,None]

        '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''
        '''%%% Euler-Cromer method to calculate velocity and position'''
        '''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

        ''' calculate the evolution jupiter through time'''
        jupiter[:,1] += h *    (-ps.G/(d_sun_jup**3)* jupiter[:,0])
        jupiter[:,0] += h * jupiter[:,1]

        ''' calculate the evolution astroids through time'''
        astroids[:,1] += h * (-ps.G/(d_sun_ast**3)* astroids[:,0]
                           + (-ps.G*ps.M_jup/(d_jup_ast**3) * (astroids[:,0] - jupiter[:,0]) ) )
        astroids[:,0] += h * astroids[:,1]

        # if t%10000 ==0:
        '''delete diverging astroids'''
        bound_astroids = np.logical_and( d_sun_ast[:,0] > 1.7,  d_sun_ast[:,0] < 4.0 )
        astroids = astroids[bound_astroids]

    if save:
        np.savez(str(extra_name) + "_date_" + str(current_date) +  "_all_info_time_" +str(time)+"_h_"+str(h)+"_n_"+str(number_of_astroids),\
         a_pos=astroids[:,0], a_vel=astroids[:,1], j_pos=jupiter[:,0], j_vel=jupiter[:,1], d_astroid=d_sun_ast)

    print ("astroids left", np.sum(bound_astroids))

    return jupiter, astroids


def convergence_test(time, h, save=False, extra_name=''):
    '''This function is to investigate the error convergence of the Euler-Cromer method for a 3 planet system. However, it does not work correctly.'''

    p_1_pos = open("p_1_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    p_2_pos = open("p_2_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    p_3_pos = open("p_3_positions_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    # p_1_vel = open("p_1_velocities_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    # p_2_vel = open("p_2_velocities_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    # p_3_vel = open("p_3_velocities__"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    # distance_planets = open("distance_planets_"+str(extra_name)+"_date_"+str(current_date)+"_convergence_time_"+str(time)+"_h_"+str(h)+".dat", "a")

    p_1   = np.array([[ [np.cos(2*np.pi/3),np.sin(2*np.pi/3),0.0] , [-np.sin(2*np.pi/3),np.cos(2*np.pi/3),0.0] ]]) * ps.a
    p_2   = np.array([[ [np.cos(4*np.pi/3),np.sin(4*np.pi/3),0.0] , [-np.sin(4*np.pi/3),np.cos(4*np.pi/3),0.0] ]]) * ps.a
    p_3   = np.array([[ [np.cos(2*np.pi  ),np.sin(2*np.pi  ),0.0] , [-np.sin(2*np.pi  ),np.cos(2*np.pi  ),0.0] ]]) * ps.a



    n = int(time/h) #number of timesteps
    for t in range(n-1):
        '''calculate the distances between the three planets'''

        d_one_two = np.sqrt(    ( p_1[:,0][:,0] - p_2[:,0][:,0] )**2
                              + ( p_1[:,0][:,1] - p_2[:,0][:,1] )**2
                              + ( p_1[:,0][:,2] - p_2[:,0][:,2] )**2
                              )[:,None]

        d_one_three = np.sqrt(  ( p_1[:,0][:,0] - p_3[:,0][:,0] )**2
                              + ( p_1[:,0][:,1] - p_3[:,0][:,1] )**2
                              + ( p_1[:,0][:,2] - p_3[:,0][:,2] )**2
                              )[:,None]

        d_two_three = np.sqrt(  ( p_2[:,0][:,0] - p_3[:,0][:,0] )**2
                              + ( p_2[:,0][:,1] - p_3[:,0][:,1] )**2
                              + ( p_2[:,0][:,2] - p_3[:,0][:,2] )**2
                              )[:,None]

        ''' calculate the evolution of the planets through time'''

        p_1[:,1]   += h * ( -ps.G/(d_one_two**3) * (p_2[:,0]-p_1[:,0]) ) + h * ( -ps.G/(d_one_three**3) * (p_1[:,0]-p_3[:,0]) )
        p_1[:,0]   += h * p_1[:,1]

        p_2[:,1]   += h * ( -ps.G/(d_one_two**3) * (p_2[:,0]-p_1[:,0]) ) + h * ( -ps.G/(d_two_three**3) * (p_3[:,0]-p_2[:,0]) )
        p_2[:,0]   += h * p_2[:,1]

        p_3[:,1] += h * (-ps.G/(d_one_three**3) * (p_1[:,0] - p_3[:,0])) + h * ( -ps.G/(d_two_three**3) * (p_3[:,0]-p_2[:,0]) )
        p_3[:,0] += h * p_3[:,1]

        '''saves data every 100000 timesteps.'''

        plt.plot( p_1[:,0], p_1[:,1], 'r-', label="planet 1")
        plt.plot( p_2[:,0], p_2[:,1], 's', label="planet 2", c=c2)
        plt.plot( p_3[:,0], p_3[:,1], '^', label="planet 3", c=c3)

        if save:
            # np.savez(str(extra_name) + "_date_" + str(current_date) +  "_convergence_time_" +str(time)+"_h_"+str(h),\
            #  p_1_pos=p_1[:,0], p_1_vel=p_1[:,1], p_2_pos=p_2[:,0], p_2_vel=p_2[:,1], p_3_pos=p_3[:,0], p_3_vel=p_3[:,1])
            np.savetxt(p_1_pos,p_1[:,0], fmt='%1.4e')
            np.savetxt(p_2_pos,p_2[:,0], fmt='%1.4e')
            np.savetxt(p_3_pos,p_3[:,0], fmt='%1.4e')
        # np.savetxt(p_1_vel,p_1[:,1])
        # np.savetxt(p_2_vel,p_2[:,1])
        # np.savetxt(p_3_vel,p_3[:,1])
        # np.savetxt(distance_planets, distance_planets)
    # plt.axis('equal')


    plt.show()
    return p_1[:,0], p_2[:,0], p_3[:,0]#, distance_planets
