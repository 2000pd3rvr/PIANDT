/**
 * Dynamic menu generation - Automatically populates ALL navigation menus
 * based on files in the corresponding directory structure
 * Works for all triads (In/Proc/Out) and all sections (about_piandt, units, etc.)
 * FUTURE-PROOF: Automatically adapts to new pages and menu structures
 */

(function() {
    'use strict';
    
    function calculateRelativePath(fromPath, toTriad, targetSection) {
        // Count depth of current path
        const depth = (fromPath.match(/\//g) || []).length - 1;
        
        // Determine current triad
        let currentTriad = null;
        if (fromPath.includes('/in/')) currentTriad = 'in';
        else if (fromPath.includes('/processing/')) currentTriad = 'processing';
        else if (fromPath.includes('/out/')) currentTriad = 'out';
        
        // Determine current section
        let currentSection = null;
        if (fromPath.includes('/about_piandt/')) currentSection = 'about_piandt';
        else if (fromPath.includes('/units/')) currentSection = 'units';
        
        // Calculate path
        if (toTriad === currentTriad) {
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
            const targetDir = triadDirs[toTriad];
            if (depth <= 2) {
                return `../${targetDir}/${targetSection}/`;
            } else {
                return '../'.repeat(depth - 1) + `${targetDir}/${targetSection}/`;
            }
        }
    }
    
    function populateAboutPiandtSubmenu(submenu, targetTriad, currentPath) {
        if (!window.PAGES_DATA || !window.PAGES_DATA[targetTriad]) {
            console.warn('[Dynamic Menu] PAGES_DATA not available for triad:', targetTriad);
            return;
        }
        
        const pages = window.PAGES_DATA[targetTriad];
        const basePath = calculateRelativePath(currentPath, targetTriad, 'about_piandt');
        
        // Filter to only include about_piandt child pages
        const aboutPiandtChildPages = pages.filter(page => {
            if (page.type === 'about_piandt') return false;
            if (page.path && !page.path.includes('/about_piandt/')) return false;
            const validTypes = ['mission_vision', 'charitable_purposes', 'our_approach', 'trustees', 'governance'];
            return validTypes.includes(page.type);
        });
        
        // Sort by display order
        const order = ['mission_vision', 'charitable_purposes', 'our_approach', 'trustees', 'governance'];
        aboutPiandtChildPages.sort((a, b) => {
            const aIndex = order.indexOf(a.type);
            const bIndex = order.indexOf(b.type);
            return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
        });
        
        // Check if this is a local menu (direct child of dropdown-menu) or nested submenu
        const isLocalMenu = submenu.classList.contains('dropdown-menu') || 
                          submenu.parentElement?.querySelector('a.nav-link');
        const linkClass = isLocalMenu ? 'dropdown-link' : 'submenu-link';
        
        // Get existing links - if they exist and are correct, just make them clickable
        // Otherwise, create/update them
        const existingLinks = Array.from(submenu.querySelectorAll('a'));
        
        // Check if existing links match expected pages
        let linksMatch = existingLinks.length === aboutPiandtChildPages.length;
        if (linksMatch) {
            // Verify links point to correct files
            existingLinks.forEach((link, index) => {
                if (index < aboutPiandtChildPages.length) {
                    const page = aboutPiandtChildPages[index];
                    const expectedHref = basePath + page.filename;
                    const currentHref = link.getAttribute('href');
                    // Check if href matches (allowing for different path formats)
                    if (currentHref && !currentHref.endsWith(page.filename)) {
                        linksMatch = false;
                    }
                }
            });
        }
        
        if (linksMatch && existingLinks.length > 0) {
            // Links already exist and are correct - just ensure they're clickable
            console.log(`[Dynamic Menu] Links already exist and are correct - ensuring clickability`);
            existingLinks.forEach((link, index) => {
                if (index < aboutPiandtChildPages.length) {
                    const page = aboutPiandtChildPages[index];
                    
                    // CRITICAL: Ensure link is fully clickable WITHOUT replacing it
                    link.style.setProperty('pointer-events', 'auto', 'important');
                    link.style.setProperty('cursor', 'pointer', 'important');
                    link.style.setProperty('text-decoration', 'none', 'important');
                    link.style.setProperty('display', 'block', 'important');
                    link.style.setProperty('position', 'relative', 'important');
                    link.style.setProperty('z-index', '10000', 'important');
                    
                    // Remove any event handlers that might prevent navigation
                    const href = link.getAttribute('href');
                    if (href && !link.dataset.clickHandlerFixed) {
                        link.dataset.clickHandlerFixed = 'true';
                        
                        // Clone to remove any interfering handlers, but keep the original href
                        const newLink = link.cloneNode(true);
                        newLink.setAttribute('href', href); // Ensure href is preserved
                        link.parentNode.replaceChild(newLink, link);
                        
                        // Add click handler that ALLOWS navigation
                        newLink.addEventListener('click', function(e) {
                            // CRITICAL: Do NOT prevent default - allow browser navigation
                            console.log(`[Dynamic Menu] Clicked: ${page.displayName} -> ${href}`);
                            
                            const navMenu = document.querySelector('.nav-menu');
                            const hamburger = document.querySelector('.hamburger');
                            if (navMenu && hamburger) {
                                navMenu.classList.remove('active');
                                hamburger.classList.remove('active');
                            }
                            // Let the browser handle navigation - don't prevent default!
                        }, false);
                    }
                }
            });
        } else {
            // Clear and create new links
            submenu.innerHTML = '';
            
            aboutPiandtChildPages.forEach(page => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                
                let fullHref = basePath + page.filename;
                fullHref = fullHref.replace(/\/+/g, '/').replace(/^\/+/, '');
                
                a.setAttribute('href', fullHref);
                a.className = linkClass;
                a.textContent = page.displayName;
                
                // CRITICAL: Ensure link is fully clickable with highest priority
                a.style.cssText = 'pointer-events: auto !important; cursor: pointer !important; text-decoration: none !important; display: block !important; position: relative !important; z-index: 10000 !important;';
                
                // Add click handler BEFORE appending
                a.addEventListener('click', function(e) {
                    // CRITICAL: Do NOT prevent default - allow browser navigation
                    console.log(`[Dynamic Menu] Clicked: ${page.displayName} -> ${fullHref}`);
                    
                    const navMenu = document.querySelector('.nav-menu');
                    const hamburger = document.querySelector('.hamburger');
                    if (navMenu && hamburger) {
                        navMenu.classList.remove('active');
                        hamburger.classList.remove('active');
                    }
                    // Let the browser handle navigation - don't prevent default!
                    // Don't stop propagation - let the event flow normally
                }, false);
                
                li.appendChild(a);
                submenu.appendChild(li);
            });
        }
        
        console.log(`[Dynamic Menu] Populated about_piandt submenu with ${aboutPiandtChildPages.length} items for ${targetTriad}, basePath: '${basePath}'`);
        console.log(`[Dynamic Menu] Links created:`, aboutPiandtChildPages.map(p => `${p.displayName} -> ${basePath + p.filename}`));
        
        // FINAL VERIFICATION: Ensure all links in this submenu are clickable
        setTimeout(() => {
            const finalLinks = submenu.querySelectorAll('a');
            console.log(`[Dynamic Menu] Final verification: Found ${finalLinks.length} links in submenu`);
            finalLinks.forEach(link => {
                const href = link.getAttribute('href');
                link.style.cssText = 'pointer-events: auto !important; cursor: pointer !important; text-decoration: none !important; display: block !important; position: relative !important; z-index: 10000 !important;';
                console.log(`[Dynamic Menu] Verified link: ${link.textContent.trim()} -> ${href}`);
            });
        }, 100);
        console.log(`[Dynamic Menu] Links created:`, aboutPiandtChildPages.map(p => `${p.displayName} -> ${basePath + p.filename}`));
        
        // FINAL VERIFICATION: Ensure all links in this submenu are clickable
        setTimeout(() => {
            const finalLinks = submenu.querySelectorAll('a');
            finalLinks.forEach(link => {
                const href = link.getAttribute('href');
                link.style.cssText = 'pointer-events: auto !important; cursor: pointer !important; text-decoration: none !important; display: block !important; position: relative !important; z-index: 10000 !important;';
                console.log(`[Dynamic Menu] Verified link: ${link.textContent.trim()} -> ${href}`);
            });
        }, 100);
    }
    
    // Populate ALL child menus for a triad dropdown
    function populateTriadDropdown(dropdown, targetTriad, currentPath) {
        const dropdownMenu = dropdown.querySelector('.dropdown-menu');
        if (!dropdownMenu) return;
        
        // Find all "about PIANDT" links and populate their submenus
        const aboutPiandtLinks = dropdownMenu.querySelectorAll('a[href*="about_piandt"][class*="dropdown-link"]');
        aboutPiandtLinks.forEach(link => {
            const aboutPiandtItem = link.closest('li');
            if (aboutPiandtItem) {
                let aboutPiandtSubmenu = aboutPiandtItem.querySelector('ul');
                if (!aboutPiandtSubmenu) {
                    // Create submenu if it doesn't exist
                    aboutPiandtSubmenu = document.createElement('ul');
                    aboutPiandtItem.appendChild(aboutPiandtSubmenu);
                    // Add arrow if not present
                    if (!link.querySelector('.dropdown-arrow')) {
                        link.innerHTML = link.textContent.trim() + ' <span class="dropdown-arrow">▶</span>';
                    }
                }
                populateAboutPiandtSubmenu(aboutPiandtSubmenu, targetTriad, currentPath);
            }
        });
        
        // Find all "units" links - ensure they exist and are properly linked
        const unitsLinks = dropdownMenu.querySelectorAll('a[href*="units"][class*="dropdown-link"]');
        unitsLinks.forEach(link => {
            // Ensure the link points to the correct units page
            const expectedFilename = targetTriad === 'in' ? 'in_units.html' : 
                                    targetTriad === 'processing' ? 'proc_units.html' : 
                                    'out_units.html';
            const basePath = calculateRelativePath(currentPath, targetTriad, 'units');
            if (!link.getAttribute('href').endsWith(expectedFilename)) {
                link.href = basePath + expectedFilename;
            }
        });
    }
    
    function initDynamicMenus() {
        if (typeof window.PAGES_DATA === 'undefined') {
            setTimeout(initDynamicMenus, 100);
            return;
        }
        
        const currentPath = window.location.pathname;
        
        // Find all main navigation menus (In/Proc/Out dropdowns)
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
        
        // Handle local navigation menus in about_piandt pages (direct dropdown, not nested)
        // These are the menus that appear when you're ON an about_piandt page
        const localMenus = document.querySelectorAll('ul.dropdown-menu');
        localMenus.forEach(menu => {
            // Check if this menu is directly under a nav-link for about_piandt
            const parentLi = menu.parentElement;
            if (!parentLi || parentLi.tagName !== 'LI') return;
            
            const aboutPiandtLink = parentLi.querySelector('a.nav-link[href*="about_piandt"]');
            if (aboutPiandtLink && aboutPiandtLink.textContent.toLowerCase().includes('about piandt')) {
                // This is a local nav menu - determine triad from current path
                let triad = 'in';
                if (currentPath.includes('/processing/')) triad = 'processing';
                else if (currentPath.includes('/out/')) triad = 'out';
                
                console.log(`[Dynamic Menu] Found local about_piandt menu, populating for triad: ${triad}, path: ${currentPath}`);
                populateAboutPiandtSubmenu(menu, triad, currentPath);
            }
        });
        
        // CRITICAL FALLBACK: Ensure ALL about_piandt child links work, regardless of how they were created
        // This runs after a delay to catch any links that might have been missed
        setTimeout(() => {
            const allAboutPiandtLinks = document.querySelectorAll(
                'a.dropdown-link[href*="mission_vision"], ' +
                'a.dropdown-link[href*="charitable_purposes"], ' +
                'a.dropdown-link[href*="our_approach"], ' +
                'a.dropdown-link[href*="trustees"], ' +
                'a.dropdown-link[href*="governance"], ' +
                'a.submenu-link[href*="mission_vision"], ' +
                'a.submenu-link[href*="charitable_purposes"], ' +
                'a.submenu-link[href*="our_approach"], ' +
                'a.submenu-link[href*="trustees"], ' +
                'a.submenu-link[href*="governance"]'
            );
            
            console.log(`[Dynamic Menu] Fallback: Found ${allAboutPiandtLinks.length} about_piandt child links`);
            
            allAboutPiandtLinks.forEach((link, index) => {
                const href = link.getAttribute('href');
                if (!href || !href.endsWith('.html')) return;
                
                // Ensure link is clickable
                link.style.setProperty('pointer-events', 'auto', 'important');
                link.style.setProperty('cursor', 'pointer', 'important');
                link.style.setProperty('text-decoration', 'none', 'important');
                link.style.setProperty('display', 'block', 'important');
                link.style.setProperty('position', 'relative', 'important');
                link.style.setProperty('z-index', '10000', 'important');
                
                // Remove any interfering handlers and add a clean one
                if (!link.dataset.fallbackFixed) {
                    link.dataset.fallbackFixed = 'true';
                    
                    // Clone to remove any interfering handlers
                    const newLink = link.cloneNode(true);
                    newLink.setAttribute('href', href); // Preserve href
                    link.parentNode.replaceChild(newLink, link);
                    
                    // Add click handler that ALLOWS navigation
                    newLink.addEventListener('click', function(e) {
                        console.log(`[Dynamic Menu] Fallback: Clicked -> ${href}`);
                        const navMenu = document.querySelector('.nav-menu');
                        const hamburger = document.querySelector('.hamburger');
                        if (navMenu && hamburger) {
                            navMenu.classList.remove('active');
                            hamburger.classList.remove('active');
                        }
                        // CRITICAL: Do NOT prevent default - allow browser navigation
                    }, false);
                }
            });
        }, 200);
    }
    
    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDynamicMenus);
    } else {
        initDynamicMenus();
    }
    
    // Function to ensure all dynamically created links are clickable
    function ensureLinksClickable() {
        // Find all dynamically created about_piandt child links
        const aboutPiandtLinks = document.querySelectorAll('a.dropdown-link[href*="mission_vision"], a.dropdown-link[href*="charitable_purposes"], a.dropdown-link[href*="our_approach"], a.dropdown-link[href*="trustees"], a.dropdown-link[href*="governance"], a.submenu-link[href*="mission_vision"], a.submenu-link[href*="charitable_purposes"], a.submenu-link[href*="our_approach"], a.submenu-link[href*="trustees"], a.submenu-link[href*="governance"]');
        
        aboutPiandtLinks.forEach(link => {
            // Ensure link is clickable
            link.style.pointerEvents = 'auto';
            link.style.cursor = 'pointer';
            link.style.textDecoration = 'none';
            
            // Add click handler that allows navigation (if not already added)
            if (!link.dataset.clickHandlerAdded) {
                link.dataset.clickHandlerAdded = 'true';
                link.addEventListener('click', function(e) {
                    // Don't prevent default - allow normal navigation
                    const href = this.getAttribute('href');
                    console.log(`[Dynamic Menu] About PIANDT link clicked: ${href}`);
                    
                    // Close mobile menu if open
                    const navMenu = document.querySelector('.nav-menu');
                    const hamburger = document.querySelector('.hamburger');
                    if (navMenu && hamburger) {
                        navMenu.classList.remove('active');
                        hamburger.classList.remove('active');
                    }
                }, false);
            }
        });
    }
    
    // Re-run after delay to catch any late-loading content
    setTimeout(() => {
        initDynamicMenus();
        ensureLinksClickable();
    }, 500);
    setTimeout(() => {
        initDynamicMenus();
        ensureLinksClickable();
    }, 1000);
    
    // Observe DOM changes for dynamically added menus
    const observer = new MutationObserver(() => {
        setTimeout(() => {
            initDynamicMenus();
            ensureLinksClickable();
        }, 100);
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
