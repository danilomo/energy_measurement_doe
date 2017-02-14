#### Introduction

It helps to create experimental designs for the energy_measurement_scripts project.

Just modify the ./pythonScripts/experiments.py file and override the Experiment class. 
Override the getConfig and getProviderConfig and make them return a dictionary containing the configuration parameters
for the VM provider and for the experiment.
