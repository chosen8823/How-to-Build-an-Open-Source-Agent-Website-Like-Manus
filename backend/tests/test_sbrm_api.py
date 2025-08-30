import json
from datetime import datetime


def test_sbrm_health(client):
    res = client.get('/api/sbrm/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'online'
    assert 'component' in data and data['component'] == 'sbrm_orchestrator'


def test_sbrm_phase_activation(client):
    # Invalid
    res = client.post('/api/sbrm/phase', json={'phase': 0})
    assert res.status_code == 400

    # Activate phase 1
    res = client.post('/api/sbrm/phase', json={'phase': 1})
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'activated'
    assert data['phase'] == 1
    assert data['activated_gpus'] == 1

    # Status reflects
    res = client.get('/api/sbrm/status')
    assert res.status_code == 200
    s = res.get_json()
    assert s['phase'] == 1
    assert s['activated_gpus'] == 1


def test_sbrm_telemetry(client):
    # Simulate telemetry
    res = client.post('/api/sbrm/telemetry/GPU-1', json={'intensity': 0.7})
    assert res.status_code == 200
    t = res.get_json()
    for k in ['emf_microtesla', 'cryo_temp_c', 'photon_cps', 'coherence', 'timestamp']:
        assert k in t

    # Fetch last telemetry
    res = client.get('/api/sbrm/telemetry/GPU-1')
    assert res.status_code == 200