"""Render our SAE model pages from the packaged, pinned checkpoint metadata.

Run from any directory with Python's standard library; no upstream SDKs or
checkpoint downloads are involved. Metadata refresh is a separate source audit.
"""
from collections import defaultdict
import gzip
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/methods/sae/models'
RESOURCE = ROOT / 'src/vlm_probing/sae/resources/published_model_cards.json.gz'


def value(item):
    return 'Not specified' if item is None else str(item)


def escape_cell(item):
    return value(item).replace('|', '\\|').replace('\n', ' ')


def card_section(card, method_links=True):
    method = card['method']
    method_label = 'Not reported' if method == 'unknown' else method
    if method_links and method in {'relu', 'topk', 'gated', 'jumprelu', 'abstopk', 'batchtopk', 'matryoshka_batchtopk', 'matching_pursuit'}:
        method_label = f'[{method_label}](../../{method}.md)'
    size = card['dimensions']
    origin = card['origin']
    lines = [f'<a id="{card["id"]}"></a>', '', f'## {escape_cell(card["title"])}', '',
        f'**Model ID:** `{card["id"]}`', '',
        f'[Download weights]({card["links"]["checkpoint"]})' if card['download']['kind'] == 'file' else f'[Checkpoint files]({card["links"]["checkpoint"]})', '',
        '| Property | Value |', '| --- | --- |',
        f'| Artifact | {"SAE dictionary" if card["artifact_kind"] == "sae" else "Vision backbone; no SAE dictionary"} |',
        f'| Base model | `{escape_cell(card["base_model"])}` |',
        f'| Method | {method_label} |', f'| Source hook / output | `{escape_cell(card.get("hook"))}` |',
        f'| Layer | {escape_cell(card.get("layer"))} |',
        f'| Activation width | {escape_cell(size.get("activation"))} |',
        f'| Dictionary features | {escape_cell(size.get("features"))} |',
        f'| Checkpoint license | {escape_cell(origin.get("checkpoint_license"))} |',
        f'| Checkpoint revision | `{escape_cell(card["download"].get("revision"))}` |',
        f'| Tensor format | {escape_cell(origin.get("format"))} |', '']
    if card.get('input_conventions'):
        lines += ['**Input / activation conventions:**', '', '`' + json.dumps(card['input_conventions'], ensure_ascii=False, separators=(', ', ': ')) + '`', '']
    if card['download'].get('sha256'):
        lines += [f'**Weight SHA256:** `{card["download"]["sha256"]}`', '']
    if card['links'].get('config'):
        lines += [f'[Checkpoint configuration]({card["links"]["config"]})', '']
    if card.get('source_binding_requirements'):
        lines += ['**Source model settings:** `' + json.dumps(card['source_binding_requirements'], ensure_ascii=False) + '`', '']
    if card.get('source_alias_note'):
        lines += [card['source_alias_note'], '']
    aliases = card.get('registry_aliases', [])
    if aliases:
        lines += ['**Published release names:** ' + '; '.join(f'`{a["release"]}` / `{a["sae_id"]}`' for a in aliases), '']
    return '\n'.join(lines)


