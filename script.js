// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Auto-position submenus consistently per parent menu level
// All child menus within a parent (In/Proc/Out) point in the same direction
// If ANY child menu level would equal or exceed the right margin, ALL menus point leftward
//
// FUTURE-PROOF: This function automatically works for new pages/menus because:
// - Uses generic selectors (.nav-menu > .dropdown) - finds any top-level parent
// - Dynamically detects parent type from link text/href - no hardcoded names
// - Finds ALL child menus at ALL nesting levels - works for any depth
// - Uses MutationObserver to detect DOM changes - catches dynamically added menus
// - Re-runs on window resize - adapts to viewport changes
function initSubmenuPositioning() {
    // Find all top-level dropdown menus (In, Proc, Out, or any future parents)
    // This selector is generic and will find any top-level dropdown menu
    const topLevelDropdowns = document.querySelectorAll('.nav-menu > .dropdown');
    
    topLevelDropdowns.forEach(parentDropdown => {
        const parentLink = parentDropdown.querySelector('a.nav-link');
        if (!parentLink) return;
        
        // Determine which parent this is (In, Proc, or Out)
        const linkText = parentLink.textContent.trim();
        const linkHref = parentLink.getAttribute('href') || '';
        let parentType = null;
        
        if (linkText.includes('In') || linkHref.includes('/in.html') || linkHref.includes('/in/in.html')) {
            parentType = 'in';
        } else if (linkText.includes('Proc') || linkHref.includes('/processing.html') || linkHref.includes('/processing/processing.html')) {
            parentType = 'processing';
        } else if (linkText.includes('Out') || linkHref.includes('/out.html') || linkHref.includes('/out/out.html')) {
            parentType = 'out';
        }
        
        // Get the parent dropdown menu
        const parentDropdownMenu = parentDropdown.querySelector('.dropdown-menu');
        if (!parentDropdownMenu) return;
        
        // Calculate if this parent menu should point leftward or rightward
        function determineParentDirection() {
            const parentRect = parentDropdown.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const padding = 10;
            const safetyMargin = 20;
            const rightMargin = viewportWidth - padding - safetyMargin;
            
            // Find maximum nesting depth
            let maxDepth = 0;
            function findMaxDepth(element, currentDepth = 0) {
                // Get direct child li elements, then their direct child ul elements
                const directLiChildren = Array.from(element.children).filter(child => child.tagName === 'LI');
                const childMenus = [];
                directLiChildren.forEach(li => {
                    const directUlChild = Array.from(li.children).find(child => child.tagName === 'UL');
                    if (directUlChild) {
                        childMenus.push(directUlChild);
                    }
                });
                
                if (childMenus.length === 0) {
                    if (currentDepth > maxDepth) {
                        maxDepth = currentDepth;
                    }
                    return;
                }
                childMenus.forEach(childMenu => {
                    findMaxDepth(childMenu, currentDepth + 1);
                });
            }
            findMaxDepth(parentDropdownMenu);
            
            // Estimate submenu width (average width for nested menus)
            const estimatedSubmenuWidth = 220;
            
            // Calculate rightmost edge position if all menus point rightward
            // This represents the worst-case scenario
            const rightmostEdgePosition = parentRect.right + (estimatedSubmenuWidth * maxDepth);
            
            // Debug logging
            console.log(`[Menu Direction] ${parentType || 'unknown'}: parent.right=${parentRect.right.toFixed(0)}, maxDepth=${maxDepth}, rightmostEdge=${rightmostEdgePosition.toFixed(0)}, rightMargin=${rightMargin.toFixed(0)}`);
            
            // Check if rightmost edge would equal or exceed right margin
            if (rightmostEdgePosition >= rightMargin) {
                // ANY menu level would exceed right margin → point ALL leftward
                console.log(`[Menu Direction] ${parentType || 'unknown'}: OVERFLOW DETECTED → pointing LEFTWARD`);
                return 'leftward';
            }
            
            // Also check each menu level individually
            const allChildMenus = parentDropdownMenu.querySelectorAll('ul');
            for (let childMenu of allChildMenus) {
                // Calculate depth of this menu
                let depth = 0;
                let current = childMenu;
                while (current && current !== parentDropdownMenu) {
                    if (current.tagName === 'UL') {
                        depth++;
                    }
                    current = current.parentElement;
                }
                
                // Get parent menu item
                const parentMenuItem = childMenu.parentElement;
                if (parentMenuItem) {
                    const menuItemRect = parentMenuItem.getBoundingClientRect();
                    // Calculate where this menu's right edge would be
                    const estimatedRightEdge = menuItemRect.right + estimatedSubmenuWidth;
                    
                    // If this menu would equal or exceed right margin, point all leftward
                    if (estimatedRightEdge >= rightMargin) {
                        console.log(`[Menu Direction] ${parentType || 'unknown'}: Individual menu overflow → pointing LEFTWARD`);
                        return 'leftward';
                    }
                }
            }
            
            // For Out and Proc, also check if parent is close to right edge
            if (parentType === 'out' || parentType === 'processing') {
                const spaceOnRight = viewportWidth - parentRect.right - padding - safetyMargin;
                const spaceOnLeft = parentRect.left - padding;
                
                // If parent is in right 70% of screen or space on right is limited, prefer leftward
                if (parentRect.right > viewportWidth * 0.7 || spaceOnRight < spaceOnLeft * 1.2) {
                    console.log(`[Menu Direction] ${parentType}: Close to right edge → pointing LEFTWARD`);
                    return 'leftward';
                }
            }
            
            // Default: rightward if there's enough space
            console.log(`[Menu Direction] ${parentType || 'unknown'}: Enough space → pointing RIGHTWARD`);
            return 'rightward';
        }
        
        // Determine direction for this parent menu
        const parentDirection = determineParentDirection();
        
        // Find ALL child menus at ALL levels within this parent
        const allChildMenus = parentDropdownMenu.querySelectorAll('ul');
        
        // Apply consistent direction to all child menus with STRONG inline styles
        allChildMenus.forEach(childMenu => {
            if (parentDirection === 'leftward') {
                // Point leftward - add class and set styles
                childMenu.classList.add('submenu-reversed');
                childMenu.style.setProperty('left', 'auto', 'important');
                childMenu.style.setProperty('right', '100%', 'important');
                childMenu.style.setProperty('margin-left', '0', 'important');
                childMenu.style.setProperty('margin-right', '2px', 'important');
            } else {
                // Point rightward - remove class and set styles
                childMenu.classList.remove('submenu-reversed');
                childMenu.style.setProperty('left', '100%', 'important');
                childMenu.style.setProperty('right', 'auto', 'important');
                childMenu.style.setProperty('margin-left', '2px', 'important');
                childMenu.style.setProperty('margin-right', '0', 'important');
            }
        });
        
        // Set up hover handlers to maintain consistency
        const menuItemsWithChildren = parentDropdownMenu.querySelectorAll('li:has(> ul)');
        
        menuItemsWithChildren.forEach(menuItem => {
            // Get direct child ul (not nested)
            const submenu = Array.from(menuItem.children).find(child => child.tagName === 'UL');
            if (!submenu) return;
            
            // On hover, ensure consistent direction is maintained
            menuItem.addEventListener('mouseenter', () => {
                if (parentDirection === 'leftward') {
                    submenu.classList.add('submenu-reversed');
                    submenu.style.setProperty('left', 'auto', 'important');
                    submenu.style.setProperty('right', '100%', 'important');
                    submenu.style.setProperty('margin-left', '0', 'important');
                    submenu.style.setProperty('margin-right', '2px', 'important');
                } else {
                    submenu.classList.remove('submenu-reversed');
                    submenu.style.setProperty('left', '100%', 'important');
                    submenu.style.setProperty('right', 'auto', 'important');
                    submenu.style.setProperty('margin-left', '2px', 'important');
                    submenu.style.setProperty('margin-right', '0', 'important');
                }
            });
        });
    });
    
    // Re-check on window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            initSubmenuPositioning();
        }, 100);
    });
}

