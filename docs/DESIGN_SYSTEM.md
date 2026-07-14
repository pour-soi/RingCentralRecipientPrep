# Pour Design System

Version 1.0

The Pour Design System defines the visual and interaction language for Pour desktop applications. It is a specification for future design and engineering work, not a reusable UI framework.

## 1. Philosophy

Pour applications should feel calm, professional, minimal, and efficient. The interface should make information easy to scan and actions easy to complete without visual noise.

Core principles:

- **Desktop-first:** Design for productive desktop use, not mobile-style simplification.
- **Information-focused:** Prioritize clear hierarchy, readable data, and efficient workflows.
- **Local-first:** Reinforce trust by making local data ownership and predictable behavior visible.
- **Calm and minimal:** Use restraint in color, shadow, borders, and motion.
- **Professional:** Every screen should feel stable, intentional, and production-ready.
- **Readable:** Text, tables, controls, and spacing must remain comfortable at common DPI settings.
- **Responsive:** Layouts should adapt continuously to available window size.
- **Consistent:** Shared patterns should behave the same across the Pour product family.

Avoid:

- Decorative clutter.
- Overly saturated color palettes.
- Marketing-style hero layouts inside tools.
- Abrupt layout jumps unless wrapping is genuinely necessary.
- Controls that require users to guess state or workflow.

## 2. Layout System

Pour desktop applications use a stable four-region structure:

```text
+--------------------------------------------------------------+
| Header                                                       |
+-------------------+------------------------------------------+
| Sidebar           | Main Content                             |
|                   |                                          |
|                   |                                          |
|                   |                                          |
+-------------------+------------------------------------------+
| Bottom Action Area                                           |
+--------------------------------------------------------------+
```

### Header

Purpose:

- Identify the application.
- Provide global search or global actions.
- Hold the most important primary command.

Hierarchy:

- Brand block appears first.
- Search or navigation controls occupy flexible space.
- Primary actions stay visible before secondary actions.

Spacing:

- Use 16-24 px outer padding.
- Use 8-12 px between related controls.
- Use 16 px between unrelated control groups.

### Sidebar

Purpose:

- Provide local navigation, grouping, or filters.
- Keep context visible while the user works.

Hierarchy:

- Section title at the top.
- Main navigation or group list fills the remaining height.
- Management actions are anchored near the bottom.

Proportions:

- Sidebar should be wide enough for labels but never dominate the window.
- Width adapts fluidly with the window.
- Long names should elide instead of forcing horizontal growth.

### Main Content

Purpose:

- Present the primary task surface.
- Show data, forms, table views, filters, and contextual actions.

Hierarchy:

- Page title and metadata first.
- Filters or toolbar controls second.
- Main data or empty state third.
- Contextual actions near the content they affect.

### Bottom Action Area

Purpose:

- Hold batch actions, status text, or workflow confirmation controls.
- Stay visually connected to the content, not floating independently.

Behavior:

- Align with the main content grid.
- Collapse or wrap only when necessary.
- Preserve readable button labels.

## 3. Responsive Layout Rules

Pour applications use one continuous fluid layout.

Rules:

- Do not create separate desktop and compact interfaces unless the workflow truly changes.
- Resize continuously as the window changes.
- Use proportional sizing for major regions.
- Prefer size policies, stretch factors, and calculated widths over fixed dimensions.
- Reduce flexible whitespace before reducing essential controls.
- Let dense content scroll when it cannot reasonably shrink further.
- Preserve the same visual hierarchy at all supported window sizes.

Responsive elements:

- **Sidebar:** Narrows gradually as the window narrows; labels elide when needed.
- **Main content:** Consumes remaining space and adapts margins and internal gaps.
- **Search:** Expands when space is available and compresses before actions are hidden.
- **Header actions:** Maintain consistent height; wrap only when necessary.
- **Filters:** Share available width fluidly and avoid oversized fixed fields.
- **Tables:** Redistribute column widths continuously; less important columns shrink first.
- **Margins:** Use larger margins on wide windows and smaller margins on compact windows.
- **Spacing:** Related controls remain grouped while global spacing compresses proportionally.

Logo rules:

- Preserve the original aspect ratio.
- Never crop, stretch, squash, rotate, recolor, or redraw.
- Keep the complete logo visible at all supported sizes.
- Size the logo according to available space and product hierarchy.
- Use optical alignment against nearby typography, not only image bounds.

## 4. Color System

Pour uses a light, restrained blue-gray palette. Colors should support information hierarchy rather than dominate it.

| Role | HEX | Usage |
| --- | --- | --- |
| Primary | `#4F83F1` | Primary buttons, active controls, key accents |
| Primary Hover | `#3F73E3` | Hover state for primary actions |
| Background | `#F6FAFF` | App background |
| Surface | `#FFFFFF` | Cards, panels, tables, dialogs |
| Surface Soft | `#F2F7FF` | Subtle toolbar and selected-row backgrounds |
| Border | `#D8E4F2` | Cards, inputs, table dividers |
| Border Strong | `#C4D3E6` | Focused controls and important separators |
| Text | `#17233A` | Primary text |
| Text Secondary | `#5E718C` | Labels, captions, metadata |
| Hover | `#EEF5FF` | Hover surfaces and list rows |
| Selection | `#E7F0FF` | Selected items and active sidebar rows |
| Success | `#1F8A4C` | Valid status, success messages |
| Success Surface | `#E4F7EC` | Success badge background |
| Warning | `#B7791F` | Warning text and icons |
| Warning Surface | `#FFF4D6` | Warning badge background |
| Error | `#D92D20` | Destructive actions and validation errors |
| Error Surface | `#FDECEC` | Error badge and destructive hover background |

