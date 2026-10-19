# Pixtral

[Home](../../README.md) / [Model support](README.md)

Pixtral-12B uses a spatial patch encoder and a Mistral decoder through the native
Transformers `LlavaForConditionalGeneration` class. The automatic adapter supports
residual lenses and interventions, projected heads, IOI-style path patching, and
consumed eager attention scores/probabilities. All seven attention attribution
methods in the technical report were executed on the pretrained checkpoint.
See the [official Transformers guide](https://huggingface.co/docs/transformers/model_doc/pixtral).

Install `python -m pip install "vlmprobe[transformers,visualization]"`.
The default checkpoint is about 12B parameters and requires substantial GPU memory.

```python
from io import BytesIO
from urllib.request import urlopen
from pathlib import Path
import os
import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
from vlmprobe import Prober, visualization as viz

checkpoint = os.environ.get("VLM_PROBING_MODEL", "mistral-community/pixtral-12b")
device = os.environ.get("VLM_PROBING_DEVICE", "cuda:0")
processor = AutoProcessor.from_pretrained(checkpoint)
# Transformers 5.3.x: apply the native Mistral regex correction after loading.
tokenizer = processor.tokenizer
tokenizer._patch_mistral_regex(
    tokenizer, checkpoint, init_kwargs=tokenizer.init_kwargs,
    fix_mistral_regex=True, is_local=Path(checkpoint).is_dir(),
)
model = LlavaForConditionalGeneration.from_pretrained(
    checkpoint, dtype=torch.bfloat16, attn_implementation="eager"
).to(device).eval()
probe = Prober(model, processor)
url = "https://raw.githubusercontent.com/gexinh/vlm-probing/main/demos/assets/images/2341576.jpg"
with urlopen(url, timeout=30) as response:
    image = Image.open(BytesIO(response.read())).convert("RGB")

messages = [{"role": "user", "content": [
    {"type": "image"}, {"type": "text", "text": "Is the shirt black or yellow?"}
]}]
prompt = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = probe.prepare(
    prompt=prompt, image=image,
    device=device, size={"longest_edge": 256}
)
inputs.kwargs["pixel_values"] = inputs.kwargs["pixel_values"].to(torch.bfloat16)
capabilities = probe.describe()["methods"]
for name, item in capabilities.items():
    print(name, item["available"], item["sites"], item["missing"])
layers = capabilities["lens.logit"]["sites"]
selected = list(dict.fromkeys([layers[0], layers[len(layers) // 2], layers[-1]]))
result = probe.lens.logit(layers=selected).run(inputs)
target_id = int(result.tensors["logits"][-1, 0].argmax())
print("Target token:", target_id, repr(tokenizer.decode([target_id])))
ax = viz.plot_lens_heatmap(result, target_token_id=target_id)
ax.figure.savefig("pixtral-logit-lens.png", bbox_inches="tight")
result.save("pixtral-logit-lens-result")
```

The snippet applies Transformers 5.3's native Mistral tokenizer correction
after loading: that version's constructor passes the correction flag twice.
Checkpoint files remain unchanged. The report uses a square-padded input and
256-pixel longest edge, giving a verified 16×16 grid. Image-row separators are
text positions, not patch positions. For arbitrary aspect ratios, derive the
grid from processor `image_sizes`; never infer a square grid from token count.
Use `SequenceLogProb` with aligned answer masks for multi-token answers.

The same [method APIs](../methods/README.md) apply to this binding; the example
above is one complete readout, not a list of supported methods. See the
[shared workflow](README.md#use-any-supported-method). For a spatial overlay,
use the actual processed image and rectangular patch grid; row-separator tokens
must not be included as visual patches. Fitted lenses require Pixtral-specific
artifacts and full-vocabulary Attention Lens training can be very expensive.