// Initialize submenu positioning when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSubmenuPositioning);
} else {
    initSubmenuPositioning();
}

// Re-initialize after dynamic menus are loaded
setTimeout(initSubmenuPositioning, 600);
setTimeout(initSubmenuPositioning, 1000);

// Also observe DOM changes for dynamically added menus
// FUTURE-PROOF: This ensures new menus added via JavaScript are automatically positioned
const observer = new MutationObserver((mutations) => {
    // Only re-run if dropdown menus were added/modified
    let shouldUpdate = false;
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && (
                node.classList?.contains('dropdown') ||
                node.classList?.contains('dropdown-menu') ||
                node.querySelector?.('.dropdown') ||
                node.querySelector?.('.dropdown-menu')
            )) {
                shouldUpdate = true;
            }
        });
    });
    if (shouldUpdate) {
        setTimeout(initSubmenuPositioning, 100);
    }
});
observer.observe(document.body, { childList: true, subtree: true });

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-link, .dropdown-link, .submenu-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Handle dropdown menus on mobile
const dropdowns = document.querySelectorAll('.dropdown');
dropdowns.forEach(dropdown => {
    const dropdownLink = dropdown.querySelector('.nav-link');
    if (dropdownLink) {
        dropdownLink.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                dropdown.classList.toggle('active');
            }
        });
    }
});

