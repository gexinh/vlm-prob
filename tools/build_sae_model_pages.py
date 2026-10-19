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
import os
import argparse

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/methods/sae/models'
RESOURCE = ROOT / 'src/vlm_probing/sae/resources/published_model_cards.json.gz'


def value(item):
    return 'Not specified' if item is None else str(item)


def escape_cell(item):
    return value(item).replace('|', '\\|').replace('\n', ' ')


def natural_key(text):
    """Keep model sizes and layer numbers in numerical reading order."""
    return tuple(int(part) if part.isdigit() else part.lower()
                 for part in re.split(r'(\d+)', text))


def backbone_family(base_model):
    """Group the declared backbone, independently of its checkpoint author."""
    name = base_model.lower().rsplit('/', 1)[-1]
    if 'clip-vit-' in name:
        return 'CLIP', 'vision'
    if name.startswith(('dino-', 'dinov2', 'dino_')):
        return 'DINO', 'vision'
    if name.startswith('deepseek-'):
        return 'DeepSeek', 'language'
    for prefix, family in (('gpt2', 'GPT-2'), ('gpt-oss', 'GPT-OSS'),
                           ('gemma', 'Gemma'), ('llama', 'Llama'),
                           ('meta-llama', 'Llama'), ('qwen', 'Qwen'),
                           ('pythia', 'Pythia'), ('mistral', 'Mistral')):
        if name.startswith(prefix):
            return family, 'language'
    return 'Other backbones', 'other'


def model_anchor(base_model):
    return 'model-' + re.sub(r'[^a-z0-9]+', '-', base_model.lower()).strip('-')


def layer_summary(cards):
    """Compress contiguous layer runs without filling gaps in the metadata."""
    layers = sorted({card['layer'] for card in cards if card['layer'] is not None})
    runs = []
    for layer in layers:
        if runs and layer == runs[-1][-1] + 1:
            runs[-1].append(layer)
        else:
            runs.append([layer])
    labels = [str(run[0]) if len(run) == 1 else
              ', '.join(map(str, run)) if len(run) == 2 else
              f'{run[0]}–{run[-1]}' for run in runs]
    if layers and any(card['layer'] is None for card in cards):
        labels.append('unspecified')
    return ', '.join(labels) or '—'


def output_summary(cards):
    outputs = set()
    for card in cards:
        hook = card.get('hook')
        if hook:
            # The full source hook remains on each model information card.
            hook = re.sub(r'^blocks\.\d+\.', '', hook)
            hook = re.sub(r'_layer_\d+$', '', hook)
            outputs.add(hook.replace('hook_', ''))
    return ', '.join(f'`{escape_cell(hook)}`' for hook in sorted(outputs)) or '—'


def card_path(card):
    path, anchor = card['links']['card'].split('#', 1)
    return f'{Path(path).name}#{anchor}'


