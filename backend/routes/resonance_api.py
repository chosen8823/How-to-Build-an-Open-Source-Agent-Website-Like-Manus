#!/usr/bin/env python3
"""
⚡ RESONANCE PROTOCOL API ROUTES
Flask API endpoints for intelligent AI query routing
Connects Tampermonkey script → Python router → C++ proxy
"""

import logging
from flask import Blueprint, request, jsonify
from datetime import datetime
from typing import Optional
import asyncio

logger = logging.getLogger(__name__)

# Create blueprint
resonance_bp = Blueprint('resonance', __name__, url_prefix='/api/resonance')

# Global router instance (will be set when blueprint is registered)
_router = None


def register_resonance_routes(app, nemo_path: Optional[str] = None):
    """
    Register Resonance Protocol routes with Flask app

    Args:
        app: Flask application
        nemo_path: Path to NVIDIA NeMo model in SPI directory
    """
    global _router

    try:
        from integrations.resonance_protocol import (
            get_resonance_router,
            NeMoLocalHandler,
            ModelEndpoint
        )

        # Initialize router
        _router = get_resonance_router(nemo_path)

        # Register local NeMo handler if path provided
        if nemo_path:
            nemo_handler = NeMoLocalHandler(nemo_path)
            _router.register_endpoint(
                ModelEndpoint.LOCAL_NEMO,
                nemo_handler,
                cost_per_query=0.0  # Free!
            )
            logger.info(f"✅ NeMo handler registered: {nemo_path}")

        # Register ChatGPT web session handler if available
        try:
            from integrations.chatgpt_session import ChatGPTSession

            async def chatgpt_handler(query: str, context: dict = None):
                """Handler for ChatGPT web session"""
                session = ChatGPTSession()
                response = session.send_message(query)
                return response

            _router.register_endpoint(
                ModelEndpoint.CHATGPT_WEB,
                chatgpt_handler,
                cost_per_query=0.0  # Web session, not API
            )
            logger.info("✅ ChatGPT web session handler registered")

        except Exception as e:
            logger.warning(f"ChatGPT handler not available: {e}")

        # Register blueprint
        app.register_blueprint(resonance_bp)
        logger.info("⚡ Resonance Protocol API routes registered")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to register Resonance routes: {e}")
        return False


