# Nav-Menu and Breadcrumb Logic

## Problem Description

Pages across the site had inconsistent navigation menu and breadcrumb structures. Some pages had:
- Multiple duplicate/malformed nav-menus
- Breadcrumbs in wrong positions (after nav-menu instead of before)
- Incorrect breadcrumb paths
- Nav-menus showing wrong sections (e.g., "about PIANDT" under "units")
- Missing nested menu structures
- Broken logo links (incorrect relative paths)

## Root Cause

The navigation structure was not following a consistent pattern. Each page should show:
1. **Breadcrumb**: The hierarchical path showing where you are in the site structure
2. **Nav-menu**: The section-specific menu showing children of the current section

## Solution Overview

### Key Principles

1. **Breadcrumb shows the path hierarchy**: Always shows the full path from the main triad page to the current page
2. **Nav-menu shows section children**: Shows only the children of the section you're currently in
3. **Position matters**: Breadcrumb comes AFTER logo-container, BEFORE nav-menu
4. **Relative paths**: All links must use correct relative paths based on file location

## Technical Implementation

### Structure Pattern

```html
<nav class="navbar">
    <div class="nav-container">
        <div class="logo-container">
            <a href="[CORRECT_RELATIVE_PATH]/index.html" class="logo">PI<span class="logo-and">and</span>T</a>
            <!-- logo subtitle -->
        </div>
        
        <!-- BREADCRUMB: After logo-container, before nav-menu -->
        <span class="logo-suffix">
            <a href="[PATH_TO_TRIAD].html">[Triad Name]</a>
            -&gt;<a href="[PATH_TO_SECTION].html">[Section Name]</a>
            <!-- Add more levels as needed -->
        </span>
        
        <!-- NAV-MENU: Shows children of current section -->
        <ul class="nav-menu">
            <li class="dropdown">
                <a href="[CURRENT_SECTION].html" class="nav-link">[Section Name] <span class="dropdown-arrow">▼</span></a>
                <ul class="dropdown-menu">
                    <!-- Children of current section -->
                </ul>
            </li>
        </ul>
        
        <!-- Theme toggle and hamburger -->
    </div>
</nav>
```

### Breadcrumb Logic

The breadcrumb shows the hierarchical path from the main triad page to the current page:

**Examples:**
- Main page: `Proc` (just the triad)
- Section page: `Proc -> about PIANDT` or `Proc -> units`
- Section child page: `Proc -> about PIANDT -> our mission and vision` or `Proc -> about PIANDT -> charitable purposes`
- Sub-section page: `Proc -> units -> machine intelligence`
- Deep page: `Proc -> units -> machine intelligence -> vision -> products -> software`
- Deep child page: `Proc -> units -> machine intelligence -> vision -> services -> R&D`

**Path Calculation:**
- From `processing/units/miu/proc_miu.html` to `processing.html`: `../../processing.html` (up 2 levels)
- From `processing/units/miu/vision/proc_miu_vision.html` to `processing.html`: `../../../processing.html` (up 3 levels)
- From `processing/units/miu/vision/products/proc_miu_vision_products.html` to `processing.html`: `../../../../processing.html` (up 4 levels)

### Nav-Menu Logic

The nav-menu shows **only the children of the section you're currently in**:

**Examples:**
- On `proc_units.html` (units section): Shows "units" dropdown with "machine intelligence" as child
- On `proc_about_piandt.html` (about_piandt section): Shows "about PIANDT" dropdown with its children (mission_vision, charitable_purposes, etc.)
- On `proc_miu.html` (machine intelligence section): Shows "machine intelligence" dropdown with "vision" as child
- On `proc_miu_vision.html` (vision section): Shows "vision" dropdown with "products" and "services" as children
- On `proc_miu_vision_products.html` (products section): Shows "products" dropdown with "software" and "hardware" as children

**Important Rules:**
1. **Never show sibling sections**: "about PIANDT" should NOT appear under "units" (they are siblings, not parent-child)
2. **Show only direct children**: If you're in "units", show "machine intelligence", not "vision" (vision is a child of machine intelligence, not units)
3. **Include nested structure**: When showing children, include their full nested structure (e.g., vision -> products -> software/hardware)