def build():
    payload = json.loads(gzip.decompress(RESOURCE.read_bytes()))
    cards = payload['models']
    DESTINATION.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(list)
    for card in cards:
        if card['artifact_kind'] == 'sae':
            page = card['links']['card'].split('#')[0]
            groups[page].append(card)
    published = (DESTINATION / 'published').resolve()
    expected = {(ROOT / page).resolve() for page in groups}
    if any(path.parent != published for path in expected):
        raise ValueError('checkpoint pages must stay inside the generated published directory')
    # A metadata refresh may remove aliases/repositories or reduce page counts.
    # Retire only obsolete generated pages, keeping the hand-written model hub.
    for previous in published.glob('*-p*.md'):
        if previous.resolve() not in expected:
            previous.unlink()
    by_repo = defaultdict(list)
    for page, group in groups.items():
        group.sort(key=lambda c: (c['layer'] is None, c['layer'] or 0, c['dimensions']['features'] or 0, c['origin']['sae_id']))
        by_repo[group[0]['download']['repo_id']].append(page)
    for repo, pages in by_repo.items():
        pages.sort(key=lambda p: int(re.search(r'-p(\d+)\.md$', p)[1]))
        for n, page in enumerate(pages):
            group = groups[page]
            path = ROOT / page
            path.parent.mkdir(parents=True, exist_ok=True)
            names = sorted({c['base_model'] for c in group})
            lines = [f'# {repo}', '', '[Model hub](../README.md) · [All checkpoint repositories](README.md)', '',
                f'Published SAE dictionaries for **{", ".join(names)}**. Page {n+1} of {len(pages)}.', '',
                f'[Author checkpoint repository](https://huggingface.co/{repo})', '',
                'Select a dictionary below, download its author weights, and preserve its source model, hook and input conventions when converting to the native artifact format.', '',
                'Pages: ' + ' · '.join(f'[{i+1}]({Path(p).name})' for i, p in enumerate(pages)), '']
            for card in group:
                lines += [card_section(card), '---', '']
            source_urls = sorted({c['origin'].get('registry_source_url') for c in group if c['origin'].get('registry_source_url')})
            lines += ['## Metadata sources', ''] + [f'- [Pinned published listing {i+1}]({url})' for i, url in enumerate(source_urls)]
            path.write_text('\n'.join(lines)+'\n')
    # A compact index keeps the common model hub readable.
    index = ['# Published SAE checkpoint repositories', '', '[Model hub](../README.md) · [Standalone searchable catalog](../catalog.html)', '',
             '| Checkpoint repository | Base model | Dictionaries | Pages |', '| --- | --- | ---: | ---: |']
    for repo, pages in sorted(by_repo.items()):
        dictionaries = [c for p in pages for c in groups[p]]
        models = ', '.join(sorted({c['base_model'] for c in dictionaries}))
        index += [f'| [{escape_cell(repo)}]({Path(pages[0]).name}) | {escape_cell(models)} | {len(dictionaries)} | {len(pages)} |']
    (DESTINATION/'published/README.md').write_text('\n'.join(index)+'\n')
    backbones = [c for c in cards if c['artifact_kind'] == 'backbone']
    lines = ['# Vision backbones for SAE training', '', '[Model hub](README.md) · [Training guide](../training/README.md)', '',
        'These are pretrained **vision backbones**, not pretrained SAE dictionaries. They correspond to the activation-extraction models described in the Overcomplete source. Use their activations to train a dictionary with the shared SAE training workflow.', '',
        'The untagged ViT alias is represented by an explicitly named published variant. Preserve the chosen checkpoint and transform in your training provenance.', '']
    for card in backbones:
        lines += [card_section(card, method_links=False), f'[Model repository]({card["links"]["repository"]})', '', '---', '']
    (DESTINATION/'backbones.md').write_text('\n'.join(lines).rstrip()+'\n')
    # The standalone catalog embeds its data, so it also works from a local file.
    columns = []
    for c in cards:
        columns.append([c['id'], c['base_model'], c['method'], c.get('hook'), c['dimensions'].get('activation'), c['dimensions'].get('features'), c['modality'], c['artifact_kind'], c['links']['card'].split('docs/methods/sae/models/')[1], c['links']['repository'], c['links']['checkpoint'], c['origin'].get('checkpoint_license'), ' '.join(a['release']+' '+a['sae_id'] for a in c.get('registry_aliases',[]))])
    data = json.dumps(columns, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    document = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VLMProbe SAE models</title><style>
body{font:15px system-ui,sans-serif;background:#f5f7fb;color:#17314b;margin:0}main{max-width:1480px;margin:40px auto;padding:0 25px}h1{color:#087d89;margin-bottom:8px}p{max-width:1050px;line-height:1.6}a{color:#095fc0}header,section{background:white;border:1px solid #d7e1ef;border-radius:12px;padding:22px;margin:18px 0}.controls{display:flex;gap:12px;flex-wrap:wrap}input,select,button{font:inherit;border:1px solid #bed0e6;padding:10px;border-radius:7px;background:white}input{min-width:320px;flex:1}button{cursor:pointer;color:#1359bb}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:12px 9px;border-bottom:1px solid #e5ebf4;vertical-align:top}th{color:#365a7c;font-size:13px}td{font-size:13px;overflow-wrap:anywhere}code{font-size:12px}.scroll{overflow:auto}.nav{display:flex;align-items:center;gap:15px;margin:18px 0}.muted{color:#62798f}.kind{display:inline-block;padding:3px 7px;border-radius:4px;background:#edf3fb;color:#385f89}small{color:#668096}</style></head><body><main><header><a href="README.md">Model hub</a><h1>SAE models and checkpoints</h1><p>Author-published sparse dictionaries for language, vision and multimodal backbones, with our own model information pages and direct checkpoint downloads. Select a dictionary by its exact source model, hook and input conventions; raw author weights require conversion before native model-bound use.</p><p class="muted">Snapshot: 2026-10-19. __COUNTS__ unique SAE checkpoints; five separately labeled vision backbones. Alias names for the same checkpoint are merged. Unreported fields remain unspecified.</p></header><section><div class="controls"><input id="search" placeholder="Search model, hook, release, feature width or model ID"><select id="method"><option value="">All methods</option></select><select id="kind"><option value="sae">SAE dictionaries</option><option value="backbone">Vision backbones</option><option value="">All model resources</option></select><select id="modality"><option value="">All modalities</option><option value="vision">Vision</option><option value="language">Language</option><option value="multimodal">Multimodal</option><option value="unknown">Not specified by source</option></select></div><div class="nav"><button id="prev">Previous</button><span id="count"></span><button id="next">Next</button></div><div class="scroll"><table><thead><tr><th>Base model</th><th>Method / kind</th><th>Source hook</th><th>Activation → features</th><th>Our model information</th><th>Weights</th></tr></thead><tbody id="rows"></tbody></table></div></section></main><script id="model-data" type="application/json">__DATA__</script><script>
const models=JSON.parse(document.getElementById('model-data').textContent);const $=id=>document.getElementById(id);const esc=x=>String(x??'Not specified').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const method of [...new Set(models.filter(m=>m[7]==='sae').map(m=>m[2]))].sort()){const o=document.createElement('option');o.value=method;o.textContent=method==='unknown'?'Method not reported':method;$('method').appendChild(o)}
let page=0,selected=[];const perPage=50;function draw(reset=true){if(reset)page=0;const q=$('search').value.toLowerCase();selected=models.filter(m=>(!$('kind').value||m[7]===$('kind').value)&&(!$('method').value||m[2]===$('method').value)&&(!$('modality').value||(m[6]??'unknown')===$('modality').value)&&(!q||m.join(' ').toLowerCase().includes(q)));page=Math.max(0,Math.min(page,Math.ceil(selected.length/perPage)-1));$('count').textContent=selected.length.toLocaleString()+' models · page '+(page+1)+' / '+Math.max(1,Math.ceil(selected.length/perPage));$('prev').disabled=page===0;$('next').disabled=(page+1)*perPage>=selected.length;$('rows').innerHTML=selected.slice(page*perPage,(page+1)*perPage).map(m=>'<tr><td>'+esc(m[1])+'<br><small>'+esc(m[0])+'</small></td><td>'+esc(m[2]==='unknown'?'Not reported':m[2])+'<br><span class="kind">'+esc(m[7])+'</span></td><td><code>'+esc(m[3])+'</code></td><td>'+esc(m[4])+' → '+esc(m[5])+'</td><td><a href="'+esc(m[8])+'">Open our card</a></td><td><a href="'+esc(m[10])+'">Download / files</a><br><a href="'+esc(m[9])+'">Model repository</a></td></tr>').join('')}
for(const id of ['search','method','kind','modality'])$(id).addEventListener(id==='search'?'input':'change',()=>draw());$('prev').onclick=()=>{page--;draw(false)};$('next').onclick=()=>{page++;draw(false)};draw();</script></body></html>'''
    document = document.replace('__DATA__', data).replace('__COUNTS__', str(payload['counts']['sae_dictionaries']))
    (DESTINATION/'catalog.html').write_text(document)
    print(json.dumps({'sae_cards':payload['counts']['sae_dictionaries'],'backbone_cards':len(backbones),'repository_pages':len(groups),'html_bytes':len(document.encode())}))


if __name__ == '__main__':
    build()