// Theme Toggle Functionality - Helper functions
// Inject stylesheet immediately if dark theme is detected (runs before DOMContentLoaded)
(function() {
    if (typeof localStorage !== 'undefined') {
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            // Inject stylesheet immediately in head
            const darkThemeStyle = document.createElement('style');
            darkThemeStyle.id = 'dark-theme-override-style';
            darkThemeStyle.textContent = `
                /* Override CSS variables at root level */
                :root.dark-theme,
                html.dark-theme,
                body.dark-theme {
                    --color-text: #ffffff !important;
                    --color-text-light: #ffffff !important;
                }
                
                /* Force all content-text and children to white */
                body.dark-theme .content-text,
                html.dark-theme .content-text,
                body.dark-theme .content-text *,
                html.dark-theme .content-text *,
                body.dark-theme .content-text p,
                html.dark-theme .content-text p,
                body.dark-theme .section .content-text,
                html.dark-theme .section .content-text,
                body.dark-theme .section .content-text *,
                html.dark-theme .section .content-text *,
                body.dark-theme .section .content-text p,
                html.dark-theme .section .content-text p,
                body.dark-theme main .content-text,
                html.dark-theme main .content-text,
                body.dark-theme main .content-text *,
                html.dark-theme main .content-text *,
                body.dark-theme main .content-text p,
                html.dark-theme main .content-text p,
                body.dark-theme .container .content-text,
                html.dark-theme .container .content-text,
                body.dark-theme .container .content-text *,
                html.dark-theme .container .content-text *,
                body.dark-theme .container .content-text p,
                html.dark-theme .container .content-text p,
                body.dark-theme .content-grid .content-text,
                html.dark-theme .content-grid .content-text,
                body.dark-theme .content-grid .content-text *,
                html.dark-theme .content-grid .content-text *,
                body.dark-theme .content-grid .content-text p,
                html.dark-theme .content-grid .content-text p {
                    color: #ffffff !important;
                    --color-text: #ffffff !important;
                    --color-text-light: #ffffff !important;
                }
                
                /* Force background colors */
                body.dark-theme main,
                html.dark-theme main,
                body.dark-theme .section,
                html.dark-theme .section,
                body.dark-theme .container,
                html.dark-theme .container,
                body.dark-theme .content-grid,
                html.dark-theme .content-grid {
                    background-color: #1a1a1a !important;
                    color: #ffffff !important;
                    --color-text: #ffffff !important;
                    --color-text-light: #ffffff !important;
                }
                
                /* Force h1 in content-grid */
                body.dark-theme .content-grid h1,
                html.dark-theme .content-grid h1,
                body.dark-theme .content-text h1,
                html.dark-theme .content-text h1 {
                    color: #ffffff !important;
                }
            `;
            // Insert immediately if head exists, otherwise wait for it
            if (document.head) {
                document.head.appendChild(darkThemeStyle);
            } else {
                document.addEventListener('DOMContentLoaded', function() {
                    if (!document.getElementById('dark-theme-override-style')) {
                        document.head.appendChild(darkThemeStyle);
                    }
                });
            }
        }
    }
})();

