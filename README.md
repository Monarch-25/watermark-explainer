# Watermarking Large Language Models — An Interactive Explainer

An interactive explainer for Kirchenbauer et al., “A Watermark for Large Language Models” (ICML 2023, [arXiv:2301.10226](https://arxiv.org/abs/2301.10226)).

**Live page:** https://monarch-25.github.io/watermark-explainer/

Using an abstract vocabulary (tokens carry no meaning), it reconstructs the paper's construction from first principles: hashed green/red partitioning, hard vs. soft watermarking, and the z-test detector — all evaluated live in the page, with hover definitions on every key term and formula.

## Contents

| File | What |
|---|---|
| `index.html` | The complete explainer. Single file, zero dependencies, runs offline. |
| `site/index.html` | Identical copy, served for local preview. |
| `watermark_torch.py` | The same mathematics in PyTorch — an independent check of the page's statistics. |
| `HOSTING.md` | Publishing notes, including the Substack situation. |

Paper defaults throughout: γ = 0.25, δ = 2.0, detection at z > 4 (one-sided p ≈ 3×10⁻⁵). Token highlighting follows the paper's Figure 1 convention.
