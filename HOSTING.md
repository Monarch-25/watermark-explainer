# Hosting this explainer (free) + Substack

## The one key fact about Substack

**Substack strips `<script>` and arbitrary `<iframe>` embeds** — no free workaround puts
live JavaScript *inside* a Substack post. Anyone promising otherwise is selling you a GIF.
The professional pattern (used by every interactive Substack I respect):

1. Host the interactive page free elsewhere (below — 5 minutes).
2. In the Substack post: explainer prose + static screenshots / a screen-recorded GIF + a big
   “▶ Open the interactive lab” button linking to the hosted page.

Readers get one click to full interactivity; the post itself still reads perfectly in email.

## Option A — GitHub Pages (recommended: free, permanent, versioned)

```bash
cd /Users/mozart/Documents/ml/research/watermarking
git init && git add site/index.html && git commit -m "watermark explainer"
gh repo create watermark-explainer --public --source=. --push
# then: repo Settings → Pages → Deploy from branch → main, folder /(root),
# move index.html to repo root OR set Pages to /site folder... simplest:
```

Simplest layout: put `index.html` at the repo root (copy it there). Your URL becomes
`https://<you>.github.io/watermark-explainer/`. Free, HTTPS, no sleep, custom domain optional.

## Option B — Netlify Drop (fastest, no git)

1. Go to `app.netlify.com/drop`, drag the `site/` folder.
2. Done — you get a `*.netlify.app` URL. Free tier is plenty for a static page.

Cloudflare Pages works identically (drag-and-drop or git).

## Option C — Hugging Face Spaces (if you later want a Python backend)

Only needed if you upgrade to a real model backend. For this static page, A/B are better
(Spaces static hosting works too, but sleeps on the free tier).

## Making the Substack post shine

- **GIF preview:** record 10–15 s of pressing Play + dragging δ (QuickTime → `ffmpeg -i in.mov -vf fps=12,scale=900:-1 out.gif`, or Licecap). Put it where the demo would be, captioned “live version linked below”.
- **Button:** Substack's button block → “▶ Try the interactive watermark lab” → your hosted URL (first link, above the fold, and once more after the statistics section).
- **Fallback figures:** export two screenshots (soft mode z-trajectory + histogram) so email readers (no JS, no GIF autoplay in some clients) still get the argument.
- **Note the scope disclaimer** (already in §08): controlled Gaussian distributions, not a production LM — keeps you honest and preempts the obvious comment.

## If you ever leave Substack

Ghost (HTML cards), Buttondown (raw HTML in posts), or any self-hosted blog accept this
`index.html` (or parts of it) pasted directly — full interactivity inline, no changes needed.
