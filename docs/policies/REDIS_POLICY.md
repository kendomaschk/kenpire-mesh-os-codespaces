# Redis Usage & Inventory — Single Source Clarifier

**Status:** AUTHORITATIVE GUARDRAILS + SNAPSHOT CONTEXT  
**Applies to:** Redis usage across DirtyRAG, Trifecta, and Mesh runtime  
**Audience:** Jarvess, Finish_it, ClauseWitch, future maintainers

---

## INTENT (READ THIS FIRST)

This document exists to eliminate confusion by combining:

1. Hard rules for Redis usage (enforceable)
2. A lightweight inventory snapshot (non-authoritative)

Rules are permanent until explicitly revised.  
Inventory is informational and may change.

---

## PART I — REDIS RULES OF ENGAGEMENT (AUTHORITATIVE)

### Core Principle

**Redis is working memory, not knowledge storage.**

If something would be unsafe written on a whiteboard that auto-erases, it does not belong in Redis.

---

### Bucket Model (MANDATORY)

| Bucket | Name | Redis Allowed | Description |
|------|------|---------------|-------------|
| A | Ephemeral Runtime | ✅ YES | Live context, session state, short-lived agent memory |
| B | Indexed / Derived | ⚠️ POINTERS ONLY | Embeddings, recall indices, metadata referencing external truth |
| C | Canonical / IP-Locked | ❌ NO | Capsules, ProofLock assets, core logic, proprietary content |

---

### Hard Rules (Non-Negotiable)

1. TTL is required for all Redis keys unless explicitly exempted  
2. No IP-locked or canonical content may be stored in Redis  
3. Redis may store:
   - IDs
   - hashes
   - pointers
   - embeddings  
   **Never full source content**
4. Every Redis key MUST declare:
   - bucket
   - origin
   - ttl
   - ip_level

### Pattern example (structure only)

```json
{
  "key": "dirtyrag:session:123",
  "bucket": "A",
  "origin": "dirtyrag",
  "ttl": "30m",
  "ip_level": "internal"
}
```
