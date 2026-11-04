import os
import sys
import json

# Version control:
    #VSCode 1.90.1
    #Python 3.11.9
    #GSASII 35338b (gsas2full-Latest-Windows-x86_64.exe)
    # I have been running the script using the base kernel downloaded with GSASII
    
# Version control:
    #VSCode 1.90.1
    #Python 3.11.9
    #GSASII 0c1165 (note: run git pull to ensure latest version)
    #numpy  1.26.4
    #scipy  1.14.0

# Note: If running on ISAAC server (linux OS),
#       the program may have an issue locating the binary files
#       as well as downloading and compiling all necessary files.
#       Ensure that a binary location is located properly after running G2.sc.ShowVersions().

# Before running: ensure file paths are specific to YOUR own directory, be sure to update/check they are correct

# Add the GSAS-II module path
current_directory = os.getcwd()
#FIXME replace below with the path to your main GSAS-II directory
sys.path.insert(0, os.path.join(current_directory, "GSAS-II-5797"))

# Import necessary modules
import G2script as G2sc
import numpy as np 
from matplotlib import pyplot as plt 
import csv
from scipy.stats import qmc

#print(G2sc.ShowVersions())

# Define paths|
current_directory = os.getcwd()

workdir = os.path.join(current_directory, "gsasscripting", "GPX")  # Project directory
datadir = os.path.join(current_directory, "data")  # Data directory

# RANDOM SAMPLING
# Define how many samples hecre
num = 25000

# Latin hypercube sampling
def hypercubesample():
    ranges = [
        (0.4, 0.5), # xO1
        (0, 0.1), # UO1
        (0.8, 1.2), # OccTi1
        (0, 0.1), # UTi1
        (0.8, 1.2), # OccHo1
        (0, 0.1), # UHo1
        (0.8, 1.2), # OccO2
        (0, 0.1), # UO2
    ]
    sampler = qmc.LatinHypercube(d=8, seed=123)
    samples = sampler.random(n=num)
    scaled_samples = qmc.scale(samples, [r[0] for r in ranges], [r[1] for r in ranges])
    return scaled_samples

p = hypercubesample()