### Logo Link Logic

The logo should always link to the root `index.html`. Calculate the relative path based on file depth:

**Path Calculation:**
- From root: `index.html`
- From `processing/`: `../index.html` (up 1 level)
- From `processing/units/`: `../../index.html` (up 2 levels)
- From `processing/units/miu/`: `../../../index.html` (up 3 levels)
- From `processing/units/miu/vision/`: `../../../../index.html` (up 4 levels)
- From `processing/units/miu/vision/products/`: `../../../../../index.html` (up 5 levels)

**Formula:** Count the number of directories in the path, that's how many `../` you need.

## Step-by-Step Fix Process

### 1. Identify Page Location
Determine:
- Which triad? (in, processing, out)
- Which section? (about_piandt, units, etc.)
- What depth? (main page, section page, sub-section, etc.)

### 2. Calculate Breadcrumb
- Start with the triad name and link
- Add each section level in the hierarchy
- Use correct relative paths for each level

### 3. Determine Nav-Menu Content
- Identify the current section
- Find all direct children of that section
- Build nested structure if children have sub-children

### 4. Fix Logo Link
- Count directory depth
- Use that many `../` to reach root `index.html`

### 5. Clean Up
- Remove all duplicate/malformed nav-menus
- Remove breadcrumbs in wrong positions
- Ensure only ONE nav-menu remains
- Ensure breadcrumb is in correct position (after logo-container, before nav-menu)

## Examples

### Example 1: Main Triad Page
**File:** `processing/processing.html`

**Breadcrumb:**
```html
<span class="logo-suffix"><a href="processing.html">Proc</a></span>
```

**Nav-Menu:**
```html
<ul class="nav-menu">
    <li class="dropdown">
        <a href="processing.html" class="nav-link">Proc <span class="dropdown-arrow">▼</span></a>
        <ul class="dropdown-menu">
            <li>
                <a href="about_piandt/proc_about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                <ul>
                    <li><a href="about_piandt/proc_mission_vision.html" class="submenu-link">our mission and vision</a></li>
                    <!-- ... other children ... -->
                </ul>
            </li>
            <li>
                <a href="units/proc_units.html" class="dropdown-link">units <span class="dropdown-arrow">▶</span></a>
            </li>
        </ul>
    </li>
</ul>
```

**Logo Link:** `../index.html` (up 1 level from `processing/`)

### Example 2: Section Page
**File:** `processing/units/proc_units.html`

**Breadcrumb:**
```html
<span class="logo-suffix">
    <a href="../processing.html">Proc</a>
    -&gt;<a href="proc_units.html">units</a>
</span>
```

### Example 2a: Section Child Page
**File:** `processing/about_piandt/proc_mission_vision.html`

**Breadcrumb:**
```html
<span class="logo-suffix">
    <a href="../processing.html">Proc</a>
    -&gt;<a href="proc_about_piandt.html">about PIANDT</a>
    -&gt;<a href="proc_mission_vision.html">our mission and vision</a>
</span>
```

**Note:** Child pages must include the final page name in the breadcrumb, matching the pattern used for deep nested pages (e.g., services -> R&D).

**Nav-Menu:**
```html
<ul class="nav-menu">
    <li class="dropdown">
        <a href="proc_units.html" class="nav-link">units <span class="dropdown-arrow">▼</span></a>
        <ul class="dropdown-menu">
            <li>
                <a href="miu/proc_miu.html" class="dropdown-link">machine intelligence <span class="dropdown-arrow">▶</span></a>
                <ul>
                    <li>
                        <a href="miu/vision/proc_miu_vision.html" class="submenu-link">vision <span class="dropdown-arrow">▶</span></a>
                        <ul>
                            <!-- nested structure -->
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
```

**Logo Link:** `../../index.html` (up 2 levels from `processing/units/`)

### Example 3: Deep Page
**File:** `processing/units/miu/vision/products/proc_miu_vision_products_software.html`

