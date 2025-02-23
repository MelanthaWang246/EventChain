model_path=/mnt/workspace/pretrain_model/qwen2/qwen/Qwen2.5-14B-Instruct

CUDA_VISIBLE_DEVICES=1 
python -m vllm.entrypoints.openai.api_server \
    --port 9000  \
    --served-model-name Qwen2.5-14B-Instruct \
    --model ${model_path} \
    --gpu-memory-utilization 0.5 \
    --max-model-len 32768 \
    --max-num-batched-tokens 40960 \
    --max-num-seqs 10