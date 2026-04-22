#!/bin/bash
#SBATCH -J "NL To LTL"     # Job name
#SBATCH -o job_output.out           # Output log
#SBATCH -e job_err.err              # Error log
#SBATCH -p academic                 # Partition
#SBATCH -t 04:00:00                 # 2h runtime
#SBATCH -G 2                        # 2 GPUs

# If necessary, include the specific versions required
module load python/3.10.20

# Define the paths to your project directories here
DIR_PATH="/home/zdserocki/RBE575/"
REPO_PATH="${DIR_PATH}/Efficient-Eng-2-LTL-RBE575"

# Create an environment for the job
python -m venv ${DIR_PATH}/LTL-venv
source ${DIR_PATH}/LTL-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ${REPO_PATH}/requirements.txt

# Run the main wrapper file with relevant arguments
python ${REPO_PATH}/P1-MyAutoPano/Phase2/Code/Wrapper.py