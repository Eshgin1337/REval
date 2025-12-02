# create_batch_configs.py
import os
import json
import sys

def setup_batch_config(model_id):
    """Setup all configuration files needed for batch execution"""
    config_dir = '.configs'
    os.makedirs(config_dir, exist_ok=True)
    
    # Load or create base config
    if os.path.exists('.eval_config'):
        with open('.eval_config', 'r') as f:
            base_config = json.load(f)
    else:
        print("Error: No .eval_config found. Run: python evaluation.py config")
        return False
    
    # Update model_id
    base_config['model_id'] = model_id
    
    # Create config for each task
    tasks = ['coverage', 'state', 'path', 'output', 'consistency']
    for task in tasks:
        task_config = base_config.copy()
        task_config['task'] = task
        
        config_file = os.path.join(config_dir, f"{model_id}_{task}")
        with open(config_file, 'w') as f:
            json.dump(task_config, f)
        print(f"Created: {config_file}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python create_batch_configs.py <model_id>")
        print("Example: python create_batch_configs.py gpt-3.5")
        sys.exit(1)
    
    model_id = sys.argv[1]
    if setup_batch_config(model_id):
        print(f"\nBatch configuration complete for model: {model_id}")
        print(f"Now run: python batch_run.py {model_id}")
