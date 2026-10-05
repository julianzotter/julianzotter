# NEXUS AI-OS — Routing Layer Reference (SKILLS.md)
<!-- version: 1.0.0 | updated: 2026-10-05 -->
<!-- Authority: config/signal_matrix.yaml + backend/moe_router.py + backend/kernel_router.py -->
<!-- This file documents the full routing stack. Update whenever a new kernel or expert is added. -->

## Overview

NEXUS routes every engineering query through a **3-layer routing stack**:

```
User Query
    │
    ▼
[1] Signal Matrix (domain scoring)   backend/signal_matrix.py
    │  detect_scope(text) → scope (BETONBAU / HOLZBAU / ...)
    │  compute(scope)     → SignalResult (score, risk, R/E/C/A/U)
    │
    ▼
[2] MoE Router (expert activation)   backend/moe_router.py
    │  route(scope, top_k=2)  → [E-STATIK, E-NORMEN, ...]
    │  sparsity(scope)         → fraction of inactive experts
    │
    ▼
[3] Kernel Router (AEC dispatch)     backend/kernel_router.py
       route_kernel(norm_tag, nachweis_typ) → kernel module
       Routing table source: config/signal_matrix.yaml
```

---

## Layer 1 — Signal Matrix (Domain Scoring)

**File:** `backend/signal_matrix.py`

Computes a readiness score `S = 0.35·R + 0.30·E + 0.20·C + 0.10·A − 0.05·U` per engineering scope.

### Scope Profiles

| Scope | R | E | C | A | U | Typical S |
|-------|---|---|---|---|---|-----------|
| BETONBAU | .92 | .90 | .88 | .85 | .10 | **0.870** |
| FERTIGTEIL | .89 | .86 | .84 | .81 | .13 | **0.843** |
| HOLZBAU | .88 | .85 | .82 | .79 | .15 | **0.838** |
| STAHLBAU | .85 | .82 | .78 | .75 | .18 | **0.815** |
| KI-WERKZEUG | .90 | .75 | .70 | .95 | .20 | **0.830** |
| BIM | .80 | .78 | .75 | .88 | .12 | **0.791** |
| ALLGEMEIN | .55 | .55 | .55 | .55 | .45 | **0.502** |

### Scope Detection Keywords

| Scope | Keywords |
|-------|----------|
| HOLZBAU | holz, gl24, gl28, c24, c16, ec5, brettschicht, kerto, clt, bsp |
| BETONBAU | beton, stahlbeton, c30, c40, c25, ec2, durchstanz |
| STAHLBAU | stahl, s355, s275, ipe, hea, heb, ec3 |
| BIM | ifc, bim, revit, allplan, speckle, glTF |
| FERTIGTEIL | fertigteil, precast, elementdecke, doppelwand |
| KI-WERKZEUG | ki, llm, agent, gpt, claude, deepseek, rag, embedding |

---

## Layer 2 — MoE Router (Expert Activation)

**File:** `backend/moe_router.py`

Sparse top-k expert activation. Default: `top_k = 2`.

### Expert → Scope Mapping

| Expert | Scopes | Score |
|--------|--------|-------|
| E-STATIK | HOLZBAU, BETONBAU, STAHLBAU, FERTIGTEIL | 0.95 |
| E-KI | KI-WERKZEUG | 0.92 |
| E-NORMEN | HOLZBAU, BETONBAU, STAHLBAU, FERTIGTEIL, ALLGEMEIN | 0.90 |
| E-MAT | HOLZBAU, BETONBAU, STAHLBAU, FERTIGTEIL | 0.88 |
| E-BIM | BIM | 0.85 |
| E-RPT | alle Scopes | 0.80 |

**Sparsity** = (total_experts − top_k) / total_experts  
→ BETONBAU mit top_k=2: (6−2)/6 = **0.667** (67 % der Experten inaktiv)

### Usage

```python
from moe_router import route, sparsity
experts = route("BETONBAU", top_k=2)
# [{"expert": "E-STATIK", "score": 0.95, "active": True},
#  {"expert": "E-NORMEN", "score": 0.90, "active": True}, ...]
```

---

## Layer 3 — Kernel Router (AEC Dispatch)

**File:** `backend/kernel_router.py`  
**Data:** `config/signal_matrix.yaml`

Routes `(norm_tag, nachweis_typ)` to the Python kernel that executes the structural proof.

