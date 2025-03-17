from vllm import LLM, SamplingParams
import yaml
import os
import sys
import torch_neuronx
import pandas as pd
from huggingface_hub import snapshot_download

books_df_dataset=os.environ['BOOKS_DF_DS']
books_df_dataset_expanded_interest=os.environ['BOOKS_DF_DS_EXP_INTEREST']
repo_id=os.environ['COMPILED_MODEL_ID']
repo_dir=repo_id
os.environ['NEURON_COMPILED_ARTIFACTS']=repo_id
os.environ['VLLM_NEURON_FRAMEWORK']='neuronx-distributed-inference'

snapshot_download(repo_id=repo_id,local_dir=repo_dir)
print(f"Repository '{repo_id}' downloaded to '{repo_dir}'.")

books_df = pd.read_pickle(books_df_dataset)

if len(sys.argv) <= 1:
    print("Error: Please provide a path to a YAML configuration file.")
    sys.exit(1)

config_path = sys.argv[1]
with open(config_path, 'r') as f:
    model_vllm_config_yaml = f.read()

#with torch_neuronx.experimental.neuron_cores_context(start_nc=3):
model_vllm_config = yaml.safe_load(model_vllm_config_yaml)
llm_model = LLM(**model_vllm_config)

def expand_interest(user_reviews):
    """
    Expands the user's book interest using LLM reasoning.
    Ensures the returned type is a valid string for embeddings.
    """
    prompt = f"Expand the following book interests: {user_reviews}"
    sampling_params = SamplingParams(top_k=64)
    request_output = llm_model.generate([prompt],sampling_params=sampling_params)[0]
    # Extract text from request_output
    if request_output.outputs and hasattr(request_output.outputs[0], 'text'):
        expanded_text = request_output.outputs[0].text
    else:
        expanded_text = str(request_output)
    return expanded_text.strip()

# Test the expand_interest function
test_user_interest = "I love epic sci-fi novels with deep world-building."
expanded_test_interest = expand_interest(test_user_interest)
print("✅ Expanded Interest Example:", expanded_test_interest)
# Expand interests for all users
books_df["expanded_interest"] = books_df["review/text"].apply(expand_interest)
books_df.to_pickle(books_df_dataset_expanded_interest)
print(f"✅ Expanded Interests Generated in {books_df_dataset_expanded_interest}!")
