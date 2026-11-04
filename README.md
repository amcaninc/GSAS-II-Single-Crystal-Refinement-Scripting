# GSAS-II-Single-Crystal-Refinement-Scripting
Using the scriptable version of the GSAS-II software at https://advancedphotonsource.github.io/ to refine Ho2Ti2O7 automatically with different refinement tasks

### Description
This is a snippet of code used to generate evenly-spaced training data across an 8-D parameter space via Latin hypercube sampling. This allows for input of physically-informed parameter bounds for crystal Ho2Ti2O7, combined with use of .hkl files from four different cuts of the crystal at 110K and 293K. For each iteration, the parameters from Latin Hypercube sampling are inputted as either fractional occupancy ("F"), atomic position ("X"), or Uiso thermal displacement ("U") parameters for either the O1, Ti1, Ho1, or O2 atoms in the crystal, and a simulated reflection list is generated from GSAS-II for comparison with experimental data. Data can be generated this way in large quantity for use in training machine learning models, such as physically-constrained autoencoders (see https://doi.org/10.1063/5.0320208).

This code is designed to be used as a basic template for using GSAS-II with Python scripting. For more information on how to install or use GSAS-II, see https://advancedphotonsource.github.io/. 
