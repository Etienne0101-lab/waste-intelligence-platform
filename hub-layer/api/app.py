"""Flask application for the waste-intelligence hub layer."""

from __future__ import annotations

import logging
import os
from flask import Flask, jsonify

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    @app.get("/health")
    def healthcheck() -> tuple:
        return jsonify({"status": "ok", "service": "hub-layer"}), 200

    from routes.bins import bins_bp
    from routes.facilities import facilities_bp
    from routes.analytics import analytics_bp

    app.register_blueprint(bins_bp)
    app.register_blueprint(facilities_bp)
    app.register_blueprint(analytics_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    host = os.getenv("HUB_HOST", "0.0.0.0")
    port = int(os.getenv("HUB_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
