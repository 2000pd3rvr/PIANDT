/**
 * Menu Hover Control - Ensures only one child menu is visible at a time
 * When hovering over a menu item, hide all sibling menus and show only the hovered item's child menu
 */

(function() {
    'use strict';
    
    let initialized = false;
    
    function hideAllSiblingMenus(currentMenuItem, parentMenu) {
        if (!parentMenu) return;
        
        // Find all direct child li elements in the parent menu
        const siblings = Array.from(parentMenu.children);
        
        siblings.forEach(sibling => {
            if (sibling !== currentMenuItem) {
                // Hide all direct child ul menus of this sibling
                const directUlChildren = Array.from(sibling.children).filter(child => child.tagName === 'UL');
                directUlChildren.forEach(submenu => {
                    submenu.style.opacity = '0';
                    submenu.style.visibility = 'hidden';
                });
            }
        });
    }
    
    function initMenuHoverControl() {
        // Prevent double initialization
        if (initialized) return;
        initialized = true;
        
        // Find all menu items that have child menus
        const allMenuItems = document.querySelectorAll('.dropdown-menu > li:has(> ul), .dropdown-menu ul > li:has(> ul), li:has(> ul) > ul > li:has(> ul)');
        
        allMenuItems.forEach(menuItem => {
            // Get direct child ul (not nested)
            const submenu = Array.from(menuItem.children).find(child => child.tagName === 'UL');
            if (!submenu) return;
            
            // Skip if already has event listeners (check for data attribute)
            if (menuItem.dataset.hoverControlInitialized) return;
            menuItem.dataset.hoverControlInitialized = 'true';
            
            // Get the parent container (the ul that contains this menu item)
            const parentMenu = menuItem.parentElement;
            if (!parentMenu) return;
            
            // On mouseenter (hover start)
            menuItem.addEventListener('mouseenter', function(e) {
                // Hide all sibling menus in the same parent
                hideAllSiblingMenus(menuItem, parentMenu);
                
                // Show this menu item's child menu
                submenu.style.opacity = '1';
                submenu.style.visibility = 'visible';
                submenu.style.transform = 'translateX(0)';
            });
            
            // Also handle when mouse enters the child menu itself
            submenu.addEventListener('mouseenter', function(e) {
                // Keep it visible
                submenu.style.opacity = '1';
                submenu.style.visibility = 'visible';
            });
            
            // When mouse leaves the child menu
            submenu.addEventListener('mouseleave', function(e) {
                setTimeout(() => {
                    // Check if mouse is still over menu item or its child menu
                    if (!menuItem.matches(':hover') && !submenu.matches(':hover')) {
                        submenu.style.opacity = '0';
                        submenu.style.visibility = 'hidden';
                    }
                }, 150);
            });
            
            // On mouseleave (hover end) - hide the child menu after delay
            menuItem.addEventListener('mouseleave', function(e) {
                setTimeout(() => {
                    // Check if mouse moved to child menu
                    if (!menuItem.matches(':hover') && !submenu.matches(':hover')) {
                        submenu.style.opacity = '0';
                        submenu.style.visibility = 'hidden';
                    }
                }, 150);
            });
        });
        
        // Also handle top-level dropdown menus (In/Proc/Out)
        const topLevelDropdowns = document.querySelectorAll('.nav-menu > .dropdown');
        
        topLevelDropdowns.forEach(dropdown => {
            const dropdownMenu = dropdown.querySelector('.dropdown-menu');
            if (!dropdownMenu) return;
            
            // Skip if already initialized
            if (dropdown.dataset.hoverControlInitialized) return;
            dropdown.dataset.hoverControlInitialized = 'true';
            
            dropdown.addEventListener('mouseenter', function() {
                // Hide all other top-level dropdown menus
                topLevelDropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        const otherMenu = otherDropdown.querySelector('.dropdown-menu');
                        if (otherMenu) {
                            otherMenu.style.opacity = '0';
                            otherMenu.style.visibility = 'hidden';
                        }
                    }
                });
                
                // Show this dropdown's menu
                dropdownMenu.style.opacity = '1';
                dropdownMenu.style.visibility = 'visible';
                dropdownMenu.style.transform = 'translateY(0)';
            });
            
            dropdown.addEventListener('mouseleave', function() {
                setTimeout(() => {
                    if (!dropdown.matches(':hover') && !dropdownMenu.matches(':hover')) {
                        dropdownMenu.style.opacity = '0';
                        dropdownMenu.style.visibility = 'hidden';
                    }
                }, 150);
            });
        });
    }
    
    function reinitMenuHoverControl() {
        initialized = false;
        initMenuHoverControl();
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMenuHoverControl);
    } else {
        initMenuHoverControl();
    }
    
    // Re-run after dynamic content is loaded
    setTimeout(reinitMenuHoverControl, 600);
    setTimeout(reinitMenuHoverControl, 1000);
    
    // Observe DOM changes for dynamically added menus
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            let shouldUpdate = false;
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && (
                            (node.classList && (
                                node.classList.contains('dropdown-menu') ||
                                node.classList.contains('dropdown')
                            )) ||
                            node.querySelector('.dropdown-menu') ||
                            node.querySelector('.dropdown')
                        )) {
                            shouldUpdate = true;
                        }
                    });
                }
            });
            if (shouldUpdate) {
                setTimeout(reinitMenuHoverControl, 100);
            }
        });
        
        if (document.body) {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    }
})();