### Current Routing Table

| SM-ID | norm_tag | nachweis_typ | Kernel | Status | Validated |
|-------|----------|--------------|--------|--------|-----------|
| SM-001 | EC2 | BIEGE | `ec2_fertigteil_kernel.py` | IMPLEMENTED | ✅ M1-A PASS |
| SM-002 | EC2 | SCHUB | `ec2_fertigteil_kernel_B.py` | IMPL_PENDING | ⏳ M1-B pending |
| SM-003 | EC2 | DURCHSTANZEN | — | SPEC_ONLY | — |
| SM-010 | EC5 | KNICKEN | `ec5_buckling.py` | SPEC_ONLY | — |
| SM-011 | EC5 | BIEGE | — | SPEC_ONLY | — |
| SM-020 | CENTS19103 | VERBUND-GAMMA2 | `hbv_gamma2_kernel.py` | KERNEL_DEFINED | — |
| SM-030 | SEILSTATIK | ZUGKRAFT | — | SPEC_ONLY | — |
| SM-040 | SIGEPLAN | SICHERHEITSPLAN | — | SPEC_ONLY | — |

**Coverage:** 1/8 = 12.5 % validated (target: M1-B → 25 %)

### Usage

```python
from kernel_router import route_kernel, coverage_report
result = route_kernel("EC2", "BIEGE")
# {"id": "SM-001", "norm_tag": "EC2", "nachweis_typ": "BIEGE",
#  "kernel": "ec2_fertigteil_kernel.py", "status": "IMPLEMENTED", "validated": True, ...}

report = coverage_report()
# {"total": 8, "implemented": 1, "coverage_pct": 12.5, "by_status": {...}}
```

### Kernel Output Schema (mandatory fields)

Every kernel must return a dict with at minimum:

```python
{
    "norm_tag":     "EC2",          # routing key
    "material_tag": "BETON-STAHL",  # routing key
    "nachweis_typ": "BIEGE",        # routing key
    "status":       "PASS",         # "PASS" | "FAIL"
    "eta":          0.964,          # Ausnutzungsgrad 0..1
    "case_id":      "P205-FT-..."   # golden case or runtime ID
}
```

---

## Full Pipeline Example

```python
from signal_matrix import detect_scope, compute as sig_compute
from moe_router import route as moe_route
from kernel_router import route_kernel

task = "Fertigteilträger EC2 Schub L=7.5m"
scope  = detect_scope(task)              # → "FERTIGTEIL"
sig    = sig_compute(scope)             # → SignalResult(score=0.843, risk="HIGH")
experts = moe_route(scope, top_k=2)    # → [E-STATIK, E-NORMEN]
kernel  = route_kernel("EC2", "SCHUB") # → {kernel: "ec2_fertigteil_kernel_B.py", ...}
# → execute kernel_router result → log to feedback.jsonl
```

---

## Adding a New Kernel

1. Write `kernels/{name}.py` with mandatory output schema
2. Add entry to `config/signal_matrix.yaml` with status `IMPL_PENDING`
3. Create `golden_cases/{name}_golden.json` with handrechnung from **independent source**
   (Schneider Bautabellen or ÖNORM-Kommentar — NOT same formula as kernel)
4. Run kernel against golden case; log result to `feedback.jsonl`
5. On PASS: update `signal_matrix.yaml` status → `IMPLEMENTED`, `validated: true`
6. Bump `signal_matrix.yaml` version (PATCH)
7. Commit: `feat(kernel): SM-XXX <norm_tag> <nachweis_typ> — M1-X PASS`

---

## Known Gaps & Roadmap

| Gap | Priority | Notes |
|-----|----------|-------|
| M1-B Schub Colab run | P0 | Code ready, run `ec2_fertigteil_kernel_B.py` |
| Merkle chain in feedback.jsonl | P0 | Add `prev_hash` to `log_feedback()` |
| EC5 Knicken kernel | P1 | Canonical workflow W2 |
| HBV γ2 golden case | P1 | Against CEN/TS 19103 Annex example |
| MoE Router → Kernel Router bridge | P1 | Wire `moe_route()` output into `route_kernel()` |
| SQLite WAL + FTS5 index (AP7) | P2 | For Knowledge Base fast-path queries |
| Circular validation fix | P0 | Replace handrechnung values with Schneider source |

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-10-05 | Initial SKILLS.md — 3-layer routing stack documented |
