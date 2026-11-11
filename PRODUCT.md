# Product record

## Platform
Web, public static site; desktop and mobile touch/keyboard browsers.

## Stack
Python standard-library scraper and static builder; I-Lang configuration; GitHub Actions; Cloudflare Pages. Existing production URL: https://vps-deals-promo-radar-3cx.pages.dev/ .

## Users
Inferred: people selecting a VPS who need to compare published monthly prices, memory and compute before visiting the provider. Both a first-time purchaser and an experienced developer should understand the figures.

## Product Purpose
Reduce the effort of inspecting official VPS price tables while keeping the original source, check date and billing caveats visible.

## Positioning
Independent price monitor. A published regular price is not presented as a discount. There is no performance ranking or promise that providers with similar specifications are equivalent.

## Operating Context
Inferred: users arrive from search, compare a handful of plans on a phone or desktop, and then inspect a provider's checkout. The website remains readable without JavaScript and on a slow connection. Prices are observations rather than live quotes.

## Capabilities and Constraints
- Current dataset: three monitored providers; priced plans are published only when verified. Data counts change with successful fetches.
- Official sources, real machine identifiers, current prices and dates come from existing data; unknown prices stay absent.
- Existing automatic refresh, canonical URLs, structured data, sitemap and robots remain intact.
- Small local JavaScript may progressively filter and sort already rendered offers. It never fetches prices or gates content.
- No added service subscription, third-party font, runtime model, fabricated endorsement, income claim or user account.
- Existing crawler-access and Google Rich Results Test limitations are separate operating issues; this redesign does not claim to solve them.

## Brand Commitments
Keep vps-deals, the existing owned logo and forest-green identity. Treat the newly supplied design document as the operative visual brief. Do not copy award-site assets, layouts or brand copy.

## Evidence on Hand
Real data/offers.json; provider source links; public commits and Actions history; existing production site and earlier browser captures. No verified customer, audience, revenue, endorsement, award or comparative performance evidence exists.

## Product Principles
1. Put cost and specifications before visual ornament.
2. Let every published number lead back to a source.
3. Use one strong reading hierarchy and a predictable decision path.
4. Retain a useful static page when enhancement is unavailable.
5. Describe uncertainty at the point of use.

## Accessibility and Inclusion
Minimum body size 16px, functional labels 14px, headings at least 1.3 line-height, semantic headings, keyboard-operable native controls, 44px targets, visible focus, readable contrast, reduced-motion fallback, no color-only status. Layout must work at 320px through 4K and zoom. Long names and empty/no-result data must remain usable.
