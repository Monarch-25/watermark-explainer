"""Abstract-vocabulary Kirchenbauer et al. (2023) watermark — mirrors site/index.html.

Run:  conda activate torch && python watermark_torch.py
"""
import math
import torch

KEY = 15485863


def green_list(prev_token: int, V: int, gamma: float) -> torch.Tensor:
    """Reproduceable partition: seed RNG with hash(prev_token), like the paper's
    `hash(s^(t-1))`. Detector can recompute this without the LM."""
    g = torch.Generator().manual_seed(KEY + int(prev_token))
    perm = torch.randperm(V, generator=g)
    k = max(1, int(math.floor(gamma * V)))
    mask = torch.zeros(V)
    mask[perm[:k]] = 1.0
    return mask  # 1.0 == green


def toy_logits(rng: torch.Generator, V: int, entropy: str) -> torch.Tensor:
    if entropy == "low":  # peaky: one near-deterministic token
        l = torch.randn(V, generator=rng) * 0.5
        l[int(torch.randint(V, (1,), generator=rng))] += 4.0
        return l
    if entropy == "high":  # flat: many plausible tokens
        return torch.randn(V, generator=rng) * 1.0
    # mixed: alternate — shows soft watermark biting only when it is cheap
    return toy_logits(rng, V, "low" if int(torch.randint(2, (1,), generator=rng)) else "high")


def generate(seed=0, V=24, T=80, gamma=0.25, delta=2.0, mode="soft", entropy="mixed"):
    gen_rng = torch.Generator().manual_seed(seed)
    seq, greens, tv = [], [], []
    prev = int(torch.randint(V, (1,), generator=gen_rng))
    for _ in range(T):
        logits = toy_logits(gen_rng, V, entropy)
        G = green_list(prev, V, gamma)
        if mode == "off":
            probs = torch.softmax(logits, 0)
        elif mode == "hard":
            wm = torch.where(G.bool(), logits, torch.tensor(-1e9))
            probs = torch.softmax(wm, 0)
        else:  # soft: l_hat = l + delta * 1_G  (Algorithm 2)
            probs = torch.softmax(logits + delta * G, 0)
            tv.append(float(0.5 * (probs - torch.softmax(logits, 0)).abs().sum()))
        tok = int(torch.multinomial(probs, 1))
        seq.append(tok)
        greens.append(float(G[tok].item()))
        prev = tok
    return seq, greens, (sum(tv) / len(tv) if tv else 0.0)


def z_score(n_green: float, T: int, gamma: float) -> float:
    return (n_green - gamma * T) / math.sqrt(T * gamma * (1 - gamma))


if __name__ == "__main__":
    V, T, gamma, delta = 12, 8, 0.25, 2.0
    torch.manual_seed(0)
    print("=== one step as matrices (V=12) ===")
    logits = torch.randn(V) * 1.5
    logits[0] = 3.0
    G = green_list(prev_token=7, V=V, gamma=gamma)
    print("logits   :", logits.numpy().round(2))
    print("greenmask:", G.numpy().astype(int), f"(green idx {torch.where(G.bool())[0].tolist()})")
    print("l_hat    :", (logits + delta * G).numpy().round(2), " <- l + delta*1_G")
    print("p        :", torch.softmax(logits, 0).numpy().round(3))
    print("p_hat    :", torch.softmax(logits + delta * G, 0).numpy().round(3))

    print("\n=== sequences (V=24, T=80, gamma=0.25, delta=2.0) ===")
    for mode in ("off", "soft", "hard"):
        seq, greens, tv = generate(mode=mode)
        z = z_score(sum(greens), T=80, gamma=gamma)
        print(f"{mode:4s} greens={int(sum(greens)):3d}/80  z={z:+6.2f}  "
              f"mean|p-hat - p|_TV={tv:.3f}  seq[:12]={seq[:12]}")
    print("\nPaper rule of thumb: reject H0 (='human, no knowledge of green lists') if z > 4 "
          "(one-sided p ~ 3e-5).")