**Breadcrumb:**
```html
<span class="logo-suffix">
    <a href="../../../../processing.html">Proc</a>
    -&gt;<a href="../../../proc_units.html">units</a>
    -&gt;<a href="../../proc_miu.html">machine intelligence</a>
    -&gt;<a href="../proc_miu_vision.html">vision</a>
    -&gt;<a href="proc_miu_vision_products.html">products</a>
    -&gt;<a href="proc_miu_vision_products_software.html">software</a>
</span>
```

**Nav-Menu:**
```html
<ul class="nav-menu">
    <li class="dropdown">
        <a href="proc_miu_vision_products.html" class="nav-link">products <span class="dropdown-arrow">▼</span></a>
        <ul class="dropdown-menu">
            <li><a href="proc_miu_vision_products_software.html" class="dropdown-link">software</a></li>
            <li><a href="proc_miu_vision_products_hardware.html" class="dropdown-link">hardware</a></li>
        </ul>
    </li>
</ul>
```

**Logo Link:** `../../../../../index.html` (up 6 levels from `processing/units/miu/vision/products/`)

## Common Mistakes to Avoid

1. **Putting breadcrumb in wrong position**: Must be AFTER logo-container, BEFORE nav-menu
2. **Showing sibling sections**: Don't show "about PIANDT" under "units" - they're siblings
3. **Incorrect relative paths**: Count directory levels carefully
4. **Missing nested structure**: Include full nested menus for children
5. **Multiple nav-menus**: Remove all duplicates, keep only one
6. **Wrong logo path**: Logo must always link to root `index.html`
7. **Incomplete breadcrumbs for child pages**: Child pages must include the final page name in the breadcrumb (e.g., `Proc -> about PIANDT -> our mission and vision`, not just `Proc -> about PIANDT`)

## JavaScript Support

The `contextual-nav.js` file has been updated to recognize "about_piandt" section pages (similar to "units" section). This ensures the nav-menu is visible on about_piandt pages.

**Key Code:**
```javascript
if (currentSection === 'about_piandt' && (navLinkText.includes('about piandt') || navLinkText.includes('about_piandt'))) {
    // This is the about_piandt section menu - always show it
    dropdown.style.display = '';
}
```

## Testing Checklist

For each page, verify:
- [ ] Breadcrumb shows correct hierarchical path
- [ ] Breadcrumb includes final page name for child pages (e.g., `Proc -> about PIANDT -> our mission and vision`)
- [ ] Breadcrumb links work correctly
- [ ] Nav-menu shows only children of current section
- [ ] Nav-menu nested structure is complete
- [ ] Logo link works (goes to root index.html)
- [ ] Only ONE nav-menu exists
- [ ] Breadcrumb is positioned correctly (after logo-container, before nav-menu)
- [ ] No duplicate or malformed nav-menus
- [ ] All relative paths are correct

## Files Modified

### JavaScript Files
- `contextual-nav.js` - Added support for "about_piandt" section recognition

### HTML Files (Examples)
- `processing/about_piandt/proc_about_piandt.html`
- `processing/about_piandt/proc_mission_vision.html`
- `processing/about_piandt/proc_charitable_purposes.html`
- `processing/about_piandt/proc_our_approach.html`
- `processing/about_piandt/proc_trustees.html`
- `processing/about_piandt/proc_governance.html`
- `processing/processing.html`
- `processing/units/proc_units.html`
- `processing/units/miu/proc_miu.html`
- `processing/units/miu/vision/proc_miu_vision.html`
- `processing/units/miu/vision/products/proc_miu_vision_products.html`
- `processing/units/miu/vision/products/proc_miu_vision_products_software.html`
- `processing/units/miu/vision/products/proc_miu_vision_products_hardware.html`
- (And many more...)

## Future-Proofing

When adding new pages:
1. Follow the structure pattern exactly
2. Calculate relative paths based on file location
3. Show only direct children in nav-menu
4. Include full nested structure for children
5. Test breadcrumb and nav-menu functionality
6. Verify logo link works

## Related Fixes

- `navmenu_fix.md` - Navigation menu population logic
- `overflow_fix.md` - Menu overflow handling

