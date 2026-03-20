# 📱 PiPhone — UX Design System
> AwesomePie iOS · Visual identity derived from JPGLabs portfolio
> Owner: Jader Philipe Germano · Stack: Native Swift · iOS 26.4
> Version: 2.x design target (updating from v2.1)

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Native first** | Pure Apple SDK. No Electron, no React Native. UIKit + SwiftUI only. |
| **Intelligence visible** | The AI tier being used is always surfaced. Never hide latency. |
| **Voice as a first-class citizen** | Waveform is never decorative — it maps real audio amplitude. |
| **Dark by default** | Dark theme as primary. Light theme is opt-in, not afterthought. |
| **Glassmorphism with restraint** | Only on overlays and settings panels. Not on primary content. |
| **Zero brand noise** | No loud gradients on chat. Minimal chrome. Content is the UI. |

---

## 2. Color Tokens

### Base Palette

```
Background
  --bg-primary:      #0A0A0F   (deepest surface — chat base)
  --bg-secondary:    #111118   (card surfaces)
  --bg-elevated:     #1A1A26   (modals, sheets)
  --bg-glass:        rgba(20, 20, 35, 0.72) + blur(24px)  ← glassmorphism

Accent — Pi Blue (brand)
  --accent-primary:  #4F8EF7   (active state, CTA, tier indicator)
  --accent-soft:     rgba(79, 142, 247, 0.15)             ← chip backgrounds
  --accent-glow:     rgba(79, 142, 247, 0.08)             ← waveform glow

Status
  --status-local:    #34C759   (green  — tiers 1-2 local Ollama)
  --status-vps:      #FF9F0A   (amber  — tier 3 VPS)
  --status-openai:   #10A37F   (teal   — tiers 4-5 OpenAI)
  --status-gemini:   #4285F4   (blue   — tiers 6-7 Gemini)
  --status-claude:   #D97706   (gold   — tier 8 Anthropic)
  --status-error:    #FF453A   (red    — offline / timeout)

Text
  --text-primary:    #F2F2F7   (iOS system label equivalent)
  --text-secondary:  #8E8E98   (secondary label)
  --text-muted:      #48484F   (placeholder, disabled)

Borders
  --border-subtle:   rgba(255, 255, 255, 0.06)
  --border-active:   rgba(79, 142, 247, 0.40)
```

### Tier Indicator Pill Colors

| Tier | Label | Color token |
|------|-------|-------------|
| 1–2 | Local | `--status-local` |
| 3 | VPS | `--status-vps` |
| 4–5 | OpenAI | `--status-openai` |
| 6–7 | Gemini | `--status-gemini` |
| 8 | Claude | `--status-claude` |
| — | Offline | `--status-error` |

---

## 3. Typography

```
Font family: SF Pro (system) — no custom fonts

Scale (Dynamic Type compatible):
  Display:    SF Pro Display  · 34pt · weight .bold
  Title1:     SF Pro Display  · 28pt · weight .semibold
  Title2:     SF Pro Text     · 22pt · weight .semibold
  Headline:   SF Pro Text     · 17pt · weight .semibold
  Body:       SF Pro Text     · 17pt · weight .regular
  Callout:    SF Pro Text     · 16pt · weight .regular
  Subhead:    SF Pro Text     · 15pt · weight .regular
  Footnote:   SF Pro Text     · 13pt · weight .regular
  Caption:    SF Pro Text     · 12pt · weight .regular  ← tier label, timestamp
  Caption2:   SF Pro Text     · 11pt · weight .regular
```

---

## 4. Spacing & Layout

```
Grid: 8pt base unit
  xs:   4pt
  sm:   8pt
  md:  16pt
  lg:  24pt
  xl:  32pt
  2xl: 48pt

Corner radius:
  pill:   999pt  (chips, tier badge)
  card:    16pt  (bubble, sheet)
  modal:   24pt  (bottom sheet)
  icon:    12pt  (app icon inset)

Safe areas: always respect UIEdgeInsets — no content under Dynamic Island
```

---

## 5. Component Inventory

### 5.1 TierIndicatorView
Small pill showing the active AI provider.

