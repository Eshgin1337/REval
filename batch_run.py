#!/usr/bin/env python3
"""
Batch execution script for REval framework.
Runs multiple evaluation tasks in parallel for a given model.
"""

import os
import sys
import subprocess
import argparse
from tqdm import tqdm

def print_usage():
    """Display detailed usage instructions"""
    print("""
Batch Execution Script for REval Framework
==========================================

Purpose: Run all evaluation tasks (coverage, state, path, output, consistency) 
         multiple times for statistical significance.

Usage: python batch_run.py <model_id>

Arguments:
  model_id    Model identifier to evaluate. This must match configuration 
              files in the .configs/ directory.

Examples:
  python batch_run.py gpt-3.5          # Run all tasks for GPT-3.5
  python batch_run.py codellama-7b     # Run all tasks for CodeLlama

Prerequisites:
  1. Configuration files must exist in .configs/ directory
  2. Files should be named: .configs/{model_id}_{task}
  3. Tasks: coverage, state, path, output, consistency

To create configuration files:
  python evaluation.py config

Output:
  Results are saved to .batch_run/ directory
  Files are named: {model_id}_{task}_run{number}

By default, each task runs 5 times for statistical reliability.
Tasks run in parallel for efficiency.
""")

def check_config_files(model_id):
    """Verify that configuration files exist for the given model"""
    tasks = ['coverage', 'state', 'path', 'output', 'consistency']
    config_dir = '.configs'
    missing_files = []
    
    if not os.path.exists(config_dir):
        print(f"ERROR: Configuration directory '{config_dir}' not found.")
        print(f"       Create it using: mkdir {config_dir}")
        return False
    
    for task in tasks:
        config_file = os.path.join(config_dir, f"{model_id}_{task}")
        if not os.path.exists(config_file):
            missing_files.append(config_file)
    
    if missing_files:
        print(f"ERROR: Missing configuration files for model '{model_id}':")
        for file in missing_files:
            print(f"       - {file}")
        print(f"\n       Create configuration files using: python evaluation.py config")
        return False
    
    return True

def main():
    # Handle help flags or no arguments
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    model_id = sys.argv[1]
    
    # Basic validation
    if model_id.startswith('-'):
        print(f"ERROR: Invalid model_id: '{model_id}'")
        print("       Use -h or --help for usage information.")
        sys.exit(1)
    
    # Check for required configuration files
    if not check_config_files(model_id):
        sys.exit(1)
    
    # Configuration
    num_repeats = 5
    config_path = '.configs'
    save_output_path = '.batch_run'
    python_path = sys.executable
    tasks = ['coverage', 'state', 'path', 'output']
    
    # Create output directory
    os.makedirs(save_output_path, exist_ok=True)
    
    def get_cmd(task, run_id):
        """Build command string for a task"""
        config_file = os.path.join(config_path, f"{model_id}_{task}")
        output_file = os.path.join(save_output_path, f"{model_id}_{task}_run{run_id}")
        return f'{python_path} evaluation.py -i {config_file} > {output_file}'
    
    # Display execution info
    print(f"Starting batch evaluation for model: {model_id}")
    print(f"Configuration directory: {config_path}")
    print(f"Output directory: {save_output_path}")
    print(f"Number of repeats per task: {num_repeats}")
    print("-" * 60)
    
    # Main execution loop
    try:
        for i in tqdm(range(num_repeats), desc="Progress"):
            procs = []
            
            # Start all tasks in parallel
            for task in tasks:
                cmd = get_cmd(task, i+1)
                proc = subprocess.Popen(cmd, shell=True)
                procs.append(proc)
                print(f'  Started {task} (process ID: {proc.pid})')
            
            # Wait for all tasks to complete
            for idx, proc in enumerate(procs):
                proc.wait()
                print(f'  Completed {tasks[idx]}')
            
            # Run consistency task (depends on others)
            proc = subprocess.Popen(get_cmd('consistency', i+1), shell=True)
            proc.wait()
            print(f'  Completed consistency check')
            print(f'  Finished iteration {i+1}/{num_repeats}')
            print()
        
        print(f"Batch execution completed successfully.")
        print(f"Results saved to: {save_output_path}/")
        
    except KeyboardInterrupt:
        print("Batch execution interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error during batch execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()