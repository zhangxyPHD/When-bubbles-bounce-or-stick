import mph
import pandas as pd
import os
from multiprocessing import Pool
import numpy as np

absolutePath = os.path.dirname(os.path.abspath(__file__))
basic_model_path = os.path.join(absolutePath, 'bubble_basic_model.mph')
filename = os.path.join(absolutePath, 'inputdata.csv')

core_num=1
para_num=10
t_step=0.002
t_max=500
Bos=[0.0002,0.0004,0.0007,0.001,0.002,0.004,0.007,0.01,0.02,0.04,0.07,0.4,0.6,0.8,1]
# Gas=[5.0,5.5,6.0,6.5,6.25,6.75,7.0,8.0,9.0,10,15,20,30,40,50,60,80,700,200,400,600,800,1000]
Gas=[6.0,6.5,7.0]
Ga_Bos=[]
for Bo in Bos:
    for Ga in Gas:
        Ga_Bos.append([Ga,Bo])

def run_simulation(params):
    Ga, Bo  = params
    L_rise=10
    refine_num=7
    # Connect to a COMSOL server instance
    client = mph.start(cores=core_num)  # Adjust the number of cores as needed
    saveFileName = os.path.join(absolutePath, f'bubble-L_rise{L_rise}-Ga{Ga}-Bo{Bo}-Level{refine_num}-base.mph')
    saveResultsName = os.path.join(absolutePath, f'results_L_rise{L_rise}_Ga{Ga}_Bo{Bo}_Level{refine_num}.csv')
    saveDimensionResultsName = os.path.join(absolutePath, f'results_dimension_L_rise{L_rise}_Ga{Ga}_Bo{Bo}_Level{refine_num}.csv')

    if os.path.exists(saveResultsName):
        print(f'Results already exist for L_rise = {L_rise}, Ga = {Ga}, Bo = {Bo}')
        return

    # Load the model
    model = client.load(basic_model_path)    

    # Set parameters
    model.parameter('L_rise', str(L_rise))
    model.parameter('Ga', str(Ga))
    model.parameter('Bo', str(Bo))
    model.parameter('t_max', str(t_max))
    model.parameter('t_step', str(t_step)) 
    model.parameter('refine', str(refine_num)) 
    model.save(saveFileName)


def main():
    for Ga_Bo in Ga_Bos:
        run_simulation(Ga_Bo)

if __name__ == '__main__':
    main()