function applyInlineDarkThemeStyles() {
    // Inject a dynamic stylesheet to override everything - most aggressive approach
    let darkThemeStyle = document.getElementById('dark-theme-override-style');
    if (!darkThemeStyle) {
        darkThemeStyle = document.createElement('style');
        darkThemeStyle.id = 'dark-theme-override-style';
        // Insert at the end of head to ensure it overrides everything
        document.head.appendChild(darkThemeStyle);
    }
    // Use a comprehensive stylesheet that targets every possible selector
    darkThemeStyle.textContent = `
        /* Override CSS variables at root level */
        :root.dark-theme,
        html.dark-theme,
        body.dark-theme {
            --color-text: #ffffff !important;
            --color-text-light: #ffffff !important;
        }
        
        /* Force all content-text and children to white */
        body.dark-theme .content-text,
        html.dark-theme .content-text,
        body.dark-theme .content-text *,
        html.dark-theme .content-text *,
        body.dark-theme .content-text p,
        html.dark-theme .content-text p,
        body.dark-theme .section .content-text,
        html.dark-theme .section .content-text,
        body.dark-theme .section .content-text *,
        html.dark-theme .section .content-text *,
        body.dark-theme .section .content-text p,
        html.dark-theme .section .content-text p,
        body.dark-theme main .content-text,
        html.dark-theme main .content-text,
        body.dark-theme main .content-text *,
        html.dark-theme main .content-text *,
        body.dark-theme main .content-text p,
        html.dark-theme main .content-text p,
        body.dark-theme .container .content-text,
        html.dark-theme .container .content-text,
        body.dark-theme .container .content-text *,
        html.dark-theme .container .content-text *,
        body.dark-theme .container .content-text p,
        html.dark-theme .container .content-text p,
        body.dark-theme .content-grid .content-text,
        html.dark-theme .content-grid .content-text,
        body.dark-theme .content-grid .content-text *,
        html.dark-theme .content-grid .content-text *,
        body.dark-theme .content-grid .content-text p,
        html.dark-theme .content-grid .content-text p {
            color: #ffffff !important;
            --color-text: #ffffff !important;
            --color-text-light: #ffffff !important;
        }
        
        /* Force background colors */
        body.dark-theme main,
        html.dark-theme main,
        body.dark-theme .section,
        html.dark-theme .section,
        body.dark-theme .container,
        html.dark-theme .container,
        body.dark-theme .content-grid,
        html.dark-theme .content-grid {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            --color-text: #ffffff !important;
            --color-text-light: #ffffff !important;
        }
        
        /* Force h1 in content-grid */
        body.dark-theme .content-grid h1,
        html.dark-theme .content-grid h1,
        body.dark-theme .content-text h1,
        html.dark-theme .content-text h1 {
            color: #ffffff !important;
        }
    `;
    
    // Also force update CSS variables on html and body first
    document.documentElement.style.setProperty('--color-text', '#ffffff', 'important');
    document.documentElement.style.setProperty('--color-text-light', '#ffffff', 'important');
    document.documentElement.style.setProperty('background-color', '#1a1a1a', 'important');
    document.body.style.setProperty('--color-text', '#ffffff', 'important');
    document.body.style.setProperty('--color-text-light', '#ffffff', 'important');
    document.body.style.setProperty('background-color', '#1a1a1a', 'important');
    
    // Batch DOM updates for better performance
    const contentTextElements = document.querySelectorAll('.content-text');
    const main = document.querySelector('main');
    const section = document.querySelector('.section');
    const container = document.querySelector('.container');
    const contentGrid = document.querySelector('.content-grid');
    
    // Update main containers first with CSS variables
    if (main) {
        main.style.setProperty('background-color', '#1a1a1a', 'important');
        main.style.setProperty('color', '#ffffff', 'important');
        main.style.setProperty('--color-text', '#ffffff', 'important');
        main.style.setProperty('--color-text-light', '#ffffff', 'important');
    }
    if (section) {
        section.style.setProperty('background-color', '#1a1a1a', 'important');
        section.style.setProperty('color', '#ffffff', 'important');
        section.style.setProperty('--color-text', '#ffffff', 'important');
        section.style.setProperty('--color-text-light', '#ffffff', 'important');
    }
    if (container) {
        container.style.setProperty('color', '#ffffff', 'important');
        container.style.setProperty('--color-text', '#ffffff', 'important');
        container.style.setProperty('--color-text-light', '#ffffff', 'important');
    }
    if (contentGrid) {
        contentGrid.style.setProperty('color', '#ffffff', 'important');
        contentGrid.style.setProperty('--color-text', '#ffffff', 'important');
        contentGrid.style.setProperty('--color-text-light', '#ffffff', 'important');
    }
    
    // Update all content-text elements and their children in one pass
    contentTextElements.forEach(el => {
        // Set CSS variables on the element itself
        el.style.setProperty('--color-text', '#ffffff', 'important');
        el.style.setProperty('--color-text-light', '#ffffff', 'important');
        el.style.setProperty('color', '#ffffff', 'important');
        el.style.setProperty('background-color', 'transparent', 'important');
        
        // CRITICAL: Update paragraphs FIRST with direct color override
        const paragraphs = el.querySelectorAll('p');
        paragraphs.forEach(p => {
            // Force color directly - this overrides CSS variable usage
            p.style.setProperty('color', '#ffffff', 'important');
            p.style.setProperty('--color-text-light', '#ffffff', 'important');
        });
        
        // Update ALL other children recursively
        const allChildren = el.querySelectorAll('*:not(p)');
        allChildren.forEach(child => {
            child.style.setProperty('color', '#ffffff', 'important');
        });
        
        const headings = el.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach(h => {
            h.style.setProperty('color', '#ffffff', 'important');
        });
        
        const textElements = el.querySelectorAll('strong, b, a, span, em, i');
        textElements.forEach(t => {
            t.style.setProperty('color', '#ffffff', 'important');
        });
    });
    
    // Also update h1 in content-grid
    const h1Elements = document.querySelectorAll('.content-grid h1, .content-text h1');
    h1Elements.forEach(h1 => {
        h1.style.setProperty('color', '#ffffff', 'important');
    });
}

function removeInlineDarkThemeStyles() {
    // Remove the dynamic stylesheet
    const darkThemeStyle = document.getElementById('dark-theme-override-style');
    if (darkThemeStyle) {
        darkThemeStyle.remove();
    }
    
    // CRITICAL: Remove dark background from html and body
    document.documentElement.style.removeProperty('background-color');
    document.documentElement.style.setProperty('background-color', '#ffffff', 'important');
    document.body.style.removeProperty('background-color');
    document.body.style.setProperty('background-color', '#ffffff', 'important');
    
    // Remove CSS variables from html and body
    document.documentElement.style.removeProperty('--color-text');
    document.documentElement.style.removeProperty('--color-text-light');
    document.body.style.removeProperty('--color-text');
    document.body.style.removeProperty('--color-text-light');
    
    // Batch DOM updates for better performance
    const contentTextElements = document.querySelectorAll('.content-text');
    const main = document.querySelector('main');
    const section = document.querySelector('.section');
    const container = document.querySelector('.container');
    const contentGrid = document.querySelector('.content-grid');
    
    // Update main containers first - explicitly set to white background
    if (main) {
        main.style.setProperty('background-color', '#ffffff', 'important');
        main.style.removeProperty('color');
        main.style.removeProperty('--color-text');
        main.style.removeProperty('--color-text-light');
    }
    if (section) {
        section.style.setProperty('background-color', '#ffffff', 'important');
        section.style.removeProperty('color');
        section.style.removeProperty('--color-text');
        section.style.removeProperty('--color-text-light');
    }
    if (container) {
        container.style.removeProperty('color');
        container.style.removeProperty('--color-text');
        container.style.removeProperty('--color-text-light');
    }
    if (contentGrid) {
        contentGrid.style.removeProperty('color');
        contentGrid.style.removeProperty('--color-text');
        contentGrid.style.removeProperty('--color-text-light');
    }
    
    // Remove styles from all content-text elements and their children in one pass
    contentTextElements.forEach(el => {
        el.style.removeProperty('--color-text');
        el.style.removeProperty('--color-text-light');
        el.style.removeProperty('color');
        el.style.removeProperty('background-color');
        
        // Remove from paragraphs first
        const paragraphs = el.querySelectorAll('p');
        paragraphs.forEach(p => {
            p.style.removeProperty('color');
            p.style.removeProperty('--color-text-light');
        });
        
        // Remove from ALL other children
        const allChildren = el.querySelectorAll('*:not(p)');
        allChildren.forEach(child => {
            child.style.removeProperty('color');
        });
    });
    
    // Remove from h1 elements
    const h1Elements = document.querySelectorAll('.content-grid h1, .content-text h1');
    h1Elements.forEach(h1 => {
        h1.style.removeProperty('color');
    });
}

