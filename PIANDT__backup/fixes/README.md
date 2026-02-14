# Fixes Documentation

This directory contains documentation for unique problems encountered and their solutions. This serves as a troubleshooting guide for future reference.

## Purpose

When solving unique problems that:
- Require non-obvious solutions
- Have specific implementation details
- Need to be maintained or extended in the future
- Could recur or be related to similar issues

...document them here for future reference.

## File Naming Convention

- Use descriptive, lowercase names with underscores
- Format: `[problem_area]_fix.md`
- Examples:
  - `overflow_fix.md` - Menu overflow detection and direction fix
  - `menu_hover_control_fix.md` - Menu hover behavior fixes
  - `contextual_nav_fix.md` - Contextual navigation fixes

## Documentation Template

Each fix document should include:

1. **Problem Description**
   - What was the issue?
   - Symptoms observed
   - When/where it occurred

2. **Root Cause**
   - Why did it happen?
   - Technical explanation

3. **Solution Overview**
   - High-level approach
   - Key principles

4. **Technical Implementation**
   - Code snippets
   - File locations
   - Configuration changes

5. **Future-Proofing**
   - How to prevent recurrence
   - Automatic detection mechanisms
   - Generic vs. specific solutions

6. **Testing**
   - How to verify the fix
   - Expected behavior

7. **Files Modified**
   - List of changed files
   - What changed in each

8. **Common Issues and Solutions**
   - Troubleshooting guide
   - Related problems

## Current Fixes

- **overflow_fix.md** - Menu overflow detection and direction fix
  - Prevents menus from extending beyond viewport
  - Automatically points menus leftward/rightward based on available space
  - Fully automatic for new pages/menus

- **navmenu_fix.md** - Navigation menu population fix
  - Ensures all nav-links show child menus from directory structure
  - Automatically populates menus based on actual files in directories
  - Works for all triads (In/Proc/Out) and all sections
  - Fully automatic - adapts to new pages without code changes

- **nav_menu_breadcrumb_logic.md** - Nav-menu and breadcrumb structure logic
  - Documents the correct structure pattern for nav-menus and breadcrumbs
  - Explains hierarchical breadcrumb path calculation
  - Details section-specific nav-menu logic (show only children of current section)
  - Provides step-by-step fix process and examples
  - Includes common mistakes to avoid and testing checklist

## Adding New Fixes

1. Create a new markdown file following the naming convention
2. Use the template structure above
3. Include code examples and explanations
4. Update this README with a brief description
5. Link to related fixes if applicable

---

**Last Updated:** 2024

