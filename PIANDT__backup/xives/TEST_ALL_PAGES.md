# Interactive Page Testing Guide

## Summary
- **IN**: 32 files ✅
- **PROCESSING**: 32 files ✅  
- **OUT**: 32 files ✅
- **Total**: 96 HTML files

All files have:
- Multi-sheet pagination (4 columns per sheet)
- ~75 words per paragraph
- Each paragraph fits in one column only
- Chat agent visible
- No redundant pages

## Quick Test URLs

### IN Directory (32 files)
1. http://localhost:8000/in/in.html
2. http://localhost:8000/in/about_piandt/in_about_piandt.html
3. http://localhost:8000/in/about_piandt/in_charitable_purposes.html
4. http://localhost:8000/in/about_piandt/in_governance.html
5. http://localhost:8000/in/about_piandt/in_mission_vision.html
6. http://localhost:8000/in/about_piandt/in_our_approach.html
7. http://localhost:8000/in/about_piandt/in_trustees.html
8. http://localhost:8000/in/piandt/in_about_piandt.html
9. http://localhost:8000/in/piandt/in_charitable_purposes.html
10. http://localhost:8000/in/piandt/in_mission_vision.html
11. http://localhost:8000/in/piandt/in_our_approach.html
12. http://localhost:8000/in/units/in_units.html
13. http://localhost:8000/in/units/miu/in_miu.html
14. http://localhost:8000/in/units/miu/vision/in_miu_vision.html
15. http://localhost:8000/in/units/miu/vision/products/in_miu_vision_products.html
16. http://localhost:8000/in/units/miu/vision/products/in_miu_vision_products_hardware.html
17. http://localhost:8000/in/units/miu/vision/products/in_miu_vision_products_software.html
18. http://localhost:8000/in/units/miu/vision/services/in_miu_vision_services.html
19. http://localhost:8000/in/units/miu/vision/services/in_miu_vision_services_consultancy.html
20. http://localhost:8000/in/units/miu/vision/services/in_miu_vision_services_education.html
21. http://localhost:8000/in/units/miu/vision/services/in_miu_vision_services_rd.html
22. http://localhost:8000/in/miu/in_miu.html
23. http://localhost:8000/in/miu/in_miu_products.html
24. http://localhost:8000/in/miu/in_miu_services.html
25. http://localhost:8000/in/miu/in_miu_vision.html
26. http://localhost:8000/in/miu/in_miu_vision_products.html
27. http://localhost:8000/in/miu/in_miu_vision_products_hardware.html
28. http://localhost:8000/in/miu/in_miu_vision_products_software.html
29. http://localhost:8000/in/miu/in_miu_vision_services.html
30. http://localhost:8000/in/miu/in_miu_vision_services_consultancy.html
31. http://localhost:8000/in/miu/in_miu_vision_services_education.html
32. http://localhost:8000/in/miu/in_miu_vision_services_rd.html

### PROCESSING Directory (32 files)
[See terminal output for full list]

### OUT Directory (32 files)
[See terminal output for full list]

## Testing Checklist

For each page, verify:
- [ ] Multi-sheet pagination works (4 columns visible)
- [ ] All paragraphs fit in one column (236px width)
- [ ] ~75 words per paragraph
- [ ] Chat agent button visible
- [ ] Navigation links work correctly
- [ ] No broken links
- [ ] Content displays correctly
- [ ] No scrolling needed
- [ ] Sheet navigation arrows work

## Notes
- All pages are linked in navigation menus
- No redundant/duplicate pages
- All pages accessible via menu navigation