---

**Last Updated:** December 2024
**Reference Page:** `processing/units/proc_units.html`

## Recent Fixes

### Breadcrumb Completeness for Child Pages (December 2024)
**Issue:** Breadcrumbs for about_piandt child pages were incomplete - they only showed `Proc -> about PIANDT` or `In -> about PIANDT` without the final page name, unlike services child pages which showed the full path (e.g., `Proc -> units -> machine intelligence -> vision -> services -> R&D`).

**Fix:** Updated all about_piandt child pages in both "processing" and "in" directories to include the final page name in the breadcrumb:
- `Proc -> about PIANDT -> our mission and vision`
- `Proc -> about PIANDT -> charitable purposes`
- `Proc -> about PIANDT -> our approach`
- `Proc -> about PIANDT -> trustees`
- `Proc -> about PIANDT -> governance`

Same pattern applied to "in" directory pages.

**Files Fixed:**
- `processing/about_piandt/proc_mission_vision.html`
- `processing/about_piandt/proc_charitable_purposes.html`
- `processing/about_piandt/proc_our_approach.html`
- `processing/about_piandt/proc_trustees.html`
- `processing/about_piandt/proc_governance.html`
- `in/about_piandt/in_mission_vision.html`
- `in/about_piandt/in_charitable_purposes.html`
- `in/about_piandt/in_our_approach.html`
- `in/about_piandt/in_trustees.html`
- `in/about_piandt/in_governance.html`
- `out/about_piandt/out_mission_vision.html`
- `out/about_piandt/out_charitable_purposes.html`
- `out/about_piandt/out_our_approach.html`
- `out/about_piandt/out_trustees.html`
- `out/about_piandt/out_governance.html`

## Complete Solution Applied (December 2024)

### Scope
Applied the nav-menu and breadcrumb logic from the reference page (`processing/units/proc_units.html`) to **all ~50+ pages** across the entire site:
- **Processing directory**: All pages in `processing/`, `processing/about_piandt/`, and `processing/units/` (including all nested pages)
- **In directory**: All pages in `in/`, `in/about_piandt/`, and `in/units/` (including all nested pages)
- **Out directory**: All pages in `out/`, `out/about_piandt/`, and `out/units/` (including all nested pages)

### Breadcrumb Path Patterns by Triad

#### Processing (Proc) Triad
- Main page (`processing/processing.html`): `processing.html`
- Section page (`processing/about_piandt/proc_about_piandt.html`): `../processing.html`
- Section child (`processing/about_piandt/proc_mission_vision.html`): `../processing.html`
- Units section (`processing/units/proc_units.html`): `../processing.html`
- Deep page (`processing/units/miu/vision/products/proc_miu_vision_products.html`): `../../../../processing.html`

#### In Triad
- Main page (`in/in.html`): `in.html`
- Section page (`in/about_piandt/in_about_piandt.html`): `../in.html`
- Section child (`in/about_piandt/in_mission_vision.html`): `../in.html`
- Units section (`in/units/in_units.html`): `../in.html`
- Deep page (`in/units/miu/vision/products/in_miu_vision_products.html`): `../../../../in.html`

#### Out Triad
- Main page (`out/out.html`): `out.html`
- Section page (`out/about_piandt/out_about_piandt.html`): `../out.html`
- Section child (`out/about_piandt/out_mission_vision.html`): `../out.html`
- Units section (`out/units/out_units.html`): `../out.html`
- Deep page (`out/units/miu/vision/products/out_miu_vision_products.html`): `../../../../out.html`

**Important:** Always use `../out.html` (not `../out/out.html`) for Out triad pages.

### Complete Examples by Triad

#### Example: In Triad - Section Child Page
**File:** `in/about_piandt/in_mission_vision.html`

**Breadcrumb:**
```html
<span class="logo-suffix">
    <a href="../in.html">In</a>
    -&gt;<a href="in_about_piandt.html">about PIANDT</a>
    -&gt;<a href="in_mission_vision.html">our mission and vision</a>
</span>
```

