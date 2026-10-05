"""LoRaWAN uplink ingestion service."""
from __future__ import annotations

import base64
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def ingest_lorawan_payload(lora_payload: Dict[str, Any]) -> Dict[str, Any]:
    if "data" in lora_payload:
        decoded = base64.b64decode(lora_payload["data"])
        try:
            payload_dict = json.loads(decoded.decode("utf-8"))
        except json.JSONDecodeError:
            payload_dict = {"raw_bytes": decoded.hex()}
    else:
        payload_dict = lora_payload

    cleaned = {
        "device_id": lora_payload.get("deviceName", lora_payload.get("dev_eui", "unknown")),
        "timestamp": lora_payload.get("rxTime"),
        "rssi": lora_payload.get("rxInfo", [{}])[0].get("rssi", 0),
        "payload": payload_dict,
    }
    logger.info("LoRaWAN uplink accepted from device %s", cleaned["device_id"])
    return cleaned
