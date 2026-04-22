#!/bin/bash
#SBATCH -J "NL To LTL"              # Job name
#SBATCH -A rbe577                   # Account
#SBATCH -o job_output.out           # Output log
#SBATCH -e job_err.err              # Error log
#SBATCH -p academic                 # Partition
#SBATCH -t 04:00:00                 # 4h runtime
#SBATCH -G 2                        # 2 GPUs

# Load modules
module load python/3.10.17/v6xrl7k
module load miniconda3/25.1.1/24g7bpu
module load gcc/13.2.0/itun3au

# Define paths
DIR_PATH="/home/zdserocki/RBE575"
REPO_PATH="${DIR_PATH}/Efficient-Eng-2-LTL-RBE575"

# Init conda for use in script
source $(conda info --base)/etc/profile.d/conda.sh

if [ ! -d "${DIR_PATH}/LTL-venv" ]; then
    conda create -p ${DIR_PATH}/LTL-venv python=3.10 -y
    conda activate ${DIR_PATH}/LTL-venv
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip install transformers==4.30.0
    pip install tokenizers==0.13.3
    pip install datasets
    pip install sentencepiece
    pip install jsons appdirs blobfile cached-property httpx typer whoosh more_itertools
    pip install --upgrade protobuf==3.20.0
    pip install "accelerate>=0.20.1"
else
    conda activate ${DIR_PATH}/LTL-venv
fi

# Debug info
nvcc --version || echo "nvcc not found"
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda)"

# Download BART model if not already downloaded
if [ ! -d "${REPO_PATH}/run/huggingface_models/bart-large" ]; then
    cd ${REPO_PATH}/run
    python ./semantic_parsing_with_constrained_lm/finetune/download_huggingface_lms.py
fi

# Run training
export PRETRAINED_MODEL_DIR=huggingface_models/bart-large
export TRAINED_MODEL_DIR=trained_models/
DOMAIN=drone-syn-aug

cd ${REPO_PATH}/run

python -m semantic_parsing_with_constrained_lm.finetune.lm_finetune \
    --config-name semantic_parsing_with_constrained_lm.finetune.configs.emnlp_train_config \
    --exp-names ltl_${DOMAIN}_utterance

# Run inference
python -m semantic_parsing_with_constrained_lm.run_exp \
    --config-name semantic_parsing_with_constrained_lm.configs.ltl_config \
    --log-dir logs/ \
    --model Bart \
    --eval-split test-full \
    --exp-names "ltl_Bart_test-full_${DOMAIN}_constrained_utterance_train-0"