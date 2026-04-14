#!/usr/bin/env python3
import json, hashlib, time
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("trust-chain-mcp")
_CHAINS: dict = {}
@mcp.tool(name="initiate_trust_chain")
async def initiate_trust_chain(root_agent: str, participants: list) -> str:
    chain_id = hashlib.sha256(f"{root_agent}{time.time()}".encode()).hexdigest()[:16]
    _CHAINS[chain_id] = {"root": root_agent, "participants": participants, "established_at": time.time()}
    return json.dumps({"chain_id": chain_id, "status": "established"})
@mcp.tool(name="verify_participant")
async def verify_participant(chain_id: str, agent_id: str) -> str:
    c = _CHAINS.get(chain_id)
    valid = c is not None and agent_id in c.get("participants", [])
    return json.dumps({"chain_id": chain_id, "agent": agent_id, "verified": valid})
if __name__ == "__main__":
    mcp.run()
