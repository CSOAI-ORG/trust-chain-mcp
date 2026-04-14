#!/usr/bin/env python3
"""Trust chain management, attestation, and verification — MEOK AI Labs."""
import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json
import hashlib
import time
import math
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)


def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now)
    return None


# In-memory trust store
_ANCHORS = {}  # anchor_id -> anchor data
_ATTESTATIONS = {}  # attestation_id -> attestation data
_REVOCATIONS = set()  # set of revoked anchor/attestation IDs


def _hash_data(data: str) -> str:
    """Create a SHA-256 hash of data."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _short_hash(data: str) -> str:
    """Create a short identifier hash."""
    return _hash_data(data)[:16]


def _compute_chain_hash(entries: list) -> str:
    """Compute a chained hash from a list of entries."""
    chain = ""
    for entry in entries:
        chain = _hash_data(chain + json.dumps(entry, sort_keys=True))
    return chain


mcp = FastMCP("trust-chain-mcp", instructions="Trust chain and attestation management by MEOK AI Labs.")


@mcp.tool(name="create_trust_anchor")
async def create_trust_anchor(entity_id: str, entity_name: str, trust_level: int = 5, metadata: dict = None, api_key: str = "") -> dict:
    """Create a new trust anchor (root of trust) for an entity."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    if trust_level < 1 or trust_level > 10:
        return {"error": "trust_level must be between 1 and 10."}

    now = datetime.now(timezone.utc)
    anchor_data = f"{entity_id}:{entity_name}:{now.isoformat()}"
    anchor_id = _short_hash(anchor_data)

    if anchor_id in _ANCHORS:
        return {"error": "Anchor already exists for this entity. Use add_attestation instead."}

    anchor = {
        "anchor_id": anchor_id,
        "entity_id": entity_id,
        "entity_name": entity_name,
        "trust_level": trust_level,
        "created_at": now.isoformat(),
        "fingerprint": _hash_data(anchor_data),
        "attestations": [],
        "metadata": metadata or {},
        "status": "active",
    }
    _ANCHORS[anchor_id] = anchor

    return {
        "status": "created",
        "anchor_id": anchor_id,
        "entity_id": entity_id,
        "entity_name": entity_name,
        "trust_level": trust_level,
        "fingerprint": anchor["fingerprint"],
        "created_at": anchor["created_at"],
    }


@mcp.tool(name="verify_chain")
async def verify_chain(anchor_id: str, api_key: str = "") -> dict:
    """Verify the integrity of a trust chain by validating all attestations."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    if anchor_id not in _ANCHORS:
        return {"error": f"Anchor {anchor_id} not found."}

    anchor = _ANCHORS[anchor_id]

    if anchor_id in _REVOCATIONS:
        return {
            "anchor_id": anchor_id,
            "valid": False,
            "reason": "Trust anchor has been revoked.",
            "status": "revoked",
        }

    attestation_ids = anchor.get("attestations", [])
    chain_entries = [{"anchor_id": anchor_id, "fingerprint": anchor["fingerprint"]}]
    valid_attestations = 0
    invalid_attestations = 0
    revoked_attestations = 0
    issues = []

    for att_id in attestation_ids:
        att = _ATTESTATIONS.get(att_id)
        if att is None:
            issues.append(f"Attestation {att_id} not found.")
            invalid_attestations += 1
            continue

        if att_id in _REVOCATIONS:
            issues.append(f"Attestation {att_id} has been revoked.")
            revoked_attestations += 1
            continue

        # Verify attestation hash
        expected_hash = _hash_data(f"{att['attester_id']}:{att['claim']}:{att['created_at']}")
        if att.get("hash") != expected_hash:
            issues.append(f"Attestation {att_id} hash mismatch - possible tampering.")
            invalid_attestations += 1
            continue

        chain_entries.append({"attestation_id": att_id, "hash": att["hash"]})
        valid_attestations += 1

    chain_hash = _compute_chain_hash(chain_entries)
    chain_valid = invalid_attestations == 0 and anchor_id not in _REVOCATIONS

    return {
        "anchor_id": anchor_id,
        "entity_name": anchor["entity_name"],
        "valid": chain_valid,
        "chain_hash": chain_hash,
        "chain_length": len(chain_entries),
        "attestations": {
            "total": len(attestation_ids),
            "valid": valid_attestations,
            "invalid": invalid_attestations,
            "revoked": revoked_attestations,
        },
        "issues": issues,
        "trust_level": anchor["trust_level"],
        "status": "revoked" if anchor_id in _REVOCATIONS else "valid" if chain_valid else "compromised",
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="add_attestation")
async def add_attestation(anchor_id: str, attester_id: str, claim: str, confidence: float = 0.8, evidence: str = "", api_key: str = "") -> dict:
    """Add an attestation (claim) to an existing trust anchor."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    if anchor_id not in _ANCHORS:
        return {"error": f"Anchor {anchor_id} not found."}

    if anchor_id in _REVOCATIONS:
        return {"error": "Cannot attest to a revoked anchor."}

    if confidence < 0 or confidence > 1:
        return {"error": "Confidence must be between 0.0 and 1.0."}

    now = datetime.now(timezone.utc)
    att_data = f"{attester_id}:{claim}:{now.isoformat()}"
    att_id = _short_hash(att_data)

    attestation = {
        "attestation_id": att_id,
        "anchor_id": anchor_id,
        "attester_id": attester_id,
        "claim": claim,
        "confidence": confidence,
        "evidence": evidence,
        "created_at": now.isoformat(),
        "hash": _hash_data(att_data),
        "status": "active",
    }
    _ATTESTATIONS[att_id] = attestation
    _ANCHORS[anchor_id]["attestations"].append(att_id)

    # Recompute chain hash
    chain_entries = [{"anchor_id": anchor_id, "fingerprint": _ANCHORS[anchor_id]["fingerprint"]}]
    for a_id in _ANCHORS[anchor_id]["attestations"]:
        a = _ATTESTATIONS.get(a_id)
        if a:
            chain_entries.append({"attestation_id": a_id, "hash": a["hash"]})
    chain_hash = _compute_chain_hash(chain_entries)

    return {
        "status": "attested",
        "attestation_id": att_id,
        "anchor_id": anchor_id,
        "attester_id": attester_id,
        "claim": claim,
        "confidence": confidence,
        "hash": attestation["hash"],
        "chain_hash": chain_hash,
        "chain_length": len(chain_entries),
        "created_at": attestation["created_at"],
    }


