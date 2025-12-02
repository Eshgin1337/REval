# REval
Replication package for the ICSE 2025 paper **"Reasoning Runtime Behavior of a Program with LLM: How Far Are We?"**

 

## 1. Prerequisites

### **Hardware Requirements**
- **GPT‑3.5/4 via OpenAI API:** Standard computer with internet access.
- **Open‑source LLMs locally:** NVIDIA/AMD GPUs with sufficient VRAM.
  - Experiments used **NVIDIA A800 GPUs**.
  - Hardware details: <https://docs.vllm.ai/en/latest/getting_started/installation.html>

### **Software Requirements**
- **Operating System:** Linux (primary support), macOS/Windows may work with adjustments.
- **Python:** Versions **3.8–3.11** (Conda optional but recommended).
- **Tools:** `jq` JSON processor (required for server scripts).
- **Python Dependencies:**
  - `pip install -r requirements.txt` — full local LLM support
  - `pip install -r requirements-nogpu.txt` — API‑only mode (OpenAI only)

### **No‑GPU Setup**
```bash
pip install -r requirements-nogpu.txt
```
Only OpenAI models can be evaluated in this mode.

 

## 2. Quick Start

### **2.1 Clone and Set Up Environment**
```bash
# Clone the repository
git clone https://github.com/r-eval/r-eval.github.io.git
cd REval

# Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt        # Local LLM evaluation
# OR
pip install -r requirements-nogpu.txt  # API-only mode
```

 

## 3. Environment Configuration

### **3.1 OpenAI Models (Commercial LLMs)**
1. Get your OpenAI API key: <https://platform.openai.com/account/api-keys>
2. Configure environment:
```bash
cp .env.example .env
vim .env
```
Fill in:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
# Optional:
# OPENAI_BASE_URL=https://api.openai.com/v1
```

### **3.2 Local LLMs (Open‑Source Models)**
Install **vLLM**:
```bash
pip install vllm
```
Download model weights (example: CodeLlama‑7B):
```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download('codellama/CodeLlama-7b-hf')"
```
Optional environment variables:
```bash
VLLM_HOST=localhost
VLLM_PORT=3000
```

 

## 4. Running Evaluations

### **4.1 Configuration Setup**
Start interactive configuration:
```bash
python evaluation.py config
```
You will be guided through:
- Task: **coverage**, **path**, **state**, **output**, **consistency**
- Prompt type: **direct** or **chain‑of‑thought (cot)**
- Model type: **OpenAI** or **HuggingFace**
- Model selection
- Temperature (default: **0.8**)

### **4.2 Single Evaluation**
```bash
python evaluation.py run
```

 

## 5. Batch Evaluation
### **5.1 Automated Batch Configuration (Recommended)**

If you want to batch run, you can use the command below:
```
python3 create_model_config <model_id>
```
which will automatically create separate config files that batch_run.py script requires



### **5.2 Run Batch Evaluation**
```bash
python batch_run.py gpt-3.5
```

### **Batch Details**
- **Repeats:** Each task runs **5 times** (default)
- **Parallel execution:** Enabled for efficiency
- **Output location:** `.batch_run/`
- **File naming:** `{model_id}_{task}_run{number}`

 

## 6. Model Support

### **OpenAI Models**
- **gpt‑3.5** → `gpt-3.5-turbo-0125`
- **gpt‑4** → `gpt-4-turbo-preview`

### **Local Models (vLLM Compatible)**
- Listed in `model_list.txt`
- Supported models list: <https://docs.vllm.ai/en/latest/models/supported_models.html>

 

## 7. Output and Results
- Evaluation outputs: `model_generations/`
- Batch outputs: `batch_run/`
- Configurations: `.configs/`
- Format: **JSONL** (logs, metrics, generations)

 

## 8. Troubleshooting

### **Common Issues**
#### *"Please install the vLLM package"*
Cause: Installed `requirements.txt` without GPU.
```bash
pip install -r requirements-nogpu.txt
```

#### *"OPENAI_API_KEY not found"*
- Ensure `.env` exists
- Ensure key is unquoted

#### *"Missing configuration files" (batch mode)*
- Ensure `.configs/` contains:
  - `{model}_coverage`
  - `{model}_state`
  - `{model}_path`
  - `{model}_output`
  - `{model}_consistency`

#### *Path errors in batch execution*
- Check Python version (3.8–3.11)

#### *Insufficient GPU memory*
- Use smaller model
- Enable quantization
- Reduce batch size

 

## 9. System Dependencies
- **Ubuntu/Debian:** `sudo apt-get install jq`
- **macOS:** `brew install jq`
- **Windows:** Download from jq official site

 

## 10. Advanced Usage

### **Start Local vLLM Server**
```bash
python evaluation.py config
bash start_server.sh .eval_config
```

### **Custom Model Configuration**
1. Add model to `model_list.txt`
2. Run:
```bash
python evaluation.py config
```
3. Select **HuggingFace** and enter model name

 

## 11. Important Notes
- **API Costs:** OpenAI usage incurs cost
- **Licensing:** Obey open‑source model licenses
- **Privacy:** API inputs may leave machine
- **GPU Requirements:** Local models require strong GPUs

 

## 12. File Structure
```
REval/
├── data/                    # Benchmark datasets
├── prompts/                # Prompt templates
├── model_generations/      # Evaluation results
├── .configs/               # User configurations
├── evaluation.py           # Main evaluation script
├── batch_run.py            # Batch execution script
├── inference.py            # Model interface
├── dynamics.py             # Runtime analysis engine
├── requirements.txt        # Full dependencies
├── requirements-nogpu.txt  # OpenAI-only dependencies
├── .env.example            # Environment template
└── README.md               # This file
```
