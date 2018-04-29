from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pars as ps
import numpy as np

current_date = np.datetime64('today')

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

def convergence_test(time, h):
    '''This function is to investigate the error convergence of the Euler-Cromer method for a 3 planet system. However, it does not work correctly.'''

    planet_one_pos = open("planet_one_positions_time_" +str(time)+"_h_"+str(h)+".dat", "a")
    planet_one_vel = open("planet_one_velocities_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    planet_two_pos = open("planet_two_positions_time_" +str(time)+"_h_"+str(h)+".dat", "a")
    planet_two_vel = open("planet_two_velocities_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    planet_three_pos = open("planet_three_positions_time_" +str(time)+"_h_"+str(h)+".dat", "a")
    planet_three_vel = open("planet_three_velocities_time_"+str(time)+"_h_"+str(h)+".dat", "a")
    distance_planets = open("distance_planets_time_" +str(time)+"_h_"+str(h)+".dat", "a")
    fig, axes = plt.subplots(nrows=1, ncols=1)
    w, h = fig.get_size_inches()
    fig.set_size_inches(1.2 * w, 2.4* h)

    planet_one   = np.array([[ [np.cos(  np.pi/3),np.sin(  np.pi/3),0.0] , [-np.sin(  np.pi/3),np.cos(  np.pi/3),0.0] ]])
    planet_two   = np.array([[ [np.cos(2*np.pi/3),np.sin(2*np.pi/3),0.0] , [-np.sin(2*np.pi/3),np.cos(2*np.pi/3),0.0] ]])
    planet_three = np.array([[ [np.cos(  np.pi  ),np.sin(  np.pi  ),0.0] , [-np.sin(  np.pi  ),np.cos(  np.pi  ),0.0] ]])

    n = int(time/h) #number of timesteps
    for t in range(n-1):
        '''calculate the distances between the three planets'''

        d_one_two = np.sqrt(    (planet_one[:,0][:,0]-planet_two[:,0][:,0])**2
                              + (planet_one[:,0][:,1]-planet_two[:,0][:,1])**2
                              + (planet_one[:,0][:,2]-planet_two[:,0][:,2])**2
                              )[:,None]

        d_one_three = np.sqrt(  (planet_one[:,0][:,0]-planet_three[:,0][:,0])**2
                              + (planet_one[:,0][:,1]-planet_three[:,0][:,1])**2
                              + (planet_one[:,0][:,2]-planet_three[:,0][:,2])**2
                              )[:,None]

        d_two_three = np.sqrt(  (planet_two[:,0][:,0]-planet_three[:,0][:,0])**2
                              + (planet_two[:,0][:,1]-planet_three[:,0][:,1])**2
                              + (planet_two[:,0][:,2]-planet_three[:,0][:,2])**2
                              )[:,None]

        ''' calculate the evolution of the planets through time'''

        planet_one[:,1]   += h * (-2*ps.G/(d_one_two**3) * (planet_one[:,0]-planet_two[:,0]))
        + h * (-2*G/(d_one_three**3) * (planet_one[:,0]-planet_three[:,0]))
        planet_one[:,0]   += h * planet_one[:,1]

        planet_two[:,1]   += h * (-2*ps.G/(d_one_two**3) * (planet_two[:,0]-planet_one[:,0]))
        + h * (-2*G/(d_two_three**3) * (planet_two[:,0]-planet_three[:,0]))
        planet_two[:,0]   += h * planet_two[:,1]

        planet_three[:,1] += h * (-2*ps.G/(d_one_three**3) * (planet_three[:,0] - planet_one[:,0]))
        + h * (-2*G/(d_two_three**3) * (planet_three[:,0] - planet_two[:,0]))
        planet_three[:,0] += h * planet_three[:,1]

        '''saves data every 100000 timesteps.'''
        if t < 1000000:
            np.savetxt(planet_one_pos,planet_one[:,0])
            np.savetxt(planet_two_pos,planet_two[:,0])
            np.savetxt(planet_three_pos,planet_three[:,0])
            np.savetxt(planet_one_vel,planet_one[:,1])
            np.savetxt(planet_two_vel,planet_two[:,1])
            np.savetxt(planet_three_vel,planet_three[:,1])
            np.savetxt(distance_planets, distance_planets)

    return planet_one, planet_two, planet_three, distance_planets
