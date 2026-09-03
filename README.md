# LLM Watermarking — Interactive Explainer

Abstract-vocabulary interactive explainer for Kirchenbauer et al., “A Watermark for Large Language Models” (ICML 2023, arXiv:2301.10226).

## Files

| File | What |
|---|---|
| `site/index.html` | The whole explainer + lab. Single file, zero dependencies, works offline. |
| `watermark_torch.py` | Same math in PyTorch (validates the JS engine's statistics). |
| `HOSTING.md` | How to publish free + the Substack situation. |

## Test locally

Already running now: **http://localhost:8321/index.html**

Otherwise:

```bash
cd site && python3 -m http.server 8321
# open http://localhost:8321
```

Validate the statistics against PyTorch:

```bash
conda activate torch && python watermark_torch.py
# expect: off z≈0, soft z≈+5, hard z≈+15 at T=80, γ=0.25, δ=2.0
```

## Defaults (from the paper)

γ = 0.25, δ = 2.0, reject H₀ at z > 4 (one-sided p ≈ 3×10⁻⁵). Colors follow the paper's Figure 1 convention: green/red token highlighting, blue prompt accents.