# Change structure/refinment parameters as needed, refine data, export as needed
for i in range(0, len(p)): # define number of training data files (iterations) you want

    # Type in the task that you want to perform in the filename and the code will do the rest.
        # FORMAT: filename-xtal-temp, where 1-4 gives crystal 1-4, temp = 1 means 110K, temp = 2 means 293K
    filename = str(i+1)
    folder = "//lustre/isaac24/scratch/amcaninc/training_08012026" #FIXME change to where you want to save generated files
    whichcrystal = 0
    # see if name goes correctly

    #FIXME change below to where you want to create your GPX file used by GSAS, can be opened in interactive GSAS GUI
    gpx = G2sc.G2Project(newgpx=f"//lustre/isaac24/scratch/amcaninc/training_08012026/gpx/training_08012026_{filename}.gpx") # create new project

    gpx.add_phase(os.path.join(datadir, 'HTO_original.cif'),'Ho2Ti2O7',fmthint='CIF') # add phase file

    xtals = {
    (1, 1): r"xs2555a.hkl",  # xtal1, temp = 110K
    (1, 2): r"xs2598a.hkl",  # xtal1, temp = 293K
    (2, 1): r"xs2556a.hkl",  # xtal2, temp = 110K
    (2, 2): r"xs2599a.hkl",  # xtal2, temp = 293K
    (3, 1): r"xs2560a.hkl",  # xtal3, temp = 110K
    (3, 2): r"xs2600a.hkl",  # xtal3, temp = 293K
    (4, 1): r"xs2559a.hkl",  # xtal4, temp = 110K
    (4, 2): r"xs2602a.hkl",  # xtal4, temp = 293K
    }

    crystal = 1
        # For temperature, based on third numher in the filename. If 1, temp = 110K, if 2, temp = 293K
    temperature = 1
    which_hkl = xtals.get((crystal, temperature))

    # REMEMBER to change xtal to match file path to hkl file
    # Original:
    gpx.add_single_histogram(os.path.join(datadir,f"xtal{str(crystal)}/" + which_hkl),0,fmthint='HKLF 4') # connecting exp file to phase


    #Change controls
    gpx.data['Controls']['data']['max cyc'] = 20
    gpx.data['Controls']['data']['UsrReject']['MinExt'] = .01
    gpx.data['Controls']['data']['UsrReject']['minF/sig'] = 0
    gpx.data['Controls']['data']['UsrReject']['MaxDF/F'] = 100
    gpx.data['Controls']['data']['UsrReject']['MinD'] = 0.1
    gpx.data['Controls']['data']['F**2'] = True
    gpx.data['Controls']['data']

    # Set refinement parameters for each atom
        # here they are set to be empty strings in order to ensure there is no refinement parameter
        # other options are F: fractional occupancy, X: atomic position, U: thermal displacement
    # Original:
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][0][2] = "" # O1
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][1][2] = "" # Ti1
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][2][2] = "" # Ho1
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][3][2] = "" # O2

    # p = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]
    # MAKE SURE TO CHANGE NUMPARAMS
    # numparams = 8

    # Edit the structure parameters 
        # Corresponding indices : 3 = x, 4 = y, 5 = z, 6 = frac (fractional occupancy), 10 = Uiso (thermal displacement)
    # Original:
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][0][3] = p[i][0]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][0][6] = 1
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][0][10] = p[i][1]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][1][6] = p[i][2]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][1][10] = p[i][3]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][2][6] = p[i][4]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][2][10] = p[i][5]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][3][6] = p[i][6]
    gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"][3][10] = p[i][7]

    # Phase information
    phase = gpx.phase(0)
    # Original: 
    phase.data['Histograms']['HKLF ' + which_hkl]['Extinction'][1] = 'Primary'
    phase.data['Histograms']['HKLF ' + which_hkl]


    h = gpx.histograms()[0]
    #prms = phase.data['Histograms'][h.name]
    h.set_refinements({'Scale':True})
    
    # Do the refinement
    gpx.save()
    gpx.do_refinements()
    gpx.save()
            
    # # Export only h,k,l and fcalc columns from reflection list to a .csv file
    ref_list = h.data['data'][1]['RefList']
    with open(f'{folder}/refList/hklf^2_{filename}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["h", "k", "l", "fcalc^2"])
        for row in ref_list:
            writer.writerow([row[0], row[1], row[2], row[7]])

    # # Write generated structure parameters to a .csv file
    phase_list = gpx.data["Phases"]["Ho2Ti2O7"]["Atoms"]
    filler = ""
    with open(f'{folder}/params/params_{filename}.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["label", "x", "y", "z", "frac", "Uiso"])
        writer.writerow([phase_list[0][0], "{:.10f}".format(p[i][0]), filler, filler, "{:.10f}".format(1), "{:.10f}".format(p[i][1])])
        x, y = 0, 1
        for row in phase_list[1:]:
            writer.writerow([row[0], filler, filler, filler, "{:.10f}".format(p[i][2 + x]), "{:.10f}".format(p[i][2 + y])])
            x += 2
            y += 2

    # # Write generated phase data (structure parameters after refinement) to a .txt file
    # with open(f'{folder}/ref_params/ref_params_{filename}.csv', 'w+', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["label", "x", "y", "z", "frac", "Uiso"])
    #     for row in phase_list:
    #         writer.writerow([row[0], "{:.10f}".format(row[3]), "{:.10f}".format(row[4]), "{:.10f}".format(row[5]), "{:.10f}".format(row[6]), "{:.10f}".format(row[10])])

# Write list of all points to a .txt file
with open("generated_points.txt", "w") as file:
    for point in p:
        # Write each point as a line in the file
        file.write(', '.join(map(str, point)) + '\n')

print("generated_points.txt created")