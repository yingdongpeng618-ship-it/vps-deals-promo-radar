---
name: Technology buying journal
colors: ["#173389", "#191b20", "#2447b9", "#343840", "#555d6b", "#737b88", "#a12c17", "#c7cbd2", "#e9eefb", "#f1f3f6", "#f6f7f9", "#fff"]
radii: [0]
fonts: [Georgia, Times New Roman, Segoe UI Variable Text, Segoe UI, serif, sans-serif]
sizes_px: [11,12,13,14,15,16,18,20,24,26,28,32,36,40,42,48,52,56,64,68,84]
---
# Creative North Star (authored)
An independent technology buying journal. User approved the magazine theme for production after reviewing the independent preview. Upright editorial serif, oversized wordmark, white paper, black rules, dark data headers and cobalt actions. No faux issue numbers, decorative imagery, cream/terracotta, italic display or mono labels.
# Color
Primary action #2447b9; hover #173389; ink #191b20; body #343840; secondary #555d6b; neutral canvas white and #f1f3f6; line #c7cbd2; control #737b88; focus/error #a12c17; selection/hover #e9eefb; alternate table row #f6f7f9. Secondary and tertiary are neutral information roles, no extra brand accents.
# Typography
Display/masthead Georgia upright (Times New Roman fallback), 400/700. Data, body, controls and subheads Segoe UI Variable Text/Segoe UI, 400/600. Display 84 desktop, 68 medium,56 mobile,48 narrow; article headline64/52/42/36. Body16, lead20/18, labels14, table15/16. Numeric tabular lining; heading line-height1.3; prose1.65-1.75. Reading columns62-65ch; sources76ch.
# Layout and spacing
Centered max1280, desktop side48/32, mobile20. Magazine masthead occupies a separate row above utility nav. Two-column cover leads into a horizontal price observation strip, followed by working price table. Guide spread has three open columns. Article has sticky210px contents and wide table/reading column; mobile details collapsed. Spacing primitives4,8,12,16,20,22,24,28,32,36,40,42,44,48,56,64,80,96. No rounded cards or shadows.
# Components
Masthead: white/ink, display, radius0, top28. Action: cobalt/white,body16 semibold,radius0,padding12/22,height48. Native input: white/ink,body16,radius0,padding9/12,height46. Table: ink header/white text,body15/16,radius0,padding18/20 or20/24. Contents: native details, label16/nav14, radius0. Repeated provider links use shared guide-list component selectors.
# Motion and states
650ms intro entrance uses translateY12 to0 from visible default; ease(.16,1,.3,1); reduced motion disables it. Hover, focus, disabled reset, error budget, no results and recovery retained. No loading state is simulated because all records are static.
# Accessibility
Semantic headers, tables and headings; sources inline; keyboard-scrollable table containers; native forms;44px action targets; no whole-page overflow expected. F53: repeated source/action phrases and billing units are semantic context, not decoration. Rectangular components intentionally use radius0 per requested magazine style. Device check is simulated viewport, never claimed as real phone cellular.
# Evidence and limits
Source quotes, monetary sequences and timestamps asserted identical to original Hostinger. Existing build verification8tests/14routes. Viewport screenshots and browser measurements supplied to a fresh reviewer. No award-level or all62-rule certification claimed. Production is approved. Normal robots and sitemap are retained, no preview labels or preview noindex are added.

## Production rollout
Owner approved the magazine style for the full site. All generated pages now share the masthead, palette, navigation and typography. Existing pricing content, evidence, schemas and canonical URLs remain. Preview robots restrictions and preview-only labels are removed.

## Shared production page layouts
Reference-page headlines52/44/36/32, body16 and lead20/18. Plan detail: flexible reading column and300px sticky neutral purchase aside,260px medium; single column on mobile. Source specification SVGs retain exact content and use neutral #f1f3f6/#191b20. Provider listings use flat rows and44px inspection links; mobile rows stack. Specification and billing definition lists use160px labels then flexible values, and stack on mobile. Compare uses the same black-header scrollable table. Methodology reading column72ch with prose capped65ch. Footer links are generated from configured active providers, plus compare, methodology/disclosure and source code; no unpriced provider shell is introduced.
