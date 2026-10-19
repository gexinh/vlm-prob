"""Argument-order adapter from fancy_einsum to generic einops.einsum."""
import einops

def einsum(pattern, *tensors):
    return einops.einsum(*tensors, pattern)
