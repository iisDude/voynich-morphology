"""Prevent stage writers from overwriting inputs included in the V3 freeze."""
def require_unfrozen(root):
    if (root/'INPUTS_IMMUTABLE_V3.json').exists():
        raise RuntimeError('These source/model inputs belong to immutable V3. Reproduce into a new development directory; do not overwrite them.')
