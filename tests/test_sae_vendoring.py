"""Bundled cores must not depend on an installed official SAE toolkit."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from vlmprobe.sae import list_backends, list_pretrained


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "src/vlm_probing/_vendor"
FORBIDDEN = {"sae_lens", "vit_prisma", "overcomplete", "transformer_lens"}


def test_production_sae_source_never_imports_official_toolkits():
    trees = [ROOT / "src/vlm_probing/sae"] + [VENDOR / name for name in ("saelens", "prisma", "overcomplete")]
    for directory in trees:
        for path in directory.rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
                imports = []
                if isinstance(node, ast.Import):
                    imports = [item.name for item in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    imports = [node.module or ""]
                elif isinstance(node, ast.Call) and node.args:
                    name = getattr(node.func, "id", getattr(node.func, "attr", ""))
                    if name in {"import_module", "__import__"} and isinstance(node.args[0], ast.Constant):
                        imports = [node.args[0].value]
                assert all(str(name).split(".")[0] not in FORBIDDEN for name in imports), (path, imports)


def test_discovery_uses_bundled_cores_and_pinned_registry():
    for item in list_backends():
        assert item["core_bundled"] is True
        assert item["external_package_required"] is False
    rows = list_pretrained("saelens", source="bundled", release="gpt2-small-res-jb-feature-splitting")
    assert rows
    assert rows == list_pretrained("saelens", source="installed", release="gpt2-small-res-jb-feature-splitting")


@pytest.mark.parametrize("provider,manifest", [
    ("saelens", "PROVENANCE.json"), ("prisma", "SOURCE.json"),
    ("overcomplete", "VENDOR_MANIFEST.json"),
])
def test_vendored_source_hashes_and_original_licenses(provider, manifest):
    directory = VENDOR / provider
    assert "MIT License" in (directory / "LICENSE").read_text()
    data = json.loads((directory / manifest).read_text())
    commit = data.get("source_commit", data.get("upstream_commit", data.get("commit")))
    assert isinstance(commit, str) and len(commit) == 40
    files = {}
    for row in data["files"]:
        target = row.get("target", row.get("local_path", row.get("path")))
        digest = row.get("vendored_sha256", row.get("local_sha256"))
        files[target] = digest
    files.update(data.get("local_files", {}))
    assert files
    for filename, digest in files.items():
        assert hashlib.sha256((directory / filename).read_bytes()).hexdigest() == digest, filename


def test_bundled_numerics_work_when_official_packages_are_blocked():
    # A finder raises even if an official toolkit is installed in the host
    # environment. Run in a fresh process to exclude cached module imports.
    script = r'''
import importlib.abc, sys
blocked = {'sae_lens', 'vit_prisma', 'overcomplete', 'transformer_lens'}
class NoOfficialToolkit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('unexpected official package import: ' + fullname)
sys.meta_path.insert(0, NoOfficialToolkit())
import torch
from vlmprobe.sae.backends import saelens, prisma, overcomplete
binding = {'model_id':'vectors@seed0', 'tokenizer_id':'none', 'preprocessing_id':'identity',
    'calibration_id':'independent', 'site':'residual.0', 'layer':0,
    'hook':{'module':'blocks.0','kind':'output','selector':None,'tensor_slice':None}}
x=torch.randn(6,8)
native=saelens.create_training_sae(architecture='topk',d_in=8,d_sae=16,k=3,
    normalize_activations='none',device='cpu')
a=saelens.wrap(native,binding=binding)
assert a.decode(a.encode(x)).shape == x.shape
b=overcomplete.create('topk',d_in=8,d_sae=16,top_k=3,binding=binding,device='cpu')
b.is_fitted=True
b.eval()
assert b.decode(b.encode(x)).shape == x.shape
from vlm_probing._vendor.prisma.sae import StandardSparseAutoencoder
cfg=prisma.VisionModelSAERunnerConfig(d_in=8,expansion_factor=2,model_name='vectors',
    hook_point_layer=0,layer_subtype='hook_resid_post',normalize_activations=None,
    _device='cpu',log_to_wandb=False,activation_fn_str='relu')
vision_binding={**binding,'backend_model_name':'vectors',
    'site':'blocks.0.hook_resid_post','backend_hook_name':'blocks.0.hook_resid_post',
    'hook':{**binding['hook'],'module':'blocks.0.hook_resid_post'}}
c=prisma.wrap(StandardSparseAutoencoder(cfg),binding=vision_binding)
features,ctx=c.encode_with_context(x)
assert c.decode_with_context(features,ctx).shape == x.shape
assert not blocked.intersection(sys.modules)
print('three bundled cores work without official toolkits')
'''
    completed = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, timeout=60)
    assert completed.returncode == 0, completed.stderr
