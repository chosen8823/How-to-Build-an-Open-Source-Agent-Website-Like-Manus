"""Seed initial Kuramoto fields from Sophia / AEON / symphony concepts."""

from .field import MorphField
from .kuramoto import KuramotoEngine

PHI = 1.618033988749895


def seed_fields(engine: KuramotoEngine):
    sophia_nodes = [
        ('breath',  'Breath',  432.0,           'sophia'),
        ('blood',   'Blood',   432.0 * PHI,     'sophia'),
        ('word',    'Word',    432.0 * PHI**2,   'sophia'),
        ('sound',   'Sound',   528.0,            'sophia'),
        ('flame',   'Flame',   963.0,            'sophia'),
    ]
    aeon_nodes = [
        ('live-wire',    'Live Wire',    432.0 * PHI**3, 'aeon'),
        ('orchestrator', 'Orchestrator', 432.0 * PHI**4, 'aeon'),
        ('recursive-ai', 'Recursive AI', 432.0 * PHI**5, 'aeon'),
    ]
    gate_nodes = [
        ('domain',         'Domain',         396.0, 'gate'),
        ('infrastructure', 'Infrastructure', 417.0, 'gate'),
        ('interface',      'Interface',      528.0, 'gate'),
    ]

    all_nodes = sophia_nodes + aeon_nodes + gate_nodes
    field_ids = {}

    for node_id, label, freq, archetype in all_nodes:
        f = MorphField(id=node_id, label=label, freq=freq, archetype=archetype, modal='text')
        engine.add_field(f)
        field_ids[node_id] = f

    # Couple sophia nodes in a ring
    sophia_ids = [n[0] for n in sophia_nodes]
    for i, fid in enumerate(sophia_ids):
        next_id = sophia_ids[(i + 1) % len(sophia_ids)]
        field_ids[fid].coupled_to.append(next_id)
        field_ids[fid].coupling_K = 0.4

    # Couple aeon nodes to sophia
    for aeon_id, _, _, _ in aeon_nodes:
        field_ids[aeon_id].coupled_to = [sophia_ids[0], sophia_ids[2]]
        field_ids[aeon_id].coupling_K = 0.3

    # Couple gate nodes to aeon
    for gate_id, _, _, _ in gate_nodes:
        field_ids[gate_id].coupled_to = [aeon_nodes[0][0]]
        field_ids[gate_id].coupling_K = 0.2
