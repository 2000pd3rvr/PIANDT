/**
 * Navigation Menu Populator
 * Automatically populates ALL navigation menus based on directory structure
 * Works for all triads (In/Proc/Out) and all sections (about_piandt, units, etc.)
 * FUTURE-PROOF: Automatically adapts to new pages and menu structures
 */

(function() {
    'use strict';
    
    // Calculate relative path from current page to target directory
    function calculateRelativePath(currentPath, targetTriad, targetSection) {
        // Count depth of current path
        const depth = (currentPath.match(/\//g) || []).length - 1;
        
        // Determine current triad
        let currentTriad = null;
        if (currentPath.includes('/in/')) currentTriad = 'in';
        else if (currentPath.includes('/processing/')) currentTriad = 'processing';
        else if (currentPath.includes('/out/')) currentTriad = 'out';
        
        // Determine current section
        let currentSection = null;
        if (currentPath.includes('/about_piandt/')) currentSection = 'about_piandt';
        else if (currentPath.includes('/units/')) currentSection = 'units';
        
        // Calculate path
        if (targetTriad === currentTriad) {
            // Same triad
            if (targetSection === currentSection) {
                // Same section - we're in the target directory
                return '';
            } else {
                // Different section in same triad
                if (depth === 2) {
                    // We're in a section directory (e.g., about_piandt/)
                    return `../${targetSection}/`;
                } else {
                    // We're deeper or at root
                    return '../'.repeat(depth - 1) + `${targetSection}/`;
                }
            }
        } else {
            // Different triad
            const triadDirs = { 'in': 'in', 'processing': 'processing', 'out': 'out' };
            const targetDir = triadDirs[targetTriad];
            if (depth <= 2) {
                return `../${targetDir}/${targetSection}/`;
            } else {
                return '../'.repeat(depth - 1) + `${targetDir}/${targetSection}/`;
            }
        }
    }
    
    // Populate a submenu with pages from PAGES_DATA
    function populateSubmenu(submenu, targetTriad, targetSection, currentPath) {
        if (!window.PAGES_DATA || !window.PAGES_DATA[targetTriad]) {
            return;
        }
        
        const pages = window.PAGES_DATA[targetTriad];
        const basePath = calculateRelativePath(currentPath, targetTriad, targetSection);
        
        // Clear existing items
        submenu.innerHTML = '';
        
        // Filter pages by section type
        const sectionPages = pages.filter(page => {
            if (targetSection === 'about_piandt') {
                return page.type !== 'about_piandt' && 
                       ['mission_vision', 'charitable_purposes', 'our_approach', 'trustees', 'governance'].includes(page.type);
            } else if (targetSection === 'units') {
                return page.type === 'units' || page.path.includes('/units/');
            }
            return false;
        });
        
        // Sort pages by display order
        const order = ['mission_vision', 'charitable_purposes', 'our_approach', 'trustees', 'governance'];
        sectionPages.sort((a, b) => {
            const aIndex = order.indexOf(a.type);
            const bIndex = order.indexOf(b.type);
            return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
        });
        
        // Add pages to submenu
        sectionPages.forEach(page => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = basePath + page.filename;
            a.className = 'submenu-link';
            a.textContent = page.displayName;
            li.appendChild(a);
            submenu.appendChild(li);
        });
    }
    
    // Populate main dropdown menu for a triad
    function populateTriadDropdown(dropdown, targetTriad, currentPath) {
        const dropdownMenu = dropdown.querySelector('.dropdown-menu');
        if (!dropdownMenu) return;
        
        // Find or create "about PIANDT" menu item
        let aboutPiandtItem = dropdownMenu.querySelector('li:has(a[href*="about_piandt"])');
        if (!aboutPiandtItem) {
            // Create the menu item
            aboutPiandtItem = document.createElement('li');
            const aboutLink = document.createElement('a');
            aboutLink.href = calculateRelativePath(currentPath, targetTriad, 'about_piandt') + 
                           (targetTriad === 'in' ? 'in_about_piandt.html' : 
                            targetTriad === 'processing' ? 'proc_about_piandt.html' : 
                            'out_about_piandt.html');
            aboutLink.className = 'dropdown-link';
            aboutLink.innerHTML = 'about PIANDT <span class="dropdown-arrow">▶</span>';
            
            const aboutSubmenu = document.createElement('ul');
            aboutPiandtItem.appendChild(aboutLink);
            aboutPiandtItem.appendChild(aboutSubmenu);
            dropdownMenu.insertBefore(aboutPiandtItem, dropdownMenu.firstChild);
        }
        
        // Populate "about PIANDT" submenu
        const aboutSubmenu = aboutPiandtItem.querySelector('ul');
        if (aboutSubmenu) {
            populateSubmenu(aboutSubmenu, targetTriad, 'about_piandt', currentPath);
        }
        
        // Find or create "units" menu item
        let unitsItem = dropdownMenu.querySelector('li:has(a[href*="units"])');
        if (!unitsItem) {
            unitsItem = document.createElement('li');
            const unitsLink = document.createElement('a');
            unitsLink.href = calculateRelativePath(currentPath, targetTriad, 'units') + 
                           (targetTriad === 'in' ? 'in_units.html' : 
                            targetTriad === 'processing' ? 'proc_units.html' : 
                            'out_units.html');
            unitsLink.className = 'dropdown-link';
            unitsLink.textContent = 'units';
            dropdownMenu.appendChild(unitsItem);
            unitsItem.appendChild(unitsLink);
        }
    }
    
    // Main initialization function
    function initNavMenuPopulator() {
        if (typeof window.PAGES_DATA === 'undefined') {
            setTimeout(initNavMenuPopulator, 100);
            return;
        }
        
        const currentPath = window.location.pathname;
        
        // Find all main navigation menus
        const navMenus = document.querySelectorAll('ul.nav-menu');
        
        navMenus.forEach(navMenu => {
            // Find In dropdown
            const inDropdowns = Array.from(navMenu.querySelectorAll('li.dropdown')).filter(li => {
                const link = li.querySelector('a.nav-link');
                if (!link) return false;
                const text = link.textContent.trim();
                const href = link.getAttribute('href') || '';
                return text.includes('In') || href.includes('/in.html') || href.includes('/in/in.html');
            });
            
            inDropdowns.forEach(dropdown => {
                populateTriadDropdown(dropdown, 'in', currentPath);
            });
            
            // Find Proc dropdown
            const procDropdowns = Array.from(navMenu.querySelectorAll('li.dropdown')).filter(li => {
                const link = li.querySelector('a.nav-link');
                if (!link) return false;
                const text = link.textContent.trim();
                const href = link.getAttribute('href') || '';
                return text.includes('Proc') || href.includes('/processing.html') || href.includes('/processing/processing.html');
            });
            
            procDropdowns.forEach(dropdown => {
                populateTriadDropdown(dropdown, 'processing', currentPath);
            });
            
            // Find Out dropdown
            const outDropdowns = Array.from(navMenu.querySelectorAll('li.dropdown')).filter(li => {
                const link = li.querySelector('a.nav-link');
                if (!link) return false;
                const text = link.textContent.trim();
                const href = link.getAttribute('href') || '';
                return text.includes('Out') || href.includes('/out.html') || href.includes('/out/out.html');
            });
            
            outDropdowns.forEach(dropdown => {
                populateTriadDropdown(dropdown, 'out', currentPath);
            });
        });
        
        // Also handle local navigation menus (like the one on about_piandt pages)
        const localNavLinks = document.querySelectorAll('a.nav-link[href*="about_piandt"]');
        localNavLinks.forEach(link => {
            if (link.textContent.includes('about PIANDT')) {
                const dropdown = link.closest('li.dropdown');
                if (dropdown) {
                    const dropdownMenu = dropdown.querySelector('.dropdown-menu');
                    if (dropdownMenu) {
                        // Determine triad from current path
                        let triad = 'in';
                        if (currentPath.includes('/processing/')) triad = 'processing';
                        else if (currentPath.includes('/out/')) triad = 'out';
                        
                        populateSubmenu(dropdownMenu, triad, 'about_piandt', currentPath);
                    }
                }
            }
        });
    }
    
    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavMenuPopulator);
    } else {
        initNavMenuPopulator();
    }
    
    // Re-run after delay to catch any late-loading content
    setTimeout(initNavMenuPopulator, 500);
    setTimeout(initNavMenuPopulator, 1000);
    
    // Observe DOM changes for dynamically added menus
    const observer = new MutationObserver(() => {
        setTimeout(initNavMenuPopulator, 100);
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();



