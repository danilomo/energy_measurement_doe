#!/bin/bash

cd experiments

for dir in $(ls)
do 
    cd $dir
    
    echo "Running experiment $dir..."
    
    ./start_experiment.sh
    
    cd ..
done
