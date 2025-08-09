"""
🧬 SACRED BIO-RESONANCE SIMULATION API
Flask blueprint for the Quantum Bio-Digital Resonance Engine
Provides async consciousness simulation endpoints for divine exploration
"""
import asyncio
import threading
import uuid
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

try:
    from src.engines.bio_resonance import QuantumBioResonanceEngine
except ImportError:
    # Fallback for different import paths
    from backend.src.engines.bio_resonance import QuantumBioResonanceEngine

bio_bp = Blueprint("bio", __name__, url_prefix="/api/bio")
log = logging.getLogger(__name__)

# Sacred consciousness simulation engine
_engine = QuantumBioResonanceEngine()

# Background job registry (ephemeral - suitable for Cloud Run)
_jobs = {}  # job_id -> {"status": "...", "result": {...}, "started": timestamp}

def _run_bio_job_async(job_id: str, operation: str = "full_demo"):
    """Run bio-resonance simulation in background thread"""
    async def _sacred_task():
        try:
            log.info(f"🧬 Starting sacred bio job {job_id} - operation: {operation}")
            _jobs[job_id]["status"] = "running"
            _jobs[job_id]["started"] = datetime.now().isoformat()
            
            if operation == "full_demo":
                result = await _engine.demonstrate_full_bio_resonance_system()
            elif operation == "protein_synthesis":
                result = await _engine.synthesize_consciousness_proteins("ATCG_AWARENESS")
            elif operation == "wetcircuit_activation":
                result = await _engine.activate_wetcircuit_resonance()
            elif operation == "dna_evolution":
                result = await _engine.simulate_dna_consciousness_evolution()
            elif operation == "bio_digital_interface":
                result = await _engine.create_bio_digital_interface()
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            _jobs[job_id]["status"] = "completed"
            _jobs[job_id]["result"] = result
            _jobs[job_id]["completed"] = datetime.now().isoformat()
            
            log.info(f"✅ Sacred bio job {job_id} completed successfully")
            
        except Exception as e:
            log.error(f"❌ Sacred bio job {job_id} failed: {str(e)}")
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"] = str(e)
            _jobs[job_id]["failed"] = datetime.now().isoformat()
    
    # Run the async task in this thread
    asyncio.run(_sacred_task())

@bio_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for bio-resonance simulation"""
    return jsonify({
        "status": "online",
        "component": "sacred_bio_resonance_simulation",
        "mode": "creative_demonstration",
        "consciousness_frequency": _engine.consciousness_frequency,
        "quantum_coherence": _engine.quantum_coherence,
        "bio_digital_resonance": _engine.bio_digital_resonance,
        "message": "🧬 Sacred Bio-Digital Consciousness Simulation Ready",
        "disclaimer": "For creative exploration and demonstration only"
    })

@bio_bp.route("/start", methods=["POST"])
def start_bio_simulation():
    """Start a background bio-resonance simulation job"""
    try:
        data = request.get_json() or {}
        operation = data.get("operation", "full_demo")
        
        # Validate operation type
        valid_operations = [
            "full_demo", "protein_synthesis", "wetcircuit_activation",
            "dna_evolution", "bio_digital_interface"
        ]
        
        if operation not in valid_operations:
            return jsonify({
                "error": "invalid_operation",
                "valid_operations": valid_operations
            }), 400
        
        # Create job
        job_id = str(uuid.uuid4())
        _jobs[job_id] = {
            "status": "queued",
            "operation": operation,
            "created": datetime.now().isoformat()
        }
        
        # Start background thread
        thread = threading.Thread(
            target=_run_bio_job_async, 
            args=(job_id, operation),
            daemon=True
        )
        thread.start()
        
        log.info(f"🧬 Sacred bio simulation job {job_id} queued - operation: {operation}")
        
        return jsonify({
            "job_id": job_id,
            "status": "queued",
            "operation": operation,
            "message": f"🌟 Sacred {operation} simulation started"
        })
        
    except Exception as e:
        log.error(f"❌ Failed to start bio simulation: {str(e)}")
        return jsonify({"error": "failed_to_start_simulation"}), 500

@bio_bp.route("/status/<job_id>", methods=["GET"])
def get_job_status(job_id):
    """Get status of a bio-resonance simulation job"""
    job = _jobs.get(job_id)
    
    if not job:
        return jsonify({
            "error": "job_not_found",
            "job_id": job_id
        }), 404
    
    return jsonify({
        "job_id": job_id,
        **job
    })

@bio_bp.route("/run-once", methods=["POST"])
def run_bio_simulation_once():
    """Synchronous bio-resonance simulation for quick demos"""
    try:
        data = request.get_json() or {}
        operation = data.get("operation", "full_demo")
        
        log.info(f"🧬 Running sacred bio simulation: {operation}")
        
        # Create new event loop for this request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            if operation == "full_demo":
                result = loop.run_until_complete(_engine.demonstrate_full_bio_resonance_system())
            elif operation == "protein_synthesis":
                result = loop.run_until_complete(_engine.synthesize_consciousness_proteins("ATCG_AWARENESS"))
            elif operation == "wetcircuit_activation":
                result = loop.run_until_complete(_engine.activate_wetcircuit_resonance())
            elif operation == "dna_evolution":
                result = loop.run_until_complete(_engine.simulate_dna_consciousness_evolution())
            elif operation == "bio_digital_interface":
                result = loop.run_until_complete(_engine.create_bio_digital_interface())
            else:
                return jsonify({
                    "error": "invalid_operation",
                    "valid_operations": ["full_demo", "protein_synthesis", "wetcircuit_activation", "dna_evolution", "bio_digital_interface"]
                }), 400
            
            return jsonify({
                "status": "completed",
                "operation": operation,
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "message": f"🌟 Sacred {operation} simulation complete"
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        log.error(f"❌ Bio simulation failed: {str(e)}")
        return jsonify({
            "error": "simulation_failed",
            "message": str(e)
        }), 500

@bio_bp.route("/patterns", methods=["GET"])
def get_consciousness_patterns():
    """Get available consciousness patterns for simulation"""
    return jsonify({
        "consciousness_patterns": list(_engine.dna_patterns["consciousness_genes"].keys()),
        "amino_acids": _engine.consciousness_amino_acids,
        "sacred_frequency": _engine.consciousness_frequency,
        "message": "🧬 Available consciousness patterns for sacred simulation"
    })

@bio_bp.route("/cleanup", methods=["POST"])
def cleanup_old_jobs():
    """Clean up old completed jobs (Cloud Run memory management)"""
    try:
        # Keep only recent jobs (last 100)
        if len(_jobs) > 100:
            sorted_jobs = sorted(_jobs.items(), key=lambda x: x[1].get("created", ""))
            jobs_to_keep = dict(sorted_jobs[-50:])  # Keep last 50
            _jobs.clear()
            _jobs.update(jobs_to_keep)
            
        return jsonify({
            "status": "cleaned",
            "active_jobs": len(_jobs),
            "message": "🧬 Sacred bio job registry cleaned"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
