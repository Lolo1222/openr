export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM Qwen2.5-Math-7B-Instruct \
    --RM math-shepherd-mistral-7b-prm \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 1024 \
    --num_sequence 10 \
    --save_dir qwen_mprm_result \
    --method best_of_n \
    --num_worker 32 \
    --controller_addr http://0.0.0.0:28777 \
    --local

# math-shepherd-mistral-7b-prm