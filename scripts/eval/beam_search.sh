export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM mistral-7b-sft \
    --RM math-shepherd-mistral-7b-prm \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 1024 \
    --num_sequence 4 \
    --tree_max_width 10 \
    --tree_max_depth 50 \
    --save_dir math_shepherd_result \
    --method beam_search \
    --num_worker 32 \
    --controller_addr http://0.0.0.0:28777

# math-shepherd-mistral-7b-prm