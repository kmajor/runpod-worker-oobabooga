#!/usr/bin/env bash

if [ -z "${MODEL+x}" ]; then
  MODEL="TheBloke/Synthia-34B-v1.2-GPTQ"
fi

# Replace slashes with underscores
MODEL="${MODEL//\//_}"

if [ -d "/runpod-volumetext-generation-webui/models/${MODEL}" ]; then
  echo "Starting Oobabooga Text Generation Server"
  cd /runpod-volume/text-generation-webui
  mkdir -p /runpod-volume/logs
  nohup python3 server.py \
    --listen \
    --api \
    --loader ExLlama \
    --model ${MODEL} \
    --listen-port 3000 \
    --api-blocking-port 5000 \
    --api-streaming-port 5005 &> /runpod-volume/logs/textgen.log &

  echo "Starting RunPod Handler"
  export PYTHONUNBUFFERED=1
  python3 -u /rp_handler.py
else
  echo "Model directory not found!"
fi
