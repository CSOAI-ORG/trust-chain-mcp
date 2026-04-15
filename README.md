# Trust Chain

> By [MEOK AI Labs](https://meok.ai) — Trust chain and attestation management by MEOK AI Labs.

Trust chain management, attestation, and verification — MEOK AI Labs.

## Installation

```bash
pip install trust-chain-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install trust-chain-mcp
```

## Tools

### `create_trust_anchor`
Create a new trust anchor (root of trust) for an entity.

**Parameters:**
- `entity_id` (str)
- `entity_name` (str)
- `trust_level` (int)
- `metadata` (str)

### `verify_chain`
Verify the integrity of a trust chain by validating all attestations.

**Parameters:**
- `anchor_id` (str)

### `add_attestation`
Add an attestation (claim) to an existing trust anchor.

**Parameters:**
- `anchor_id` (str)
- `attester_id` (str)
- `claim` (str)
- `confidence` (float)
- `evidence` (str)

### `get_trust_score`
Calculate a composite trust score for an anchor based on its attestations.

**Parameters:**
- `anchor_id` (str)

### `revoke_trust`
Revoke a trust anchor or attestation. This invalidates the chain.

**Parameters:**
- `target_id` (str)
- `reason` (str)
- `revoked_by` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/trust-chain-mcp](https://github.com/CSOAI-ORG/trust-chain-mcp)
- **PyPI**: [pypi.org/project/trust-chain-mcp](https://pypi.org/project/trust-chain-mcp/)

## License

MIT — MEOK AI Labs
