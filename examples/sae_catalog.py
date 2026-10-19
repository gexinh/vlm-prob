#!/usr/bin/env python3
"""Search SAE checkpoint metadata or export an offline, searchable catalog."""
import argparse
import html
import json
from pathlib import Path

from vlmprobe.sae import catalog_provenance, list_pretrained


def export_html(path):
    entries = list_pretrained()
    payload = json.dumps(entries, ensure_ascii=False).replace("<", "\\u003c")
    provenance = html.escape(json.dumps(catalog_provenance(), indent=2))
    template = """<!doctype html><meta charset="utf-8"><title>VLMProbe SAE catalog</title>
<style>body{max-width:1450px;margin:36px auto;padding:20px;font:15px/1.5 system-ui;color:#18374f;background:#f6f9fc}h1{font-size:34px}input,select,button{font:inherit;padding:9px;margin:6px;border:1px solid #ccd6e1;border-radius:5px}input{width:44%}table{border-collapse:collapse;background:white;width:100%}td,th{text-align:left;padding:10px 12px;border-bottom:1px solid #e2e8f0;vertical-align:top}th{background:#eaf0f9}td{overflow-wrap:anywhere}a{color:#147d91}.muted{color:#566c7c}pre{white-space:pre-wrap}.controls{position:sticky;top:0;background:#f6f9fc;padding:8px 0}</style>
<h1>Explore SAE resources across language and vision</h1>
<p>Search the versioned SAELens and ViT-Prisma metadata catalogs. Overcomplete provides dictionary training and probing tools; it does not publish a central SAE checkpoint registry.</p>
<p class="muted">Entries are upstream listings, not validated transfers to an arbitrary backbone. Transcoders, temporal methods and legacy formats are marked separately. Exact model, hook, normalization and preprocessing binding is required before probing.</p>
<div class="controls"><select id="backend"><option value="">All providers</option><option>saelens</option><option>prisma</option></select>
<input id="query" placeholder="Search model, release, hook or architecture"><label><input type="checkbox" id="saes" style="width:auto">Independent SAE candidates only</label>
<div><span id="count"></span> <button id="previous">Previous</button><button id="next">Next</button><span id="page"></span></div></div>
<table><thead><tr><th>Provider / resource</th><th>Model</th><th>Hook / architecture</th><th>Scope</th><th>Primary source</th></tr></thead><tbody id="rows"></tbody></table>
<details><summary>Catalog provenance</summary><pre>PROVENANCE</pre></details>
<script>const entries=PAYLOAD;let page=0;const size=80;const $=id=>document.getElementById(id);const escape=s=>String(s??'unknown').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function render(){const q=$('query').value.toLowerCase(),backend=$('backend').value;const filtered=entries.filter(r=>(!backend||r.backend===backend)&&(!$('saes').checked||(r.resource_kind==='sae'&&r.adapter_compatible!==false))&&(!q||JSON.stringify(r).toLowerCase().includes(q)));page=Math.max(0,Math.min(page,Math.max(0,Math.ceil(filtered.length/size)-1)));$('count').textContent=filtered.length+' resources';$('page').textContent='Page '+(page+1)+' / '+Math.max(1,Math.ceil(filtered.length/size));$('rows').innerHTML=filtered.slice(page*size,(page+1)*size).map(r=>`<tr><td><b>${escape(r.backend)}</b><br>${escape(r.release)}<br><small>${escape(r.sae_id)}</small></td><td>${escape(r.model)}</td><td>${escape(r.hook)}<br>${escape(r.architecture)}</td><td>${escape(r.resource_kind)}<br>${r.adapter_compatible===false?'Different activation/context contract':escape(r.loading||'Requires configuration validation')}<br><small>${escape(r.verification)}</small></td><td><a href="${escape(r.source_url)}" target="_blank" rel="noopener">Author checkpoint</a></td></tr>`).join('');}
for(const id of ['query','backend','saes'])$(id).addEventListener('input',()=>{page=0;render()});$('previous').onclick=()=>{page--;render()};$('next').onclick=()=>{page++;render()};render();</script>"""
    document = template.replace("PROVENANCE", provenance).replace("PAYLOAD", payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document)
    print(json.dumps({"html": str(path), "entries": len(entries)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["saelens", "prisma", "overcomplete"])
    parser.add_argument("--model")
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()
    if args.html:
        export_html(args.html)
    else:
        print(json.dumps(list_pretrained(args.backend, model=args.model, query=args.query,
                                        limit=args.limit), indent=2, ensure_ascii=False))
