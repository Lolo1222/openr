export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM mistral-7b-sft \
    --RM math-shepherd-mistral-7b-prm \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 2048 \
    --num_sequence 1 \
    --tree_max_width 4 \
    --tree_max_depth 50 \
    --save_dir for_gen_result \
    --method simple_mcts \
    --num_worker 32 \
    --controller_addr http://0.0.0.0:28777\
    --num_simulations 4

# math-shepherd-mistral-7b-prm