def repository_index(cards):
    """One-page backbone directory with every published collection reachable."""
    by_model = defaultdict(list)
    for card in cards:
        if card['artifact_kind'] == 'sae':
            by_model[card['base_model']].append(card)
    family_order = ('GPT-2', 'GPT-OSS', 'Gemma', 'Llama', 'DeepSeek', 'Mistral',
                    'Pythia', 'Qwen', 'CLIP', 'DINO', 'Other backbones')
    models = sorted(by_model, key=lambda name: (
        family_order.index(backbone_family(name)[0]), natural_key(name)))
    lines = ['# Published SAE checkpoint repositories', '',
             '[Model hub](../README.md) · [Search model cards](../web/README.md) · '
             '[Load a checkpoint](../../loading.md)', '',
             'Choose a backbone to browse its checkpoint collections, layers and model cards.', '']
    for kind, title in (('language', 'Language and multimodal backbones'),
                        ('vision', 'Vision backbones'), ('other', 'Other backbones')):
        selected = [name for name in models if backbone_family(name)[1] == kind]
        if not selected:
            continue
        lines += [f'## {title}', '',
                  '| Base model | Checkpoint repositories | SAE checkpoints |',
                  '| --- | ---: | ---: |']
        for name in selected:
            group = by_model[name]
            count = len({card['download']['repo_id'] for card in group})
            lines += [f'| [{escape_cell(name)}](#{model_anchor(name)}) | {count} | {len(group):,} |']
        lines += ['']
    lines += ['## Checkpoint collections by backbone', '']
    for family in family_order:
        selected = [name for name in models if backbone_family(name)[0] == family]
        if not selected:
            continue
        lines += [f'### {family}', '']
        for name in selected:
            group = by_model[name]
            lines += [f'<a id="{model_anchor(name)}"></a>', '', f'#### {escape_cell(name)}', '']
            if backbone_family(name)[1] == 'vision':
                by_scope = defaultdict(list)
                for card in group:
                    scope = card.get('input_conventions', {}).get('token_scope') or 'SAE dictionaries'
                    by_scope[scope].append(card)
                for scope, scope_cards in sorted(by_scope.items()):
                    lines += [f'**{escape_cell(scope)}**', '',
                              '| Layer | Output | Method | Features | Model card | Weights |',
                              '| ---: | --- | --- | ---: | --- | --- |']
                    for card in sorted(scope_cards, key=lambda item: (
                            item['layer'] is None, item['layer'] or 0, item.get('hook') or '', item['id'])):
                        label = {'relu': 'ReLU', 'topk': 'TopK'}.get(card['method'], card['method'])
                        if label == 'unknown':
                            label = '—'
                        features = card['dimensions'].get('features')
                        features_label = f'{features:,}' if features is not None else '—'
                        lines += [f'| {value(card["layer"])} | {output_summary([card])} | '
                                  f'{escape_cell(label)} | {features_label} | [Model card]({card_path(card)}) | '
                                  f'[Download]({card["links"]["checkpoint"]}) |']
                    lines += ['']
            else:
                by_repo = defaultdict(list)
                for card in group:
                    by_repo[card['download']['repo_id']].append(card)
                lines += ['| Checkpoint collection | Layers | Outputs | Dictionaries | Model cards | Weights |',
                          '| --- | --- | --- | ---: | --- | --- |']
                for repo, repo_cards in sorted(by_repo.items(), key=lambda pair: natural_key(pair[0])):
                    first = sorted(repo_cards, key=lambda item: natural_key(card_path(item)))[0]
                    lines += [f'| {escape_cell(repo)} | {layer_summary(repo_cards)} | '
                              f'{output_summary(repo_cards)} | {len(repo_cards):,} | '
                              f'[Browse]({card_path(first)}) | [Repository](https://huggingface.co/{repo}) |']
                lines += ['']
    return '\n'.join(lines).rstrip() + '\n'


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
    if card.get('loading', {}).get('mode') == 'native_pretrained_recipe':
        lines += ['**Load without fitting:**', '',
                  '```python', f'method = probe.sae.from_pretrained("{card["id"]}")',
                  'result = method.run(inputs)', '```', '',
                  '[Complete matching-backbone and inference example](../../loading.md).', '']
    if card.get('source_binding_requirements'):
        lines += ['**Source model settings:** `' + json.dumps(card['source_binding_requirements'], ensure_ascii=False) + '`', '']
    if card.get('source_alias_note'):
        lines += [card['source_alias_note'], '']
    aliases = card.get('registry_aliases', [])
    if aliases:
        lines += ['**Published release names:** ' + '; '.join(f'`{a["release"]}` / `{a["sae_id"]}`' for a in aliases), '']
    return '\n'.join(lines)


