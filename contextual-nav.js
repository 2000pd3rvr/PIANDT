/**
 * Contextual Navigation - Automatically adapts to any page structure
 * Dynamically shows/hides menu items based on current page location
 * Works with any new pages or menu structures without code changes
 */

(function() {
    'use strict';
    
    function initContextualNav() {
        const currentPath = window.location.pathname;
        const currentUrl = window.location.href;
        
        // Automatically detect current location from URL
        // Pattern: /{triad}/{section}/{page} or /{triad}/{page}
        const pathParts = currentPath.split('/').filter(p => p && !p.endsWith('.html'));
        const htmlFile = currentPath.split('/').pop() || '';
        
        // Detect triad from path (in, processing, out)
        let currentTriad = null;
        let currentSection = null;
        let isMainPage = false;
        
        // Check for triad in path
        if (pathParts.includes('in')) {
            currentTriad = 'in';
            const inIndex = pathParts.indexOf('in');
            // If there's something after 'in', it's a section
            if (pathParts.length > inIndex + 1) {
                currentSection = pathParts[inIndex + 1];
            } else {
                isMainPage = true;
            }
        } else if (pathParts.includes('processing')) {
            currentTriad = 'processing';
            const procIndex = pathParts.indexOf('processing');
            if (pathParts.length > procIndex + 1) {
                currentSection = pathParts[procIndex + 1];
            } else {
                isMainPage = true;
            }
        } else if (pathParts.includes('out')) {
            currentTriad = 'out';
            const outIndex = pathParts.indexOf('out');
            if (pathParts.length > outIndex + 1) {
                currentSection = pathParts[outIndex + 1];
            } else {
                isMainPage = true;
            }
        }
        
        // Find all navigation menus
        const navMenus = document.querySelectorAll('ul.nav-menu');
        
        navMenus.forEach(navMenu => {
            const dropdowns = navMenu.querySelectorAll('li.dropdown');
            
            dropdowns.forEach(dropdown => {
                const mainLink = dropdown.querySelector('a.nav-link');
                if (!mainLink) return;
                
                const linkText = mainLink.textContent.trim();
                const linkHref = mainLink.getAttribute('href') || '';
                
                // Automatically detect which triad this dropdown represents
                // Check link text and href for triad indicators
                let dropdownTriad = null;
                const linkLower = linkText.toLowerCase();
                const hrefLower = linkHref.toLowerCase();
                
        if (linkLower.includes('in') && !linkLower.includes('processing') && !linkLower.includes('out')) {
                    dropdownTriad = 'in';
                } else if (linkLower.includes('proc') || hrefLower.includes('processing')) {
                    dropdownTriad = 'processing';
                } else if (linkLower.includes('out') && !linkLower.includes('about')) {
                    dropdownTriad = 'out';
                }
                
                // Check if we're in a units sub-page (e.g., /out/units/miu/)
                // Units sub-pages have their own navigation structure, not triad navigation
                const isUnitsSubPage = pathParts.length > 2 && 
                                      (pathParts.includes('units') && 
                                       pathParts.indexOf('units') < pathParts.length - 1);
                
                // If we're in a units sub-page, show all navigation (unit-specific menus)
                if (isUnitsSubPage) {
                    dropdown.style.display = '';
                    // Don't filter items on units sub-pages - show everything
                    const topLevelItems = dropdown.querySelectorAll('ul.dropdown-menu > li');
                    topLevelItems.forEach(item => {
                        item.style.display = '';
                        const nestedItems = item.querySelectorAll('ul li');
                        nestedItems.forEach(nested => nested.style.display = '');
                    });
                    return;
                }
                
                // If we're in a specific section (not main page), show only current triad's menu
                if (currentSection && currentTriad && !isMainPage) {
                    // Special case: if we're on a units page and the nav-link is "units",
                    // always show it (it's the section-specific menu, not a triad menu)
                    const navLinkText = mainLink.textContent.trim().toLowerCase();
                    if (currentSection === 'units' && (navLinkText.includes('units') || navLinkText === 'units')) {
                        // This is the units section menu - always show it
                        dropdown.style.display = '';
                    } else if (currentSection === 'about_piandt' && (navLinkText.includes('about piandt') || navLinkText.includes('about_piandt'))) {
                        // This is the about_piandt section menu - always show it
                        dropdown.style.display = '';
                    } else if (isUnitsSubPage) {
                        // For units sub-pages (miu, vision, products, services, etc.), show section-specific menus
                        // Check if nav-link matches common section names
                        if (navLinkText.includes('services') || navLinkText.includes('products') || 
                            navLinkText.includes('vision') || navLinkText.includes('machine intelligence') ||
                            navLinkText.includes('miu')) {
                            // This is a section-specific menu on a units sub-page - always show it
                            dropdown.style.display = '';
                        } else if (dropdownTriad !== currentTriad) {
                            // Hide other triads' menus
                            dropdown.style.display = 'none';
                            return;
                        } else {
                            // Show current triad's menu
                            dropdown.style.display = '';
                        }
                    } else if (dropdownTriad !== currentTriad) {
                        // Hide other triads' menus
                        dropdown.style.display = 'none';
                        return;
                    } else {
                        // Show current triad's menu
                        dropdown.style.display = '';
                    }
                } else {
                    // On main pages or root, show all triads
                    dropdown.style.display = '';
                }
                
                // Only filter items if this dropdown matches our current triad
                if (dropdownTriad !== currentTriad) {
                    // Different triad - show all items (menu might be hidden above)
                    const topLevelItems = dropdown.querySelectorAll('ul.dropdown-menu > li');
                    topLevelItems.forEach(item => {
                        item.style.display = '';
                        const nestedItems = item.querySelectorAll('ul li');
                        nestedItems.forEach(nested => nested.style.display = '');
                    });
                    return;
                }
                
                // Get the dropdown menu
                const dropdownMenu = dropdown.querySelector('ul.dropdown-menu');
                if (!dropdownMenu) return;
                
                // Get all top-level items in this dropdown (direct children only)
                const topLevelItems = Array.from(dropdownMenu.children).filter(child => child.tagName === 'LI');
                
                topLevelItems.forEach(item => {
                    const itemLink = item.querySelector('a.dropdown-link');
                    if (!itemLink) {
                        // If no link, show the item
                        item.style.display = '';
                        return;
                    }
                    
                    const itemHref = itemLink.getAttribute('href') || '';
                    const itemText = itemLink.textContent.trim().toLowerCase();
                    
                    // Automatically detect what section this item represents
                    // Check href and text for section indicators
                    let itemSection = null;
                    const itemHrefLower = itemHref.toLowerCase();
                    
                    // Check for section in href path
                    if (itemHrefLower.includes('/about_piandt/') || itemHrefLower.includes('about_piandt') || itemText.includes('about')) {
                        itemSection = 'about_piandt';
                    } else if (itemHrefLower.includes('/units/') || itemHrefLower.includes('units') || itemText.includes('units')) {
                        itemSection = 'units';
                    } else {
                        // Try to extract section from path
                        const itemPathParts = itemHref.split('/').filter(p => p && !p.endsWith('.html'));
                        if (itemPathParts.length > 0) {
                            // Check if there's a section indicator in the path
                            const lastPart = itemPathParts[itemPathParts.length - 1];
                            if (lastPart.includes('about') || lastPart.includes('piandt')) {
                                itemSection = 'about_piandt';
                            } else if (lastPart.includes('unit')) {
                                itemSection = 'units';
                            }
                        }
                    }
                    
                    // Show/hide items based on current section
                    if (currentSection && !isMainPage) {
                        // We're in a specific section - show only matching items
                        if (itemSection === currentSection) {
                            // Show this item and all its children
                            item.style.display = '';
                            const nestedItems = item.querySelectorAll('ul li');
                            nestedItems.forEach(nested => nested.style.display = '');
                        } else if (itemSection) {
                            // Hide items from other sections
                            item.style.display = 'none';
                        } else {
                            // Unknown section - show it (might be a new section)
                            item.style.display = '';
                        }
                    } else {
                        // On main pages or unknown location - show all items
                        item.style.display = '';
                        const nestedItems = item.querySelectorAll('ul li');
                        nestedItems.forEach(nested => nested.style.display = '');
                    }
                });
            });
        });
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initContextualNav);
    } else {
        initContextualNav();
    }
    
    // Re-run after dynamic menus are populated and after page navigation
    setTimeout(initContextualNav, 600);
    setTimeout(initContextualNav, 1000);
    
    // Re-run on navigation (for single-page apps or dynamic content)
    window.addEventListener('popstate', initContextualNav);
    
    // Observe DOM changes to handle dynamically added menus
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            let shouldUpdate = false;
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && (
                            node.classList.contains('nav-menu') ||
                            node.querySelector('.nav-menu') ||
                            node.classList.contains('dropdown')
                        )) {
                            shouldUpdate = true;
                        }
                    });
                }
            });
            if (shouldUpdate) {
                setTimeout(initContextualNav, 100);
            }
        });
        
        // Observe the document body for changes
        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    }
})();
