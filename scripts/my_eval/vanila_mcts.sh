export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM Qwen2.5-Math-1.5B-Instruct \
    --RM Qwen2.5-Math-1.5B-Instruct \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 256 \
    --num_sequence 1 \
    --tree_max_width 3 \
    --tree_max_depth 10 \
    --save_dir debug \
    --method vanila_mcts \
    --num_worker 32 \
    --controller_addr http://0.0.0.0:28777 \
    --local

# math-shepherd-mistral-7b-prm