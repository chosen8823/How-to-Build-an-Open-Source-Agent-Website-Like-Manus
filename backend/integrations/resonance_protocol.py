#!/usr/bin/env python3
"""
⚡ RESONANCE PROTOCOL - Intelligent AI Query Router
Intercepts AI queries and routes to optimal endpoint:
- Local NVIDIA NeMo (free, fast)
- ChatGPT web (when needed)
- Claude, Gemini, etc.

Zero API costs - uses local models + web sessions
"""

import logging
from typing import Dict, Optional, List, Callable
from datetime import datetime
import json
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of AI queries for routing decisions"""
    SIMPLE_QA = "simple_qa"           # Simple questions - use local
    COMPLEX_REASONING = "complex"     # Complex reasoning - use ChatGPT
    CODE_GENERATION = "code"          # Code - use local NeMo
    CREATIVE_WRITING = "creative"     # Creative - use ChatGPT
    FACTUAL = "factual"               # Facts - use local
    CONVERSATION = "conversation"     # Chat - use local first
    SPECIALIZED = "specialized"       # Domain-specific - route intelligently


class ModelEndpoint(Enum):
    """Available AI endpoints"""
    LOCAL_NEMO = "local_nemo"
    CHATGPT_WEB = "chatgpt_web"
    CLAUDE_WEB = "claude_web"
    GEMINI_WEB = "gemini_web"
    HUGGINGFACE_LOCAL = "hf_local"


class ResonanceRouter:
    """
    Intelligent AI query router
    Decides where to send each query to minimize costs
    """

    def __init__(self, nemo_path: Optional[str] = None):
        """
        Initialize Resonance Router

        Args:
            nemo_path: Path to NVIDIA NeMo model (e.g., SPI directory)
        """
        self.nemo_path = nemo_path or "/path/to/SPI/nemo_model"

        # Available endpoints
        self.endpoints = {}

        # Query history for learning routing decisions
        self.query_history = []

        # Routing statistics
        self.stats = {
            "total_queries": 0,
            "local_queries": 0,
            "cloud_queries": 0,
            "cost_saved": 0.0
        }

        logger.info("⚡ Resonance Protocol initialized")

    def register_endpoint(self,
                         endpoint_type: ModelEndpoint,
                         handler: Callable,
                         cost_per_query: float = 0.0):
        """
        Register an AI endpoint

        Args:
            endpoint_type: Type of endpoint
            handler: Function to call for this endpoint
            cost_per_query: Cost per query (USD)
        """
        self.endpoints[endpoint_type] = {
            "handler": handler,
            "cost": cost_per_query,
            "total_queries": 0,
            "successful_queries": 0
        }
        logger.info(f"✅ Registered endpoint: {endpoint_type.value} (${cost_per_query}/query)")

    def classify_query(self, query: str) -> QueryType:
        """
        Classify query type to make routing decision

        Args:
            query: User's query

        Returns:
            Query type classification
        """
        query_lower = query.lower()

        # Code generation indicators
        code_keywords = ['write code', 'function', 'class', 'def ', 'import', 'script', 'python', 'javascript']
        if any(keyword in query_lower for keyword in code_keywords):
            return QueryType.CODE_GENERATION

        # Complex reasoning indicators
        complex_keywords = ['analyze', 'compare', 'evaluate', 'reason', 'argue', 'philosophy', 'ethics']
        if any(keyword in query_lower for keyword in complex_keywords):
            return QueryType.COMPLEX_REASONING

        # Creative writing indicators
        creative_keywords = ['write a story', 'poem', 'creative', 'imagine', 'story about']
        if any(keyword in query_lower for keyword in creative_keywords):
            return QueryType.CREATIVE_WRITING

        # Factual query indicators
        factual_keywords = ['what is', 'who is', 'when did', 'where is', 'how many', 'define']
        if any(keyword in query_lower for keyword in factual_keywords):
            return QueryType.FACTUAL

        # Simple Q&A
        if len(query.split()) < 15 and query.endswith('?'):
            return QueryType.SIMPLE_QA

        # Default to conversation
        return QueryType.CONVERSATION

    def route_query(self, query: str, force_endpoint: Optional[ModelEndpoint] = None) -> ModelEndpoint:
        """
        Decide which endpoint to route query to

        Args:
            query: User's query
            force_endpoint: Force specific endpoint (optional)

        Returns:
            Selected endpoint
        """
        if force_endpoint:
            return force_endpoint

        # Classify query
        query_type = self.classify_query(query)

        # Routing logic
        routing_rules = {
            QueryType.SIMPLE_QA: ModelEndpoint.LOCAL_NEMO,
            QueryType.CODE_GENERATION: ModelEndpoint.LOCAL_NEMO,  # NeMo good at code
            QueryType.FACTUAL: ModelEndpoint.LOCAL_NEMO,
            QueryType.CONVERSATION: ModelEndpoint.LOCAL_NEMO,
            QueryType.COMPLEX_REASONING: ModelEndpoint.CHATGPT_WEB,
            QueryType.CREATIVE_WRITING: ModelEndpoint.CHATGPT_WEB,
            QueryType.SPECIALIZED: ModelEndpoint.LOCAL_NEMO  # Try local first
        }

        selected = routing_rules.get(query_type, ModelEndpoint.LOCAL_NEMO)

        logger.info(f"📊 Query classified as: {query_type.value} → Routing to: {selected.value}")
        return selected

    async def process_query(self,
                           query: str,
                           context: Optional[Dict] = None,
                           force_endpoint: Optional[ModelEndpoint] = None) -> Dict:
        """
        Process query through Resonance Protocol

        Args:
            query: User's query
            context: Additional context
            force_endpoint: Force specific endpoint

        Returns:
            Response with metadata
        """
        self.stats["total_queries"] += 1
        start_time = datetime.now()

        # Route query
        endpoint = self.route_query(query, force_endpoint)

        # Get handler
        if endpoint not in self.endpoints:
            return {
                "success": False,
                "error": f"Endpoint {endpoint.value} not registered",
                "query": query
            }

        endpoint_config = self.endpoints[endpoint]
        handler = endpoint_config["handler"]

        try:
            # Call endpoint handler
            response = await handler(query, context)

            # Update statistics
            endpoint_config["total_queries"] += 1

            if response.get("success"):
                endpoint_config["successful_queries"] += 1

                # Track cost savings
                if endpoint == ModelEndpoint.LOCAL_NEMO:
                    self.stats["local_queries"] += 1
                    # Calculate savings vs ChatGPT API
                    saved = 0.002  # Approx $0.002 per ChatGPT query
                    self.stats["cost_saved"] += saved
                else:
                    self.stats["cloud_queries"] += 1

            # Add metadata
            response["metadata"] = {
                "endpoint": endpoint.value,
                "query_type": self.classify_query(query).value,
                "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000,
                "cost": endpoint_config["cost"],
                "timestamp": datetime.now().isoformat()
            }

            # Store in history
            self.query_history.append({
                "query": query,
                "endpoint": endpoint.value,
                "success": response.get("success"),
                "timestamp": datetime.now().isoformat()
            })

            return response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "endpoint": endpoint.value
            }

    def get_statistics(self) -> Dict:
        """Get routing statistics"""
        total = self.stats["total_queries"]

        return {
            "total_queries": total,
            "local_queries": self.stats["local_queries"],
            "cloud_queries": self.stats["cloud_queries"],
            "local_percentage": (self.stats["local_queries"] / total * 100) if total > 0 else 0,
            "total_cost_saved_usd": self.stats["cost_saved"],
            "avg_cost_saved_per_query": (self.stats["cost_saved"] / total) if total > 0 else 0,
            "endpoints": {
                name.value: {
                    "total_queries": config["total_queries"],
                    "successful_queries": config["successful_queries"],
                    "success_rate": (config["successful_queries"] / config["total_queries"] * 100)
                    if config["total_queries"] > 0 else 0
                }
                for name, config in self.endpoints.items()
            }
        }


class NeMoLocalHandler:
    """
    Handler for local NVIDIA NeMo model
    Loads model from SPI directory
    """

    def __init__(self, model_path: str):
        """
        Initialize NeMo handler

        Args:
            model_path: Path to NeMo model directory
        """
        self.model_path = model_path
        self.model = None
        self.model_loaded = False

        logger.info(f"🚀 NeMo handler initialized (path: {model_path})")

    def load_model(self):
        """Load NeMo model from disk"""
        if self.model_loaded:
            return

        try:
            # Import NeMo (lazy import)
            import nemo
            from nemo.collections.nlp.models import MegatronGPTModel

            logger.info(f"📦 Loading NeMo model from: {self.model_path}")

            # Load model
            self.model = MegatronGPTModel.restore_from(self.model_path)
            self.model.eval()

            self.model_loaded = True
            logger.info("✅ NeMo model loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load NeMo model: {e}")
            raise

    async def __call__(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Process query with local NeMo model

        Args:
            query: User's query
            context: Additional context

        Returns:
            Model response
        """
        # Load model if not loaded
        if not self.model_loaded:
            self.load_model()

        try:
            # Generate response
            response = self.model.generate(
                inputs=[query],
                max_length=512,
                temperature=0.7,
                top_k=50,
                top_p=0.9
            )

            # Extract text
            response_text = response[0] if isinstance(response, list) else response

            return {
                "success": True,
                "message": response_text,
                "model": "nvidia_nemo_local",
                "tokens_used": len(response_text.split()),  # Approximate
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"NeMo generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": "nvidia_nemo_local"
            }


# Singleton instance
_resonance_router: Optional[ResonanceRouter] = None


def get_resonance_router(nemo_path: Optional[str] = None) -> ResonanceRouter:
    """Get or create Resonance Router singleton"""
    global _resonance_router
    if _resonance_router is None:
        _resonance_router = ResonanceRouter(nemo_path)
    return _resonance_router