function initThemeToggle() {
const themeToggle = document.getElementById('themeToggle');
const body = document.body;
    const html = document.documentElement;
    
    if (!themeToggle) {
        // Retry if element not found yet
        setTimeout(initThemeToggle, 100);
        return;
    }
    
    const themeIcon = themeToggle.querySelector('.theme-icon');

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
    body.classList.add('dark-theme');
        html.classList.add('dark-theme');
        document.documentElement.classList.add('dark-theme');
    if (themeIcon) themeIcon.textContent = '☀️';
        // Apply inline styles on load if dark theme - use setTimeout to ensure DOM is ready
        setTimeout(() => {
            applyInlineDarkThemeStyles();
        }, 0);
} else {
    body.classList.remove('dark-theme');
        html.classList.remove('dark-theme');
        document.documentElement.classList.remove('dark-theme');
    if (themeIcon) themeIcon.textContent = '🌙';
        // Ensure no inline styles if light theme
        removeInlineDarkThemeStyles();
    }

    // Mark that listener is attached
    if (!themeToggle.hasAttribute('data-listener-attached')) {
        themeToggle.setAttribute('data-listener-attached', 'true');
        
        // Toggle theme - instant seamless change
        themeToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Disable transitions temporarily for instant theme change
            const style = document.createElement('style');
            style.textContent = `
                *, *::before, *::after {
                    transition: none !important;
                }
            `;
            document.head.appendChild(style);
            
            // Immediately toggle classes on all elements - ensure class is properly set
            const currentlyDark = body.classList.contains('dark-theme');
            if (currentlyDark) {
                // Switching to light
                body.classList.remove('dark-theme');
                html.classList.remove('dark-theme');
                document.documentElement.classList.remove('dark-theme');
            } else {
                // Switching to dark
                body.classList.add('dark-theme');
                html.classList.add('dark-theme');
                document.documentElement.classList.add('dark-theme');
            }
        const isDark = body.classList.contains('dark-theme');
            
            // Update icon immediately
        if (themeIcon) {
            themeIcon.textContent = isDark ? '☀️' : '🌙';
        }
            
            // Save preference (non-blocking)
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            // Apply or remove inline styles based on theme - do it immediately
            if (isDark) {
                applyInlineDarkThemeStyles();
            } else {
                removeInlineDarkThemeStyles();
            }
            
            // Re-enable transitions after a brief moment (for other interactions)
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    if (document.head.contains(style)) {
                        document.head.removeChild(style);
                    }
                });
            });
        });
    }
}

// Initialize theme toggle when DOM is ready - multiple fallbacks
function initializeThemeToggle() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initThemeToggle);
    } else if (document.readyState === 'interactive' || document.readyState === 'complete') {
        // DOM already loaded or nearly loaded
        initThemeToggle();
    } else {
        // Fallback: try immediately and retry if needed
        initThemeToggle();
    }
}

// Try multiple initialization methods
initializeThemeToggle();

// Also try after a short delay as fallback
setTimeout(() => {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle && !themeToggle.hasAttribute('data-listener-attached')) {
        initThemeToggle();
    }
}, 100);

