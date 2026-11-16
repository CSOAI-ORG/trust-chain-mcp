<!-- mcp-name: io.github.CSOAI-ORG/trust-chain-mcp -->
[![MCP Scorecard: 90/100](https://img.shields.io/badge/proofof.ai-90%2F100-5b21b6)](https://proofof.ai/scorecard/trust-chain-mcp.html)

# Trust Chain MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![GSPC](https://img.shields.io/badge/GSPC-live%20GET%20%2Fapi%2Fgspc-0ea5e9)](https://councilof.ai/api/gspc)
[![Measurement](https://img.shields.io/badge/Measurement-not%20certification-64748b)](https://councilof.ai/api/gspc)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/trust_chain_mcp/)
mcp-name: io.github.CSOAI-ORG/trust-chain-mcp

# Trust Chain

[![PyPI](https://img.shields.io/pypi/v/trust-chain-mcp)](https://pypi.org/project/trust-chain-mcp/) [![Python](https://img.shields.io/pypi/pyversions/trust-chain-mcp)](https://pypi.org/project/trust-chain-mcp/)


> By [MEOK AI Labs](https://meok.ai) — Trust chain and attestation management by MEOK AI Labs.

> Trust chain and attestation management by MEOK AI Labs

Trust chain and attestation management by MEOK AI Labs.

---

## 🚀 Quick Start

## Quick Install

| Client | Install |
|--------|---------|
| **Claude Desktop** | [![Install in Claude](https://img.shields.io/badge/Install-Claude-blue)](https://claude.ai) |
| **Cursor** | [![Install in Cursor](https://img.shields.io/badge/Install-Cursor-black)](https://cursor.com) |
| **VS Code** | [![Install in VS Code](https://img.shields.io/badge/Install-VS_Code-blue)](https://code.visualstudio.com) |
| **Windsurf** | [![Install in Windsurf](https://img.shields.io/badge/Install-Windsurf-purple)](https://codeium.com/windsurf) |
| **Docker** | `docker run -p 8000:8000 trust-chain-mcp` |
| **pip** | `pip install trust-chain-mcp` |

## Installation

```bash
# Install via pip
pip install trust_chain_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install trust-chain-mcp --client claude
```

## ✨ Features

- MCP protocol compliant
- Easy installation
- Well-documented API
- Production-ready
- Active maintenance

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/trust-chain-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## Honesty register (2026-09-02)

**Live authority is `GET https://councilof.ai/api/gspc`** — cite `totals.public_count` and `totals.lid` from that payload. Do not type axis counts into this README.

- **Measurement, not certification.** CSOAI Ltd measures and signs; it does not certify, accredit, or act as a notified body.
- **MEOK.ai is a shelf / frontend**, not a second Council. Printers and agents must read the live GSPC endpoint — never invent scores, never wrangler a stamp.
- Prefer honest **UNCHECKABLE** over a fake stamp. This package does **not** certify EU AI Act compliance.


## How MEOK charges

MEOK has no subscriptions and no tiers. You pay per job, and only when the agreed artifact has been delivered to you. There is no public price list. See <https://meok.ai/pricing>.

This repository's source is MIT-licensed and free to self-host.

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | Independent measurement board — live `GET /api/gspc` |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Shelf / frontend (not a second Council) |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/trust-chain-mcp](https://github.com/CSOAI-ORG/trust-chain-mcp)
- **PyPI**: [pypi.org/project/trust-chain-mcp](https://pypi.org/project/trust-chain-mcp/)

## License

MIT — MEOK AI Labs

<!-- meok-moat-footer-v1 -->
---

## Pairs with MEOK Governance Suite

Build something that touches users? You need compliance. MEOK ships 38 governance MCPs that drop in alongside this tool — EU AI Act, DORA, NIS2, CRA, GDPR, ISO 42001, FDA SaMD, MDR, Basel, MiFID II, MiCA, COPPA, and more.

```bash
# One-shot install of the governance pack
npx meok-setup --pack governance
```


→ Full catalogue: [councilof.ai](https://councilof.ai)
→ MEOK AI Labs: [meok.ai](https://meok.ai)



## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "trust-chain-mcp": {
      "command": "uvx",
      "args": ["trust-chain-mcp"]
    }
  }
}
```

Or: `pip install trust-chain-mcp` then run the `trust-chain-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `create_trust_anchor` to …"
- "Use `verify_chain` to …"
- "Use `add_attestation` to …"
