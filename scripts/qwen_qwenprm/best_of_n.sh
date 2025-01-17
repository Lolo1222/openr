export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM Qwen2.5-Math-7B-Instruct \
    --RM Qwen2.5-Math-PRM-7B \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 1024 \
    --num_sequence 10 \
    --save_dir qwen_qwenprm_result \
    --method best_of_n \
    --num_worker 32 \
    --controller_addr http://0.0.0.0:28777 \
    --local

# math-shepherd-mistral-7b-prm