// Chat Agent Functionality
function initChatAgent() {
    // Support both chatButton and chatAgentBtn IDs
    const chatButton = document.getElementById('chatButton') || document.getElementById('chatAgentBtn');
    const chatWindow = document.getElementById('chatWindow');
    const chatClose = document.getElementById('chatClose');
    const chatInput = document.getElementById('chatInput');
    const chatSend = document.getElementById('chatSend');
    const chatMessages = document.getElementById('chatMessages');

    if (chatButton && chatWindow) {
        // Mark listener as attached to prevent duplicates
        if (!chatButton.hasAttribute('data-chat-listener-attached')) {
            chatButton.setAttribute('data-chat-listener-attached', 'true');
            chatButton.addEventListener('click', () => {
                chatWindow.classList.toggle('active');
            });
        }
    }
    
    if (chatClose) {
        chatClose.addEventListener('click', () => {
            chatWindow.classList.remove('active');
        });
    }
    
    if (chatSend && chatInput) {
        const handleSend = async () => {
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Handle special commands
            if (message.startsWith('/setkey ')) {
                const apiKey = message.substring(8).trim();
                localStorage.setItem('mistral_api_key', apiKey);
                addChatMessage('✅ Mistral API key saved! You can now use AI-powered responses.', false);
                chatInput.value = '';
                return;
            }
            
            // Add user message
            addChatMessage(message, true);
            chatInput.value = '';
            chatInput.disabled = true;
            chatSend.disabled = true;
            
            // Show typing indicator
            const typingId = addTypingIndicator();
            
            try {
                // Try Mistral AI first
                const apiKey = localStorage.getItem('mistral_api_key');
                if (apiKey) {
                    const response = await getMistralResponse(message);
                    removeTypingIndicator(typingId);
                    addChatMessage(response, false);
                } else {
                    // Fallback to rule-based
                    removeTypingIndicator(typingId);
                    const fallbackResponse = getFallbackResponse(message);
                    addChatMessage(fallbackResponse, false);
                }
            } catch (error) {
                console.error('Chat error:', error);
                removeTypingIndicator(typingId);
                const fallbackResponse = getFallbackResponse(message);
                addChatMessage(fallbackResponse, false);
            } finally {
                chatInput.disabled = false;
                chatSend.disabled = false;
                chatInput.focus();
            }
        };
        
        chatSend.addEventListener('click', handleSend);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });
    }
}

// Initialize chat agent when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatAgent);
} else {
    initChatAgent();
}

// Also try after a short delay as fallback
setTimeout(() => {
    const chatButton = document.getElementById('chatButton') || document.getElementById('chatAgentBtn');
    if (chatButton && !chatButton.hasAttribute('data-chat-listener-attached')) {
        chatButton.setAttribute('data-chat-listener-attached', 'true');
        initChatAgent();
    }
}, 100);

// Conversation history for context
let conversationHistory = [];

function addChatMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format message (support basic markdown-like formatting)
    const formattedMessage = formatMessage(message);
    contentDiv.innerHTML = formattedMessage;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Store in history (keep last 10 messages)
    conversationHistory.push({ role: isUser ? 'user' : 'assistant', content: message });
    if (conversationHistory.length > 10) {
        conversationHistory.shift();
    }
}

function formatMessage(text) {
    // Convert URLs to links
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    // Convert page paths to links
    text = text.replace(/([a-z]+\/[^\.]+\.html)/g, '<a href="/$1">$1</a>');
    return text;
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return null;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<div class="message-content"><span class="typing-dots">...</span></div>';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// Mistral AI Integration
async function getMistralResponse(userMessage) {
    const apiKey = localStorage.getItem('mistral_api_key');
    if (!apiKey) {
        throw new Error('No API key');
    }
    
    // Load knowledge base if not loaded
    if (!window.MISTRAL_TRAINING || !window.MISTRAL_TRAINING.KNOWLEDGE_BASE.length) {
        if (window.MISTRAL_TRAINING && window.MISTRAL_TRAINING.loadKnowledgeBase) {
            await window.MISTRAL_TRAINING.loadKnowledgeBase();
        }
    }
    
    // Build context from knowledge base (RAG)
    const context = window.MISTRAL_TRAINING?.buildContext(userMessage) || '';
    
    // Build messages array with system prompt and context
    const messages = [
        {
            role: 'system',
            content: (window.MISTRAL_TRAINING?.SYSTEM_PROMPT || '') + '\n\n' + context
        },
        ...conversationHistory.slice(-8), // Last 8 messages for context
        { role: 'user', content: userMessage }
    ];
    
    const response = await fetch('https://api.mistral.ai/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: 'mistral-small', // Can be changed to mistral-medium or mistral-large-latest
            messages: messages,
            temperature: 0.7,
            max_tokens: 1000
        })
    });
    
    if (!response.ok) {
        const error = await response.text();
        throw new Error(`Mistral API error: ${error}`);
    }
    
    const data = await response.json();
    return data.choices[0]?.message?.content || 'I apologize, but I couldn\'t generate a response.';
}

