from huggingface_hub import login,snapshot_download
import os
repo_id="yahavb/DeepSeek-R1-Distill-Llama-70B-NxD-vllm"
snapshot_download(repo_id=repo_id,local_dir=repo_id)
print(f"Repository '{repo_id}' downloaded to '{repo_id}'.")
