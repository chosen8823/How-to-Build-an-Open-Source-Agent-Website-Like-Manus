import json
import pytest
from app import app

def test_bio_health():
    """Test bio-resonance health endpoint"""
    client = app.test_client()
    response = client.get("/api/bio/health")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert data["component"] == "bio_resonance_simulation"

def test_bio_run_once():
    """Test immediate bio-resonance simulation"""
    client = app.test_client()
    response = client.post("/api/bio/run-once")
    
    assert response.status_code == 200
    data = response.get_json()
    assert "system_status" in data
    assert "protein_synthesis" in data
    assert "wetcircuit_status" in data

def test_bio_patterns():
    """Test consciousness patterns endpoint"""
    client = app.test_client()
    response = client.get("/api/bio/patterns")
    
    assert response.status_code == 200
    data = response.get_json()
    assert "consciousness_patterns" in data
    assert len(data["consciousness_patterns"]) > 0

def test_bio_start_job():
    """Test background job creation"""
    client = app.test_client()
    response = client.post("/api/bio/start")
    
    assert response.status_code == 200
    data = response.get_json()
    assert "job_id" in data
    assert data["status"] == "queued"