def build(*, repository=None, ref=None, site_url=None):
    repository = repository or os.environ.get("GITHUB_REPOSITORY", "gexinh/vlm-prob")
    ref = ref or os.environ.get("GITHUB_REF_NAME", "main")
    site_url = site_url or "https://"+repository.split("/")[0]+".github.io/"+repository.split("/")[1]+"/sae-models/"
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
    (DESTINATION/'published/README.md').write_text(repository_index(cards))
    backbones = [c for c in cards if c['artifact_kind'] == 'backbone']
    lines = ['# Vision backbones for SAE training', '', '[Model hub](README.md) · [Training guide](../training/README.md)', '',
        'Use these pretrained **vision backbones** to collect activations and train an SAE. '
        'Each card lists the model checkpoint and output layer; the [training guide](../training/README.md) '
        'covers activation collection, dictionary fitting and evaluation.', '']
    for card in backbones:
        lines += [card_section(card, method_links=False), f'[Model repository]({card["links"]["repository"]})', '', '---', '']
    (DESTINATION/'backbones.md').write_text('\n'.join(lines).rstrip()+'\n')
    result = build_web(cards, payload['counts'], repository=repository, ref=ref, site_url=site_url)
    print(json.dumps({'sae_cards':payload['counts']['sae_dictionaries'],'backbone_cards':len(backbones),
                      'repository_pages':len(groups), **result}))


