import sys

import torch

if sys.platform != "darwin":
    from auto_gptq import AutoGPTQForCausalLM

from huggingface_hub import hf_hub_download
from langchain.llms import LlamaCpp
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig

from constants import CONTEXT_WINDOW_SIZE, MAX_NEW_TOKENS, MODELS_PATH, N_BATCH, N_GPU_LAYERS


def load_quantized_model_gguf_ggml(model_id, model_basename, device_type, logging):
    
    try:
        logging.info("Using Llamacpp for GGUF/GGML quantized models")
        model_path = hf_hub_download(
            repo_id=model_id,
            filename=model_basename,
            resume_download=True,
            cache_dir=MODELS_PATH,
        )
        kwargs = {
            "model_path": model_path,
            "n_ctx": CONTEXT_WINDOW_SIZE,
            "max_tokens": MAX_NEW_TOKENS,
            "n_batch": N_BATCH,  # set this based on your GPU & CPU RAM
        }
        if device_type.lower() == "mps":
            kwargs["n_gpu_layers"] = 1
        if device_type.lower() == "cuda":
            kwargs["n_gpu_layers"] = N_GPU_LAYERS  # set this based on your GPU

        return LlamaCpp(**kwargs)
    except TypeError:
        if "ggml" in model_basename:
            logging.INFO("If you were using GGML model, LLAMA-CPP Dropped Support, Use GGUF Instead")
        return None


def load_quantized_model_qptq(model_id, model_basename, device_type, logging):

    if sys.platform == "darwin":
        logging.INFO("GPTQ models will NOT work on Mac devices. Please choose a different model.")
        return None, None

    # The code supports all huggingface models that ends with GPTQ and have some variation
    # of .no-act.order or .safetensors in their HF repo.
    logging.info("Using AutoGPTQForCausalLM for quantized models")

    if ".safetensors" in model_basename:
        # Remove the ".safetensors" ending if present
        model_basename = model_basename.replace(".safetensors", "")

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    logging.info("Tokenizer loaded")

    model = AutoGPTQForCausalLM.from_quantized(
        model_id,
        model_basename=model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device_map="auto",
        use_triton=False,
        quantize_config=None,
    )
    return model, tokenizer


def load_full_model(model_id, model_basename, device_type, logging):

    if device_type.lower() in ["mps", "cpu"]:
        logging.info("Using LlamaTokenizer")
        tokenizer = LlamaTokenizer.from_pretrained(model_id, cache_dir="./models/")
        model = LlamaForCausalLM.from_pretrained(model_id, cache_dir="./models/")
    else:
        logging.info("Using AutoModelForCausalLM for full models")
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="./models/")
        logging.info("Tokenizer loaded")
        bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16
                )
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            cache_dir=MODELS_PATH,
            trust_remote_code=True,  # set these if you are using NVIDIA GPU
            quantization_config=bnb_config
           # load_in_4bit=True,
           # bnb_4bit_quant_type="nf4",
           # bnb_4bit_compute_dtype=torch.float16,
           # max_memory={0: "15GB"},  # Uncomment this line with you encounter CUDA out of memory errors
        )

        model.tie_weights()
    return model, tokenizer


def load_quantized_model_awq(model_id, logging):

    if sys.platform == "darwin":
        logging.INFO("AWQ models will NOT work on Mac devices. Please choose a different model.")
        return None, None

    # The code supports all huggingface models that ends with AWQ.
    logging.info("Using AutoModelForCausalLM for AWQ quantized models")

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    logging.info("Tokenizer loaded")

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        use_safetensors=True,
        trust_remote_code=True,
        device_map="auto",
    )
    return model, tokenizer
