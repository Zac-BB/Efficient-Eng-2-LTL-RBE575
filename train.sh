

export PRETRAINED_MODEL_DIR=huggingface_models/bart-large
export TRAINED_MODEL_DIR=trained_models/


DOMAIN=drone-syn-aug # for example, DOMAIN=pick-syn-aug
python -m run/semantic_parsing_with_constrained_lm.finetune.lm_finetune \
        --config-name semantic_parsing_with_constrained_lm.finetune.configs.emnlp_train_config \
        --exp-names ltl_${DOMAIN}_utterance