// Fallback rule-based responses
function getFallbackResponse(message) {
    const msg = message.toLowerCase();
    
    // Check for common queries
    if (msg.includes('what is') || msg.includes('explain')) {
        if (msg.includes('piandt')) {
            return 'PIANDT is a Proportional Information Architecture for Networked Digital Transactions. It uses a triadic system (In, Processing, Out) to manage information flow. Would you like to know more about a specific stage?';
        }
        if (msg.includes('triadic') || msg.includes('triad')) {
            return 'The triadic information architecture has three stages: In (incoming signals), Processing (analysis and transformation), and Out (delivered outputs). Each stage maintains proportional relationships (S_In ∝ S_Proc ∝ S_Out).';
        }
    }
    
    if (msg.includes('in ') || msg.includes('incoming')) {
        return 'The In stage handles incoming signals from external stakeholders. You can explore In pages to see how different types of information are received.';
    }
    
    if (msg.includes('processing') || msg.includes('proc')) {
        return 'The Processing stage analyzes and transforms incoming signals. Check the Processing pages to see how information is synthesized.';
    }
    
    if (msg.includes('out ') || msg.includes('output')) {
        return 'The Out stage delivers processed signals to stakeholders. Visit Out pages to see how information is formatted and delivered.';
    }
    
    if (msg.includes('miu') || msg.includes('machine intelligence')) {
        return 'MIU (Machine Intelligence Unit) is part of the Units section. It includes Vision, Products, and Services. Each has In, Processing, and Out variants.';
    }
    
    if (msg.includes('bidirectional') || msg.includes('both direction')) {
        return 'Yes! PIANDT supports bidirectional information flow. Signals can flow from organization to external stakeholders and vice versa.';
    }
    
    if (msg.includes('automation') || msg.includes('automated')) {
        return 'The structured nature of PIANDT enables full automation of business transactions through machine-readable formats and standardized protocols.';
    }
    
    // Default response
    return 'I can help you navigate the PIANDT website! Ask me about:\n- The triadic information architecture (In, Processing, Out)\n- Specific pages or sections\n- MIU (Machine Intelligence Unit)\n- Bidirectionality and automation\n\nTo enable AI-powered responses, type: /setkey your-mistral-api-key';
}

// ============================================
// Movie-Like Seamless Page Transitions
// ============================================
// Provides invisible, ultra-smooth transitions like a movie
// Crossfade technique for seamless navigation

(function() {
    'use strict';
    
    // Prevent multiple initializations
    if (window.pageTransitionInitialized) return;
    window.pageTransitionInitialized = true;
    
    // Configuration for movie-like transitions - no blank screen
    const FADE_IN_DURATION = 80;   // milliseconds - very fast
    const EASING = 'cubic-bezier(0.2, 0, 0.2, 1)'; // Linear-like for seamless feel
    
    // Initialize page - subtle fade-in only
    function initPageFadeIn() {
        // Start with opacity 0 for subtle fade-in
        document.body.style.opacity = '0';
        document.body.classList.add('page-fade-in');
        
        // Fade in immediately
        requestAnimationFrame(() => {
            document.body.style.opacity = '1';
            // Remove fade-in class after animation
            setTimeout(() => {
                document.body.classList.remove('page-fade-in');
            }, FADE_IN_DURATION);
        });
    }
    
    // Handle link clicks with movie-like crossfade
    function handleLinkClicks() {
        // Get all internal links (same origin)
        const links = document.querySelectorAll('a[href]');
        
        links.forEach(link => {
            // Skip if already has transition handler
            if (link.dataset.transitionHandler === 'true') return;
            link.dataset.transitionHandler = 'true';
            
            const href = link.getAttribute('href');
            
            // Skip if it's not a same-origin link or special links
            if (!href || 
                href.startsWith('#') || 
                href.startsWith('javascript:') || 
                href.startsWith('mailto:') || 
                href.startsWith('tel:') ||
                (link.hasAttribute('target') && link.getAttribute('target') === '_blank') ||
                link.hasAttribute('download')) {
                return;
            }
            
            // Check if it's a same-origin link
            try {
                const url = new URL(href, window.location.origin);
                if (url.origin !== window.location.origin) {
                    return; // External link, skip
                }
            } catch (e) {
                // Relative URL, proceed
            }
            
            // Preload page on hover for instant transition
            link.addEventListener('mouseenter', function() {
                if (href && !href.startsWith('#')) {
                    // Prefetch the page for instant loading
                    const linkElement = document.createElement('link');
                    linkElement.rel = 'prefetch';
                    linkElement.href = href;
                    document.head.appendChild(linkElement);
                }
            }, { passive: true });
            
            // Add click handler - no fade-out to prevent blank screen
            link.addEventListener('click', function(e) {
                // Don't interfere with special clicks (Ctrl/Cmd, middle mouse, etc.)
                if (e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) {
                    return;
                }
                
                // Disable pointer events but keep page visible - no blank screen
                document.body.classList.add('page-transition-out');
                
                // Allow navigation to proceed - browser handles the rest
                // The new page will fade in seamlessly without blank screen
            }, { passive: true });
        });
    }
    
    // Handle browser back/forward navigation
    function handleBrowserNavigation() {
        // Use pageshow event for seamless back/forward
        window.addEventListener('pageshow', function(event) {
            // Remove transition-out class
            document.body.classList.remove('page-transition-out');
            
            // If page was loaded from cache (back/forward)
            if (event.persisted) {
                // Instant appearance - no fade needed
                document.body.style.opacity = '1';
            } else {
                // Regular page load - subtle fade-in
                initPageFadeIn();
            }
        });
        
        // Handle page unload - no fade-out to prevent blank screen
        window.addEventListener('beforeunload', function() {
            // Just disable pointer events, keep page visible
            document.body.classList.add('page-transition-out');
        });
    }
    
    // Initialize when DOM is ready
    function initPageTransitions() {
        // Remove any existing transition classes
        document.body.classList.remove('page-transition-out');
        
        // Initialize instant appearance
        initPageFadeIn();
        
        // Setup link handlers
        handleLinkClicks();
        
        // Setup browser navigation handlers
        handleBrowserNavigation();
    }
    
    // Initialize based on document state
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPageTransitions);
    } else {
        // DOM already loaded
        initPageTransitions();
    }
    
    // Also initialize after a short delay to catch dynamically added links
    setTimeout(handleLinkClicks, 100);
    
    // Re-initialize link handlers when new content is added (for dynamic menus)
    const observer = new MutationObserver(function(mutations) {
        let shouldReinit = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.tagName === 'A' || node.querySelector('a'))) {
                        shouldReinit = true;
                    }
                });
            }
        });
        if (shouldReinit) {
            handleLinkClicks();
        }
    });
    
    // Observe the document for new links
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Preload pages on menu hover for instant transitions
    document.addEventListener('mouseover', function(e) {
        const link = e.target.closest('a[href]');
        if (link && link.dataset.transitionHandler === 'true') {
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                try {
                    const url = new URL(href, window.location.origin);
                    if (url.origin === window.location.origin) {
                        // Prefetch for instant loading
                        const prefetchLink = document.createElement('link');
                        prefetchLink.rel = 'prefetch';
                        prefetchLink.href = href;
                        if (!document.querySelector(`link[rel="prefetch"][href="${href}"]`)) {
                            document.head.appendChild(prefetchLink);
                        }
                    }
                } catch (e) {
                    // Invalid URL, skip
                }
            }
        }
    }, { passive: true });
})();