**Nav-Menu:**
```html
<ul class="nav-menu">
    <li class="dropdown">
        <a href="in_about_piandt.html" class="nav-link">about PIANDT <span class="dropdown-arrow">▼</span></a>
        <ul class="dropdown-menu">
            <li><a href="in_mission_vision.html" class="dropdown-link">our mission and vision</a></li>
            <li><a href="in_charitable_purposes.html" class="dropdown-link">charitable purposes</a></li>
            <li><a href="in_our_approach.html" class="dropdown-link">our approach</a></li>
            <li><a href="in_trustees.html" class="dropdown-link">trustees</a></li>
            <li><a href="in_governance.html" class="dropdown-link">governance</a></li>
        </ul>
    </li>
</ul>
```

**Logo Link:** `../../index.html` (up 2 levels from `in/about_piandt/`)

#### Example: Out Triad - Deep Page
**File:** `out/units/miu/vision/services/out_miu_vision_services_rd.html`

**Breadcrumb:**
```html
<span class="logo-suffix">
    <a href="../../../../out.html">Out</a>
    -&gt;<a href="../../../out_units.html">units</a>
    -&gt;<a href="../../out_miu.html">machine intelligence</a>
    -&gt;<a href="../out_miu_vision.html">vision</a>
    -&gt;<a href="out_miu_vision_services.html">services</a>
    -&gt;<a href="out_miu_vision_services_rd.html">R&amp;D</a>
</span>
```

**Nav-Menu:**
```html
<ul class="nav-menu">
    <li class="dropdown">
        <a href="out_miu_vision_services.html" class="nav-link">services <span class="dropdown-arrow">▼</span></a>
        <ul class="dropdown-menu">
            <li><a href="out_miu_vision_services_rd.html" class="dropdown-link">R&amp;D</a></li>
            <li><a href="out_miu_vision_services_consultancy.html" class="dropdown-link">consultancy</a></li>
            <li><a href="out_miu_vision_services_education.html" class="dropdown-link">education</a></li>
        </ul>
    </li>
</ul>
```

**Logo Link:** `../../../../../index.html` (up 5 levels from `out/units/miu/vision/services/`)

### Common Issues Found and Resolved

1. **Breadcrumb Path Errors**
   - **Issue**: Using `../out/out.html` instead of `../out.html`
   - **Fix**: Always use the triad name directly (e.g., `../out.html`, `../in.html`, `../processing.html`)

2. **Logo Link Depth Errors**
   - **Issue**: Using `../../index.html` for pages 5 levels deep
   - **Fix**: Count directory levels: 5 levels deep = `../../../../../index.html`

3. **Nav-Menu Showing Wrong Section**
   - **Issue**: Showing "units" nav-menu on "machine intelligence" pages
   - **Fix**: Show nav-menu for the current section only (e.g., "machine intelligence" on `proc_miu.html`)

4. **Sibling Sections in Nav-Menu**
   - **Issue**: "about PIANDT" appearing under "units" nav-menu
   - **Fix**: Remove sibling sections - they are not parent-child relationships

5. **Incomplete Breadcrumbs**
   - **Issue**: Child pages missing final page name (e.g., `Proc -> about PIANDT` instead of `Proc -> about PIANDT -> our mission and vision`)
   - **Fix**: Always include the final page name in breadcrumbs for child pages

6. **Duplicate Nav-Menus**
   - **Issue**: Multiple nav-menus (Proc, In, Out) on every page
   - **Fix**: Remove all duplicate/malformed nav-menus, keep only the section-specific one

7. **Breadcrumb Position**
   - **Issue**: Breadcrumb appearing after nav-menu or before logo-container
   - **Fix**: Always place breadcrumb after logo-container, before nav-menu

### Complete File List Fixed

