# Published SAE checkpoint repositories

[Model hub](../README.md) · [Search model cards](../web/README.md) · [Load a checkpoint](../../loading.md)

Choose a backbone to browse its checkpoint collections, layers and model cards.

## Language and multimodal backbones

| Base model | Checkpoint repositories | SAE checkpoints |
| --- | ---: | ---: |
| [gpt2-small](#model-gpt2-small) | 18 | 159 |
| [openai/gpt-oss-20b](#model-openai-gpt-oss-20b) | 1 | 6 |
| [gemma-2-2b](#model-gemma-2-2b) | 10 | 1,516 |
| [gemma-2-9b](#model-gemma-2-9b) | 5 | 1,591 |
| [gemma-2-27b](#model-gemma-2-27b) | 1 | 18 |
| [gemma-2b](#model-gemma-2b) | 1 | 5 |
| [gemma-2b-it](#model-gemma-2b-it) | 1 | 1 |
| [google/gemma-3-1b-it](#model-google-gemma-3-1b-it) | 1 | 448 |
| [google/gemma-3-1b-pt](#model-google-gemma-3-1b-pt) | 2 | 473 |
| [google/gemma-3-4b-it](#model-google-gemma-3-4b-it) | 1 | 532 |
| [google/gemma-3-4b-pt](#model-google-gemma-3-4b-pt) | 1 | 532 |
| [google/gemma-3-12b-it](#model-google-gemma-3-12b-it) | 1 | 700 |
| [google/gemma-3-12b-pt](#model-google-gemma-3-12b-pt) | 1 | 700 |
| [google/gemma-3-27b-it](#model-google-gemma-3-27b-it) | 1 | 868 |
| [google/gemma-3-27b-pt](#model-google-gemma-3-27b-pt) | 1 | 300 |
| [google/gemma-3-270m](#model-google-gemma-3-270m) | 1 | 340 |
| [google/gemma-3-270m-it](#model-google-gemma-3-270m-it) | 1 | 340 |
| [meta-llama/Llama-3.1-8B](#model-meta-llama-llama-3-1-8b) | 6 | 192 |
| [meta-llama/Llama-3.1-8B-Instruct](#model-meta-llama-llama-3-1-8b-instruct) | 2 | 8 |
| [meta-llama/Llama-3.3-70B-Instruct](#model-meta-llama-llama-3-3-70b-instruct) | 1 | 1 |
| [meta-llama/Meta-Llama-3-8B-Instruct](#model-meta-llama-meta-llama-3-8b-instruct) | 1 | 1 |
| [deepseek-ai/DeepSeek-R1-Distill-Llama-8B](#model-deepseek-ai-deepseek-r1-distill-llama-8b) | 2 | 97 |
| [mistral-7b](#model-mistral-7b) | 1 | 3 |
| [pythia-70m-deduped](#model-pythia-70m-deduped) | 4 | 207 |
| [Qwen/Qwen2.5-7B-Instruct](#model-qwen-qwen2-5-7b-instruct) | 1 | 7 |
| [Qwen/Qwen3-1.7B-Base](#model-qwen-qwen3-1-7b-base) | 2 | 56 |
| [Qwen/Qwen3-8B-Base](#model-qwen-qwen3-8b-base) | 2 | 72 |
| [Qwen/Qwen3-30B-A3B-Base](#model-qwen-qwen3-30b-a3b-base) | 2 | 96 |
| [Qwen/Qwen3.5-2B-Base](#model-qwen-qwen3-5-2b-base) | 2 | 48 |
| [Qwen/Qwen3.5-9B-Base](#model-qwen-qwen3-5-9b-base) | 2 | 64 |
| [Qwen/Qwen3.5-27B](#model-qwen-qwen3-5-27b) | 2 | 128 |
| [Qwen/Qwen3.5-35B-A3B-Base](#model-qwen-qwen3-5-35b-a3b-base) | 2 | 80 |

## Vision backbones

| Base model | Checkpoint repositories | SAE checkpoints |
| --- | ---: | ---: |
| [open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K](#model-open-clip-laion-clip-vit-b-32-datacomp-xl-s13b-b90k) | 59 | 59 |
| [facebook/dino-vitb16](#model-facebook-dino-vitb16) | 12 | 12 |

## Checkpoint collections by backbone

### GPT-2

<a id="model-gpt2-small"></a>

#### gpt2-small

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| ckkissane/attn-saes-gpt2-small-all-layers | 0–11 | `z` | 12 | [Browse](ckkissane-attn-saes-gpt2-small-all-layers-de50a414-p1.md#sae-4d4068f57bb7c87ea0e9a17f) | [Repository](https://huggingface.co/ckkissane/attn-saes-gpt2-small-all-layers) |
| jbloom/GPT2-Small-Feature-Splitting-Experiment-Layer-8 | — | — | 8 | [Browse](jbloom-gpt2-small-feature-splitting-experiment-layer-8-dbe4582b-p1.md#gpt2-layer8-relu-768) | [Repository](https://huggingface.co/jbloom/GPT2-Small-Feature-Splitting-Experiment-Layer-8) |
| jbloom/GPT2-Small-OAI-v5-32k-attn-out-SAEs | 0–11 | `attn_out` | 12 | [Browse](jbloom-gpt2-small-oai-v5-32k-attn-out-saes-b1c4c6cd-p1.md#sae-3eecdd500b0742ee9735b0de) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-attn-out-SAEs) |
| jbloom/GPT2-Small-OAI-v5-32k-mlp-out-SAEs | 0–11 | `mlp_out` | 12 | [Browse](jbloom-gpt2-small-oai-v5-32k-mlp-out-saes-97b6e554-p1.md#sae-1e5fd3b166e029266c5262e0) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-mlp-out-SAEs) |
| jbloom/GPT2-Small-OAI-v5-32k-resid-mid-SAEs | 0–11 | `resid_mid` | 12 | [Browse](jbloom-gpt2-small-oai-v5-32k-resid-mid-saes-220953a2-p1.md#sae-2b49f8ee115d52af5a127ec6) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-mid-SAEs) |
| jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs | 0–11 | `resid_post` | 12 | [Browse](jbloom-gpt2-small-oai-v5-32k-resid-post-saes-c2dcb058-p1.md#sae-0fb0414f2b3f7fd7a5d615d4) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-32k-resid-post-SAEs) |
| jbloom/GPT2-Small-OAI-v5-128k-attn-out-SAEs | 0–11 | `attn_out` | 12 | [Browse](jbloom-gpt2-small-oai-v5-128k-attn-out-saes-8b402446-p1.md#sae-0e827d4cd5d2a4ae01f75ee2) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-128k-attn-out-SAEs) |
| jbloom/GPT2-Small-OAI-v5-128k-mlp-out-SAEs | 0–11 | `mlp_out` | 12 | [Browse](jbloom-gpt2-small-oai-v5-128k-mlp-out-saes-4b098455-p1.md#sae-3e8c62ab8e709363f6014b09) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-128k-mlp-out-SAEs) |
| jbloom/GPT2-Small-OAI-v5-128k-resid-mid-SAEs | 0–11 | `resid_mid` | 12 | [Browse](jbloom-gpt2-small-oai-v5-128k-resid-mid-saes-8c387a6a-p1.md#sae-0d8a23b25ac17beb34098695) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-128k-resid-mid-SAEs) |
| jbloom/GPT2-Small-OAI-v5-128k-resid-post-SAEs | 0–11 | `resid_post` | 12 | [Browse](jbloom-gpt2-small-oai-v5-128k-resid-post-saes-28ac392d-p1.md#sae-7c881af933e18a2b45fbbe57) | [Repository](https://huggingface.co/jbloom/GPT2-Small-OAI-v5-128k-resid-post-SAEs) |
| jbloom/GPT2-Small-SAEs-Reformatted | 0–11 | `resid_post`, `resid_pre` | 13 | [Browse](jbloom-gpt2-small-saes-reformatted-0a8353da-p1.md#sae-3d5a75db7c957832dd1b7176) | [Repository](https://huggingface.co/jbloom/GPT2-Small-SAEs-Reformatted) |
| neuronpedia/gpt2-small__res_sce-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-sce-ajt-5bdf7eb6-p1.md#sae-1fdffaadbe16273ebacb035e) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_sce-ajt) |
| neuronpedia/gpt2-small__res_scefr-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-scefr-ajt-8ca607da-p1.md#sae-8d0f59f9384db7befa32fdca) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_scefr-ajt) |
| neuronpedia/gpt2-small__res_scl-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-scl-ajt-bc821367-p1.md#sae-9a1f581a9f6db9f30429c47b) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_scl-ajt) |
| neuronpedia/gpt2-small__res_sle-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-sle-ajt-00ad5370-p1.md#sae-a2cacfef1d2582cab1543f35) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_sle-ajt) |
| neuronpedia/gpt2-small__res_slefr-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-slefr-ajt-fddf3c7e-p1.md#sae-5f43e4e14d3d29d6b0b87edb) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_slefr-ajt) |
| neuronpedia/gpt2-small__res_sll-ajt | 2, 6, 10 | `resid_pre` | 3 | [Browse](neuronpedia-gpt2-small-res-sll-ajt-f3e267fb-p1.md#sae-8edecf0602e99a4417f09c6e) | [Repository](https://huggingface.co/neuronpedia/gpt2-small__res_sll-ajt) |
| tommmcgrath/gpt2-small-mlp-out-saes | 0–11 | `mlp_out` | 12 | [Browse](tommmcgrath-gpt2-small-mlp-out-saes-bd24bb18-p1.md#sae-5dba394d38957cb65594c98a) | [Repository](https://huggingface.co/tommmcgrath/gpt2-small-mlp-out-saes) |

### GPT-OSS

<a id="model-openai-gpt-oss-20b"></a>

#### openai/gpt-oss-20b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| andyrdt/saes-gpt-oss-20b | 3, 7, 11, 15, 19, 23 | `resid_post` | 6 | [Browse](andyrdt-saes-gpt-oss-20b-65f61b4c-p1.md#sae-5f820fd323b405ba055b2ff1) | [Repository](https://huggingface.co/andyrdt/saes-gpt-oss-20b) |

### Gemma

<a id="model-gemma-2-2b"></a>

#### gemma-2-2b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| adamkarvonen/saebench_gemma-2-2b_width-2pow12_date-0108 | 12 | `resid_post` | 6 | [Browse](adamkarvonen-saebench-gemma-2-2b-width-2pow12-date-0108-04a978f7-p1.md#sae-254a46b6d65d9926525934ad) | [Repository](https://huggingface.co/adamkarvonen/saebench_gemma-2-2b_width-2pow12_date-0108) |
| canrager/saebench_gemma-2-2b_width-2pow12_date-1109 | — | — | 288 | [Browse](canrager-saebench-gemma-2-2b-width-2pow12-date-1109-4dbd15a7-p1.md#sae-1ac088491b79b339f28307ef) | [Repository](https://huggingface.co/canrager/saebench_gemma-2-2b_width-2pow12_date-1109) |
| canrager/saebench_gemma-2-2b_width-2pow14_date-0107 | 12 | `resid_post` | 6 | [Browse](canrager-saebench-gemma-2-2b-width-2pow14-date-0107-e1ca0c29-p1.md#sae-0450f0e3756f7cf9786fe3b4) | [Repository](https://huggingface.co/canrager/saebench_gemma-2-2b_width-2pow14_date-0107) |
| canrager/saebench_gemma-2-2b_width-2pow14_date-1109 | — | — | 288 | [Browse](canrager-saebench-gemma-2-2b-width-2pow14-date-1109-9aedbf14-p1.md#sae-0c88e0af7bbd5e577e81d01d) | [Repository](https://huggingface.co/canrager/saebench_gemma-2-2b_width-2pow14_date-1109) |
| canrager/saebench_gemma-2-2b_width-2pow16_date-0107 | 12 | `resid_post` | 6 | [Browse](canrager-saebench-gemma-2-2b-width-2pow16-date-0107-8204d8d2-p1.md#sae-0d695e6ee90df4e1dd1cc2de) | [Repository](https://huggingface.co/canrager/saebench_gemma-2-2b_width-2pow16_date-0107) |
| canrager/saebench_gemma-2-2b_width-2pow16_date-1109 | — | — | 36 | [Browse](canrager-saebench-gemma-2-2b-width-2pow16-date-1109-4e0c83a9-p1.md#sae-0b8a8d027c203db26877b259) | [Repository](https://huggingface.co/canrager/saebench_gemma-2-2b_width-2pow16_date-1109) |
| chanind/gemma-2-2b-batch-topk-matryoshka-saes-w-32k-l0-40 | 0–24 | `resid_post` | 50 | [Browse](chanind-gemma-2-2b-batch-topk-matryoshka-saes-w-32k-l0-40-7b149c13-p1.md#sae-0ec8f2ef8625282b2f1cd9db) | [Repository](https://huggingface.co/chanind/gemma-2-2b-batch-topk-matryoshka-saes-w-32k-l0-40) |
| google/gemma-scope-2b-pt-att | 0–25 | `attn.z` | 260 | [Browse](google-gemma-scope-2b-pt-att-da0daf1e-p1.md#sae-2ae4c016a70881732016b1c5) | [Repository](https://huggingface.co/google/gemma-scope-2b-pt-att) |
| google/gemma-scope-2b-pt-mlp | 0–25 | `mlp_out` | 260 | [Browse](google-gemma-scope-2b-pt-mlp-ba5a0c5c-p1.md#sae-0b64c6286d65140ec6589aff) | [Repository](https://huggingface.co/google/gemma-scope-2b-pt-mlp) |
| google/gemma-scope-2b-pt-res | 0–25 | `embed`, `resid_post` | 316 | [Browse](google-gemma-scope-2b-pt-res-e75f316a-p1.md#sae-0e078e9b37b75d71033ef0a9) | [Repository](https://huggingface.co/google/gemma-scope-2b-pt-res) |

<a id="model-gemma-2-9b"></a>

#### gemma-2-9b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| chanind/gemma-2-9b-batch-topk-matryoshka-saes-w-32k-l0-60 | 0–40 | `resid_post` | 41 | [Browse](chanind-gemma-2-9b-batch-topk-matryoshka-saes-w-32k-l0-60-56fa1df2-p1.md#sae-0d6dfaa835c84947ab473abe) | [Repository](https://huggingface.co/chanind/gemma-2-9b-batch-topk-matryoshka-saes-w-32k-l0-60) |
| google/gemma-scope-9b-it-res | 9, 20, 31 | `resid_post` | 30 | [Browse](google-gemma-scope-9b-it-res-87f737ba-p1.md#sae-0fcd8a3be640db4a15c06d27) | [Repository](https://huggingface.co/google/gemma-scope-9b-it-res) |
| google/gemma-scope-9b-pt-att | 0–41 | `attn.z` | 492 | [Browse](google-gemma-scope-9b-pt-att-3e987dde-p1.md#sae-0ab4cad5d55b62b8d65e9e8b) | [Repository](https://huggingface.co/google/gemma-scope-9b-pt-att) |
| google/gemma-scope-9b-pt-mlp | 0–41 | `mlp_out` | 492 | [Browse](google-gemma-scope-9b-pt-mlp-21125446-p1.md#sae-00c81fd759e3b79831f95534) | [Repository](https://huggingface.co/google/gemma-scope-9b-pt-mlp) |
| google/gemma-scope-9b-pt-res | 0–41 | `embed`, `resid_post` | 536 | [Browse](google-gemma-scope-9b-pt-res-540fe824-p1.md#sae-0ab419d7535f941c76a1e014) | [Repository](https://huggingface.co/google/gemma-scope-9b-pt-res) |

<a id="model-gemma-2-27b"></a>

#### gemma-2-27b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-27b-pt-res | 10, 22, 34 | `resid_post` | 18 | [Browse](google-gemma-scope-27b-pt-res-130ac1ad-p1.md#sae-02f3cd22124e0cd1b5803f2a) | [Repository](https://huggingface.co/google/gemma-scope-27b-pt-res) |

<a id="model-gemma-2b"></a>

#### gemma-2b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| jbloom/Gemma-2b-Residual-Stream-SAEs | 0, 6, 10, 12, 17 | `resid_post` | 5 | [Browse](jbloom-gemma-2b-residual-stream-saes-6d57323d-p1.md#sae-13ff5b33ffbc5cac252c5da2) | [Repository](https://huggingface.co/jbloom/Gemma-2b-Residual-Stream-SAEs) |

<a id="model-gemma-2b-it"></a>

#### gemma-2b-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| jbloom/Gemma-2b-IT-Residual-Stream-SAEs | 12 | `resid_post` | 1 | [Browse](jbloom-gemma-2b-it-residual-stream-saes-7364cdb4-p1.md#sae-bd477d8e3911b1de6da6ec9b) | [Repository](https://huggingface.co/jbloom/Gemma-2b-IT-Residual-Stream-SAEs) |

<a id="model-google-gemma-3-1b-it"></a>

#### google/gemma-3-1b-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-1b-it | 0–25 | `attn.z`, `mlp_out`, `resid_post` | 448 | [Browse](google-gemma-scope-2-1b-it-f226822b-p1.md#sae-0f48e825210569e94d042f35) | [Repository](https://huggingface.co/google/gemma-scope-2-1b-it) |

<a id="model-google-gemma-3-1b-pt"></a>

#### google/gemma-3-1b-pt

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| chanind/gemma-3-1b-batch-topk-matryoshka-saes-w-32k-l0-40 | 0–24 | `resid_post` | 25 | [Browse](chanind-gemma-3-1b-batch-topk-matryoshka-saes-w-32k-l0-40-2eb358ba-p1.md#sae-0a5888fd020ad3c83dc16493) | [Repository](https://huggingface.co/chanind/gemma-3-1b-batch-topk-matryoshka-saes-w-32k-l0-40) |
| google/gemma-scope-2-1b-pt | 0–25 | `attn.z`, `mlp_out`, `resid_post` | 448 | [Browse](google-gemma-scope-2-1b-pt-e19ab56f-p1.md#sae-0d952e5c2db3d4432f98f730) | [Repository](https://huggingface.co/google/gemma-scope-2-1b-pt) |

<a id="model-google-gemma-3-4b-it"></a>

#### google/gemma-3-4b-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-4b-it | 0–33 | `attn.z`, `mlp_out`, `resid_post` | 532 | [Browse](google-gemma-scope-2-4b-it-b95fdb9a-p1.md#sae-1e0337d3f7148fa71ef77e3d) | [Repository](https://huggingface.co/google/gemma-scope-2-4b-it) |

<a id="model-google-gemma-3-4b-pt"></a>

#### google/gemma-3-4b-pt

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-4b-pt | 0–33 | `attn.z`, `mlp_out`, `resid_post` | 532 | [Browse](google-gemma-scope-2-4b-pt-568216a4-p1.md#sae-0abcc6e651e01d7b9aee4ab9) | [Repository](https://huggingface.co/google/gemma-scope-2-4b-pt) |

<a id="model-google-gemma-3-12b-it"></a>

#### google/gemma-3-12b-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-12b-it | 0–47 | `attn.z`, `mlp_out`, `resid_post` | 700 | [Browse](google-gemma-scope-2-12b-it-e2dafd87-p1.md#sae-0a28fba8253e2dbf3115196b) | [Repository](https://huggingface.co/google/gemma-scope-2-12b-it) |

<a id="model-google-gemma-3-12b-pt"></a>

#### google/gemma-3-12b-pt

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-12b-pt | 0–47 | `attn.z`, `mlp_out`, `resid_post` | 700 | [Browse](google-gemma-scope-2-12b-pt-f0957440-p1.md#sae-0b639367d10f5eefdac9435f) | [Repository](https://huggingface.co/google/gemma-scope-2-12b-pt) |

<a id="model-google-gemma-3-27b-it"></a>

#### google/gemma-3-27b-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-27b-it | 0–61 | `attn.z`, `mlp_out`, `resid_post` | 868 | [Browse](google-gemma-scope-2-27b-it-1873c12a-p1.md#sae-2a8acfb030183e878e2a3f2d) | [Repository](https://huggingface.co/google/gemma-scope-2-27b-it) |

<a id="model-google-gemma-3-27b-pt"></a>

#### google/gemma-3-27b-pt

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-27b-pt | 0–61 | `resid_post` | 300 | [Browse](google-gemma-scope-2-27b-pt-e710759f-p1.md#sae-00cae8b73cede1c593c39095) | [Repository](https://huggingface.co/google/gemma-scope-2-27b-pt) |

<a id="model-google-gemma-3-270m"></a>

#### google/gemma-3-270m

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-270m-pt | 0–17 | `attn.z`, `mlp_out`, `resid_post` | 340 | [Browse](google-gemma-scope-2-270m-pt-060fac8c-p1.md#sae-2c45205a31db084ac6f6fcf5) | [Repository](https://huggingface.co/google/gemma-scope-2-270m-pt) |

<a id="model-google-gemma-3-270m-it"></a>

#### google/gemma-3-270m-it

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| google/gemma-scope-2-270m-it | 0–17 | `attn.z`, `mlp_out`, `resid_post` | 340 | [Browse](google-gemma-scope-2-270m-it-fbd9b5b9-p1.md#sae-0af8c6595baac9b7c5c13e9c) | [Repository](https://huggingface.co/google/gemma-scope-2-270m-it) |

### Llama

<a id="model-meta-llama-llama-3-1-8b"></a>

#### meta-llama/Llama-3.1-8B

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| fnlp/Llama3_1-8B-Base-LXA-8x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxa-8x-7f4178f3-p1.md#sae-00f01116cff749f5cab30ad6) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXA-8x) |
| fnlp/Llama3_1-8B-Base-LXA-32x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxa-32x-9166f68d-p1.md#sae-0aa37b9d25089b9e1f97e28e) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXA-32x) |
| fnlp/Llama3_1-8B-Base-LXM-8x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxm-8x-a115a280-p1.md#sae-0baa9874ccb2d7d276c15931) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXM-8x) |
| fnlp/Llama3_1-8B-Base-LXM-32x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxm-32x-0717e2c8-p1.md#sae-0dba734f18da1cf37c364a6b) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXM-32x) |
| fnlp/Llama3_1-8B-Base-LXR-8x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxr-8x-4ab21145-p1.md#sae-1c2cc5cdc48383880f67c7e8) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXR-8x) |
| fnlp/Llama3_1-8B-Base-LXR-32x | — | — | 32 | [Browse](fnlp-llama3-1-8b-base-lxr-32x-aae6c3a4-p1.md#sae-1c276e5242f7e6b5587061b6) | [Repository](https://huggingface.co/fnlp/Llama3_1-8B-Base-LXR-32x) |

<a id="model-meta-llama-llama-3-1-8b-instruct"></a>

#### meta-llama/Llama-3.1-8B-Instruct

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| andyrdt/saes-llama-3.1-8b-instruct | 3, 7, 11, 15, 19, 23, 27 | `resid_post` | 7 | [Browse](andyrdt-saes-llama-3-1-8b-instruct-8ffd883b-p1.md#sae-0ab1b4b3c146e2118bfbc444) | [Repository](https://huggingface.co/andyrdt/saes-llama-3.1-8b-instruct) |
| Goodfire/Llama-3.1-8B-Instruct-SAE-l19 | 19 | `resid_post` | 1 | [Browse](goodfire-llama-3-1-8b-instruct-sae-l19-c605baef-p1.md#sae-67c6bcd9c84048110d5346b4) | [Repository](https://huggingface.co/Goodfire/Llama-3.1-8B-Instruct-SAE-l19) |

<a id="model-meta-llama-llama-3-3-70b-instruct"></a>

#### meta-llama/Llama-3.3-70B-Instruct

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Goodfire/Llama-3.3-70B-Instruct-SAE-l50 | 50 | `resid_post` | 1 | [Browse](goodfire-llama-3-3-70b-instruct-sae-l50-fc45854c-p1.md#sae-238447a2c9870a399a3e6ad9) | [Repository](https://huggingface.co/Goodfire/Llama-3.3-70B-Instruct-SAE-l50) |

<a id="model-meta-llama-meta-llama-3-8b-instruct"></a>

#### meta-llama/Meta-Llama-3-8B-Instruct

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Juliushanhanhan/llama-3-8b-it-res | 25 | `resid_post` | 1 | [Browse](juliushanhanhan-llama-3-8b-it-res-c9fb7b2c-p1.md#sae-60771e1259570fd1e84467bc) | [Repository](https://huggingface.co/Juliushanhanhan/llama-3-8b-it-res) |

### DeepSeek

<a id="model-deepseek-ai-deepseek-r1-distill-llama-8b"></a>

#### deepseek-ai/DeepSeek-R1-Distill-Llama-8B

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| fnlp/Llama-Scope-R1-Distill | — | — | 96 | [Browse](fnlp-llama-scope-r1-distill-d8b6fc49-p1.md#sae-0a3c72860285f3b7c0b67982) | [Repository](https://huggingface.co/fnlp/Llama-Scope-R1-Distill) |
| qresearch/DeepSeek-R1-Distill-Llama-8B-SAE-l19 | 19 | `resid_post` | 1 | [Browse](qresearch-deepseek-r1-distill-llama-8b-sae-l19-ef51b546-p1.md#sae-f80de4274d1467f86b0b08c0) | [Repository](https://huggingface.co/qresearch/DeepSeek-R1-Distill-Llama-8B-SAE-l19) |

### Mistral

<a id="model-mistral-7b"></a>

#### mistral-7b

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| JoshEngels/Mistral-7B-Residual-Stream-SAEs | 8, 16, 24 | `resid_pre` | 3 | [Browse](joshengels-mistral-7b-residual-stream-saes-b0afde64-p1.md#sae-9f3dd058a877c9cdced2fcdd) | [Repository](https://huggingface.co/JoshEngels/Mistral-7B-Residual-Stream-SAEs) |

### Pythia

<a id="model-pythia-70m-deduped"></a>

#### pythia-70m-deduped

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| canrager/lm_sae | 3, 4, unspecified | `resid_post` | 188 | [Browse](canrager-lm-sae-f1118512-p1.md#sae-0ed9683868c1aa737d8c277e) | [Repository](https://huggingface.co/canrager/lm_sae) |
| ctigges/pythia-70m-deduped__att-sm_processed | 0–5 | `attn_out` | 6 | [Browse](ctigges-pythia-70m-deduped-att-sm-processed-b2bfe902-p1.md#sae-1e048e213f3c1228a93474c1) | [Repository](https://huggingface.co/ctigges/pythia-70m-deduped__att-sm_processed) |
| ctigges/pythia-70m-deduped__mlp-sm_processed | 0–5 | `mlp_out` | 6 | [Browse](ctigges-pythia-70m-deduped-mlp-sm-processed-bcc481e5-p1.md#sae-0fee16fa159a9d813dd0e106) | [Repository](https://huggingface.co/ctigges/pythia-70m-deduped__mlp-sm_processed) |
| ctigges/pythia-70m-deduped__res-sm_processed | 0–5 | `resid_post`, `resid_pre` | 7 | [Browse](ctigges-pythia-70m-deduped-res-sm-processed-57dc984f-p1.md#sae-1c9c15fa82cd55e2dbd3e44a) | [Repository](https://huggingface.co/ctigges/pythia-70m-deduped__res-sm_processed) |

### Qwen

<a id="model-qwen-qwen2-5-7b-instruct"></a>

#### Qwen/Qwen2.5-7B-Instruct

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| andyrdt/saes-qwen2.5-7b-instruct | 3, 7, 11, 15, 19, 23, 27 | `resid_post` | 7 | [Browse](andyrdt-saes-qwen2-5-7b-instruct-87be31eb-p1.md#sae-0c7ccf7d6f311b9d5b5a9644) | [Repository](https://huggingface.co/andyrdt/saes-qwen2.5-7b-instruct) |

<a id="model-qwen-qwen3-1-7b-base"></a>

#### Qwen/Qwen3-1.7B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_50 | 0–27 | `resid_post` | 28 | [Browse](qwen-sae-res-qwen3-1-7b-base-w32k-l0-50-36adacad-p1.md#sae-0cdc68ed94feec058a73f896) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_50) |
| Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_100 | 0–27 | `resid_post` | 28 | [Browse](qwen-sae-res-qwen3-1-7b-base-w32k-l0-100-f6e0808c-p1.md#sae-0d37fc6b08bbbc5ad17ae8ce) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-1.7B-Base-W32K-L0_100) |

<a id="model-qwen-qwen3-8b-base"></a>

#### Qwen/Qwen3-8B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3-8B-Base-W64K-L0_50 | 0–35 | `resid_post` | 36 | [Browse](qwen-sae-res-qwen3-8b-base-w64k-l0-50-006e008d-p1.md#sae-1ac32a356ef3b2b9af7d351b) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-8B-Base-W64K-L0_50) |
| Qwen/SAE-Res-Qwen3-8B-Base-W64K-L0_100 | 0–35 | `resid_post` | 36 | [Browse](qwen-sae-res-qwen3-8b-base-w64k-l0-100-a6bb8249-p1.md#sae-0aa815715694a480a031d3d3) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-8B-Base-W64K-L0_100) |

<a id="model-qwen-qwen3-30b-a3b-base"></a>

#### Qwen/Qwen3-30B-A3B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3-30B-A3B-Base-W32K-L0_50 | 0–47 | `resid_post` | 48 | [Browse](qwen-sae-res-qwen3-30b-a3b-base-w32k-l0-50-0bf3548a-p1.md#sae-0e3c2d5ea7dcf0590ae42e01) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-30B-A3B-Base-W32K-L0_50) |
| Qwen/SAE-Res-Qwen3-30B-A3B-Base-W128K-L0_100 | 0–47 | `resid_post` | 48 | [Browse](qwen-sae-res-qwen3-30b-a3b-base-w128k-l0-100-5566ff71-p1.md#sae-0ade84a6d4a9ad6ee4fbdf9e) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3-30B-A3B-Base-W128K-L0_100) |

<a id="model-qwen-qwen3-5-2b-base"></a>

#### Qwen/Qwen3.5-2B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3.5-2B-Base-W32K-L0_50 | 0–23 | `resid_post` | 24 | [Browse](qwen-sae-res-qwen3-5-2b-base-w32k-l0-50-14a2898e-p1.md#sae-3ca78e0aa9320ee8f55e1a6f) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-2B-Base-W32K-L0_50) |
| Qwen/SAE-Res-Qwen3.5-2B-Base-W32K-L0_100 | 0–23 | `resid_post` | 24 | [Browse](qwen-sae-res-qwen3-5-2b-base-w32k-l0-100-125da098-p1.md#sae-0db63071097c5ce11ee5453d) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-2B-Base-W32K-L0_100) |

<a id="model-qwen-qwen3-5-9b-base"></a>

#### Qwen/Qwen3.5-9B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3.5-9B-Base-W64K-L0_50 | 0–31 | `resid_post` | 32 | [Browse](qwen-sae-res-qwen3-5-9b-base-w64k-l0-50-9816ef38-p1.md#sae-1d98225fce91478689bb7f60) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-9B-Base-W64K-L0_50) |
| Qwen/SAE-Res-Qwen3.5-9B-Base-W64K-L0_100 | 0–31 | `resid_post` | 32 | [Browse](qwen-sae-res-qwen3-5-9b-base-w64k-l0-100-12d9a24c-p1.md#sae-1acc2475cf6eb77062c8c137) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-9B-Base-W64K-L0_100) |

<a id="model-qwen-qwen3-5-27b"></a>

#### Qwen/Qwen3.5-27B

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_50 | 0–63 | `resid_post` | 64 | [Browse](qwen-sae-res-qwen3-5-27b-w80k-l0-50-1c92d28d-p1.md#sae-2ebaabaaf45d94aec82fa3e6) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_50) |
| Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_100 | 0–63 | `resid_post` | 64 | [Browse](qwen-sae-res-qwen3-5-27b-w80k-l0-100-5cfeb0a2-p1.md#sae-03d0ae3a7f07a97761b1c8e0) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_100) |

<a id="model-qwen-qwen3-5-35b-a3b-base"></a>

#### Qwen/Qwen3.5-35B-A3B-Base

| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |
| --- | --- | --- | ---: | --- | --- |
| Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50 | 0–39 | `resid_post` | 40 | [Browse](qwen-sae-res-qwen3-5-35b-a3b-base-w32k-l0-50-0f560694-p1.md#sae-0e37060cc63cf9b393e15337) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W32K-L0_50) |
| Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W128K-L0_100 | 0–39 | `resid_post` | 40 | [Browse](qwen-sae-res-qwen3-5-35b-a3b-base-w128k-l0-100-cdb3a097-p1.md#sae-0c195ff57cd2f81603fd1020) | [Repository](https://huggingface.co/Qwen/SAE-Res-Qwen3.5-35B-A3B-Base-W128K-L0_100) |

### CLIP

<a id="model-open-clip-laion-clip-vit-b-32-datacomp-xl-s13b-b90k"></a>

#### open-clip:laion/CLIP-ViT-B-32-DataComp.XL-s13B-b90K

**Top K SAEs (CLS only, k = 64)**

| Layer | Output | Method | Features | Model card | Weights |
| ---: | --- | --- | ---: | --- | --- |
| 0 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-0-hook-resid-post-be001792-p1.md#sae-d7ece304fec63470bc384a1e) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_0-hook_resid_post/resolve/6fe455e88a73f8721b0a8afe4b2db8557088cd2f/weights.pt) |
| 1 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-1-hook-resid-post-29b9f564-p1.md#sae-1d0d97efc1c45a769bfe9dee) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_1-hook_resid_post/resolve/8f0be31adc16157e158c3b9d14c4bc4f282e337f/weights.pt) |
| 2 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-2-hook-resid-post-6fbc3f2c-p1.md#sae-5333c803640f5d830b7ee968) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_2-hook_resid_post/resolve/4ca1d7079f312b15cd374b73761ffcf12eef8148/weights.pt) |
| 3 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-3-hook-resid-post-99d7643c-p1.md#sae-bd01de0b59a94e90f3a39629) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_3-hook_resid_post/resolve/d71b7014b2f8c960b85343cacb421c2def88fe9f/weights.pt) |
| 4 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-4-hook-resid-post-630f76a9-p1.md#sae-70ff8ffa6b1392058c4c511a) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_4-hook_resid_post/resolve/eddfce67119159c145466742dcb712de8bafdd58/weights.pt) |
| 5 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-5-hook-resid-post-c1f66c4a-p1.md#sae-cf8f20e859b7ca81ff242e94) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_5-hook_resid_post/resolve/cf8840b023929b709d6c7238b7cdefe97511e967/weights.pt) |
| 6 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-6-hook-resid-post-df4eac96-p1.md#sae-0d3eeb21874158c2ddbb1d80) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_6-hook_resid_post/resolve/79975e9b36184bf814b42ba9671f043084f332fc/weights.pt) |
| 7 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-7-hook-resid-post-e3ad2f47-p1.md#sae-3cdcd024d8e27ce15c3e0981) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_7-hook_resid_post/resolve/527f3226fad896771450c831943b59eaaefdb8b1/weights.pt) |
| 8 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-8-hook-resid-post-d9381dbb-p1.md#sae-30c4190ef087c103e10db516) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_8-hook_resid_post/resolve/44707538700459cd0949dd97ba3a7e9d28370e7c/weights.pt) |
| 9 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-9-hook-resid-post-65c78350-p1.md#sae-ea0799ee152a8f1f6a4410ab) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_9-hook_resid_post/resolve/3c9b2342e4a6fa6206fd3a1aea7da48ed838f9c4/weights.pt) |
| 10 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-10-hook-resid-post-09f6d4b3-p1.md#sae-8f2733f6e94098dc207f0028) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_10-hook_resid_post/resolve/5fc8afde379bc28d8eae35ce6eb36edaeca90ba2/weights.pt) |
| 11 | `resid_post` | TopK | 49,152 | [Model card](prisma-multimodal-sae-top-k-64-cls-only-layer-11-hook-resid-post-5eda9b30-p1.md#sae-0fafbffebcc920f372943f8f) | [Download](https://huggingface.co/Prisma-Multimodal/sae-top_k-64-cls_only-layer_11-hook_resid_post/resolve/73611b78df558947515c213b56be74c3b2be91f0/weights.pt) |

**Vanilla SAEs (All Patches)**

| Layer | Output | Method | Features | Model card | Weights |
| ---: | --- | --- | ---: | --- | --- |
| 0 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-0-hook-mlp-out-l1-1e-05-a34cb36b-p1.md#sae-e5f5a0ac64324f3783143e76) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-0-hook_mlp_out-l1-1e-05/resolve/0e273446e43dbf30254b9f556acb2fde4cf25655/n_images_2600058.pt) |
| 0 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-0-hook-resid-post-l1-1e-05-36e55f9a-p1.md#sae-2e419a0d48acbb754fc53195) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-0-hook_resid_post-l1-1e-05/resolve/3ed2b73f1e254b70913fb2e3adfc236c75b7d3a3/n_images_2600058.pt) |
| 1 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-1-hook-mlp-out-l1-1e-05-b8bbb10d-p1.md#sae-878eddf6ae7b5ef1875974be) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-1-hook_mlp_out-l1-1e-05/resolve/dae506aef5c78520db211e7a0778728357c7b5b4/n_images_2600058.pt) |
| 1 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-1-hook-resid-post-l1-1e-05-141818f7-p1.md#sae-e3d3312cca4a0fdeae185936) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-1-hook_resid_post-l1-1e-05/resolve/935ddbb89b49c1c810fd56aed5cc5fe0a52241bd/n_images_2600058.pt) |
| 2 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-2-hook-mlp-out-l1-1e-05-5be9a52a-p1.md#sae-e2c32dd565fdfd51e9b0e164) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-2-hook_mlp_out-l1-1e-05/resolve/4fe8d11cdd2212530cfdc35bd403e0c408b3343b/n_images_2600058.pt) |
| 2 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-2-hook-resid-post-l1-5e-05-5499880f-p1.md#sae-674f201bb2f7584983a80c05) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-2-hook_resid_post-l1-5e-05/resolve/6fe7a320ce8e6872fb2edb990dab78b43d947d1d/n_images_2600058.pt) |
| 3 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-3-hook-mlp-out-l1-1e-05-525688c9-p1.md#sae-190a9beb1d1433158d151c22) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-3-hook_mlp_out-l1-1e-05/resolve/4b9dadc4af09812e5997c7219ee914d2eb7a8667/n_images_2600058.pt) |
| 3 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-3-hook-resid-post-l1-1e-05-3aee6425-p1.md#sae-927b003a11b4ce9fd59b7937) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-3-hook_resid_post-l1-1e-05/resolve/3b85c4f033f83aad23bec92d08ceac5d71531342/n_images_2600058.pt) |
| 4 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook-mlp-out-l1-1e-05-c406e95a-p1.md#sae-f68d7273774eba2b107a77fa) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_mlp_out-l1-1e-05/resolve/5292d390fdb6212fed88eba19a7fedea0c7bc261/n_images_2600058.pt) |
| 4 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook-resid-post-l1-1e-05-4e0cc490-p1.md#sae-cc5adaa79ff5a387ffefa3a1) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-4-hook_resid_post-l1-1e-05/resolve/fe7440845eb19ad81f20b3e72462954a255d0875/n_images_2600058.pt) |
| 5 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-5-hook-mlp-out-l1-1e-05-cf0c6bd1-p1.md#sae-7e71857ef1043f8566531c3a) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-5-hook_mlp_out-l1-1e-05/resolve/b8932ed5bb3396b63ac17cba42f1043a80890f87/n_images_2600058.pt) |
| 5 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-5-hook-resid-post-l1-1e-05-a9aef118-p1.md#sae-b4da134cdfbdc4a967c0596a) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-5-hook_resid_post-l1-1e-05/resolve/77b4bd78c143783cba3fa120c613fb34018b77e9/n_images_2600058.pt) |
| 6 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-6-hook-mlp-out-l1-1e-05-4814cce8-p1.md#sae-5fba767750021d53691d1f7e) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-6-hook_mlp_out-l1-1e-05/resolve/e105fc43a3a056e434f8004fc58086fd95d7f9c9/n_images_2600058.pt) |
| 6 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-6-hook-resid-post-l1-1e-05-4e216de2-p1.md#sae-e05fdad5b69e792dbcb1c60a) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-6-hook_resid_post-l1-1e-05/resolve/dd9af074421e816a283d14cfb314e6bc20db0a52/n_images_2600058.pt) |
| 7 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-7-hook-mlp-out-l1-1e-05-b1dceebd-p1.md#sae-b2a006f15a3327acf8065687) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-7-hook_mlp_out-l1-1e-05/resolve/a3c5becf8de6ee7c5273c110de7abf4c1196c322/n_images_2600058.pt) |
| 7 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-7-hook-resid-post-l1-1e-05-4e9d2a73-p1.md#sae-b9b97c995de56f7e73c354c3) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-7-hook_resid_post-l1-1e-05/resolve/4bda95d6bb72d97658729f04102a370febf15163/n_images_2600058.pt) |
| 8 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-8-hook-mlp-out-l1-1e-05-0e5ab714-p1.md#sae-201b7eed53c25590b5b3bae5) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-8-hook_mlp_out-l1-1e-05/resolve/d642a005de6a1c1cdcdbb334272502fde0a03129/n_images_2600058.pt) |
| 8 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-8-hook-resid-post-l1-1e-05-f3bff603-p1.md#sae-d406e7295e615fd2fcbb2e31) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-8-hook_resid_post-l1-1e-05/resolve/cc45aa71fcf004d1bc5a103677f927d70a9ddd81/n_images_2600058.pt) |
| 9 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-9-hook-mlp-out-l1-1e-05-5ea9a4c5-p1.md#sae-bde5dd51a6f6149ffd68956e) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-9-hook_mlp_out-l1-1e-05/resolve/51f6f2d618a8896049b73654188745cda389991c/n_images_2600058.pt) |
| 9 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-9-hook-resid-post-l1-1e-05-3e9c9b79-p1.md#sae-a593ad1fd4733438e7223722) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-9-hook_resid_post-l1-1e-05/resolve/9ec4ff364c08d2413b59e8e87b55c07bd4f1096a/n_images_2600058.pt) |
| 10 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-10-hook-mlp-out-l1-1e-05-c8408b46-p1.md#sae-931d2e8b7be9569585bc92fb) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-10-hook_mlp_out-l1-1e-05/resolve/1e0dcc98c63aed3ce28f0387027cf8df6784fef1/weights.pt) |
| 10 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-10-hook-resid-post-l1-1e-0-f8d5a4b5-p1.md#sae-c007ea744faf6a16c824aef6) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-10-hook_resid_post-l1-1e-05/resolve/15fc6e2dbdfcd267246c685476a0973d17dfabe1/n_images_2600058.pt) |
| 11 | `mlp_out` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook-mlp-out-l1-5e-05-e5d2598a-p1.md#sae-6d9e06b327105f319e6695c3) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook_mlp_out-l1-5e-05/resolve/96dbef7f18fef5cff5252883220ec57815ae9094/n_images_2600058.pt) |
| 11 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook-resid-post-l1-1e-0-19d81acc-p1.md#clip-b32-layer11-relu-49152) | [Download](https://huggingface.co/Prisma-Multimodal/sparse-autoencoder-clip-b-32-sae-vanilla-x64-layer-11-hook_resid_post-l1-1e-05/resolve/2b1cb17ffb8b06e7f45a699dfc97d417f9879be4/weights.pt) |

**Vanilla SAEs (CLS only)**

| Layer | Output | Method | Features | Model card | Weights |
| ---: | --- | --- | ---: | --- | --- |
| 0 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-0-hook-resid-post-936-799987792969-82-6ce6c6c4-p1.md#sae-a01dcb48bffd2c67f19a8759) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_0-hook_resid_post-936.799987792969-82/resolve/760d678a5684d1d944baee5e0b7bcc39f90dc8cf/weights.pt) |
| 1 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-1-hook-resid-post-314-175018310547-85-0684272a-p1.md#sae-aaa40f88156ba9dbaedac539) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_1-hook_resid_post-314.175018310547-85/resolve/041499f5113b484de8b3d86a3de55e116cd41cf6/weights.pt) |
| 2 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-2-hook-resid-post-711-121887207031-96-de933e89-p1.md#sae-51ef002337748979bc62ad68) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_2-hook_resid_post-711.121887207031-96/resolve/2f09f5f7d7502b81b13588c1ddfe37b6fa46c139/weights.pt) |
| 3 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-3-hook-resid-post-686-334411621094-95-e1b24974-p1.md#sae-f3d349494af30c9e39d690de) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_3-hook_resid_post-686.334411621094-95/resolve/748fddc2d14afaee4139b5c55bf02fbdb68b1de0/weights.pt) |
| 4 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-4-hook-resid-post-682-543762207031-95-70371ff9-p1.md#sae-255774d206df3ad72b4024a8) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_4-hook_resid_post-682.543762207031-95/resolve/f3e572015d45722a995f1d7e34708708fda9dae5/weights.pt) |
| 5 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-5-hook-resid-post-510-356262207031-94-b941bfe0-p1.md#sae-4faaf453917766f203e933ae) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_5-hook_resid_post-510.356262207031-94/resolve/497762f5ff26aa4564235c6b744bbc1d9bdcdf48/weights.pt) |
| 6 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-6-hook-resid-post-430-556243896484-92-1dba0e16-p1.md#sae-04aae79c4dde7568a8ec2863) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_6-hook_resid_post-430.556243896484-92/resolve/cb3cea6778563e0ac5a8ffbae6721249fc2ae38b/weights.pt) |
| 7 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-7-hook-resid-post-492-959381103516-88-e202cdb5-p1.md#sae-b3e2f3c2d6074ac51cb81c0e) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_7-hook_resid_post-492.959381103516-88/resolve/36ee6452a83a0101b8ffee2ca6b4459b76bd037b/weights.pt) |
| 8 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-8-hook-resid-post-635-018737792969-76-fcf44fe7-p1.md#sae-50fe9fab1696d0574cdfea8b) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_8-hook_resid_post-635.018737792969-76/resolve/cae7e5a7dca90fbbba8dfa39d58c6a7deda7753e/weights.pt) |
| 9 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-9-hook-resid-post-518-621887207031-74-1d594d37-p1.md#sae-f0938b880f2ce662e2ca793b) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_9-hook_resid_post-518.621887207031-74/resolve/a3f85d49f189ba732b6cd4e214efcf86307fc9ed/weights.pt) |
| 10 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-10-hook-resid-post-552-512512207031-74-e664f8b9-p1.md#sae-86ac8a2e9b4ff0a886d24057) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_10-hook_resid_post-552.512512207031-74/resolve/765c2de91f9453f0bad5c80312f59e61964f2e49/weights.pt) |
| 11 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-cls-11-hook-resid-post-383-75-65-ae3695da-p1.md#sae-a1a1057ac74f9290dcc5a4d8) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-CLS_11-hook_resid_post-383.75-65/resolve/ff2600336274e7c17b8d1dd691a691a8c86a93c6/weights.pt) |

**Vanilla Spatial Patches**

| Layer | Output | Method | Features | Model card | Weights |
| ---: | --- | --- | ---: | --- | --- |
| 0 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-0-hook-resid-post-989-203430175781-99-9ad70c1c-p1.md#sae-87312e3556a7af3fd97ee019) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_0-hook_resid_post-989.203430175781-99/resolve/44118ebc22bc0da7f5244b28381b052efacc8e5b/weights.pt) |
| 1 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-1-hook-resid-post-757-82958984375-99-90302bb4-p1.md#sae-c3eb199bf05436ceaca478fd) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_1-hook_resid_post-757.82958984375-99/resolve/67f252c3e77dd4c72e705d292981a56c1444d846/weights.pt) |
| 2 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-2-hook-resid-post-1007-89801025391-99-00a5d998-p1.md#sae-324b7bc29e3573fe58cc18c4) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_2-hook_resid_post-1007.89801025391-99/resolve/bdcb9850512a4601f8c030b8a66416ec790b4945/weights.pt) |
| 3 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-3-hook-resid-post-935-601989746094-99-8179ed03-p1.md#sae-385eb4432e847ab625e6e051) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_3-hook_resid_post-935.601989746094-99/resolve/ce1d25363f0d1f744bf91e5f2faa29b5fc3272a2/weights.pt) |
| 4 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-4-hook-resid-post-965-410095214844-99-eb153d5e-p1.md#sae-069d1b34e54df45822877176) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_4-hook_resid_post-965.410095214844-99/resolve/538e8b9719f69e112f903c53671095e1750ace55/weights.pt) |
| 5 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-5-hook-resid-post-964-674072265625-99-79654e4e-p1.md#sae-459f715adb690bdfc13187be) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_5-hook_resid_post-964.674072265625-99/resolve/b706687068d7c14ae6e96e168a83cffa39ab8e27/weights.pt) |
| 6 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-6-hook-resid-post-1006-57165527344-99-9ca90cc0-p1.md#sae-be8aea5e5d803797fa3d84dd) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_6-hook_resid_post-1006.57165527344-99/resolve/6e85800f1878b775a73c4962f05dcfdfb47f68bd/weights.pt) |
| 7 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-7-hook-resid-post-984-1376953125-99-e1a98e5f-p1.md#sae-30d13e6974c07fdcfe6e56f6) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_7-hook_resid_post-984.1376953125-99/resolve/24cd8b80c8b9632b554326991fe8c29b0d912f61/weights.pt) |
| 8 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-8-hook-resid-post-965-125-99-76bed52f-p1.md#sae-625034bcb4d6b8615ca82292) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_8-hook_resid_post-965.125-99/resolve/8b3af6e8a0c9566d1e9fd0d9a5a7c2876ff300f6/weights.pt) |
| 9 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-9-hook-resid-post-854-891540527344-99-34b94475-p1.md#sae-2f43929f73123055f0abc341) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_9-hook_resid_post-854.891540527344-99/resolve/103552e06f03dfe68ab6096c1c798af468a6807c/weights.pt) |
| 11 | `resid_post` | ReLU | 49,152 | [Model card](prisma-multimodal-imagenet-sweep-vanilla-x64-spatial-max-11-hook-resid-post-829-0498046875-99-58f22b51-p1.md#sae-5a825b8db82ff1565aa982c7) | [Download](https://huggingface.co/Prisma-Multimodal/imagenet-sweep-vanilla-x64-Spatial_max_11-hook_resid_post-829.0498046875-99/resolve/4faf9b365b401540bfec509208e42e639cdd39d8/weights.pt) |

### DINO

<a id="model-facebook-dino-vitb16"></a>

#### facebook/dino-vitb16

**Vanilla SAEs (All Patches)**

| Layer | Output | Method | Features | Model card | Weights |
| ---: | --- | --- | ---: | --- | --- |
| 0 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-0-resid-post-507-98-3a6c7680-p1.md#sae-f1ea8668fa9868f9acfb0a14) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_0-resid_post-507-98/resolve/c44792cf34df589b145a8f9f2d7751e9e0d4c6f3/weights.pt) |
| 1 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-1-resid-post-549-95-8b19f0dc-p1.md#sae-9ca27cce3fb7724e72b47056) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_1-resid_post-549-95/resolve/8d826594ece0ba46ba75eca1148dcde74eea7dea/weights.pt) |
| 2 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-2-resid-post-661-95-104918d4-p1.md#sae-981ce5c7d3f20f1f243c7e05) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_2-resid_post-661-95/resolve/36e70ddc8fbb40d2033ce06449b7cc0e27e151a3/weights.pt) |
| 3 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-3-resid-post-989-95-4d256a16-p1.md#sae-86a8975f03a0bd8a7b03164d) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_3-resid_post-989-95/resolve/f10912d22f794387d295cbfb5f9b8217d9e45ba2/weights.pt) |
| 4 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-4-resid-post-876-99-af43df66-p1.md#sae-02866003c9f53b6f7367c884) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_4-resid_post-876-99/resolve/d02128d8540c162da9903b2d6cde66411449e57c/weights.pt) |
| 5 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-5-resid-post-1001-98-321266c9-p1.md#sae-8e9bafed84c8cf59acbd4f3d) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_5-resid_post-1001-98/resolve/70b00cb039c450e03b17ccd10b5831c0af894614/weights.pt) |
| 6 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-6-resid-post-962-99-e5b77a16-p1.md#sae-cd8142668e73214e94f36a49) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_6-resid_post-962-99/resolve/af0d86a21fd508bc718f37cabc60951029b01f4a/weights.pt) |
| 7 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-7-resid-post-1086-98-5de834b7-p1.md#sae-71e3dbf4a4616a3f32ed1d7f) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_7-resid_post-1086-98/resolve/195a814def34f86e6b78fefd45a643eb246508dc/weights.pt) |
| 8 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-8-resid-post-530-90-55650052-p1.md#sae-ba55c0e6f61b26c6677993ff) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_8-resid_post-530-90/resolve/405583318c0d666e11546206f8710cbcc0c10e25/weights.pt) |
| 9 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-9-resid-post-1105-99-306f741b-p1.md#sae-92e1f361e3f9604ccdfafd98) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_9-resid_post-1105-99/resolve/cc93ebc09d4e867d78a17f2f5924005b7be044ff/weights.pt) |
| 10 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-10-resid-post-835-99-be707896-p1.md#sae-9cb9a2f96929744a0786d19d) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_10-resid_post-835-99/resolve/38558531e1c54926e58092caf769b1fc5960237d/weights.pt) |
| 11 | `resid_post` | ReLU | — | [Model card](prisma-multimodal-dino-vanilla-x64-all-patches-11-resid-post-1085-99-effecb2a-p1.md#sae-bb76f6cdae5ae9a58a09428d) | [Download](https://huggingface.co/Prisma-Multimodal/DINO-vanilla-x64-all_patches_11-resid_post-1085-99/resolve/3e3ea0cdcde4186db8069f4fe0ce219e8693155a/weights.pt) |
