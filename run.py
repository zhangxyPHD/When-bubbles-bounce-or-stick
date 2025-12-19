#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import mph
import pandas as pd
import os

def parse_arguments():
    """
    Parse command-line arguments for a single simulation run:
      --Bo (Bond number)
      --Ga (Galilei number)
      --Lrise (rise distance)
      --refine_num (mesh refinement level)
      --t_step (time step)
      --t_max (max simulation time)
      --cores (number of cores for COMSOL, default=32)
    """
    parser = argparse.ArgumentParser(
        description='Run a single COMSOL bubble model simulation with given parameters.'
    )
    parser.add_argument('--Bo', type=str, required=True,
                        help='Bond number, e.g., 0.1. (Now stored as string!)')
    parser.add_argument('--Ga', type=str, required=True,
                        help='Galilei number, e.g., 4. (Now stored as string!)')
    parser.add_argument('--Lrise', type=str, required=True,
                        help='Bubble rise distance, e.g., 20. (Now stored as string!)')
    parser.add_argument('--refine_num', type=str, required=True,
                        help='Mesh refinement level, e.g., 8. (Now stored as string!)')
    parser.add_argument('--t_step', type=str, required=True,
                        help='Time step, e.g., 0.1. (Now stored as string!)')
    parser.add_argument('--t_max', type=str, required=True,
                        help='Max simulation time, e.g., 0.2. (Now stored as string!)')
    parser.add_argument('--cores', type=str, default='32',
                        help='Number of cores for COMSOL to use (default=32, but stored as string!).')
    parser.add_argument('--name', type=str, default='32',
                        help='Name for COMSOL to use (default=32, now stored as string!).')
    return parser.parse_args()

def main():
    # ========== Parse the command-line arguments ==========
    args = parse_arguments()

    Bo         = args.Bo
    Ga         = args.Ga
    L_rise     = args.Lrise
    refine_num = args.refine_num
    t_step     = args.t_step
    t_max      = args.t_max
    cores      = args.cores
    name      = args.name

    # ========== Directories and file paths ==========
    absolute_path     = os.path.dirname(os.path.abspath(__file__))
    basic_model_path  = os.path.join(absolute_path, 'Axi_bubble_basic_model.mph')
    
    # Output names
    save_file_name    = os.path.join(
        absolute_path, f'bubble_{name}.mph'
    )
    save_results_name = os.path.join(
        absolute_path, f'results_{name}.csv'
    )
    save_results_name1 = os.path.join(
        absolute_path, f'results_{name}-1.csv'
    )
    save_video_name = os.path.join(
        absolute_path, f'video_{name}.webm'
    )
    save_video_name1 = os.path.join(
        absolute_path, f'video_{name}-1.webm'
    )
    # ========== Check if results already exist ==========
    if os.path.exists(save_results_name):
        print(f'[Skip] Results already exist for L_rise={L_rise}, Ga={Ga}, Bo={Bo}.')
        return

    # ========== Start the COMSOL client with specified cores ==========
    print(f'[Info] Starting COMSOL with {cores} cores...')
    client = mph.start(cores=cores)

    # ========== Load the base model ==========
    print(f'[Info] Loading base model: {basic_model_path}')
    model = client.load(basic_model_path)

    # ========== Set model parameters ==========
    model.parameter('L_rise',  str(L_rise))
    model.parameter('Ga',      str(Ga))
    model.parameter('Bo',      str(Bo))
    model.parameter('t_step',  str(t_step))
    model.parameter('t_max',   str(t_max))
    model.parameter('refine',  str(refine_num))

    # Optional: Save once after setting parameters
    model.save(save_file_name)

    # ========== Define columns to evaluate ==========
    columns = [
        't', 'velocity', 'center', 'max_x', 'max_y', 'min_y',
        'max_y_Axi', 'min_y_Axi', 'ratio', 'area', 'R_eq',
        'E_k', 'E_P', 'E_e', 'E_s', 'Int_Ee'
    ]

    try:
        # ========== Solve the model ==========
        print('[Info] Solving the model ...')
        model.solve()
        
        # ========== Evaluate results ==========
        print('[Info] Evaluating results ...')
        results = model.evaluate(columns, dataset='Study 1//Remeshed Solution 1')
        df = pd.DataFrame(results, columns=columns)
        df = df.round(8)

        # Adjust potential energy by its minimum value, if needed
        min_EP = df['E_P'].min()
        df['E_P'] = df['E_P'] - min_EP

        # Flip the y-direction if required
        df['center'] = -1 * df['center']
        df['max_y']  = -1 * df['max_y']
        df['min_y']  = -1 * df['min_y']

        # Save to CSV
        df.to_csv(save_results_name, index=False)
        print(f'[OK] Results saved to {save_results_name}')

        model.export('Video', save_video_name)
        print(f'[OK] Video saved to {save_video_name}')


        # Save the solved model
        model.save(save_file_name)
        print(f'[OK] Solved model saved to {save_file_name}')

    except Exception as e:
        print(f'[Error] Exception for L_rise={L_rise}, Ga={Ga}, Bo={Bo}:\n{e}')
        # Optionally, attempt partial results extraction here if needed
        # ========== Evaluate results ==========
        print('[Info] Evaluating results ...')
        results = model.evaluate(columns, dataset='Study 1//Remeshed Solution 1')
        df = pd.DataFrame(results, columns=columns)
        df = df.round(8)

        # Adjust potential energy by its minimum value, if needed
        min_EP = df['E_P'].min()
        df['E_P'] = df['E_P'] - min_EP

        # Flip the y-direction if required
        df['center'] = -1 * df['center']
        df['max_y']  = -1 * df['max_y']
        df['min_y']  = -1 * df['min_y']

        # Save to CSV
        df.to_csv(save_results_name1, index=False)
        print(f'[OK] Results saved to {save_results_name1}')
        model.export('Video', save_video_name1)
        print(f'[OK] Video saved to {save_video_name1}')
        # Save the solved model
        model.save(save_file_name)
        print(f'[OK] Solved model saved to {save_file_name}')
    finally:
        # Remove the model from the client to free resources
        client.remove(model)
        print('[Done] Model removed from COMSOL client.')

if __name__ == '__main__':
    main()
