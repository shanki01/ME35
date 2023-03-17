from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
import math

def main():

    x_knots = np.array([0, 1, 3, 6, 9, 11, 12])
    y_knots = np.array([-16, -14, -12, -11.5, -12, -14, -16])

    t_knots = np.array([0, 1, 2, 3, 4, 5, 6])

    t_eval = np.linspace(t_knots[0], t_knots[-1], 200)

    y_traj = dict()
    x_traj = dict()

    y_traj["spline_clamped"] = CubicSpline(t_knots, y_knots, bc_type='clamped')
    x_traj["spline_clamped-x"] = CubicSpline(t_knots, x_knots, bc_type='clamped')


    theta1 = []
    theta2 = []
    x_new = []
    y_new = []
    y = y_traj["spline_clamped"](t_eval)
    x = x_traj["spline_clamped-x"](t_eval)

    plt.figure(3)
    plt.plot(x,y)
    plt.title('Leg Trajectory')
    plt.xlim(0,12)
    plt.xlabel('x Position (cm)')
    plt.ylim(-16,0)
    plt.ylabel('y Position (cm)')
    plt.show()

    L1 = 7
    L2 = 13
    for n in range(len(x)):
        L3 = ((x[n]**2) + (y[n]**2))**0.5
        cos_a2 =((L3**2)-(L1**2)-(L2**2))/(-2*L1*L2)
        a2 = math.atan2((1-(cos_a2**2))**0.5, cos_a2)
        theta_2 = math.pi-a2
        theta2.append(theta_2)
        cos_a1 = ((L2**2)-(L1**2)-(L3**2))/(-2*L1*L3)
        a1 = math.atan2((1-(cos_a1**2))**0.5,cos_a1)
        theta_1 = math.atan2(y[n],x[n])-a1
        theta1.append(theta_1)
        
    np.savetxt('theta1.csv',theta1,delimiter = ',')
    np.savetxt('theta2.csv',theta2,delimiter = ',')

if '__main__' == __name__:
    main()
