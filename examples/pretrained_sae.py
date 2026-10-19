"""Use a published GPT2 SAE, save and reload it, without training."""
from argparse import ArgumentParser
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from vlmprobe import Prober, visualization as viz

BASE = 'openai-community/gpt2'
REVISION = '607a30d783dfa663caf39e06633721c8d4cfcd7e'
CARD = 'sae-6783018355728933dae6d812'


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path, default=Path('outputs/pretrained_sae_cache'))
    parser.add_argument('--output-dir', type=Path, default=Path('outputs/pretrained_sae'))
    parser.add_argument('--device', default='cpu')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(4)
    tokenizer = AutoTokenizer.from_pretrained(BASE, revision=REVISION, cache_dir=args.cache_dir, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(BASE, revision=REVISION,
        cache_dir=args.cache_dir, dtype=torch.float32, attn_implementation='eager').to(args.device).eval()
    probe = Prober(model, tokenizer)
    method = probe.sae.from_pretrained(CARD, cache_dir=args.cache_dir, device=args.device)
    text = 'The microscope revealed a complex pattern of cells in the tissue.'
    inputs = tokenizer(text, return_tensors='pt', add_special_tokens=False).to(args.device)
    result = method.run(inputs)
    result.save(args.output_dir / 'features')
    method.profile(top_k=3).run(inputs).save(args.output_dir / 'profile')
    method.save(args.output_dir / 'dictionary')
    restored = probe.sae.load(args.output_dir / 'dictionary', device=args.device)
    torch.testing.assert_close(restored.run(inputs).tensors['features'], result.tensors['features'])
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4))
    viz.plot_sae_activity(result, top_k=12, ax=ax)
    ax.set_title('Published GPT2 layer-0 TopK SAE: feature activity')
    fig.tight_layout()
    fig.savefig(args.output_dir / 'activity.png', dpi=180)
    plt.close(fig)
    summary = {'card_id': CARD, 'base_model': BASE, 'base_revision': REVISION,
        'text': text, 'tokens': tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]),
        'feature_shape': list(result.tensors['features'].shape),
        'l0': result.tensors['l0'].tolist(), 'training_called': False,
        'pretrained_verification': method.sae.source_metadata['pretrained_verification']}
    (args.output_dir / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'output': str(args.output_dir), 'feature_shape': summary['feature_shape'],
                      'training_called': False}))


if __name__ == '__main__':
    main()
