---
name: Procurement instrument
authorship: Authored for this project; no award recognition is claimed
fonts: [Trebuchet MS, Segoe UI, sans-serif]
colors:
  primary: '#245c48'
  primary_hover: '#174432'
  secondary: '#123d34'
  on_secondary: '#e7f4ee'
  tertiary_focus: '#ad4b09'
  canvas: '#f3f6f6'
  surface: '#ffffff'
  ink: '#142d26'
  muted: '#4d6259'
  line: '#c5d3cc'
  control_border: '#71867b'
  track: '#e3ece7'
  selection: '#cfe8de'
font_sizes: [16, 20, 32, 48]
font_weights: [400, 700]
radius: [0, 6, 14]
spacing: [4, 8, 12, 16, 24, 32, 48, 64, 96]
depth: none
motion: {feedback_ms: 140, entrance_ms: 600, easing: 'cubic-bezier(.16,1,.3,1)'}
---

## Creative North Star
Authored: a readable component-test instrument, where the actual price distribution provides visual character. The user should be able to inspect figures before reading promotional language. The green brand identifies the instrument; its neutral data plane carries the decision.

## Color and surfaces
Primary green is for links, price meters and actions. Secondary forest is the introductory region; its text uses the tinted on-secondary color. Focus uses the tertiary amber. Neutral canvas, white surface, ink, muted text, borders and meter tracks are the listed semantic tokens. There are no gradients, glow, decorative shadows or dark-mode inversion. Native meter backgrounds are explicitly reset. Only surfaces that require separation, such as a purchase summary, use the 14px radius. Form controls use 6px. Rows and meters remain square and unboxed.

## Typography
One local system family stack: Trebuchet MS, Segoe UI, sans-serif. Display is 48px on wide screens and 32px at 1100px and below; headlines are 32px wide and 20px at 760px and below; component titles are 20px; body, labels, captions, table cells and controls are 16px. Weights are 400 and 700. Body line-height is 1.6; headings and prices are 1.3. Display tracking is -.02em and headline tracking -.01em. Body has no tracking. Body measure is normally 45–70ch, prose 65ch, with shorter contextual captions. Text wraps rather than truncates. Headings use balance and paragraphs pretty when supported.

## Layout and rhythm
The centered page is at most 1400px wide. Outer gutters are 32px wide-screen and 16px on narrow screens. Core spacing uses the frontmatter scale. The desktop introduction and cost readout are siblings; they stack at 760px. Section groups use 48–96px separation and internal groups use 8–24px. Offer rows use a shared four-column grid on wide screens, three columns plus the action at medium sizes, and two columns with specifications below on mobile. Comparison tables intentionally scroll within a labelled, keyboard-focusable region. No body content is clipped or hidden to make a layout fit.

## Components
Component properties are capped at eight each. Header: backgroundColor, textColor, typography, padding, height. Primary/secondary action: backgroundColor, textColor, typography, rounded, padding, height. Offer row: backgroundColor, textColor, typography, padding, width. Source status: textColor, typography, padding, width. Meter readout: backgroundColor, textColor, typography, height, width. Purchase summary: backgroundColor, textColor, typography, rounded, padding, width. Form field: backgroundColor, textColor, typography, rounded, padding, height, width. Footer: textColor, typography, padding, width. Repeated offer rows come from one template, shared across home and provider pages.

## Interaction and states
Static source links are always available. Optional local enhancement reveals native search, numeric budget and sort controls after initialization, filters rendered observations and announces the result count. Zero matches includes a reset action. Negative/invalid budgets show a recovery message and aria-invalid rather than hiding the dataset. Reset is disabled at defaults; disabled styling is explicit. Existing source failures show verification status and an official-source action. There is no network form submission or artificial loading state. Input and selection remain on the device.

## Motion and accessibility
One 600ms transform-only readout entrance moves visible content 12px; nothing starts transparent. It has no loop and no hidden-at-rest state. Reduced motion disables it and transitions. Native controls have minimum 44px height, buttons 48px, and navigation links 44px. Focus is a 3px amber outline with 4px offset. Selection, caret, scrollbar and underline offset are themed. Tabular numbers are used for observed values. A skip link is available on keyboard focus. Meter descriptions include the real plan, currency and monthly amount; explanatory copy states that cost bars do not encode performance.

## Evidence and limitations
Source facts come from the current official-source dataset. Product context and visual direction are authored or explicitly inferred in PRODUCT.md and work/design-direction.md. Review artifacts and screenshots belong in work/design-engine-review/. Rule results distinguish browser evidence, source inspection and unknowns. External award judging, real-device Core Web Vitals and untested browser/assistive-technology combinations cannot be certified by visual inspection. Existing Google Rich Results/crawler issues are not claimed resolved by this visual change.

Mobile offer prices use 32px amounts, a separate 16px USD label, and an inline 16px /mo period; narrow layouts retain the same readable scale.