// ============================================
// Hard Refresh on Resize and Column Changes
// ============================================
// Automatically hard refreshes page when viewport or column sizes change

(function() {
    'use strict';
    
    // Prevent multiple initializations
    if (window.resizeRefreshInitialized) return;
    window.resizeRefreshInitialized = true;
    
    let resizeTimer;
    let isRefreshing = false;
    let lastWidth = window.innerWidth;
    let lastHeight = window.innerHeight;
    
    // Get current column count based on viewport width - MUST be defined first
    function getColumnCount() {
        const width = window.innerWidth;
        if (width < 768) return 1;      // Mobile
        if (width < 1024) return 2;    // Tablet
        if (width < 1440) return 3;    // Desktop
        return 4;                       // Large desktop
    }
    
    let lastColumnCount = getColumnCount();
    
    // Hard refresh the page - simple and direct
    function hardRefresh() {
        if (isRefreshing) return;
        isRefreshing = true;
        
        // Force hard refresh - bypass cache
        window.location.reload(true);
    }
    
    // Handle resize events - refresh on ANY resize
    function handleResize() {
        if (isRefreshing) return;
        
        const currentWidth = window.innerWidth;
        const currentHeight = window.innerHeight;
        const currentColumnCount = getColumnCount();
        
        // Check if column count changed (breakpoint crossed)
        if (currentColumnCount !== lastColumnCount) {
            lastColumnCount = currentColumnCount;
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(hardRefresh, 200);
            return;
        }
        
        // Check if size changed significantly
        const widthChanged = Math.abs(currentWidth - lastWidth) > 10;
        const heightChanged = Math.abs(currentHeight - lastHeight) > 10;
        
        if (widthChanged || heightChanged) {
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(hardRefresh, 200);
        }
    }
    
    // Handle orientation changes
    function handleOrientationChange() {
        if (isRefreshing) return;
        setTimeout(hardRefresh, 100);
    }
    
    // Monitor column changes with ResizeObserver
    function observeColumnChanges() {
        const contentElements = document.querySelectorAll('main, .content-grid, .section, .container');
        
        if (contentElements.length > 0 && window.ResizeObserver) {
            const resizeObserver = new ResizeObserver(function(entries) {
                if (isRefreshing) return;
                
                for (let entry of entries) {
                    const currentColumnCount = getColumnCount();
                    if (currentColumnCount !== lastColumnCount) {
                        lastColumnCount = currentColumnCount;
                        clearTimeout(resizeTimer);
                        resizeTimer = setTimeout(hardRefresh, 200);
                        break;
                    }
                }
            });
            
            contentElements.forEach(function(element) {
                resizeObserver.observe(element);
            });
        }
    }
    
    // Initialize immediately
    function initResizeRefresh() {
        // Listen for window resize
        window.addEventListener('resize', handleResize, { passive: true });
        
        // Listen for orientation changes
        window.addEventListener('orientationchange', handleOrientationChange, { passive: true });
        
        // Monitor column changes
        observeColumnChanges();
        
        // Re-observe after delay for dynamic content
        setTimeout(observeColumnChanges, 500);
    }
    
    // Initialize immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initResizeRefresh);
    } else {
        initResizeRefresh();
    }
    
    // Re-observe when new content is added
    if (document.body) {
        const observer = new MutationObserver(function() {
            observeColumnChanges();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
})();
