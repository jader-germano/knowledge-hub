# Design System Extraction — 4 Reference HTML Files

## Scope

Sources analyzed:

- `/Users/philipegermano/code/jpglabs/docs/reference/web-captures/google-antigravity-auth-success.html`
- `Stripe Press — Ideas for progress.html`
- `/Users/philipegermano/code/jpglabs/docs/reference/web-captures/jpglabs-pi-products-and-services.html`
- `/Users/philipegermano/code/jpglabs/docs/reference/web-captures/monkeytype-typing-test.html`

This is a Phase 0 discovery artifact aligned to the `figma-generate-library` workflow. No Figma writes were performed.

## Outcome

The four files do not describe a single visual system. They cluster into four distinct interface modes:

1. `Google Light Product`
2. `Stripe Editorial Dark`
3. `Monkeytype Terminal Dark`
4. `JPGLabs Product Dark`

The cleanest Figma library shape is:

- `Primitives` collection
- `Color` collection with 4 modes
- `Spacing` collection
- `Radius` collection
- `Motion` collection
- Typography styles grouped by theme
- Components grouped by theme family

## Recommended Figma Collections

### `Color` collection

Suggested modes:

- `Google Light`
- `Stripe Editorial Dark`
- `Monkeytype Terminal Dark`
- `JPGLabs Product Dark`

Suggested semantic token names:

- `color/bg/default`
- `color/bg/subtle`
- `color/surface/default`
- `color/surface/raised`
- `color/text/default`
- `color/text/subtle`
- `color/text/inverse`
- `color/action/primary`
- `color/action/primary-hover`
- `color/action/secondary`
- `color/border/default`
- `color/border/subtle`
- `color/status/error`
- `color/status/error-subtle`
- `color/icon/default`

### `Spacing` collection

Base 4px rhythm is consistent enough across the references to standardize:

- `spacing/0 = 0`
- `spacing/1 = 4`
- `spacing/2 = 8`
- `spacing/3 = 12`
- `spacing/4 = 16`
- `spacing/6 = 24`
- `spacing/9 = 36`
- `spacing/12 = 48`
- `spacing/15 = 60`
- `spacing/20 = 80`
- `spacing/30 = 120`
- `spacing/45 = 180`

### `Radius` collection

- `radius/none = 0`
- `radius/sm = 4`
- `radius/md = 8`
- `radius/lg = 16`
- `radius/xl = 24`
- `radius/2xl = 36`
- `radius/3xl = 48`
- `radius/full = 9999`

### `Motion` collection

Only Google Antigravity exposes a mature easing set in the provided sources. Use it as the motion foundation:

- `motion/ease/out/quad = cubic-bezier(.25, .46, .45, .94)`
- `motion/ease/out/cubic = cubic-bezier(.215, .61, .355, 1)`
- `motion/ease/out/quart = cubic-bezier(.165, .84, .44, 1)`
- `motion/ease/in-out/cubic = cubic-bezier(.645, .045, .355, 1)`
- `motion/ease/out/back = cubic-bezier(.34, 1.85, .64, 1)`

## Theme Extraction

### 1. Google Antigravity

Authoritative source quality: high. The referenced stylesheet exposes a complete token system.

#### Core colors

- `color/bg/default = #FFFFFF`
- `color/bg/subtle = #F8F9FC`
- `color/surface/raised = #EFF2F7`
- `color/surface/high = #E6EAF0`
- `color/text/default = #121317`
- `color/text/subtle = #45474D`
- `color/action/primary = #121317`
- `color/action/secondary = rgba(183, 191, 217, 0.10)`
- `color/action/link = #3279F9`
- `color/border/subtle = rgba(33, 34, 38, 0.06)`
- `color/border/default = rgba(33, 34, 38, 0.12)`

#### Typography

Families:

- `Google Sans Flex` for interface and display
- `Google Sans Code` for special/code-like callouts
- `Google Symbols` for iconography

Key type tokens extracted from CSS:

- `display/landing = 72 / 72.04 / -1.44`
- `heading/4xl = 42 / 43.68 / -0.73`
- `heading/3xl = 32 / 33.92 / -0.15`
- `body/md = 17.5 / 25.38 / 0.18`
- `caption = 14.5 / 21.02 / 0.16`
- `small = 12.5 / 15.5 / 0.11`

#### Shape and layout

- 12-column grid on desktop
- page margin `72`
- gutter `64`, reduced responsively
- radius scale `4 / 8 / 16 / 24 / 36 / 48 / full`
- pill navigation/buttons are a first-class pattern

#### Component families

- top navigation with pill buttons
- primary CTA pill button
- secondary/tonal button
- hero headline block
- video trigger control
- use-case media cards
- carousel navigation
- blog cards
- download banner
- structured footer navigation

### 2. Stripe Press

Authoritative source quality: medium. The saved HTML and live rendering expose stable typography and palette, but the visual system is content-driven and many colors appear tied to individual covers.

#### Core colors

Stable interface colors:

- `color/bg/default = #201819`
- `color/text/default = #FFFFFF`
- `color/text/accent = #DFC78E`
- `color/surface/default = #6E665B`