WEB_DOCUMENT = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SAE models · VLMProbe</title><style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f5f7fb;color:#17314b;font:15px/1.55 system-ui,sans-serif}main{max-width:1480px;margin:32px auto;padding:0 24px}header,section{background:#fff;border:1px solid #d7e1ef;border-radius:12px;padding:22px;margin:18px 0}h1{color:#087d89;margin:10px 0}h2{margin-top:0;color:#087d89}p{max-width:1060px}a{color:#095fc0}button,input,select{font:inherit;border:1px solid #bed0e6;padding:9px;border-radius:6px;background:#fff;color:inherit}button{cursor:pointer;color:#1359bb}button:disabled{opacity:.45;cursor:default}input{min-width:220px;flex:2}select{flex:1;max-width:100%;min-width:145px}.controls{display:flex;gap:10px;flex-wrap:wrap}.field{flex:1;min-width:160px;display:flex;flex-direction:column;gap:4px}.field.search{flex:3;min-width:230px}label{font-size:13px;font-weight:600}.nav,.links{display:flex;gap:14px;align-items:center;flex-wrap:wrap}.nav{margin:18px 0}.muted{color:#62798f}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%}td,th{padding:11px 9px;text-align:left;border-bottom:1px solid #e5ebf4;vertical-align:top;overflow-wrap:anywhere}th{color:#365a7c;font-size:13px}td{font-size:13px}small{font-size:12px;color:#62798f}code,pre{font:12px/1.6 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#f3f6fb;border-radius:6px;padding:14px}.badge{font-size:12px;background:#edf3fb;border-radius:4px;padding:3px 7px;white-space:nowrap}.properties th{width:210px}.details-top{display:flex;gap:12px;align-items:start;justify-content:space-between}.card-id{display:block;margin:10px 0}.error{color:#a83023}.notice{border-left:3px solid #5b78b8;padding-left:13px}.hidden,[hidden]{display:none!important}.summary{font-variant-numeric:tabular-nums}#detail{scroll-margin-top:18px}#status{margin:12px 0}summary{cursor:pointer;font-weight:600}details{margin:15px 0}.empty{text-align:center;padding:35px}.links a{font-weight:600}@media(max-width:680px){main{padding:0 10px;margin:10px auto}header,section{padding:16px}.properties th{width:125px}.field{min-width:130px}input{min-width:120px}}
</style></head><body><main>
<header><nav class="links"><a href="../">Project home</a><a id="hub-link" href="__HUB__">Model hub</a><a id="markdown-link" href="__MARKDOWN__">Browse on GitHub</a></nav>
<h1>SAE models and checkpoints</h1><p>Find a published dictionary by its exact backbone, method and activation hook. Open a model card for its weights, input conventions and source configuration.</p>
<p class="muted">__COUNT__ SAE dictionaries · __BACKBONES__ separately labeled vision backbones. Published aliases for the same checkpoint are merged; unreported fields remain unspecified.</p>
<noscript><p>JavaScript is needed for search and rendered cards. <a href="__MARKDOWN__">Browse the complete Markdown repository index</a>.</p></noscript></header>
<section id="detail" hidden tabindex="-1" aria-label="Selected model information" aria-live="polite"></section>
<section aria-label="Search published models"><div class="controls">
<div class="field search"><label for="search">Search</label><input id="search" type="search" placeholder="Backbone, hook, release, feature width or model ID" disabled></div>
<div class="field"><label for="method">Method</label><select id="method" disabled><option value="">All methods</option></select></div>
<div class="field"><label for="kind">Resource</label><select id="kind" disabled><option value="sae">SAE dictionaries</option><option value="backbone">Vision backbones</option><option value="">All resources</option></select></div>
<div class="field"><label for="modality">Modality</label><select id="modality" disabled><option value="">All modalities</option><option value="vision">Vision</option><option value="language">Language</option><option value="multimodal">Multimodal</option><option value="unknown">Not specified</option></select></div>
<div class="field"><label for="format">Checkpoint format</label><select id="format" disabled><option value="">All source formats</option></select></div></div>
<p id="status" role="status">Loading the search index…</p>
<div class="nav"><button id="prev" disabled>Previous</button><span id="count" class="summary"></span><button id="next" disabled>Next</button></div>
<div class="scroll"><table><thead><tr><th>Base model / ID</th><th>Method / resource</th><th>Source hook</th><th>Activation → features</th><th>Model card</th></tr></thead><tbody id="rows"></tbody></table></div></section>
</main><script>
'use strict';
const githubRoot=__GITHUB_JSON__;
const $=id=>document.getElementById(id);
const esc=value=>String(value??'Not specified').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeURL=value=>{try{const url=new URL(value,location.href);return ['https:','http:'].includes(url.protocol)?url.href:null}catch{return null}};
const link=(url,label)=>{const safe=safeURL(url);return safe?'<a href="'+esc(safe)+'">'+esc(label)+'</a>':'<span>'+esc(label)+' unavailable</span>'};
let models=[],byID=new Map(),page=0,selected=[],activeCard=null,requestID=0;
const perPage=40,shards=new Map();
async function getJSON(path){const response=await fetch(path);if(!response.ok)throw new Error('HTTP '+response.status+' for '+path);return response.json()}
function option(id,value,label){const node=document.createElement('option');node.value=value;node.textContent=label;$(id).appendChild(node)}
function draw(reset=true){
 if(reset)page=0;
 const terms=$('search').value.trim().toLowerCase().split(/\s+/).filter(Boolean);
 selected=models.filter(m=>(!$('kind').value||m.kind===$('kind').value)&&(!$('method').value||m.method===$('method').value)&&(!$('modality').value||m.modality===$('modality').value)&&(!$('format').value||m.format===$('format').value)&&terms.every(q=>m.search.includes(q)));
 const pages=Math.max(1,Math.ceil(selected.length/perPage));page=Math.max(0,Math.min(page,pages-1));
 $('count').textContent=selected.length.toLocaleString()+' resources · page '+(page+1)+' / '+pages;
 $('prev').disabled=page===0;$('next').disabled=(page+1)*perPage>=selected.length;
 $('rows').innerHTML=selected.slice(page*perPage,(page+1)*perPage).map(m=>'<tr data-model-id="'+esc(m.id)+'"><td>'+esc(m.base)+'<br><small>'+esc(m.id)+'</small></td><td>'+esc(m.method==='unknown'?'Not reported':m.method==='not_applicable'?'Not applicable':m.method)+'<br><span class="badge">'+esc(m.kind==='sae'?'SAE dictionary':'Vision backbone')+'</span></td><td><code>'+esc(m.hook)+'</code></td><td>'+esc(m.width)+' → '+esc(m.features)+'</td><td><a class="card-link" href="#'+encodeURIComponent(m.id)+'">Open model card</a></td></tr>').join('')||'<tr><td colspan="5" class="empty">No resources match these filters.</td></tr>';
}
function property(name,value){return '<tr><th scope="row">'+esc(name)+'</th><td>'+esc(value)+'</td></tr>'}
function jsonBlock(title,value){return value&&Object.keys(value).length?'<h3>'+esc(title)+'</h3><pre>'+esc(JSON.stringify(value,null,2))+'</pre>':''}
function closeCard(){requestID++;activeCard=null;$('detail').hidden=true;history.pushState(null,'',location.pathname+location.search)}
function renderCard(card){
 const d=card.download||{},o=card.origin||{},size=card.dimensions||{},links=card.links||{};
 const markdown=githubRoot+'/'+links.card;
 const aliases=card.registry_aliases||[];
 $('detail').innerHTML='<div class="details-top"><div><span class="badge">'+esc(card.artifact_kind==='sae'?'SAE dictionary':'Vision backbone; not an SAE')+'</span><h2>'+esc(card.title)+'</h2></div><button id="close-card" aria-label="Close model card">Close</button></div>'+
 '<code class="card-id">'+esc(card.id)+'</code><div class="links">'+link(links.checkpoint,d.kind==='file'?'Download weights':'Checkpoint files')+link(links.repository,'Author repository')+(links.config?link(links.config,'Checkpoint configuration'):'')+link(markdown,'Markdown card')+link(location.href,'Permalink')+'</div>'+
 '<table class="properties"><tbody>'+property('Base model',card.base_model)+property('Method',card.method==='unknown'?'Not reported':card.method==='not_applicable'?'Not applicable':card.method)+property('Modality',card.modality)+property('Hook / output',card.hook)+property('Layer',card.layer)+property('Activation width',size.activation)+property('Dictionary features',size.features)+property('Checkpoint format',o.format)+property('Checkpoint license',o.checkpoint_license)+property('Checkpoint revision',d.revision)+property('Weight SHA256',d.sha256)+property('Checkpoint path',d.path)+'</tbody></table>'+
 jsonBlock('Input and activation conventions',card.input_conventions)+jsonBlock('Source model settings',card.source_binding_requirements)+
 (card.loading?'<h3>Use this checkpoint</h3><p>'+esc(card.loading.instruction)+'</p>':'')+
 (card.source_alias_note?'<p class="notice">'+esc(card.source_alias_note)+'</p>':'')+
 (aliases.length?'<details><summary>Published release names ('+aliases.length+')</summary><ul>'+aliases.map(a=>'<li><code>'+esc(a.release)+'</code> / <code>'+esc(a.sae_id)+'</code></li>').join('')+'</ul></details>':'')+
 '<h3>Source and evidence</h3><p>'+link(o.registry_source_url||o.source_url,'Pinned metadata source')+'</p>'+jsonBlock('Recorded evidence',card.evidence)+
 '<details><summary>Complete model metadata</summary><pre>'+esc(JSON.stringify(card,null,2))+'</pre></details>';
 $('close-card').onclick=closeCard;
}
async function showHash(scroll=true){
 const token=++requestID;let id;
 try{id=decodeURIComponent(location.hash.slice(1))}catch{id=''}
 if(!id){$('detail').hidden=true;activeCard=null;return}
 $('detail').hidden=false;$('detail').innerHTML='<p role="status">Loading model card…</p>';
 const model=byID.get(id);
 if(!model){$('detail').innerHTML='<h2>Model not found</h2><p>The model ID '+esc(id)+' is absent from this catalog. Use search or browse the GitHub index.</p>';return}
 try{
  if(!shards.has(model.shard))shards.set(model.shard,getJSON('cards/'+model.shard+'.json').catch(error=>{shards.delete(model.shard);throw error}));
  const cards=await shards.get(model.shard);if(token!==requestID)return;
  const card=cards[id];if(!card)throw new Error('Card is absent from its metadata shard');
  activeCard=card;renderCard(card);
  if(scroll){$('detail').scrollIntoView({behavior:'smooth',block:'start'});$('detail').focus({preventScroll:true})}
 }catch(error){if(token===requestID)$('detail').innerHTML='<h2>Could not load model card</h2><p class="error">'+esc(error.message)+'</p><p>Reload the page or '+link(githubRoot+'/'+model.markdown,'open the Markdown card')+'.</p>'}
}
async function init(){
 try{
  if(location.protocol==='file:')throw new Error('Open the hosted catalog or serve this folder over HTTP; browsers block JSON fetches from local files.');
  const data=await getJSON('catalog-index.json');
  models=data.rows.map(r=>{const m={id:r[0],base:data.base_models[r[1]],method:data.methods[r[2]],hook:r[3]===null?null:data.hooks[r[3]],width:r[4],features:r[5],modality:data.modalities[r[6]],kind:data.kinds[r[7]],repository:data.repositories[r[8]],layer:r[9],aliases:r[10],format:data.formats[r[11]],shard:r[12],markdown:r[13]};m.search=[m.id,m.base,m.method,m.hook,m.width,m.features,m.modality,m.kind,m.repository,m.layer,m.aliases,m.format].join(' ').toLowerCase();return m});
  byID=new Map(models.map(m=>[m.id,m]));
  for(const value of [...new Set(models.filter(m=>m.kind==='sae').map(m=>m.method))].sort())option('method',value,value==='unknown'?'Method not reported':value);
  for(const value of data.formats.slice().sort())option('format',value,value);
  for(const id of ['search','method','kind','modality','format'])$(id).disabled=false;
  $('status').textContent='Search '+models.length.toLocaleString()+' resources. Model details load only when selected.';
  draw();await showHash(Boolean(location.hash));
 }catch(error){$('status').className='error';$('status').textContent='Catalog unavailable: '+error.message}
}
let debounce;
$('search').addEventListener('input',()=>{clearTimeout(debounce);debounce=setTimeout(()=>draw(),100)});
for(const id of ['method','kind','modality','format'])$(id).addEventListener('change',()=>draw());
$('prev').onclick=()=>{page--;draw(false)};$('next').onclick=()=>{page++;draw(false)};
window.addEventListener('hashchange',()=>{if(models.length)showHash()});
$('rows').addEventListener('click',event=>{const anchor=event.target.closest('a.card-link');if(anchor&&anchor.hash===location.hash){event.preventDefault();showHash()}});
init();
</script></body></html>'''


def build_web(cards, counts, *, repository, ref, site_url, output=None):
    """Small shell, compact search metadata and bounded on-demand card shards."""
    import hashlib
    from urllib.parse import quote
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('repository must be owner/name')
    github_root = f'https://github.com/{repository}/blob/{quote(ref, safe="/")}'
    web = Path(output) if output is not None else DESTINATION / 'web'
    shards_path = web / 'cards'
    shards_path.mkdir(parents=True, exist_ok=True)
    fields = {name: [] for name in ('base_models','methods','hooks','modalities','kinds','repositories','formats')}
    indices = {name: {} for name in fields}
    def intern(name, entry):
        if entry not in indices[name]:
            indices[name][entry] = len(fields[name])
            fields[name].append(entry)
        return indices[name][entry]
    rows, shards = [], defaultdict(dict)
    for card in cards:
        identifier = card['id']
        shard = f'{int(hashlib.sha256(identifier.encode()).hexdigest()[:8],16) % 64:02x}'
        shards[shard][identifier] = card
        repo = card['download'].get('repo_id') or card['links']['repository']
        aliases = ' '.join(a['release']+' '+a['sae_id'] for a in card.get('registry_aliases', []))
        rows.append([identifier, intern('base_models',card['base_model']), intern('methods',card['method']),
            intern('hooks',card['hook']) if card.get('hook') is not None else None,
            card['dimensions'].get('activation'), card['dimensions'].get('features'),
            intern('modalities',card.get('modality') or 'unknown'), intern('kinds',card['artifact_kind']),
            intern('repositories',repo), card.get('layer'), aliases, intern('formats',card['origin'].get('format') or 'Not specified'),
            shard, card['links']['card']])
    index = {'schema':'vlmprobe-sae-web-index-v1', 'counts':counts, **fields, 'rows':rows}
    (web/'catalog-index.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n')
    for shard, group in shards.items():
        (shards_path/f'{shard}.json').write_text(json.dumps(group,ensure_ascii=False,separators=(',',':'))+'\n')
    expected = {f'{shard}.json' for shard in shards}
    for previous in shards_path.glob('*.json'):
        if previous.name not in expected:
            previous.unlink()
    markdown = github_root+'/docs/methods/sae/models/published/README.md'
    hub = github_root+'/docs/methods/sae/models/README.md'
    document = WEB_DOCUMENT.replace('__HUB__',html.escape(hub,quote=True)).replace('__MARKDOWN__',html.escape(markdown,quote=True))
    document = document.replace('__COUNT__',f'{counts["sae_dictionaries"]:,}').replace('__BACKBONES__',str(counts['backbones']))
    document = document.replace('__GITHUB_JSON__',json.dumps(github_root).replace('<','\\u003c'))
    (web/'index.html').write_text(document+'\n')
    instructions = '''# Search SAE model cards

