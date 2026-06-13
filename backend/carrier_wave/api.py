"""Carrier wave REST API — Flask Blueprint."""

from flask import Blueprint, request, jsonify
import asyncio
from .search_ingestion import fetch_duckduckgo

carrier_bp = Blueprint('carrier', __name__)


@carrier_bp.route('/api/carrier/query', methods=['POST'])
def carrier_query():
    data = request.get_json(force=True)
    query = data.get('query', '')
    cosig = data.get('cosig', {})
    result = asyncio.run(fetch_duckduckgo(query))
    result['cosig'] = cosig
    return jsonify(result)