@resonance_bp.route('/query', methods=['POST'])
def route_query():
    """
    ⚡ MAIN ENDPOINT: Route AI query through Resonance Protocol

    This is what the Tampermonkey script calls

    Request body:
    {
        "query": "User's question",
        "context": {"source": "chatgpt", "conversation_id": "..."},
        "force_endpoint": "local_nemo" (optional)
    }

    Response:
    {
        "success": true,
        "message": "AI response",
        "metadata": {
            "endpoint": "local_nemo",
            "query_type": "simple_qa",
            "processing_time_ms": 150,
            "cost": 0.0
        }
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        data = request.get_json()
        query = data.get('query', '')
        context = data.get('context', {})
        force_endpoint = data.get('force_endpoint', None)

        if not query:
            return jsonify({
                "success": False,
                "error": "Missing 'query' parameter"
            }), 400

        # Convert force_endpoint string to enum if provided
        endpoint_enum = None
        if force_endpoint:
            from integrations.resonance_protocol import ModelEndpoint
            try:
                endpoint_enum = ModelEndpoint(force_endpoint)
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": f"Invalid endpoint: {force_endpoint}"
                }), 400

        # Process query through router (async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            _router.process_query(query, context, endpoint_enum)
        )
        loop.close()

        return jsonify(response)

    except Exception as e:
        logger.error(f"Query routing error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    📊 Get routing statistics

    Response:
    {
        "total_queries": 1234,
        "local_queries": 1000,
        "cloud_queries": 234,
        "local_percentage": 81.04,
        "total_cost_saved_usd": 2.468,
        "avg_cost_saved_per_query": 0.002,
        "endpoints": {
            "local_nemo": {
                "total_queries": 1000,
                "successful_queries": 985,
                "success_rate": 98.5
            }
        }
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        stats = _router.get_statistics()

        return jsonify({
            "success": True,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Statistics error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/configure', methods=['POST'])
def configure():
    """
    ⚙️ Configure Resonance Protocol

    Request body:
    {
        "nemo_path": "/path/to/SPI/nemo_model",
        "endpoints": {
            "local_nemo": {
                "enabled": true,
                "cost": 0.0
            },
            "chatgpt_web": {
                "enabled": true,
                "cost": 0.0
            }
        }
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        data = request.get_json()
        nemo_path = data.get('nemo_path')

        # Update NeMo path if provided
        if nemo_path:
            from integrations.resonance_protocol import NeMoLocalHandler, ModelEndpoint

            # Remove old NeMo handler
            if ModelEndpoint.LOCAL_NEMO in _router.endpoints:
                del _router.endpoints[ModelEndpoint.LOCAL_NEMO]

            # Register new NeMo handler
            nemo_handler = NeMoLocalHandler(nemo_path)
            _router.register_endpoint(
                ModelEndpoint.LOCAL_NEMO,
                nemo_handler,
                cost_per_query=0.0
            )

            _router.nemo_path = nemo_path
            logger.info(f"✅ NeMo path updated: {nemo_path}")

        return jsonify({
            "success": True,
            "message": "Configuration updated",
            "nemo_path": _router.nemo_path if _router else None,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Configuration error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/health', methods=['GET'])
def health_check():
    """
    🏥 Health check endpoint

    Response:
    {
        "status": "healthy",
        "router_initialized": true,
        "endpoints_registered": ["local_nemo", "chatgpt_web"],
        "nemo_path": "/path/to/SPI/nemo_model",
        "total_queries_processed": 1234
    }
    """
    try:
        if _router is None:
            return jsonify({
                "status": "unhealthy",
                "router_initialized": False,
                "error": "Router not initialized"
            }), 503

        from integrations.resonance_protocol import ModelEndpoint

        return jsonify({
            "status": "healthy",
            "router_initialized": True,
            "endpoints_registered": [ep.value for ep in _router.endpoints.keys()],
            "nemo_path": _router.nemo_path,
            "total_queries_processed": _router.stats["total_queries"],
            "cost_saved_usd": _router.stats["cost_saved"],
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@resonance_bp.route('/classify', methods=['POST'])
def classify_query():
    """
    🔍 Classify query type without processing

    Useful for testing/debugging routing decisions

    Request body:
    {
        "query": "What is Python?"
    }

    Response:
    {
        "query": "What is Python?",
        "query_type": "simple_qa",
        "recommended_endpoint": "local_nemo",
        "reasoning": "Short factual question, ideal for local model"
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        data = request.get_json()
        query = data.get('query', '')

        if not query:
            return jsonify({
                "success": False,
                "error": "Missing 'query' parameter"
            }), 400

        # Classify query
        query_type = _router.classify_query(query)
        recommended_endpoint = _router.route_query(query)

        # Generate reasoning
        reasoning_map = {
            "simple_qa": "Short factual question, ideal for local model",
            "code": "Code generation task, local NeMo handles well",
            "factual": "Factual query, can be answered locally",
            "conversation": "Conversational query, local model sufficient",
            "complex": "Complex reasoning required, using ChatGPT",
            "creative": "Creative writing task, using ChatGPT"
        }

        return jsonify({
            "success": True,
            "query": query,
            "query_type": query_type.value,
            "recommended_endpoint": recommended_endpoint.value,
            "reasoning": reasoning_map.get(query_type.value, "Default routing"),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/history', methods=['GET'])
def get_history():
    """
    📜 Get query history

    Query params:
    - limit: Number of recent queries to return (default: 100)
    - offset: Offset for pagination (default: 0)

    Response:
    {
        "success": true,
        "history": [
            {
                "query": "What is Python?",
                "endpoint": "local_nemo",
                "success": true,
                "timestamp": "2025-01-22T10:30:00"
            }
        ],
        "total": 1234,
        "limit": 100,
        "offset": 0
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Get history slice
        total = len(_router.query_history)
        history_slice = _router.query_history[offset:offset + limit]

        return jsonify({
            "success": True,
            "history": history_slice,
            "total": total,
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/test', methods=['POST'])
def test_endpoint():
    """
    🧪 Test specific endpoint directly

    Request body:
    {
        "endpoint": "local_nemo",
        "query": "Test query"
    }
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        data = request.get_json()
        endpoint_str = data.get('endpoint', '')
        query = data.get('query', 'Test query')

        from integrations.resonance_protocol import ModelEndpoint

        try:
            endpoint = ModelEndpoint(endpoint_str)
        except ValueError:
            return jsonify({
                "success": False,
                "error": f"Invalid endpoint: {endpoint_str}",
                "available_endpoints": [ep.value for ep in ModelEndpoint]
            }), 400

        if endpoint not in _router.endpoints:
            return jsonify({
                "success": False,
                "error": f"Endpoint not registered: {endpoint_str}",
                "registered_endpoints": [ep.value for ep in _router.endpoints.keys()]
            }), 400

        # Test endpoint
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            _router.process_query(query, {}, endpoint)
        )
        loop.close()

        return jsonify({
            "success": True,
            "test_result": response,
            "endpoint_tested": endpoint_str,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Endpoint test error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@resonance_bp.route('/reset-stats', methods=['POST'])
def reset_statistics():
    """
    🔄 Reset routing statistics

    Useful for testing or starting fresh
    """
    try:
        if _router is None:
            return jsonify({
                "success": False,
                "error": "Resonance Protocol not initialized"
            }), 503

        # Reset stats
        _router.stats = {
            "total_queries": 0,
            "local_queries": 0,
            "cloud_queries": 0,
            "cost_saved": 0.0
        }

        # Reset endpoint stats
        for endpoint in _router.endpoints.values():
            endpoint["total_queries"] = 0
            endpoint["successful_queries"] = 0

        # Clear history
        _router.query_history.clear()

        logger.info("📊 Statistics reset")

        return jsonify({
            "success": True,
            "message": "Statistics reset successfully",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
