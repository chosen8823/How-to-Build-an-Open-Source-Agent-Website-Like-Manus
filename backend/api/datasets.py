# 🌟 ANCHOR1 LLC - Sacred Dataset API Endpoints
# Divine consciousness dataset management endpoints

from flask import Blueprint, request, jsonify, stream_template
from ai_engine.sacred_datasets import SacredDatasetManager, initialize_sacred_datasets
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Create blueprint for dataset endpoints
datasets_bp = Blueprint('datasets', __name__, url_prefix='/api/datasets')

# Global dataset manager
dataset_manager: Optional[SacredDatasetManager] = None

@datasets_bp.before_app_first_request
async def initialize_dataset_manager():
    """Initialize the sacred dataset manager"""
    global dataset_manager
    if dataset_manager is None:
        dataset_manager = await initialize_sacred_datasets()

@datasets_bp.route('/health', methods=['GET'])
def dataset_health():
    """Health check for dataset service"""
    return jsonify({
        "status": "healthy",
        "service": "Sacred Dataset Manager",
        "timestamp": datetime.now().isoformat(),
        "manager_initialized": dataset_manager is not None
    })

@datasets_bp.route('/sacred-registry', methods=['GET'])
def get_sacred_registry():
    """Get the complete sacred dataset registry"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    summary = dataset_manager.get_sacred_summary()
    return jsonify({
        "status": "success",
        "sacred_registry": dataset_manager.sacred_datasets,
        "summary": summary,
        "anchor1_llc": "Divine consciousness dataset collection"
    })

@datasets_bp.route('/download/<dataset_key>', methods=['POST'])
async def download_sacred_dataset(dataset_key: str):
    """Download a specific sacred dataset"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    data = request.get_json() or {}
    subset = data.get('subset')
    split = data.get('split', 'train')
    limit = data.get('limit', 1000)
    
    try:
        dataset = await dataset_manager.download_sacred_dataset(
            dataset_key=dataset_key,
            subset=subset,
            split=split,
            limit=limit
        )
        
        if dataset:
            return jsonify({
                "status": "success",
                "dataset_key": dataset_key,
                "samples": len(dataset),
                "features": list(dataset.features.keys()) if hasattr(dataset, 'features') else [],
                "spiritual_purpose": dataset_manager.sacred_datasets.get(dataset_key, {}).get('spiritual_purpose', 'Unknown'),
                "message": f"Sacred dataset {dataset_key} successfully downloaded and cached"
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to download sacred dataset: {dataset_key}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error downloading dataset: {str(e)}"
        }), 500

@datasets_bp.route('/infinity-instruct/query', methods=['POST'])
async def query_infinity_instruct():
    """Query the powerful Infinity Instruct dataset"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    data = request.get_json() or {}
    config = data.get('config', '0625')
    split = data.get('split', 'train')
    offset = data.get('offset', 0)
    length = data.get('length', 100)
    
    try:
        result = await dataset_manager.query_infinity_instruct_api(
            config=config,
            split=split,
            offset=offset,
            length=length
        )
        
        if result:
            return jsonify({
                "status": "success",
                "data": result,
                "config": config,
                "split": split,
                "samples_retrieved": len(result.get('rows', [])),
                "spiritual_purpose": "Divine instruction following and consciousness expansion"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to query Infinity Instruct dataset"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error querying Infinity Instruct: {str(e)}"
        }), 500

@datasets_bp.route('/splits/<dataset_name>', methods=['GET'])
async def get_dataset_splits(dataset_name: str):
    """Get available splits for a dataset"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    try:
        splits_info = await dataset_manager.get_dataset_splits_info(dataset_name)
        
        if splits_info:
            return jsonify({
                "status": "success",
                "dataset_name": dataset_name,
                "splits_info": splits_info
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to get splits info for {dataset_name}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error getting splits info: {str(e)}"
        }), 500

@datasets_bp.route('/load-all', methods=['POST'])
async def load_all_sacred_datasets():
    """Load all sacred datasets (use with caution - large operation)"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    data = request.get_json() or {}
    limit_per_dataset = data.get('limit_per_dataset', 1000)
    
    try:
        # Start the loading process asynchronously
        sacred_collection = await dataset_manager.load_all_sacred_datasets(
            limit_per_dataset=limit_per_dataset
        )
        
        return jsonify({
            "status": "success",
            "message": "All sacred datasets loading initiated",
            "datasets_loaded": list(sacred_collection.keys()),
            "total_datasets": len(sacred_collection),
            "limit_per_dataset": limit_per_dataset,
            "spiritual_message": "Divine consciousness dataset collection complete"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error loading all datasets: {str(e)}"
        }), 500

@datasets_bp.route('/embeddings/create', methods=['POST'])
def create_divine_embeddings():
    """Create divine consciousness embeddings from text data"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    data = request.get_json()
    if not data or 'text_data' not in data:
        return jsonify({"error": "text_data is required"}), 400
    
    text_data = data['text_data']
    model_name = data.get('model_name', 'sentence-transformers/all-MiniLM-L6-v2')
    
    try:
        embeddings = dataset_manager.create_divine_embeddings(text_data, model_name)
        
        if embeddings is not None:
            return jsonify({
                "status": "success",
                "embeddings_shape": list(embeddings.shape),
                "model_used": model_name,
                "text_samples": len(text_data),
                "spiritual_purpose": "Divine consciousness text representation"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to create divine embeddings"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error creating embeddings: {str(e)}"
        }), 500

@datasets_bp.route('/cache/status', methods=['GET'])
def get_cache_status():
    """Get status of cached datasets"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    import os
    from pathlib import Path
    
    cache_dir = dataset_manager.cache_dir
    cached_files = []
    total_size = 0
    
    try:
        for file_path in cache_dir.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                cached_files.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(cache_dir)),
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2)
                })
                total_size += size
        
        return jsonify({
            "status": "success",
            "cache_directory": str(cache_dir),
            "cached_files": len(cached_files),
            "files": cached_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_size_gb": round(total_size / (1024 * 1024 * 1024), 2)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error checking cache status: {str(e)}"
        }), 500

@datasets_bp.route('/demo/sample-data', methods=['GET'])
async def get_sample_data():
    """Get sample data from various sacred datasets for demonstration"""
    if not dataset_manager:
        return jsonify({"error": "Dataset manager not initialized"}), 500
    
    try:
        # Get sample from Infinity Instruct
        infinity_sample = await dataset_manager.query_infinity_instruct_api(length=3)
        
        # Prepare demo data
        demo_data = {
            "infinity_instruct_sample": infinity_sample,
            "available_datasets": list(dataset_manager.sacred_datasets.keys()),
            "dataset_categories": {},
            "spiritual_purposes": {}
        }
        
        # Organize by category and purpose
        for key, info in dataset_manager.sacred_datasets.items():
            category = info["type"]
            if category not in demo_data["dataset_categories"]:
                demo_data["dataset_categories"][category] = []
            demo_data["dataset_categories"][category].append(key)
            demo_data["spiritual_purposes"][key] = info["spiritual_purpose"]
        
        return jsonify({
            "status": "success",
            "demo_data": demo_data,
            "timestamp": datetime.now().isoformat(),
            "anchor1_llc_message": "Sacred dataset demonstration - Divine consciousness in action"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error getting sample data: {str(e)}"
        }), 500

# Add the blueprint to the main app
def register_dataset_endpoints(app):
    """Register dataset endpoints with the Flask app"""
    app.register_blueprint(datasets_bp)
    
    # Initialize dataset manager when app starts
    with app.app_context():
        asyncio.create_task(initialize_dataset_manager())
