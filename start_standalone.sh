#!/usr/bin/env bash

MODEL="TheBloke_Synthia-70B-v1.1-GPTQ"

echo "Worker Initiated"

echo "Starting Oobabooga Text Generation Server"
cd /workspace/text-generation-webui
source /workspace/text-generation-webui/venv/bin/activate
mkdir -p /workspace/logs
nohup python3 server.py \
  --listen \
  --api \
  --loader ExLlama \
  --model ${MODEL} \
  --listen-port 3000 \
  --api-blocking-port 5000 \
  --api-streaming-port 5005 &> /workspace/logs/textgen.log &

echo "Starting RunPod Handler"
export PYTHONUNBUFFERED=1
python -u /rp_handler.py
