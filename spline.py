#!/usr/bin/env python3
# *_* coding: utf-8 *_*

from scipy.interpolate import CubicSpline
from scipy.interpolate import CubicHermiteSpline
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import numpy as np
import math
"""
Required Packages:
====================================================
pip3 install matplotlib  # Plotting!
pip3 install scipy       # spline interpolation
pip3 install numpy       # vector / matrix library

Also useful:
====================================================
pip3 install yapf        # autoformatting

License:  MIT
"""


def main():
    """
    Simple script to compare different types of spline interpolation.

    Constructs several types of interpolation splines through the same
    data set and plots them. This makes it simple to compare the pros
    and cons for each type of interpolator. The object returned by the
    interpolation solver code are fancy wrappers around vectors of 
    polynomial coefficients. You can read the docs for the interpolation
    library to figure out how to grab these coefficients and do interesting
    things with them. For example, you can manually joint two splines 
    together end to end, or evaluate the splines using your own code.

    See also:
    https://docs.scipy.org/doc/scipy/reference/interpolate.html#module-scipy.interpolate

    Notation:
      t = time (input)
      y = value (output)
    """

    # Arbitrary data to fit the spline through.
    # Try experimenting with changing these values or adding more.
    x_knots = np.array([0, 1, 2, 1.5, 0, -1.5, -2, -1, 0])
    y_knots = np.array([0, 1, 2, 3, 2.25, 3, 2, 1, 0])

    # derivative (slope) at the knots, used only for cubic hermite.
    dy_knots = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Fit the spline through the "knot" points
    # Must be monotonically increasing, but not necessarily uniformly spaced
    t_knots = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

    # Plot the spline using the "evaluation" points
    t_eval = np.linspace(t_knots[0], t_knots[-1], 200)

    # Empty dictionary, we will add different types of interpolation
    # splines here. This can then be used later on by plotting code.
    y_traj = dict()
    x_traj = dict()

    # Here are two common boundary conditions used for cubic "spline" interplation.
    # Try experimenting with different boundary condition types (`bc_type`)
    # - Pro: smooth (continuous acceleration)
    # - Con: globally coupled, overshoot ("ringing"), requires sparse solve
    y_traj["spline_clamped"] = CubicSpline(t_knots, y_knots, bc_type='clamped')
    y_traj["spline_clamped-x"] = CubicSpline(t_knots, x_knots, bc_type='clamped')


    theta1 = []
    theta2 = []
    x_new = []
    y_new = []
    x = y_traj["spline_clamped-x"](t_eval)
    y = y_traj["spline_clamped"](t_eval)
    L1 = 2.75
    L2 = 2.75
    for n in range(len(x)):
        L3 = ((x[n]**2) + (y[n]**2))**0.5
        cos_a2 =((L3**2)-(L1**2)-(L2**2))/(-2*L1*L2)
        a2 = math.atan2((1-(cos_a2**2))**0.5, cos_a2)
        theta_2 = math.pi-a2
        theta2.append(theta_2)
        cos_a1 = ((L2**2)-(L1**2)-(L3**2))/(-2*L1*L3)
        a1 = math.atan2((1-(cos_a1**2))**0.5,cos_a1)
        theta_1 = math.atan2(x[n],y[n])-a1
        theta1.append(theta_1)
        
        x_new_n = L1*math.cos(theta_1)+ L2*math.cos(theta_1 + theta_2)
        y_new_n = L1*math.sin(theta_1)+ L2*math.sin(theta_1 + theta_2)
        x_new.append(x_new_n)
        y_new.append(y_new_n)
    np.savetxt('theta1.csv',theta1,delimiter = ',')
    np.savetxt('theta2.csv',theta2,delimiter = ',')


    plt.figure(3)
    plt.plot(x_new,y_new)
    plt.plot(t_eval,theta1)
    plt.plot(t_eval,theta2)
    plt.show()

    print(theta_1)

    

if '__main__' == __name__:
    main()
