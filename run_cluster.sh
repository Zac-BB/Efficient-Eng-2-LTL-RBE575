#!/bin/bash
#SBATCH -J "NL To LTL"              # Job name
#SBATCH -A rbe577
#SBATCH -o job_output.out           # Output log
#SBATCH -e job_err.err              # Error log
#SBATCH -p academic                 # Partition
#SBATCH -t 04:00:00                 # 2h runtime
#SBATCH -G 2                        # 2 GPUs

# If necessary, include the specific versions required
module load python/3.10.17

# Define the paths to your project directories here
DIR_PATH="/home/zdserocki/RBE575"
REPO_PATH="${DIR_PATH}/Efficient-Eng-2-LTL-RBE575"

# Create an environment for the job
module load python/3.10.17/v6xrl7k
module load miniconda3/25.1.1/24g7bpu

# Create conda env only if it doesn't exist
if [ ! -d "${DIR_PATH}/LTL-venv" ]; then
    conda create -p ${DIR_PATH}/LTL-venv --file ${REPO_PATH}/requirements.txt -y
fi

conda activate ${DIR_PATH}/LTL-venv
pip install -r ${REPO_PATH}/requirements.txt

# Run the main wrapper file with relevant arguments
export PRETRAINED_MODEL_DIR=huggingface_models/bart-large
export TRAINED_MODEL_DIR=trained_models/

DOMAIN=drone-syn-aug # for example, DOMAIN=pick-syn-aug
python ${REPO_PATH}/run/semantic_parsing_with_constrained_lm/finetune/lm_finetune.py \
    --config-name semantic_parsing_with_constrained_lm.finetune.configs.emnlp_train_config \
    --exp-names ltl_${DOMAIN}_utterance