Observed art-direction palette from the file:

- `#143199`
- `#2328A0`
- `#96DCED`
- `#C1B676`
- `#FFB55E`
- `#FFA6A6`
- `#0A2540`

Recommendation: keep these as `color/art/*` or `color/cover/*` tokens, not global semantic UI colors.

#### Typography

Families:

- `Ivar Headline` for display and titles
- `Ivar Text` for reading text
- `Georgia` as body fallback

Observed style direction:

- serif editorial display
- gold-on-dark metadata and titles
- minimal, high-contrast hierarchy
- almost no rounded geometry

#### Shape and layout

- sharp rectangular cards
- image-led product grid
- dark gallery canvas
- floating overlay/navigation layer
- newsletter form embedded in footer/editorial section

#### Component families

- book/film/podcast cards
- product detail overlays
- editorial hero titles
- newsletter input + submit
- floating navigation rail
- social icon links
- cookie consent bar

### 3. Monkeytype

Authoritative source quality: high. The root theme tokens are explicit in the HTML and CSS.

#### Core colors

- `color/bg/default = #323437`
- `color/surface/default = #2c2e31`
- `color/text/default = #d1d0c5`
- `color/text/subtle = #646669`
- `color/action/primary = #e2b714`
- `color/caret/default = #e2b714`
- `color/status/error = #ca4754`
- `color/status/error-subtle = #7e2a33`

#### Typography

Families:

- `Roboto Mono` as system default
- `Lexend Deca` for brand wordmark
- optional theme font system for user customization

Style direction:

- mono-first interface
- dense stats and controls
- dark terminal aesthetic with muted neutrals and one strong accent

#### Shape and layout

- `roundness = .5rem`
- content max width `1536`
- state changes mostly use `.125s` and `.25s`
- hover/focus frequently invert foreground/background
- solid buttons and text buttons share the same semantic token set

#### Component families

- filled button
- text button
- icon button
- modal/dialog
- checkbox
- select/dropdown
- text input / textarea
- avatar
- badge
- stats group
- table
- activity heatmap
- charts
- test-mode segmented controls
- typing stage with caret and live metrics

### 4. JPGLabs

Authoritative source quality: low-medium. The provided HTML exposes only inline Tailwind config plus body overrides. The referenced built CSS bundle was not available in the local file set.

#### Core colors

- `color/bg/default = #08090a`
- `color/surface/default = #111214`
- `color/border/default = #30363d`
- `color/text/default = #e6edf3`
- `color/action/primary = #3b82f6`

#### System notes

- `darkMode = 'class'`
- Tailwind-based implementation
- product-dark palette close to GitHub Dark / developer SaaS surfaces

#### Reliable extraction limit

Only the inline theme extension is authoritative from the provided file. Component-level extraction for this source remains incomplete until the missing built stylesheet or live app URL is available.

## Cross-Source Synthesis

### Shared primitives worth standardizing

- 4px spacing rhythm
- dark and light semantic surface layers
- a single error semantic family
- rounded controls for product UIs
- mono + display font pairings

### Theme split that should remain separate

- Google uses polished product UI with a complete semantic token graph
- Stripe uses editorial art direction with content-colored cards
- Monkeytype uses terminal utility UI with high-frequency state transitions
- JPGLabs is a minimal dark SaaS product shell

## Recommended Typography Style Groups

- `Google/Display/*`
- `Google/Body/*`
- `Stripe/Headline/*`
- `Stripe/Reading/*`
- `Monkeytype/Mono/*`
- `Monkeytype/Brand/*`
- `JPGLabs/Product/*` once the missing CSS is available

## Recommended Component Pages in Figma

- `Google/Button`
- `Google/Nav Pill`
- `Google/Card`
- `Google/Carousel Controls`
- `Google/Footer Link Group`
- `Stripe/Product Card`
- `Stripe/Editorial Header`
- `Stripe/Newsletter Form`
- `Stripe/Overlay Navigation`
- `Monkeytype/Button`
- `Monkeytype/Text Button`
- `Monkeytype/Input`
- `Monkeytype/Modal`
- `Monkeytype/Stats Block`
- `Monkeytype/Segmented Control`
- `Monkeytype/Badge`
- `JPGLabs/Button`
- `JPGLabs/Card`
- `JPGLabs/Bordered Panel`

## Gaps and Risks

- JPGLabs component extraction is partial because the built CSS bundle was not available with the provided file.
- Stripe colors mix interface tokens and content/cover art colors; these must be separated before building primitives.
- Google already contains a mature design token system and should be treated as the strongest source of semantic structure.
- Monkeytype contains a mature runtime theme system and is the strongest source for dark utility-product patterns.

## Build Recommendation

If this is turned into a Figma library, use this order:

1. Create `Primitives`, `Color`, `Spacing`, `Radius`, and `Motion`.
2. Add 4 modes to `Color`.
3. Create typography styles grouped by theme.
4. Build shared primitives first: button, input, card, nav pill, badge, modal.
5. Split the library into product vs editorial component families instead of forcing one visual language.
