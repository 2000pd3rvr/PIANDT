#!/usr/bin/env node
/**
 * Generate pages-data.js with all page information for dynamic menu generation
 */
const fs = require('fs');
const path = require('path');

const baseDir = __dirname + '/..';

// Get all HTML files in about_piandt directories
const pages = {
    in: [],
    processing: [],
    out: []
};

function scanDirectory(dir, triad) {
    if (!fs.existsSync(dir)) return;
    
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        if (file.endsWith('.html')) {
            const filePath = path.join(dir, file);
            const relPath = path.relative(baseDir, filePath).replace(/\\/g, '/');
            
            // Extract page type from filename
            let pageType = 'other';
            if (file.includes('mission_vision')) pageType = 'mission_vision';
            else if (file.includes('charitable_purposes')) pageType = 'charitable_purposes';
            else if (file.includes('our_approach')) pageType = 'our_approach';
            else if (file.includes('trustees')) pageType = 'trustees';
            else if (file.includes('governance')) pageType = 'governance';
            else if (file.includes('about_piandt')) pageType = 'about_piandt';
            
            pages[triad].push({
                filename: file,
                path: relPath,
                type: pageType,
                displayName: getDisplayName(file, pageType)
            });
        }
    });
    
    // Sort by display order
    const order = ['about_piandt', 'mission_vision', 'charitable_purposes', 'our_approach', 'trustees', 'governance'];
    pages[triad].sort((a, b) => {
        const aIndex = order.indexOf(a.type);
        const bIndex = order.indexOf(b.type);
        return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
    });
}

function getDisplayName(filename, type) {
    const names = {
        'about_piandt': 'about PIANDT',
        'mission_vision': 'our mission and vision',
        'charitable_purposes': 'charitable purposes',
        'our_approach': 'Our approach',
        'trustees': 'trustees',
        'governance': 'governance'
    };
    return names[type] || filename.replace(/\.html$/, '').replace(/_/g, ' ');
}

// Scan all about_piandt directories
scanDirectory(path.join(baseDir, 'in', 'about_piandt'), 'in');
scanDirectory(path.join(baseDir, 'processing', 'about_piandt'), 'processing');
scanDirectory(path.join(baseDir, 'out', 'about_piandt'), 'out');

// Generate JavaScript file
const jsContent = `// Auto-generated pages data for dynamic menu generation
// Generated: ${new Date().toISOString()}
const PAGES_DATA = ${JSON.stringify(pages, null, 2)};

// Export for use in browser
if (typeof window !== 'undefined') {
    window.PAGES_DATA = PAGES_DATA;
}
`;

fs.writeFileSync(path.join(baseDir, 'pages-data.js'), jsContent);
console.log('Generated pages-data.js');
console.log(`In pages: ${pages.in.length}`);
console.log(`Processing pages: ${pages.processing.length}`);
console.log(`Out pages: ${pages.out.length}`);