Search by backbone, SAE method, activation hook or dictionary width. Open a card
to view its source configuration, input conventions and checkpoint downloads.

## On the project page

Open **SAE checkpoints** in the project page navigation. Select **Open model
card** beside a search result to view its details. The URL fragment identifies
the selected dictionary, so you can copy the URL to share that card directly.

## From a local checkout

Run this command in the repository root:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/docs/methods/sae/models/web/>. Keep the server running
while searching and opening cards; the catalog loads its data over HTTP.

## On GitHub

Use the [model directory](../published/README.md) to browse checkpoints grouped
by backbone and open their Markdown cards.
'''
    (web/'README.md').write_text(instructions)

    # Legacy catalog URLs become a lightweight launcher. The old 4 MB embedded
    # data page is retired; local-file users get the Markdown or HTTP options.
    launcher = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VLMProbe SAE model catalog</title><style>body{{max-width:740px;margin:60px auto;padding:20px;font:17px/1.7 system-ui;color:#17314b}}a{{color:#087d89}}code{{background:#f0f4fa;padding:3px}}</style><h1>SAE models and checkpoints</h1><p><a href="{html.escape(site_url,quote=True)}">Open the searchable web catalog</a></p><p><a href="{html.escape(markdown,quote=True)}">Browse the GitHub repository index</a></p><p>For a local checkout, run <code>python -m http.server 8000</code> in the repository root and open <a href="http://localhost:8000/docs/methods/sae/models/web/">the local catalog</a>. Model cards and search data are loaded on demand.</p></html>'''
    if output is None:
        (DESTINATION/'catalog.html').write_text(launcher+'\n')
    return {'index_html_bytes':len(document.encode()), 'search_index_bytes':(web/'catalog-index.json').stat().st_size,
            'detail_shards':len(shards),'largest_shard_bytes':max(p.stat().st_size for p in shards_path.glob('*.json'))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', help='GitHub owner/name for Markdown fallback links')
    parser.add_argument('--ref', help='Git ref containing the generated Markdown model cards')
    parser.add_argument('--site-url', help='Hosted searchable catalog URL for the small compatibility launcher')
    args = parser.parse_args()
    build(repository=args.repository, ref=args.ref, site_url=args.site_url)
