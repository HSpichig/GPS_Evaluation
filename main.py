import numpy as np
import pandas as pd
from math import *
import matplotlib.pyplot as plt
from fitter import Fitter
from pyproj import Geod
from scipy.stats import t

# pip install pandas, numpy, fitter, pyproj, matplotlib, openpyxl


# Transforms coordinates of the form [long, lat] to distance to reference point (d) and angle from north (phi) in rad
# Takes as input the coordinates of the reference point (zero) and of the point to transform (coords)
# Both points are to be formatted as follows [long, lat]
# Returns [d, phi] of coords
def transform_to_rad(zero, coords):
    g = Geod(ellps='WGS84') # Initiate Geode based on WGS84
    a, phi, d = g.inv(zero[1], zero[0], coords[1], coords[0])
    #print(phi)
    return [d, radians(phi)]


def read_reference_data(path):
    report_raw = pd.read_excel(path).values.tolist()[1:]
    report = []
    for i in range(len(report_raw)):
        id = report_raw[i][0]
        name = report_raw[i][1]
        lat = report_raw[i][9]
        long = report_raw[i][10]
        if i > 0:
            if (report_raw[i-1][9] != lat) | (report_raw[i-1][10] != long):
                # Remove entries where location was not updated
                report.append([id, name, long, lat])
        else:
            report.append([id, name, long, lat])
    return report


# Function returning the probability of E given P
# Inputs:
# P: Coordinates of point P in form [long, lat]
# E: Coordinates of point E in form [long, lat]
# hw: half of the wedge size used to calculate the angular probability
# Ref: list of reference measures from point P in form [[x0,y0],...]
# Returns list of probabilities in form [pphi, pdist] where
# pphi: the probability to observe a measurement in a (2 * hw) wedge centered around the angle of the evidence
# pdist: the probability to observe a measurement at the distance of the evidence given it is within the given wedge
def get_probabilities(P, E, Ref, hw, n):
    E_rad = transform_to_rad(P,E)
    Ref_rad = []

    for i in Ref:
        Ref_rad.append(transform_to_rad(P, [float(i[2]), float(i[3])]))

    phi_c = 0 # Initialise counter for measurement points within angle
    wedge = [] # Initialise list of distances within the wedge
    for i in Ref_rad:
        if (i[1] >= E_rad[1] - hw) & (i[1] <= E_rad[1] + hw):
            wedge.append(i[0])
            phi_c += 1

    print("Fraction within wedge for P" + n + ": " + str(len(wedge)))
    print("Distances within wedge for P" + n + ": " + str(wedge))
    if wedge:
        f = Fitter(wedge, distributions='t')
        f.fit()
        t_par = f.get_best()['t']
        pd = t.pdf(E_rad[0], t_par['df'], t_par['loc'], t_par['scale'])
        plot_wedge(wedge, E_rad[0], n)
    else:
        pd = 0
    return [float(phi_c) / float(len(Ref_rad)), pd]


# Draws a histogram of the inputted reference data collection (wedge) and the observed Evidence value (d_E)
def plot_wedge(wedge, d_E, n):
    plt.clf()
    plt.cla()
    plt.hist(wedge, color='darkgray', bins=np.arange(0, 160, 5), density=True)
    plt.plot(2 * [d_E], [0, 0.15], c='red')
    plt.savefig('hist_Wedge' + n + '.png', bbox_inches='tight')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    hw = pi/6 # Half of the wedge size used for the angular probability

    P1_measurements = read_reference_data('Report_P1.xlsx')
    print("P1: " + str(len(P1_measurements)))
    P2_measurements = read_reference_data('Report_P2.xlsx')
    print("P2: " + str(len(P2_measurements)))

    P1 = [6.573832039, 46.521592273] # Coordinates of P1
    P2 = [6.575116326, 46.521954786] # Coordinates of P2

    E = [6.57394444444444, 46.5213305555556] # Coordinates of E

    e_p1 = transform_to_rad(E, P1)
    e_p2 = transform_to_rad(E, P2)
    print("E -> P1" + str(e_p1))
    print("E -> P2" + str(e_p2))

    P1_probs = get_probabilities(P1, E, P1_measurements, hw, "1")
    P2_probs = get_probabilities(P2, E, P2_measurements, hw, "2")

    print("Angular probability given P1: " + str(P1_probs[0]))
    print("Angular probability given P2: " + str(P2_probs[0]))
    print("Distance probability given P1 and phi1: " + str(P1_probs[1]))
    print("Distance probability given P2 and phi2: " + str(P2_probs[1]))

    LR = (P1_probs[0] * P1_probs[1]) / (P2_probs[0] * P2_probs[1])
    print("LR in favour of P1: " + str(LR))

    # This section draws the scatter plot
    plt.cla()
    plt.clf()

    x_val = []
    y_val = []
    for i in P1_measurements:
        x_val.append(float(i[2]))
        y_val.append(float(i[3]))

    plt.scatter(x_val, y_val, s=15, c='darkgray', marker='x', label='P1 reference')

    x_val = []
    y_val = []
    for i in P2_measurements:
        x_val.append(float(i[2]))
        y_val.append(float(i[3]))

    plt.scatter(x_val, y_val, c='dimgray', s=15, marker='x', label='P2 reference')
    plt.scatter(P1[0], P1[1], c='darkgray', s=7, label='P1')
    plt.annotate("P1", (P1[0] + 0.00002, P1[1]), c='darkgray')
    plt.scatter(P2[0], P2[1], c='dimgray', s=7, label='P2')
    plt.annotate("P2", (P2[0] + 0.00002, P2[1]), c='dimgray')
    plt.scatter(E[0], E[1], c='black', s=7, label='E1')
    plt.annotate("E1", (E[0] - 0.0001, E[1] - 0.00005), c='black')
    plt.legend()

    plt.savefig('Scatter.png', bbox_inches='tight')


#Author: Spichiger Hannes