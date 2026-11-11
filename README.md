# vps-deals / RADAR

Independent, official-source VPS price and promotion monitor for **en-US**. Default niche: VPS hosting. Default brand: vps-deals. Sources: DigitalOcean, Hetzner, OVHcloud.

**Live site:** https://vps-deals-promo-radar-3cx.pages.dev — hosted on Cloudflare Pages with repository-triggered builds.

## Run

Python 3.12+, standard library only. No model calls, paid APIs, packages, or provider API keys.

```sh
python -m unittest discover -s tests -v
python scraper.py
python build.py
python verify.py
python -m http.server 4190 --directory site
```

Open http://localhost:4190. Unassigned `base_url` builds are noindex and contain no production sitemap URLs.

## Change the site

`.ilang/site.ilang` is the only source for brand, base URL, provider list, adapters, fields and rendering policy. The `::JSON_BEGIN` / `::JSON_END` block is a strict JSON payload inside the human-readable I-Lang document; `config.py` validates it. Both scraper and builder read it. Remove a provider there, run scraper + build, and its provider and deal pages disappear. The test suite actually exercises this.

DigitalOcean's adapter reads the first six-column Basic Regular pricing table and its actual purchase-URL plan identifiers. It takes only the unambiguous monthly cell, never hourly numbers, credits, original prices or renewal prices. Other providers currently use `monitor_only`: their public pages are monitored but prices are not guessed. Add a reviewed deterministic adapter before publishing their prices. Feed/sitemap discovery is not implemented in v1; v1 uses official pricing pages.

Every record includes the official source, UTC check timestamp, source SHA-256, plan ID and the exact observed monthly cell. `data/offers.json` is public, including fetch statuses. The bot checks robots.txt before fetching. HTTP 404 robots is treated as no restrictions; network/403/5xx robots errors fail closed. No certificate bypass, login scraping or anti-bot evasion.

## Automatic updates and deployment

`.github/workflows/update.yml` requests updates every six hours at minute 23 UTC (Beijing approximately 02:23, 08:23, 14:23, 20:23). GitHub scheduling can be delayed; it is not an uptime guarantee. `workflow_dispatch` supports an immediate manual run. Each observation commit contains real fetch timestamps and statuses, even when prices are unchanged. Built files are uploaded as an Actions artifact. The workflow uses GitHub's ephemeral built-in `GITHUB_TOKEN`, not a user API key. Website visitors and public-source fetches need no key. Public standard runners are free under GitHub's current policy; larger runners are excluded. Review platform terms and quotas before scaling.

Cloudflare Pages: connect this **public** repository, production branch `main`, build command `python build.py`, output directory `site`. No environment variables or API secrets are required. A committed observation triggers Pages' Git integration. Each scheduled refresh causes about 120–124 builds/month, within the currently documented Free limit of 500, shared with other deployments on the account. Platform policies can change.

After Pages creates a project, copy its **returned actual production URL** into `base_url` and `@SITE domain` in `.ilang/site.ilang`, then rebuild and commit. Never guess the hostname from the project name. Verify canonical links, robots and every sitemap URL externally. The builder deliberately refuses to invent a production hostname.

The latest observations are built into static pages. Failed sources have no current priced plans. Entries over 30 hours old and expired entries are omitted at build time. If the scheduler or deployment stops, an already-published static page cannot expire itself: check the visible timestamp and provider checkout. Monitor Actions failures. Public repository schedules may be disabled after 60 days without repository activity; automation is not guaranteed to run forever.

## Structured data

Deal pages: Product + Offer + BreadcrumbList. Provider pages: Service with AggregateOffer when prices exist. Home/compare: ItemList. Only observed price/currency fields are emitted. No invented availability, discount, reviews or priceValidUntil. No FAQ block is published, so there is no FAQPage markup. Canonical and sitemap generation use the assigned actual base URL. Local JSON syntax, internal links and sitemap counts are validated by `verify.py`; that is **not** Google's Rich Results Test. Google may require/recommend further fields and does not guarantee rich results. A live Google test must be recorded separately.

## Monetization

Until a programme is approved, provider `affiliate_url` stays empty and all outbound links go directly to official pages. After approval, add only a legitimate provider-approved tracking link; deal pages label affiliate links and emit `rel=sponsored`. Commissions, eligibility, permitted countries, payout and coupon rules must be checked against the programme's current terms. No fabricated income or programme approval. No brand bidding, cookie injection, fake scarcity or self-referrals. Possible later layers: clearly labelled direct sponsorship and independently authored paid research; none is activated or claimed now.

Public source code and a website do not establish income or transferable business value. An eventual sale requires demonstrable traffic, earnings, rights and a buyer. Domain age, GitHub commits and backlinks do not guarantee search rankings. A custom domain gives control over branding and URLs, but registration is optional and costs money; it is not required for the free Pages launch. No mass social posting is configured. A unified brand/avatar is provided; X/FB integrations are intentionally deferred.

## Sources and operating limits

- https://www.digitalocean.com/pricing/droplets
- https://www.hetzner.com/cloud/
- https://us.ovhcloud.com/vps/
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://developers.cloudflare.com/pages/platform/limits/
- https://developers.google.com/search/docs/appearance/structured-data/product-snippet

站点规则用 I-Lang 协议描述，见 `.ilang/site.ilang`；协议说明：ilang.ai。
