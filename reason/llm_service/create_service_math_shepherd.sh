### Note!!!!!!#########
rm -rf ./logs_fastchat/

set -e

HOST_ADDR=0.0.0.0
CONTROLER_PORT=28777
WORKER_BASE_PORT=30010

echo PYTHON_EXECUTABLE=$(which python3)
PYTHON_EXECUTABLE=$(which python3)

POLICY_MODEL_NAME=peiyi9979/mistral-7b-sft
VALUE_MODEL_NAME=peiyi9979/math-shepherd-mistral-7b-prm

# Change MODEL_BASE POLICY_MODEL_NAME VALUE_MODEL_NAME
MODEL_BASE=/data2/OpenLLMs
CUDA_DEVICE_BASE=4
# POLICY_MODEL_NAME=Qwen2.5-Math-7B-Instruct
# VALUE_MODEL_NAME=Qwen2.5-Math-1.5B-Instruct
MODEL_PATH=$MODEL_BASE/$POLICY_MODEL_NAME
VALUE_MODEL_PATH=$MODEL_BASE/$VALUE_MODEL_NAME

LOGDIR=logs_fastchat

tmux start-server
tmux new-session -s fastchat2 -n controller -d
tmux send-keys "export LOGDIR=${LOGDIR}" Enter
tmux send-keys "$PYTHON_EXECUTABLE -m fastchat.serve.controller --port ${CONTROLER_PORT} --host $HOST_ADDR" Enter

NUM_LM_WORKER=1
NUM_RM_WORKER=1
# NUM_LM_WORKER=2
# NUM_RM_WORKER=2

echo "Wait 10 seconds ..."
sleep 5

echo "Starting workers"
for i in $(seq 0 $((NUM_LM_WORKER-1)))
do
  WORKER_PORT=$((WORKER_BASE_PORT+i))
  tmux new-window -n policy_worker_$i
  tmux send-keys "export LOGDIR=${LOGDIR}" Enter
  tmux send-keys "CUDA_VISIBLE_DEVICES=$((i+CUDA_DEVICE_BASE)) $PYTHON_EXECUTABLE -m reason.llm_service.workers.vllm_worker --model-path $MODEL_PATH --controller-address http://$HOST_ADDR:$CONTROLER_PORT --host $HOST_ADDR --port $WORKER_PORT --worker-address http://$HOST_ADDR:$WORKER_PORT --dtype bfloat16" Enter
done


# start value service
for i in $(seq 0 $((NUM_RM_WORKER-1)))
do
  WORKER_PORT=$((i+WORKER_BASE_PORT+NUM_LM_WORKER))
  tmux new-window -n value_worker
  tmux send-keys "export LOGDIR=${LOGDIR}" Enter
  tmux send-keys "CUDA_VISIBLE_DEVICES=6 $PYTHON_EXECUTABLE -m reason.llm_service.workers.reward_model_worker --model-path $VALUE_MODEL_PATH --controller-address http://$HOST_ADDR:$CONTROLER_PORT --host $HOST_ADDR --port $WORKER_PORT --worker-address http://$HOST_ADDR:$WORKER_PORT" Enter
  # tmux send-keys "CUDA_VISIBLE_DEVICES=$((i+NUM_LM_WORKER+CUDA_DEVICE_BASE)) $PYTHON_EXECUTABLE -m reason.llm_service.workers.reward_model_worker --model-path $VALUE_MODEL_PATH --controller-address http://$HOST_ADDR:$CONTROLER_PORT --host $HOST_ADDR --port $WORKER_PORT --worker-address http://$HOST_ADDR:$WORKER_PORT" Enter
done