```
┌─────────────────────────┐
│ ● Local  qwen2.5-coder  │  ← green dot + model name + latency
└─────────────────────────┘
State variants: local | vps | openai | gemini | claude | offline | loading
```

### 5.2 WaveformView
Real-time amplitude bars during voice input.

```
     │   │
   │ │ │ │ │
 │ │ │ │ │ │ │
─────────────────
 ← 32 bars, height maps to Float amplitude, color = --accent-primary
 Idle state: flat line at 20% height, opacity 0.3
 Active state: full animation, glow shadow rgba(79,142,247,0.4)
```

### 5.3 BubbleShape
Chat message container.

```
User bubble:
┌──────────────────────────┐
│ message text here        │  bg: --accent-soft, leading edge square
└──────────────────────────┘

Pi bubble:
┌──────────────────────────┐
│ response text            │  bg: --bg-secondary, trailing edge square
│ with inline markdown     │
└──────────────────────────┘
  Timestamp + tier badge below, right-aligned
```

### 5.4 QuickChipView
Horizontally scrollable suggestion chips on welcome screen.

```
┌──────────┐ ┌─────────────────┐ ┌──────────────┐
│ 💡 Explain│ │ 🔧 Debug my code│ │ 📝 Summarize │
└──────────┘ └─────────────────┘ └──────────────┘
bg: --accent-soft  border: --border-active  text: --accent-primary
```

### 5.5 GlassSettingsPanel (bottom sheet)
Settings overlay with glassmorphism background.

```
╔══════════════════════════════════╗
║  Settings                  ✕    ║  ← blurred bg behind
╠══════════════════════════════════╣
║  Provider        [Local    ▾]   ║
║  Model           [qwen2.5  ▾]   ║
║  ─────────────────────────────  ║
║  API Keys                       ║
║  OpenAI     [●●●●●●    Test]    ║
║  Gemini     [not set   Add ]    ║
║  Anthropic  [●●●●●●    Test]    ║
║  ─────────────────────────────  ║
║  Voice      [ ON  ●────────]    ║
║  Theme      [Dark  ●───────]    ║
╚══════════════════════════════════╝
```

---

## 6. Screen Map

```
App Launch
    │
    ▼
[SplashView]  0.6s · Pi logo pulse animation
    │
    ├── First run ──► [WelcomeView]
    │                      │
    │               Quick chips + tagline
    │                      │
    └── Returning ──► [ChatView] ◄──────────────────┐
                           │                         │
                     Input bar (bottom)              │
                     [🎙 hold] [text field] [▶ send] │
                           │                         │
                     [VoiceOverlayView]               │
                       WaveformView                  │
                       Transcript live               │
                       Cancel / Send               ──┘
                           │
                     [TierIndicatorView] ← always visible top-right
                           │
                     [GlassSettingsPanel] ← swipe up from input bar
```

---

## 7. Screen Wireframes

### 7.1 WelcomeView

```
┌─────────────────────────────────┐
│                                 │  ← status bar
│                                 │
│            🥧                   │
│          AwesomePie             │  Title1 · --text-primary
│    Your local-first AI          │  Subhead · --text-secondary
│                                 │
│  ─────────────────────────────  │
│  Try asking...                  │  Caption · --text-muted
│                                 │
│  ┌──────────┐ ┌──────────────┐  │
│  │💡 Explain│ │🔧 Debug code │  │  QuickChipView
│  └──────────┘ └──────────────┘  │
│  ┌──────────┐ ┌──────────────┐  │
│  │📝 Summary│ │🌐 Translate  │  │
│  └──────────┘ └──────────────┘  │
│                                 │
│  ─────────────────────────────  │
│  [🎙]  Ask me anything...  [▶] │  ← input bar · --bg-elevated
└─────────────────────────────────┘
```

### 7.2 ChatView (active session)

