import os

# Define the absolute path to the 'prompts' directory, relative to this script's location
PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompts')

def build_direct_prompt(task, **kwargs):
    with open(os.path.join(PROMPTS_DIR, f'direct_{task}.txt'), 'r') as f:
        template = f.read()
        return template.format(**kwargs)

def build_cot_prompt(task, **kwargs):
    with open(os.path.join(PROMPTS_DIR, f'cot_{task}.txt'), 'r') as f:
        template = f.read()
        return template.format(**kwargs)
