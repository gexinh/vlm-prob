"""Local PyTorch hook containers used by the selected SAE arithmetic.

These replace TransformerLens containers without importing a transformer stack.
Named modules are ordinary PyTorch identity points. TransformerLens cache,
context-manager and HookedTransformer APIs are intentionally outside this core.
"""
from torch import nn


class HookPoint(nn.Module):
    def forward(self, value):
        return value


class HookedRootModule(nn.Module):
    def setup(self):
        self.mod_dict = dict(self.named_modules())
        self.hook_dict = {name: module for name, module in self.named_modules()
                          if isinstance(module, HookPoint)}