```
┌─────────────────────────────────┐
│  AwesomePie      ● Local  14ms  │  ← nav + TierIndicatorView
├─────────────────────────────────┤
│                                 │
│              ┌──────────────┐   │
│              │ Hello! What  │   │  User bubble · right-aligned
│              │ is CQRS?     │   │
│              └──────────────┘   │
│                          12:01  │
│                                 │
│  ┌──────────────────────────┐   │
│  │ CQRS (Command Query      │   │  Pi bubble · left-aligned
│  │ Responsibility Segre...  │   │
│  │ **Command** — mutates    │   │  InlineMarkdownText
│  │ **Query** — reads only   │   │
│  └──────────────────────────┘   │
│  ● Local · qwen2.5-coder  12:01 │  ← tier badge below bubble
│                                 │
├─────────────────────────────────┤
│  [🎙]  Message...          [▶] │
└─────────────────────────────────┘
```

### 7.3 VoiceOverlayView

```
┌─────────────────────────────────┐
│                                 │
│                                 │
│   ┌─────────────────────────┐   │
│   │  ╔═══════════════════╗  │   │  ← glass card
│   │  ║  Listening...     ║  │   │
│   │  ║                   ║  │   │
│   │  ║  ▁▂▄▇▅▃▂▁▄▇▅▃▁   ║  │   │  WaveformView
│   │  ║                   ║  │   │
│   │  ║  "What is the..." ║  │   │  live transcript
│   │  ╚═══════════════════╝  │   │
│   └─────────────────────────┘   │
│                                 │
│         [  Cancel  ]            │
│         [  Send ▶  ]            │  ← appears after 0.5s silence
│                                 │
└─────────────────────────────────┘
  bg: --bg-primary opacity 0.92 + blur
```

---

## 8. Motion & Interaction

| Element | Animation | Duration | Curve |
|---------|-----------|----------|-------|
| App launch logo | Scale 0.8→1.0 + opacity 0→1 | 400ms | easeOut |
| Bubble appear | Slide up 8pt + opacity 0→1 | 280ms | spring(0.7) |
| Tier badge change | Cross-fade | 200ms | easeInOut |
| WaveformView bars | Per-bar height lerp | 60fps | linear |
| Voice overlay | Sheet slide up | 350ms | spring(0.8) |
| Quick chips | Staggered fade-in | 40ms delay per chip | easeOut |
| Settings panel | Blur materialize | 300ms | easeInOut |

---

## 9. Accessibility

- All interactive elements: minimum 44×44pt touch target
- Dynamic Type: all text uses SF Pro system scale — no fixed sizes in pt literals
- VoiceOver labels on WaveformView: `"Listening, audio level N%"`
- TierIndicatorView: `accessibilityLabel = "Using \(provider), \(latency) milliseconds"`
- Color is never the sole indicator of state — always paired with text or icon

---

## 10. Implementation Map (ThemeKit)

```swift
// Token references in SwiftUI
struct ThemeKit {
    struct Color {
        static let bgPrimary    = Color("bg-primary")      // Assets.xcassets
        static let accentPrimary = Color("accent-primary")
        static let tierLocal    = Color("status-local")
        static let tierVPS      = Color("status-vps")
        static let tierOpenAI   = Color("status-openai")
        static let tierGemini   = Color("status-gemini")
        static let tierClaude   = Color("status-claude")
    }

    struct Radius {
        static let pill:   CGFloat = 999
        static let card:   CGFloat = 16
        static let modal:  CGFloat = 24
    }

    struct Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }
}
```

---

## 11. Update Phase Scope (v2.x)

| Screen | Status | Notes |
|--------|--------|-------|
| WelcomeView | ✅ Exists | Validate quick chips design matches tokens above |
| ChatView + BubbleShape | ✅ Exists | Add tier badge below Pi bubbles |
| WaveformView | ✅ Exists | Confirm glow shadow on active state |
| GlassSettingsPanel | ✅ Exists | Add API key status rows (OpenAI / Gemini) |
| TierIndicatorView | 🟡 Inferred | Verify it surfaces tier + latency |
| SplashView | 🟡 Inferred | Confirm pulse animation |
| VoiceOverlayView | 🟡 Inferred | Confirm cancel/send CTA timing |
| ThemeKit tokens | ⚠️ Formalize | Align with tokens defined in section 2 |

---

_Created: 2026-03-19 · Branch: claude/piphone-ux-design-uZs8j_
_Source: JPGLabs portfolio identity + AwesomePie iOS v2.1 observed patterns_