## 5. Typography

Use the platform UI font where possible. On Windows, prefer Segoe UI. On macOS development builds, use the system UI font.

| Role | Size | Weight | Line Height | Notes |
| --- | ---: | ---: | ---: | --- |
| Window title | 24-28 px | 600 | 1.2 | Application or page-level title |
| Section title | 18-22 px | 600 | 1.25 | Main content section headings |
| Card title | 15-17 px | 600 | 1.3 | Panel and grouped content titles |
| Body | 13-14 px | 400 | 1.45 | Standard text |
| Caption | 11-12 px | 400-500 | 1.35 | Metadata, helper text, table labels |
| Button | 13-14 px | 500-600 | 1.2 | Command labels |
| Table header | 12-13 px | 600 | 1.2 | Column labels |
| Table cell | 13-14 px | 400-500 | 1.35 | Data rows |

Guidelines:

- Do not shrink text below readable desktop sizes to force fit.
- Use font weight and spacing before adding more color.
- Use ellipsis for long labels in constrained spaces.
- Keep letter spacing at the platform default.

## 6. Spacing System

Use a small, predictable spacing scale:

| Value | Usage |
| ---: | --- |
| 4 px | Tight icon-label gaps, fine table padding |
| 8 px | Related controls, checkbox-label gaps, compact row spacing |
| 12 px | Standard control gaps, toolbar spacing |
| 16 px | Section padding, card padding, form group gaps |
| 20 px | Header padding, medium page spacing |
| 24 px | Major section separation, large card padding |
| 32 px | Wide layout margins and major vertical rhythm |

Rules:

- Related controls should be closer than unrelated controls.
- Major sections should align to the same content grid.
- Avoid unique spacing values unless the component requires optical adjustment.
- Reduce margins fluidly at compact sizes before compressing controls.

## 7. Components

### Buttons

Purpose:

- Trigger commands and workflow actions.

Behavior:

- Primary buttons represent the main action.
- Secondary buttons support common actions.
- Destructive buttons must be visually distinct and require confirmation when data loss is possible.

Sizing:

- Standard height: 36-40 px.
- Compact height: no less than 32 px.
- Horizontal padding: 12-16 px.

States:

- Default, hover, pressed, focus, disabled, loading where applicable.

### Cards

Purpose:

- Group related content or repeated items.

Behavior:

- Cards should not be nested inside other cards.
- Use borders and subtle surfaces instead of heavy shadows.

Sizing:

- Radius: 8-12 px.
- Padding: 16-24 px depending on density.

States:

- Default, hover when clickable, selected when part of a selectable list.

### Sidebar

Purpose:

- Provide persistent navigation or group context.

Behavior:

- Active item is visually clear.
- Long labels elide with tooltips when practical.
- Counts align consistently.

Sizing:

- Width adapts with the window.
- Practical minimum should preserve icons, counts, and recognizable labels.

States:

- Default, hover, active, disabled, drag target where applicable.

### Header

Purpose:

- Provide brand identity, global search, and global commands.

Behavior:

- Brand area remains stable.
- Search and action controls resize with available width.
- Primary action remains easy to find.

Sizing:

- Header height should be driven by content and padding, not arbitrary fixed values.

States:

- Search focus, action hover, disabled actions where appropriate.

### Toolbar

Purpose:

- Group controls that affect the current view.

Behavior:

- Controls should be visually grouped by purpose.
- Toolbars may wrap if width is constrained.

Sizing:

- Controls share consistent height.
- Gaps use 8-12 px for related groups and 16 px between groups.

States:

- Default, hover, focus, disabled.

### Search

Purpose:

- Filter or locate information quickly.

Behavior:

- Search should be responsive and stretchable.
- Placeholder text must be concise.
- Results should update predictably.

Sizing:

- Minimum width should preserve usability.
- Maximum width should avoid swallowing unrelated controls.

States:

- Empty, focused, active query, no results, disabled.

### Tables

Purpose:

- Present dense structured data.

Behavior:

- Tables should consume available width.
- Important columns stay readable.
- Less important columns shrink and elide first.

Sizing:

- Row height: 44-52 px.
- Header height: 40-44 px.

States:

- Default row, hover row, selected/checked row, sorted column, disabled row.

### Dialogs

Purpose:

- Confirm decisions, collect focused input, or show important information.

Behavior:

- Keep dialogs focused on one task.
- Destructive confirmations must describe the consequence.
- Dialogs should not inherit main-window minimum-size constraints.

Sizing:

- Width should fit content with reasonable max width.
- Use 20-24 px padding.

States:

