export PYTHONPATH=$(pwd)
# CUDA_DEVICE_BASE=4
# CUDA_VISIBLE_DEVICES=$((CUDA_DEVICE_BASE)) 
python reason/evaluation/evaluate.py \
    --LM Qwen2.5-Math-1.5B-Instruct \
    --task_name MATH \
    --temperature 0.0 \
    --max_new_tokens 256 \
    --save_dir results \
    --method cot \
    --num_worker 2 \
    --controller_addr http://0.0.0.0:28777