@mcp.tool(name="get_trust_score")
async def get_trust_score(anchor_id: str, api_key: str = "") -> dict:
    """Calculate a composite trust score for an anchor based on its attestations."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    if anchor_id not in _ANCHORS:
        return {"error": f"Anchor {anchor_id} not found."}

    anchor = _ANCHORS[anchor_id]

    if anchor_id in _REVOCATIONS:
        return {
            "anchor_id": anchor_id,
            "trust_score": 0.0,
            "status": "revoked",
            "reason": "Anchor has been revoked.",
        }

    attestation_ids = anchor.get("attestations", [])
    active_attestations = []
    for att_id in attestation_ids:
        att = _ATTESTATIONS.get(att_id)
        if att and att_id not in _REVOCATIONS:
            active_attestations.append(att)

    # Base score from trust level (0-10 scaled to 0-0.5)
    base_score = anchor["trust_level"] / 20.0

    # Attestation score: weighted average of confidences, scaled by count
    if active_attestations:
        avg_confidence = sum(a["confidence"] for a in active_attestations) / len(active_attestations)
        # Logarithmic scaling for number of attestations (diminishing returns)
        count_factor = min(1.0, math.log(len(active_attestations) + 1) / math.log(20))
        attestation_score = avg_confidence * count_factor * 0.5
    else:
        avg_confidence = 0
        count_factor = 0
        attestation_score = 0

    total_score = round(min(1.0, base_score + attestation_score), 4)

    # Unique attesters
    unique_attesters = len(set(a["attester_id"] for a in active_attestations))

    age_hours = 0
    if active_attestations:
        latest = max(a["created_at"] for a in active_attestations)
        try:
            age_hours = round((datetime.now(timezone.utc) - datetime.fromisoformat(latest.replace("Z", "+00:00"))).total_seconds() / 3600, 1)
        except (ValueError, TypeError):
            pass

    if total_score >= 0.8:
        rating = "excellent"
    elif total_score >= 0.6:
        rating = "good"
    elif total_score >= 0.4:
        rating = "moderate"
    elif total_score >= 0.2:
        rating = "low"
    else:
        rating = "minimal"

    return {
        "anchor_id": anchor_id,
        "entity_name": anchor["entity_name"],
        "trust_score": total_score,
        "rating": rating,
        "components": {
            "base_score": round(base_score, 4),
            "attestation_score": round(attestation_score, 4),
            "trust_level": anchor["trust_level"],
            "avg_confidence": round(avg_confidence, 4),
            "count_factor": round(count_factor, 4),
        },
        "attestation_count": len(active_attestations),
        "unique_attesters": unique_attesters,
        "hours_since_last_attestation": age_hours,
        "status": "active",
    }


@mcp.tool(name="revoke_trust")
async def revoke_trust(target_id: str, reason: str, revoked_by: str, api_key: str = "") -> dict:
    """Revoke a trust anchor or attestation. This invalidates the chain."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(api_key or "anon"):
        return err

    target_type = None
    target_name = None

    if target_id in _ANCHORS:
        target_type = "anchor"
        target_name = _ANCHORS[target_id]["entity_name"]
        _ANCHORS[target_id]["status"] = "revoked"
    elif target_id in _ATTESTATIONS:
        target_type = "attestation"
        target_name = f"attestation by {_ATTESTATIONS[target_id]['attester_id']}"
        _ATTESTATIONS[target_id]["status"] = "revoked"
    else:
        return {"error": f"Target {target_id} not found as anchor or attestation."}

    if target_id in _REVOCATIONS:
        return {"error": f"Target {target_id} is already revoked."}

    _REVOCATIONS.add(target_id)

    # If revoking an anchor, count affected attestations
    affected = 0
    if target_type == "anchor":
        affected = len(_ANCHORS[target_id].get("attestations", []))

    return {
        "status": "revoked",
        "target_id": target_id,
        "target_type": target_type,
        "target_name": target_name,
        "reason": reason,
        "revoked_by": revoked_by,
        "revoked_at": datetime.now(timezone.utc).isoformat(),
        "affected_attestations": affected,
        "note": "All chain verifications involving this target will now fail." if target_type == "anchor" else "This attestation will be excluded from trust score calculations.",
    }


if __name__ == "__main__":
    mcp.run()
