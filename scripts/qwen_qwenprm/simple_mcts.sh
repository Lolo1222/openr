export PYTHONPATH=$(pwd)
python reason/evaluation/evaluate.py \
    --LM Qwen2.5-Math-7B-Instruct \
    --RM Qwen2.5-Math-PRM-7B \
    --task_name MATH \
    --temperature 0.7 \
    --max_new_tokens 1024 \
    --num_sequence 1 \
    --tree_max_width 10 \
    --tree_max_depth 50 \
    --save_dir qwen_qwenprm_result \
    --method simple_mcts \
    --num_worker 32 \
    --num_simulations 20 \
    --controller_addr http://0.0.0.0:28777
# python reason/evaluation/evaluate.py \
#     --LM Qwen2.5-Math-7B-Instruct \
#     --RM math-shepherd-mistral-7b-prm \
#     --task_name MATH \
#     --temperature 0.8 \
#     --max_new_tokens 1024 \
#     --num_sequence 1 \
#     --tree_max_width 10 \
#     --tree_max_depth 50 \
#     --save_dir qwen_mprm_result \
#     --method simple_mcts \
#     --num_worker 32 \
#     --num_simulations 10 \
#     --local \
#     --controller_addr http://0.0.0.0:28777

# math-shepherd-mistral-7b-prm