**Processing Directory (18 pages):**
- `processing/processing.html`
- `processing/about_piandt/proc_about_piandt.html`
- `processing/about_piandt/proc_mission_vision.html`
- `processing/about_piandt/proc_charitable_purposes.html`
- `processing/about_piandt/proc_our_approach.html`
- `processing/about_piandt/proc_trustees.html`
- `processing/about_piandt/proc_governance.html`
- `processing/units/proc_units.html`
- `processing/units/miu/proc_miu.html`
- `processing/units/miu/vision/proc_miu_vision.html`
- `processing/units/miu/vision/products/proc_miu_vision_products.html`
- `processing/units/miu/vision/products/proc_miu_vision_products_software.html`
- `processing/units/miu/vision/products/proc_miu_vision_products_hardware.html`
- `processing/units/miu/vision/services/proc_miu_vision_services.html`
- `processing/units/miu/vision/services/proc_miu_vision_services_rd.html`
- `processing/units/miu/vision/services/proc_miu_vision_services_consultancy.html`
- `processing/units/miu/vision/services/proc_miu_vision_services_education.html`

**In Directory (18 pages):**
- `in/about_piandt/in_about_piandt.html`
- `in/about_piandt/in_mission_vision.html`
- `in/about_piandt/in_charitable_purposes.html`
- `in/about_piandt/in_our_approach.html`
- `in/about_piandt/in_trustees.html`
- `in/about_piandt/in_governance.html`
- `in/units/in_units.html`
- `in/units/miu/in_miu.html`
- `in/units/miu/vision/in_miu_vision.html`
- `in/units/miu/vision/products/in_miu_vision_products.html`
- `in/units/miu/vision/products/in_miu_vision_products_software.html`
- `in/units/miu/vision/products/in_miu_vision_products_hardware.html`
- `in/units/miu/vision/services/in_miu_vision_services.html`
- `in/units/miu/vision/services/in_miu_vision_services_rd.html`
- `in/units/miu/vision/services/in_miu_vision_services_consultancy.html`
- `in/units/miu/vision/services/in_miu_vision_services_education.html`

**Out Directory (18 pages):**
- `out/out.html`
- `out/about_piandt/out_about_piandt.html`
- `out/about_piandt/out_mission_vision.html`
- `out/about_piandt/out_charitable_purposes.html`
- `out/about_piandt/out_our_approach.html`
- `out/about_piandt/out_trustees.html`
- `out/about_piandt/out_governance.html`
- `out/units/out_units.html`
- `out/units/miu/out_miu.html`
- `out/units/miu/vision/out_miu_vision.html`
- `out/units/miu/vision/products/out_miu_vision_products.html`
- `out/units/miu/vision/products/out_miu_vision_products_software.html`
- `out/units/miu/vision/products/out_miu_vision_products_hardware.html`
- `out/units/miu/vision/services/out_miu_vision_services.html`
- `out/units/miu/vision/services/out_miu_vision_services_rd.html`
- `out/units/miu/vision/services/out_miu_vision_services_consultancy.html`
- `out/units/miu/vision/services/out_miu_vision_services_education.html`

**Total: 54 pages fixed**

### Quick Reference: Path Calculation Cheat Sheet

| File Location | Logo Link | Breadcrumb to Triad |
|--------------|-----------|---------------------|
| `[triad]/[triad].html` | `../index.html` | `[triad].html` |
| `[triad]/about_piandt/[page].html` | `../../index.html` | `../[triad].html` |
| `[triad]/units/[page].html` | `../../index.html` | `../[triad].html` |
| `[triad]/units/miu/[page].html` | `../../../index.html` | `../../[triad].html` |
| `[triad]/units/miu/vision/[page].html` | `../../../../index.html` | `../../../[triad].html` |
| `[triad]/units/miu/vision/products/[page].html` | `../../../../../index.html` | `../../../../[triad].html` |
| `[triad]/units/miu/vision/services/[page].html` | `../../../../../index.html` | `../../../../[triad].html` |

### Verification Steps

After fixing any page, verify:
1. Logo link works (click logo, should go to root `index.html`)
2. Breadcrumb shows complete path including final page name
3. Breadcrumb links work (each link in breadcrumb should navigate correctly)
4. Nav-menu shows only children of current section
5. Nav-menu nested structure is complete and visible on hover
6. No duplicate nav-menus exist
7. Breadcrumb is positioned correctly (after logo-container, before nav-menu)