- Open, focused control, validation error, disabled action, loading where applicable.

### Status Bar

Purpose:

- Provide low-priority status, counts, or feedback.

Behavior:

- Status text should not compete with primary actions.
- Use concise messages.

Sizing:

- Height: 32-40 px.
- Align to the same content grid as the main area.

States:

- Neutral, success, warning, error.

### Checkboxes

Purpose:

- Represent binary state or item inclusion.

Behavior:

- Use checked state as the source of truth where checkboxes drive bulk actions.
- Keep checkbox hit areas comfortable.

Sizing:

- Visual box: 16-20 px.
- Hit area: at least 32 px.

States:

- Unchecked, checked, indeterminate, hover, focus, disabled.

### Combo Boxes

Purpose:

- Choose one value from a compact list.

Behavior:

- Labels should be clear and adjacent.
- Values may elide when space is constrained.

Sizing:

- Height: 36-40 px.
- Width should adapt to layout context.

States:

- Closed, open, hover, focus, disabled.

### Text Fields

Purpose:

- Capture short text, numbers, or structured input.

Behavior:

- Use clear placeholders.
- Validate where the user can act on feedback.

Sizing:

- Height: 36-40 px.
- Padding: 10-12 px horizontal.

States:

- Empty, focused, filled, error, disabled.

### Empty State

Purpose:

- Explain why content is missing and offer the next useful action.

Behavior:

- Differentiate between truly empty data and filtered no-results states.
- Keep copy short.
- Show primary actions when they help the user proceed.

Sizing:

- Center within available content area using layouts.
- Avoid fake centering with fixed margins.

States:

- Empty database, no search results, unavailable content, loading failure.

## 8. Tables

Table specifications:

- **Row height:** 44-52 px depending on content density.
- **Header height:** 40-44 px.
- **Header alignment:** Match the alignment of cell content below.
- **Checkbox alignment:** Center horizontally and vertically in the select column.
- **Column resizing:** Fixed for selection, minimum readable width for identity columns, stretch for notes/details.
- **Selection:** Checked state and row selection should be visually distinct when both exist.
- **Hover:** Use a subtle surface change, not strong color.
- **Sorting:** Indicate active sort through the header control or sort icon.
- **Responsive behavior:** Shrink secondary columns first; preserve identity columns and action affordances.
- **Overflow:** Prefer cell elision and table scrolling over forcing the entire window wider.

Recommended column strategy:

```text
Select      fixed
Identity    flexible minimum
Category    content-aware, elides when needed
Details     stretch
Status      content-aware
Actions     fixed or content-aware
```

## 9. Icons

Icon style:

- Stroke-based icons.
- Rounded line joins and caps where available.
- Consistent optical size.
- Minimal filled icons only for strong status or brand moments.

Recommended sizes:

- 16 px for compact table or inline icons.
- 18-20 px for toolbar and button icons.
- 24 px for sidebar section or empty-state icons.

Alignment:

- Icons align to text optical center.
- Icon-label gap: 6-8 px.
- Icon-only buttons require accessible labels or tooltips.

## 10. Motion

Motion should be minimal and functional.

Preferred durations:

- Hover and focus transitions: 100-150 ms.
- Panel or menu appearance: 120-180 ms.
- State changes that need attention: 150-220 ms.

Rules:

- Do not animate layout in ways that make controls feel unstable.
- Avoid decorative motion.
- Respect platform accessibility settings where possible.
- Instant response is preferred for data-heavy workflows.

## 11. Naming Convention

Future reusable widgets should use the `P` prefix:

- `PButton`
- `PCard`
- `PSidebar`
- `PHeader`
- `PTable`
- `PSearchBar`
- `PDialog`
- `PToolbar`
- `PStatusBar`

Guidelines:

- Names should describe reusable component roles, not one application feature.
- Component APIs should separate visual styling from business behavior.
- Naming should remain stable across Pour applications.

## 12. Future PourUI

This document can later become a shared `PourUI/` package, but no framework should be created until multiple applications need the same implementation.

Possible future structure:

```text
PourUI/
  theme.py
  layout.py
  widgets/
    button.py
    card.py
    sidebar.py
    header.py
    table.py
    search.py
    dialog.py
  components/
    empty_state.py
    action_bar.py
    filter_toolbar.py
```

Responsibilities:

- `theme.py`: colors, typography, radius, shadows, states.
- `layout.py`: spacing scale, responsive sizing helpers, content grid rules.
- `widgets/`: low-level reusable controls.
- `components/`: composed UI patterns shared across applications.

Until then, each application should follow this specification directly.

## 13. Future Applications

Every future Pour application should inherit this design language so the product family feels coherent.

Examples:

- **PourSend:** Recipient preparation and group management.
- **PourInput:** Local-first structured input workflows.
- **PourClip:** Clipboard preparation and transformation utilities.
- **PourFlow:** Desktop workflow organization.
- **PourForm:** Form preparation and local data collection.

Family rules:

- Use the same visual hierarchy.
- Use the same spacing and typography scale.
- Use the same desktop-first interaction patterns.
- Preserve local-first clarity.
- Let each app have its own workflow while still feeling unmistakably Pour.
