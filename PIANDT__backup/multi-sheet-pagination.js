/**
 * Multi-Sheet Pagination System
 * 
 * Maintains strict 4-column, 20-lines-per-column layout
 * Splits content into multiple "sheets" when content exceeds one page
 * Provides arrow navigation between sheets
 */

(function() {
    'use strict';

    // Configuration
    const LINES_PER_COLUMN = 20;
    const COLUMNS = 4;
    const SHEET_CLASS = 'content-sheet';
    const ACTIVE_SHEET_CLASS = 'sheet-active';
    const PAGINATION_CONTAINER_CLASS = 'sheet-pagination-container';
    const NAV_ARROW_CLASS = 'sheet-nav-arrow';
    const SHEET_INDICATOR_CLASS = 'sheet-indicator';
    const CURRENT_SHEET_CLASS = 'sheet-current';

    // Responsive breakpoints - keep 4 columns on larger screens
    const BREAKPOINT_MOBILE = 768;
    const BREAKPOINT_TABLET = 1024;
    
    /**
     * Get the appropriate column count based on viewport width
     * Desktop (>1024px): 4 columns
     * Tablet (768-1024px): 2 columns  
     * Mobile (<768px): 1 column
     */
    function getColumnCount() {
        const width = window.innerWidth;
        if (width < BREAKPOINT_MOBILE) {
            return 1; // Mobile: 1 column
        } else if (width < BREAKPOINT_TABLET) {
            return 2; // Tablet: 2 columns
        } else {
            return COLUMNS; // Desktop: 4 columns (always)
        }
    }

    /**
     * Calculate the exact height to fit within viewport without scrolling
     * Dynamically calculates based on available viewport height minus navbar/header
     */
    function calculateSheetHeight(element) {
        // Get viewport dimensions
        const viewportHeight = window.innerHeight;
        const viewportWidth = window.innerWidth;
        
        // Calculate space taken by navbar and other elements
        const navbar = document.querySelector('.navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : (viewportWidth < 768 ? 60 : 80);
        const section = element.closest('.section');
        const sectionPaddingTop = section ? parseFloat(window.getComputedStyle(section).paddingTop) || 0 : 0;
        const heading = element.parentElement.querySelector('h1');
        const headingHeight = heading ? heading.offsetHeight + parseFloat(window.getComputedStyle(heading).marginBottom) || 0 : 0;
        
        // Responsive reserved space - less on mobile
        let reservedSpace = navbarHeight + sectionPaddingTop + headingHeight;
        if (viewportWidth < 480) {
            reservedSpace += 20; // Less margin on small screens
        } else if (viewportWidth < 768) {
            reservedSpace += 30;
        } else {
            reservedSpace += 40; // Full margin on desktop
        }
        
        // Calculate available height for content
        const availableHeight = viewportHeight - reservedSpace;
        
        // Responsive minimum height
        const minHeight = viewportWidth < 480 ? 200 : (viewportWidth < 768 ? 250 : 300);
        const sheetHeight = Math.max(minHeight, availableHeight);
        
        console.log(`[Responsive] Viewport: ${viewportWidth}x${viewportHeight}px, Reserved: ${reservedSpace}px, Available: ${availableHeight}px, Sheet height: ${sheetHeight}px`);
        
        return sheetHeight;
    }
    
    /**
     * Calculate how much content (in single-column lines) is needed to fill
     * 4 columns with 20 lines each = 80 lines total
     */
    function calculateContentLinesNeeded() {
        return LINES_PER_COLUMN * COLUMNS; // 20 × 4 = 80 lines
    }

    /**
     * Measure the actual height of content when rendered in 4 columns
     * Returns the height the content takes when distributed across 4 columns
     */
    function measureContentHeight(contentHTML, containerWidth, computedStyle) {
        const tempDiv = document.createElement('div');
        
        // CRITICAL: Use actual column count from viewport, but ensure desktop uses 4 columns
        // This prevents mismatch between measurement and splitting
        const actualColumnCount = getColumnCount();
        const measureColumnCount = actualColumnCount >= COLUMNS ? COLUMNS : actualColumnCount;
        
        tempDiv.style.cssText = `
            position: absolute;
            visibility: hidden;
            width: ${containerWidth}px !important;
            min-width: ${containerWidth}px !important;
            max-width: ${containerWidth}px !important;
            column-count: ${measureColumnCount} !important;
            -webkit-column-count: ${measureColumnCount} !important;
            -moz-column-count: ${measureColumnCount} !important;
            column-gap: ${computedStyle.columnGap || '4rem'} !important;
            -webkit-column-gap: ${computedStyle.columnGap || '4rem'} !important;
            -moz-column-gap: ${computedStyle.columnGap || '4rem'} !important;
            /* CRITICAL: Do NOT set column-width when using column-count - it causes columns to merge */
            column-fill: auto !important;
            -webkit-column-fill: auto !important;
            font-size: ${computedStyle.fontSize || '1.15rem'} !important;
            line-height: ${computedStyle.lineHeight || '1.9'} !important;
            font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
            text-align: justify !important;
            padding: 0 !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            top: -9999px;
            left: -9999px;
        `;
        
        tempDiv.innerHTML = contentHTML;
        document.body.appendChild(tempDiv);
        
        // Force a reflow to ensure columns are calculated
        void tempDiv.offsetHeight;
        
        const height = tempDiv.offsetHeight;
        document.body.removeChild(tempDiv);
        
        return height;
    }
    
    /**
     * Measure content height in a single column to determine how many lines it represents
     * This helps us calculate if we have enough content to fill 4 columns × 20 lines
     */
    function measureContentHeightSingleColumn(contentHTML, containerWidth, computedStyle) {
        const tempDiv = document.createElement('div');
        const singleColumnWidth = (containerWidth - (parseFloat(computedStyle.columnGap) || 64) * (COLUMNS - 1)) / COLUMNS;
        
        tempDiv.style.cssText = `
            position: absolute;
            visibility: hidden;
            width: ${singleColumnWidth}px !important;
            min-width: ${singleColumnWidth}px !important;
            max-width: ${singleColumnWidth}px !important;
            column-count: 1 !important;
            font-size: ${computedStyle.fontSize || '1.15rem'} !important;
            line-height: ${computedStyle.lineHeight || '1.9'} !important;
            font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
            text-align: justify !important;
            padding: 0 !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            top: -9999px;
            left: -9999px;
        `;
        
        tempDiv.innerHTML = contentHTML;
        document.body.appendChild(tempDiv);
        
        void tempDiv.offsetHeight;
        const height = tempDiv.offsetHeight;
        document.body.removeChild(tempDiv);
        
        // Calculate approximate number of lines
        const lineHeight = parseFloat(computedStyle.lineHeight) || parseFloat(computedStyle.fontSize) * 1.9;
        const lines = Math.ceil(height / lineHeight);
        
        return { height, lines };
    }

    /**
     * Split content intelligently at natural break points
     * Logic: Fill each sheet completely (4 columns × 20 lines) before creating next sheet
     * Always create at least one sheet, even if content is short
     */
    function splitContentAtBreakPoints(contentHTML, sheetHeight, containerWidth, computedStyle) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(contentHTML, 'text/html');
        const body = doc.body;
        
        // If content is just one paragraph, we need to split it
        const elements = Array.from(body.children);
        if (elements.length === 0) {
            // Always return at least one sheet, even if empty
            return [contentHTML || '<p></p>'];
        }
        
        const sheets = [];
        const columnGap = computedStyle.columnGap || computedStyle.getPropertyValue('column-gap') || '4rem';
        
        // Create a temporary measuring container with exact same styles
        // CRITICAL: Use actual column count from viewport to match display
        // But ensure we always measure with 4 columns on desktop to fill all 4 before new sheet
        const actualColumnCount = getColumnCount();
        const measureColumnCount = actualColumnCount >= COLUMNS ? COLUMNS : actualColumnCount;
        const measureDiv = document.createElement('div');
        measureDiv.style.cssText = `
            position: absolute;
            visibility: hidden;
            width: ${containerWidth}px !important;
            min-width: ${containerWidth}px !important;
            max-width: ${containerWidth}px !important;
            column-count: ${measureColumnCount} !important;
            -webkit-column-count: ${measureColumnCount} !important;
            -moz-column-count: ${measureColumnCount} !important;
            column-gap: ${columnGap} !important;
            -webkit-column-gap: ${columnGap} !important;
            -moz-column-gap: ${columnGap} !important;
            /* CRITICAL: Do NOT set column-width when using column-count - it causes columns to merge */
            column-fill: auto !important;
            -webkit-column-fill: auto !important;
            font-size: ${computedStyle.fontSize || '1.15rem'} !important;
            line-height: ${computedStyle.lineHeight || '1.9'} !important;
            font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
            text-align: justify !important;
            box-sizing: border-box !important;
            top: -9999px;
            left: -9999px;
        `;
        document.body.appendChild(measureDiv);
        
        // Helper function to measure content height in 4 columns
        function measureHeight(content) {
            measureDiv.innerHTML = content;
            void measureDiv.offsetHeight;
            return measureDiv.offsetHeight;
        }
        
        // Helper function to measure content in single column to estimate total lines
        function measureSingleColumnLines(content) {
            const singleColumnDiv = document.createElement('div');
            const singleColumnWidth = (containerWidth - (parseFloat(columnGap) || 64) * (measureColumnCount - 1)) / measureColumnCount;
            const lineHeight = parseFloat(computedStyle.lineHeight) || parseFloat(computedStyle.fontSize) * 1.9;
            
            singleColumnDiv.style.cssText = `
                position: absolute;
                visibility: hidden;
                width: ${singleColumnWidth}px !important;
                column-count: 1 !important;
                font-size: ${computedStyle.fontSize || '1.15rem'} !important;
                line-height: ${computedStyle.lineHeight || '1.9'} !important;
                font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
                text-align: justify !important;
                top: -9999px;
                left: -9999px;
            `;
            
            singleColumnDiv.innerHTML = content;
            document.body.appendChild(singleColumnDiv);
            void singleColumnDiv.offsetHeight;
            const singleColumnHeight = singleColumnDiv.offsetHeight;
            document.body.removeChild(singleColumnDiv);
            
            // Calculate approximate number of lines
            const lines = Math.ceil(singleColumnHeight / lineHeight);
            return lines;
        }
        
        // Helper function to check if content fills sheet (4 columns × 20 lines)
        // CRITICAL: Must ensure ALL 4 columns are FULL before creating a new sheet
        // This means the content must fill the full sheet height in 4-column layout
        // AND have at least 294 words (98% of 300 words = 75 words × 4 columns)
        function isSheetFull(content) {
            // Get current display column count (4 for desktop, 2 for tablet, 1 for mobile)
            const currentDisplayColumnCount = getColumnCount();
            const targetWordsPerSheet = 75 * currentDisplayColumnCount; // 300 for 4 columns, 150 for 2, 75 for 1
            const minWordsNeeded = Math.ceil(targetWordsPerSheet * 0.98); // 294 for 4 columns, 147 for 2, 74 for 1
            const minLinesNeeded = LINES_PER_COLUMN * currentDisplayColumnCount; // 80 for 4 columns, 40 for 2, 20 for 1
            
            // PRIMARY CHECK: Word count must meet minimum requirement
            // CRITICAL: For desktop (4 columns), must have at least 294 words before creating next sheet
            // This ensures all 4 columns are full with ~75 words each
            const textContent = content.replace(/<[^>]+>/g, '');
            const wordCount = textContent.split(/\s+/).filter(w => w.trim().length > 0).length;
            
            if (wordCount < minWordsNeeded) {
                console.log(`[isSheetFull] Word count insufficient: ${wordCount} words (need ${minWordsNeeded} for ${currentDisplayColumnCount} columns, target: ${targetWordsPerSheet})`);
                return false; // Not enough words - columns not full
            }
            
            // SECONDARY CHECK: Height in current column layout MUST reach or exceed sheetHeight
            // This is the most accurate visual measure - if content doesn't fill the height,
            // it means not all columns are full, so we should NOT create a new sheet
            const heightInCurrentCols = measureHeight(content);
            
            // Content must fill at least 98% of sheet height in current column layout
            // This ensures all columns are actually being used
            if (heightInCurrentCols < sheetHeight * 0.98) {
                console.log(`[isSheetFull] Height insufficient: ${heightInCurrentCols}px (need ${sheetHeight * 0.98}px for ${currentDisplayColumnCount} columns)`);
                return false; // Not full - don't create new sheet yet
            }
            
            // TERTIARY CHECK: Line count must meet minimum requirement
            // This ensures the last column (column 4 on desktop) has content
            const totalLines = measureSingleColumnLines(content);
            
            if (totalLines < minLinesNeeded) {
                console.log(`[isSheetFull] Line count insufficient: ${totalLines} lines (need ${minLinesNeeded} for ${currentDisplayColumnCount} columns)`);
                return false; // Not enough lines - last column likely empty
            }
            
            // All conditions met: enough words, enough height, enough lines
            // This means all columns are truly full
            const avgWordsPerColumn = Math.round(wordCount / currentDisplayColumnCount);
            console.log(`[isSheetFull] ✓ Sheet is FULL: ${wordCount} words (avg: ${avgWordsPerColumn}/column), ${heightInCurrentCols}px height, ${totalLines} lines for ${currentDisplayColumnCount} columns`);
            return true;
        }
        
        // If we have a single large element (like one big paragraph), split it by words
        if (elements.length === 1) {
            const element = elements[0];
            const elementText = element.textContent || '';
            const words = elementText.split(/\s+/).filter(w => w.trim().length > 0);
            
            if (words.length === 0) {
                // Empty content, still create one sheet
                sheets.push(element.outerHTML);
                document.body.removeChild(measureDiv);
                return sheets;
            }
            
            // Iterative approach: build each sheet by adding words until it's full
            // CRITICAL: Must ensure column 4 has at least 20 lines before moving to next sheet
            let currentSheetWords = [];
            
            for (let i = 0; i < words.length; i++) {
                // Add next word to current sheet
                const testWords = [...currentSheetWords, words[i]];
                const testElement = element.cloneNode(true);
                testElement.textContent = testWords.join(' ');
                const testContent = testElement.outerHTML;
                
                // Check if sheet is full (including column 4 having 20 lines)
                if (isSheetFull(testContent) && currentSheetWords.length > 0) {
                    // Current sheet is full (all 4 columns including column 4), save it and start new one
                    const fullSheetElement = element.cloneNode(true);
                    fullSheetElement.textContent = currentSheetWords.join(' ');
                    sheets.push(fullSheetElement.outerHTML);
                    
                    console.log(`Sheet ${sheets.length} filled: ${currentSheetWords.length} words, column 4 has at least 20 lines`);
                    
                    // Start new sheet with current word
                    currentSheetWords = [words[i]];
                } else {
                    // Add word to current sheet
                    currentSheetWords.push(words[i]);
                }
            }
            
            // Add remaining words to final sheet (even if not full)
            if (currentSheetWords.length > 0) {
                const finalSheetElement = element.cloneNode(true);
                finalSheetElement.textContent = currentSheetWords.join(' ');
                const finalContent = finalSheetElement.outerHTML;
                
                // Verify final sheet - if it's full (including column 4), log it
                if (isSheetFull(finalContent)) {
                    console.log(`Final sheet ${sheets.length + 1} filled: ${currentSheetWords.length} words, column 4 has at least 20 lines`);
                } else {
                    const finalLines = measureSingleColumnLines(finalContent);
                    console.log(`Final sheet ${sheets.length + 1} partial: ${currentSheetWords.length} words, ~${finalLines} lines total (column 4 may have less than 20 lines)`);
                }
                
                sheets.push(finalContent);
            }
            
            // Always ensure at least one sheet exists
            if (sheets.length === 0) {
                sheets.push(element.outerHTML);
            }
            
            console.log(`Single element: ${words.length} words split into ${sheets.length} sheets`);
            
            // Clean up measureDiv for single element path
            if (measureDiv.parentNode) {
                document.body.removeChild(measureDiv);
            }
        } else {
            // CRITICAL: Dynamic content splitting based on available space
            // Calculate words per column based on viewport size and available height
            
            console.log(`[Dynamic Splitting] Found ${elements.length} paragraph elements, calculating words per column based on viewport`);
            
            // Step 1: Calculate available column height and words per column
            const currentColumnCount = getColumnCount();
            const singleColumnWidth = (containerWidth - (parseFloat(columnGap) || 64) * (currentColumnCount - 1)) / currentColumnCount;
            const lineHeight = parseFloat(computedStyle.lineHeight) || parseFloat(computedStyle.fontSize) * 1.9;
            const fontSize = parseFloat(computedStyle.fontSize) || parseFloat(window.getComputedStyle(document.body).fontSize);
            
            // Calculate how many lines fit in one column
            const linesPerColumn = Math.floor(sheetHeight / lineHeight);
            
            // Measure how many words fit in one column by testing with sample text
            // Responsive: Adjusts based on viewport size
            function calculateWordsPerColumn() {
                // Get responsive font size based on viewport
                let responsiveFontSize = computedStyle.fontSize || '1.08rem';
                let responsiveLineHeight = computedStyle.lineHeight || '1.9';
                
                // Adjust for different screen sizes
                const viewportWidth = window.innerWidth;
                if (viewportWidth < 480) {
                    responsiveFontSize = '0.9rem';
                    responsiveLineHeight = '1.6';
                } else if (viewportWidth < 768) {
                    responsiveFontSize = '0.95rem';
                    responsiveLineHeight = '1.7';
                } else if (viewportWidth < 1024) {
                    responsiveFontSize = '1rem';
                    responsiveLineHeight = '1.8';
                }
                
                const testDiv = document.createElement('div');
                testDiv.style.cssText = `
                    position: absolute;
                    visibility: hidden;
                    width: ${singleColumnWidth}px !important;
                    column-count: 1 !important;
                    font-size: ${responsiveFontSize} !important;
                    line-height: ${responsiveLineHeight} !important;
                    font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
                    text-align: justify !important;
                    height: ${sheetHeight}px !important;
                    overflow: hidden !important;
                    top: -9999px;
                    left: -9999px;
                    box-sizing: border-box !important;
                `;
                document.body.appendChild(testDiv);
                
                // Binary search to find how many words fit
                // Target words per column: Desktop ~75, Tablet ~37, Mobile ~18
                let bestFit = 75; // Default fallback for desktop
                
                // Adjust default based on viewport to match target words per column
                if (viewportWidth < 480) {
                    bestFit = 18; // Mobile: ~18 words per column
                } else if (viewportWidth < 768) {
                    bestFit = 18; // Mobile: ~18 words per column
                } else if (viewportWidth < 1024) {
                    bestFit = 37; // Tablet: ~37 words per column
                } else {
                    bestFit = 75; // Desktop: ~75 words per column
                }
                
                // Test with increasing word counts to find the maximum that fits
                // Adjust range based on target words per column
                let maxTestWords, startWords, stepSize;
                if (viewportWidth < 768) {
                    // Mobile: target ~18 words
                    maxTestWords = 30;
                    startWords = 10;
                    stepSize = 2;
                } else if (viewportWidth < 1024) {
                    // Tablet: target ~37 words
                    maxTestWords = 60;
                    startWords = 20;
                    stepSize = 3;
                } else {
                    // Desktop: target ~75 words
                    maxTestWords = 150;
                    startWords = 50;
                    stepSize = 5;
                }
                
                for (let testWords = startWords; testWords <= maxTestWords; testWords += stepSize) {
                    const testContent = `<p>${"word ".repeat(testWords)}</p>`;
                    testDiv.innerHTML = testContent;
                    void testDiv.offsetHeight;
                    const contentHeight = testDiv.offsetHeight;
                    
                    if (contentHeight <= sheetHeight * 1.05) { // Allow 5% overflow tolerance
                        bestFit = testWords;
                    } else {
                        break; // Found the limit
                    }
                }
                
                document.body.removeChild(testDiv);
                
                // Ensure minimum words per column based on target
                let minWords;
                if (viewportWidth < 768) {
                    minWords = 15; // Mobile: minimum 15 words
                } else if (viewportWidth < 1024) {
                    minWords = 30; // Tablet: minimum 30 words
                } else {
                    minWords = 60; // Desktop: minimum 60 words
                }
                
                return Math.max(bestFit, minWords);
            }
            
            const wordsPerColumn = calculateWordsPerColumn();
            const wordsPerSheet = wordsPerColumn * currentColumnCount;
            
            console.log(`[Dynamic Splitting] Viewport: ${window.innerWidth}x${window.innerHeight}px, Columns: ${currentColumnCount}, Sheet height: ${sheetHeight}px, Words per column: ~${wordsPerColumn}, Words per sheet: ~${wordsPerSheet}`);
            console.log(`[Dynamic Splitting] Note: With fewer words per column (${wordsPerColumn}), the system will automatically create more sheets to accommodate all content`);
            console.log(`[Dynamic Splitting] With fewer words per column (${wordsPerColumn}), more sheets will be created to accommodate all content`);
            
            // Step 2: Extract all paragraphs and their words
            const paragraphs = [];
            elements.forEach((element) => {
                const elementHTML = element.innerHTML;
                const elementText = element.textContent || '';
                const words = elementText.split(/\s+/).filter(w => w.trim().length > 0);
                paragraphs.push({
                    html: elementHTML,
                    text: elementText,
                    words: words,
                    wordCount: words.length
                });
            });
            
            // Step 3: Dynamically split content to fill columns based on available space
            // Build sheets by adding words until columns fill, then move to next sheet
            let currentSheetContent = [];
            let currentColumnContent = [];
            let currentColumnIndex = 0;
            let paragraphIndex = 0;
            let wordIndexInParagraph = 0;
            
            while (paragraphIndex < paragraphs.length || currentColumnContent.length > 0) {
                // Get next word
                let word = null;
                if (paragraphIndex < paragraphs.length) {
                    const para = paragraphs[paragraphIndex];
                    if (wordIndexInParagraph < para.words.length) {
                        word = para.words[wordIndexInParagraph];
                        wordIndexInParagraph++;
                    } else {
                        // Move to next paragraph
                        paragraphIndex++;
                        wordIndexInParagraph = 0;
                        continue;
                    }
                } else if (currentColumnContent.length > 0) {
                    // No more words, but we have content in current column
                    break;
                } else {
                    break;
                }
                
                // Add word to current column
                currentColumnContent.push(word);
                
                // Check if current column is full
                if (currentColumnContent.length >= wordsPerColumn) {
                    // Column is full, create paragraph for this column
                    currentSheetContent.push(`<p>${currentColumnContent.join(' ')}</p>`);
                    currentColumnContent = [];
                    currentColumnIndex++;
                    
                    // Check if sheet is full (all columns filled)
                    if (currentColumnIndex >= currentColumnCount) {
                        // Sheet is full, save it and start new one
                        const sheetContent = currentSheetContent.join('\n');
                        sheets.push(sheetContent);
                        const totalWords = currentSheetContent.reduce((sum, para) => {
                            const text = para.replace(/<[^>]+>/g, '');
                            return sum + text.split(/\s+/).filter(w => w.trim().length > 0).length;
                        }, 0);
                        console.log(`Sheet ${sheets.length} filled: ${currentColumnCount} columns, ~${totalWords} words (~${Math.round(totalWords/currentColumnCount)} words/column)`);
                        currentSheetContent = [];
                        currentColumnIndex = 0;
                    }
                }
            }
            
            // Add remaining words to current column
            if (currentColumnContent.length > 0) {
                currentSheetContent.push(`<p>${currentColumnContent.join(' ')}</p>`);
                currentColumnIndex++;
            }
            
            // Pad remaining columns in current sheet if needed
            while (currentSheetContent.length < currentColumnCount && currentSheetContent.length > 0) {
                currentSheetContent.push('<p></p>');
            }
            
            // Add final sheet if it has content
            if (currentSheetContent.length > 0) {
                const sheetContent = currentSheetContent.join('\n');
                sheets.push(sheetContent);
                const totalWords = currentSheetContent.reduce((sum, para) => {
                    const text = para.replace(/<[^>]+>/g, '');
                    return sum + text.split(/\s+/).filter(w => w.trim().length > 0).length;
                }, 0);
                console.log(`Final sheet ${sheets.length}: ${currentSheetContent.length} columns, ~${totalWords} words`);
            }
            
            // Always ensure at least one sheet
            if (sheets.length === 0) {
                // Create one sheet with empty paragraphs for each column
                const emptyParas = Array(currentColumnCount).fill('<p></p>').join('\n');
                sheets.push(emptyParas);
            }
            
            const totalWords = paragraphs.reduce((sum, p) => sum + p.wordCount, 0);
            const avgWordsPerSheet = sheets.length > 0 ? Math.round(totalWords / sheets.length) : 0;
            console.log(`[Dynamic Splitting] ✓ Split ${totalWords} total words into ${sheets.length} sheets (${currentColumnCount} columns, ~${wordsPerColumn} words/column, ~${avgWordsPerSheet} words/sheet)`);
            console.log(`[Dynamic Splitting] Note: With fewer words per column (${wordsPerColumn}), more sheets (${sheets.length}) are created to display all ${totalWords} words`);
            
            // Clean up measureDiv
            if (measureDiv.parentNode) {
                document.body.removeChild(measureDiv);
            }
            
            // Always return at least one sheet
            return sheets.length > 0 ? sheets : [contentHTML || '<p></p>'];
        }
    }

    /**
     * Create navigation controls - positioned on left/right sides of content area
     */
    function createNavigationControls(sheetCount, contentElement) {
        // Previous arrow (left side) - positioned absolutely relative to content area
        const prevArrow = document.createElement('button');
        prevArrow.className = `${NAV_ARROW_CLASS} ${NAV_ARROW_CLASS}--prev`;
        prevArrow.innerHTML = '←';
        prevArrow.setAttribute('aria-label', 'Previous sheet');
        prevArrow.disabled = true;
        
        // Next arrow (right side) - positioned absolutely relative to content area
        const nextArrow = document.createElement('button');
        nextArrow.className = `${NAV_ARROW_CLASS} ${NAV_ARROW_CLASS}--next`;
        nextArrow.innerHTML = '→';
        nextArrow.setAttribute('aria-label', 'Next sheet');
        if (sheetCount <= 1) {
            nextArrow.disabled = true;
        }
        
        // Sheet indicators removed - navigation is handled by arrows only
        
        // Return arrows only (indicators removed)
        return {
            prevArrow,
            nextArrow,
            indicatorsContainer: null
        };
    }

    /**
     * Initialize pagination for a content element
     */
    function initPagination(contentElement) {
        // Check if already initialized
        if (contentElement.dataset.paginationInitialized === 'true') {
            return;
        }
        
        // Store original content BEFORE hiding
        const originalContent = contentElement.innerHTML;
        contentElement.dataset.originalContent = originalContent;
        
        // CRITICAL: Temporarily show content for measurements if it's hidden by CSS
        // This prevents flash while still allowing accurate measurements
        const computedStyleBefore = window.getComputedStyle(contentElement);
        const wasHiddenByCSS = computedStyleBefore.visibility === 'hidden' || 
                               computedStyleBefore.opacity === '0';
        
        if (wasHiddenByCSS) {
            // Temporarily show for measurements
            contentElement.style.visibility = 'visible';
            contentElement.style.opacity = '1';
            // Force a reflow to ensure element is laid out
            void contentElement.offsetHeight;
        }
        
        // Get computed styles from original element to preserve them - MUST be done while visible
        const computedStyle = window.getComputedStyle(contentElement);
        // Responsive column gap based on viewport
        let columnGap = computedStyle.columnGap || computedStyle.getPropertyValue('column-gap');
        if (!columnGap || columnGap === 'normal') {
            const viewportWidthForGap = window.innerWidth;
            if (viewportWidthForGap < 480) {
                columnGap = '1rem'; // Smaller gap on mobile
            } else if (viewportWidthForGap < 768) {
                columnGap = '1.5rem';
            } else if (viewportWidthForGap < 1024) {
                columnGap = '2rem'; // Medium gap on tablet
            } else {
                columnGap = '4rem'; // Full gap on desktop
            }
        }
        
        // Measure dimensions while element is still visible and laid out
        const containerWidth = contentElement.offsetWidth || contentElement.clientWidth;
        if (!containerWidth || containerWidth === 0) {
            console.warn('Content element has no width, skipping pagination');
            return;
        }
        
        // Calculate sheet height (20 lines) - do this while visible
        const sheetHeight = calculateSheetHeight(contentElement);
        
        // Calculate and store words per column for tracking
        const currentWordsPerColumn = calculateWordsPerColumnForViewport();
        if (currentWordsPerColumn !== null) {
            lastWordsPerColumn = currentWordsPerColumn;
            console.log(`[initPagination] Words per column: ${currentWordsPerColumn}`);
        }
        
        // Measure total content height - do this while visible, pass computedStyle
        const totalHeight = measureContentHeight(originalContent, containerWidth, computedStyle);
        
        // NOW hide content-text to prevent flash during processing
        const originalVisibility = contentElement.style.visibility;
        const originalOpacity = contentElement.style.opacity;
        contentElement.style.visibility = 'hidden';
        contentElement.style.opacity = '0';
        
        // Calculate how many sheets are needed
        // Always create at least one sheet, even if content is short
        const sheetsNeeded = Math.max(1, Math.ceil(totalHeight / sheetHeight));
        
        console.log(`Content height: ${totalHeight}px, sheet height: ${sheetHeight}px, will create ${sheetsNeeded} sheet(s)`);
        
        // Split content into sheets - pass computedStyle for accurate measurement
        const sheetContents = splitContentAtBreakPoints(originalContent, sheetHeight, containerWidth, computedStyle);
        const currentColumnCount = getColumnCount();
        console.log(`Split content into ${sheetContents.length} sheets (viewport: ${window.innerWidth}px, column count: ${currentColumnCount})`);
        
        // CRITICAL: Always ensure at least one sheet exists, even if content is very short
        if (sheetContents.length === 0) {
            console.warn('No sheets created from split, creating at least one sheet with original content');
            sheetContents.push(originalContent || '<p></p>');
        }
        
        // Verify each sheet has proper word count for desktop (4 columns)
        // This helps ensure the ~75 words per column rule is being followed
        if (currentColumnCount >= 4 && sheetContents.length > 1) {
            sheetContents.forEach((content, idx) => {
                const textContent = content.replace(/<[^>]+>/g, '');
                const wordCount = textContent.split(/\s+/).filter(w => w.trim().length > 0).length;
                const targetWords = 75 * 4; // 300 words for 4 columns
                const minWords = Math.ceil(targetWords * 0.98); // 294 words minimum
                
                if (idx < sheetContents.length - 1) {
                    // All sheets except the last must have at least 294 words (98% of 300)
                    // This ensures all 4 columns are full before creating next sheet
                    if (wordCount < minWords) {
                        console.warn(`⚠️ Sheet ${idx + 1} has only ${wordCount} words but should have at least ${minWords} words (75 words × 4 columns) before creating next sheet`);
                    } else {
                        const avgWordsPerColumn = Math.round(wordCount / 4);
                        console.log(`✓ Sheet ${idx + 1} verified: ${wordCount} words (target: ${targetWords}, min: ${minWords}, avg: ${avgWordsPerColumn} words/column)`);
                    }
                } else {
                    // Last sheet can have fewer words (partial sheet)
                    const avgWordsPerColumn = wordCount > 0 ? Math.round(wordCount / 4) : 0;
                    console.log(`Final sheet ${idx + 1}: ${wordCount} words (avg: ${avgWordsPerColumn} words/column, can be partial)`);
                }
            });
        } else if (sheetContents.length === 1) {
            // Single sheet - log word count for verification
            const textContent = sheetContents[0].replace(/<[^>]+>/g, '');
            const wordCount = textContent.split(/\s+/).filter(w => w.trim().length > 0).length;
            const avgWordsPerColumn = wordCount > 0 ? Math.round(wordCount / currentColumnCount) : 0;
            console.log(`Single sheet: ${wordCount} words total (avg: ${avgWordsPerColumn} words/column for ${currentColumnCount} columns)`);
        }
        
        // Create sheet container - use 100% width to match parent
        const sheetContainer = document.createElement('div');
        sheetContainer.className = 'sheet-container';
        sheetContainer.style.width = '100%';
        sheetContainer.style.minWidth = '0';
        sheetContainer.style.maxWidth = '100%';
        sheetContainer.style.position = 'relative';
        sheetContainer.style.boxSizing = 'border-box';
        
        // Create sheets - we'll set width after container is in DOM
        const sheets = [];
        sheetContents.forEach((content, index) => {
            const sheet = document.createElement('div');
            sheet.className = SHEET_CLASS;
            if (index === 0) {
                sheet.classList.add(ACTIVE_SHEET_CLASS);
            }
            // Set initial styles using setProperty for better reliability
            // CRITICAL: Force correct column count with all vendor prefixes based on viewport
            const initialColumnCount = getColumnCount();
            sheet.style.setProperty('display', index === 0 ? 'block' : 'none', 'important');
            sheet.style.setProperty('height', `${sheetHeight}px`, 'important');
            sheet.style.setProperty('max-height', `${sheetHeight}px`, 'important');
            sheet.style.setProperty('overflow-y', 'auto', 'important');
            sheet.style.setProperty('overflow-x', 'hidden', 'important');
            // CRITICAL: Ensure sheets are visible
            sheet.style.setProperty('visibility', 'visible', 'important');
            sheet.style.setProperty('opacity', '1', 'important');
            sheet.style.setProperty('column-count', initialColumnCount.toString(), 'important');
            sheet.style.setProperty('-webkit-column-count', initialColumnCount.toString(), 'important');
            sheet.style.setProperty('-moz-column-count', initialColumnCount.toString(), 'important');
            sheet.style.setProperty('column-gap', columnGap, 'important');
            sheet.style.setProperty('-webkit-column-gap', columnGap, 'important');
            sheet.style.setProperty('-moz-column-gap', columnGap, 'important');
            // CRITICAL: Ensure no padding or margin clips the start of the first column
            sheet.style.setProperty('padding-left', '0', 'important');
            sheet.style.setProperty('margin-left', '0', 'important');
            sheet.style.setProperty('padding-right', '0', 'important');
            sheet.style.setProperty('margin-right', '0', 'important');
            // CRITICAL: Use 'auto' instead of 'balance' to prevent browser from redistributing paragraphs
            // 'auto' fills columns sequentially (paragraph 1 in column 1, paragraph 2 in column 2, etc.)
            // 'balance' would redistribute content to balance column heights, breaking our sequential layout
            sheet.style.setProperty('column-fill', 'auto', 'important');
            sheet.style.setProperty('-webkit-column-fill', 'auto', 'important');
            // CRITICAL: Remove column-width entirely when using column-count
            // Setting column-width can interfere with column-count and cause columns to merge
            sheet.style.removeProperty('column-width');
            sheet.style.removeProperty('-webkit-column-width');
            sheet.style.removeProperty('-moz-column-width');
            // Font size is already set to 1.08rem in CSS (8% increase), use that value
            // Don't apply additional increase to avoid double-applying
            const fontSize = computedStyle.fontSize || '1.08rem';
            sheet.style.setProperty('font-size', fontSize, 'important');
            sheet.style.setProperty('line-height', computedStyle.lineHeight, 'important');
            sheet.style.setProperty('font-family', computedStyle.fontFamily, 'important');
            sheet.style.setProperty('text-align', 'justify', 'important');
            sheet.style.setProperty('color', computedStyle.color, 'important');
            sheet.style.setProperty('box-sizing', 'border-box', 'important');
            sheet.innerHTML = content;
            sheet.setAttribute('data-sheet-index', index);
            sheetContainer.appendChild(sheet);
            sheets.push(sheet);
        });
        
        // Clear the content-text styles that might interfere, but keep the class
        // CRITICAL: Remove any inline column-count first, then set to 1
        // This prevents conflicts with inline styles in HTML
        const inlineStyle = contentElement.getAttribute('style') || '';
        if (inlineStyle.includes('column-count')) {
            // Remove column-count from inline style
            const cleanedStyle = inlineStyle.replace(/column-count\s*:\s*[^;]+;?/gi, '')
                                           .replace(/-webkit-column-count\s*:\s*[^;]+;?/gi, '')
                                           .replace(/-moz-column-count\s*:\s*[^;]+;?/gi, '')
                                           .trim();
            if (cleanedStyle) {
                contentElement.setAttribute('style', cleanedStyle);
            } else {
                contentElement.removeAttribute('style');
            }
        }
        
        // Now set column-count to 1 on parent to prevent CSS column-count from interfering
        // The sheets themselves will have column-count: 4
        contentElement.style.columnCount = '1';
        contentElement.style.setProperty('column-count', '1', 'important');
        contentElement.style.setProperty('-webkit-column-count', '1', 'important');
        contentElement.style.setProperty('-moz-column-count', '1', 'important');
        
        // Also ensure sheet-container doesn't inherit column-count
        sheetContainer.style.setProperty('column-count', '1', 'important');
        sheetContainer.style.setProperty('-webkit-column-count', '1', 'important');
        sheetContainer.style.setProperty('-moz-column-count', '1', 'important');
        contentElement.style.maxHeight = '';
        contentElement.style.overflow = '';
        contentElement.style.height = 'auto';
        // Ensure full width for columns to display
        contentElement.style.width = '100%';
        contentElement.style.minWidth = '0';
        contentElement.style.maxWidth = 'none';
        contentElement.style.display = 'block';
        
        // Replace content with sheet container
        contentElement.innerHTML = '';
        contentElement.appendChild(sheetContainer);
        
        // Reduce gap between h1 and content-text by applying negative margin (about 1cm/40px)
        // BUT: Only on desktop - mobile should have proper spacing
        const viewportWidth = window.innerWidth;
        if (viewportWidth > 768) {
        contentElement.style.setProperty('margin-top', '-2.5rem', 'important');
        } else if (viewportWidth > 480) {
            contentElement.style.setProperty('margin-top', '0', 'important');
            contentElement.style.setProperty('padding-top', '0.75rem', 'important');
        } else {
            contentElement.style.setProperty('margin-top', '0', 'important');
            contentElement.style.setProperty('padding-top', '1rem', 'important');
        }
        
        // Also reduce h1 margin-bottom if it exists, but ensure minimum spacing on mobile
        const h1 = contentElement.parentElement.querySelector('h1');
        if (h1) {
            if (viewportWidth > 768) {
            h1.style.setProperty('margin-bottom', '0.5rem', 'important');
            } else if (viewportWidth > 480) {
                h1.style.setProperty('margin-bottom', '1rem', 'important');
            } else {
                h1.style.setProperty('margin-bottom', '1.25rem', 'important');
            }
        }
        
        // Update spacing on resize
        const updateSpacing = () => {
            const currentWidth = window.innerWidth;
            if (currentWidth > 768) {
                contentElement.style.setProperty('margin-top', '-2.5rem', 'important');
                contentElement.style.removeProperty('padding-top');
                if (h1) h1.style.setProperty('margin-bottom', '0.5rem', 'important');
            } else if (currentWidth > 480) {
                contentElement.style.setProperty('margin-top', '0', 'important');
                contentElement.style.setProperty('padding-top', '0.75rem', 'important');
                if (h1) h1.style.setProperty('margin-bottom', '1rem', 'important');
            } else {
                contentElement.style.setProperty('margin-top', '0', 'important');
                contentElement.style.setProperty('padding-top', '1rem', 'important');
                if (h1) h1.style.setProperty('margin-bottom', '1.25rem', 'important');
            }
        };
        
        // Listen for resize to update spacing
        window.addEventListener('resize', updateSpacing);
        
        // CRITICAL: Force immediate layout calculation to get actual width
        void contentElement.offsetHeight;
        void sheetContainer.offsetHeight;
        
        // Get the actual width of the sheet container (may differ from containerWidth due to padding/margins)
        const actualSheetContainerWidth = sheetContainer.offsetWidth || sheetContainer.clientWidth;
        console.log(`Sheet container actual width: ${actualSheetContainerWidth}px (measured container: ${containerWidth}px)`);
        
        // CRITICAL: Set explicit width on all sheets to match container
        // This ensures columns have the correct width to render 4 columns
        // Also ensure column-count is always 4
        sheets.forEach((sheet, index) => {
            const sheetStyle = sheet.getAttribute('style') || '';
            // Update width in the style string, preserving column-count
            let updatedStyle = sheetStyle.replace(
                /width:\s*[^;!]+/g, 
                `width: ${actualSheetContainerWidth}px !important`
            ).replace(
                /min-width:\s*[^;!]+/g,
                `min-width: ${actualSheetContainerWidth}px !important`
            ).replace(
                /max-width:\s*[^;!]+/g,
                `max-width: ${actualSheetContainerWidth}px !important`
            );
            
            // Ensure column-count is correct with all vendor prefixes based on viewport
            const currentColumnCount = getColumnCount();
            updatedStyle = updatedStyle.replace(
                /column-count:\s*[^;!]+/g,
                `column-count: ${currentColumnCount} !important`
            );
            // CRITICAL: Remove column-width to prevent columns from merging
            updatedStyle = updatedStyle.replace(
                /column-width:\s*[^;!]+/g,
                ''
            ).replace(
                /-webkit-column-width:\s*[^;!]+/g,
                ''
            ).replace(
                /-moz-column-width:\s*[^;!]+/g,
                ''
            );
            if (!updatedStyle.includes('column-count:')) {
                updatedStyle += ` column-count: ${currentColumnCount} !important; -webkit-column-count: ${currentColumnCount} !important; -moz-column-count: ${currentColumnCount} !important;`;
            }
            
            // If width wasn't in the style, add it
            if (!sheetStyle.includes('width:')) {
                sheet.setAttribute('style', sheetStyle + ` width: ${actualSheetContainerWidth}px !important; min-width: ${actualSheetContainerWidth}px !important; max-width: ${actualSheetContainerWidth}px !important; column-count: ${currentColumnCount} !important; -webkit-column-count: ${currentColumnCount} !important; -moz-column-count: ${currentColumnCount} !important;`);
            } else {
                sheet.setAttribute('style', updatedStyle);
            }
            
            // CRITICAL: Also remove column-width via setProperty to ensure it's gone
            sheet.style.removeProperty('column-width');
            sheet.style.removeProperty('-webkit-column-width');
            sheet.style.removeProperty('-moz-column-width');
            
            // Force reflow for first sheet to verify
            if (index === 0) {
                void sheet.offsetHeight;
                const finalSheetWidth = sheet.offsetWidth;
                const finalColumnCount = window.getComputedStyle(sheet).columnCount;
                console.log(`Sheet ${index} final width: ${finalSheetWidth}px, column-count: ${finalColumnCount}`);
                
                const expectedColumnCount = getColumnCount();
                if (parseInt(finalColumnCount) !== expectedColumnCount) {
                    console.warn(`Sheet ${index} has column-count ${finalColumnCount}, expected ${expectedColumnCount} (viewport: ${window.innerWidth}px)`);
                }
            }
        });
        
        // Restore visibility now that sheets are ready
        // CRITICAL: Explicitly set visibility and opacity to visible/1 to override CSS defaults
        // Don't just restore original values (which might be empty) - explicitly show the content
        contentElement.style.visibility = 'visible';
        contentElement.style.opacity = '1';
        
        // Force another reflow after visibility is restored to ensure columns render
        requestAnimationFrame(() => {
            void contentElement.offsetHeight;
            const firstSheet = sheets[0];
            if (firstSheet) {
                void firstSheet.offsetHeight;
                const actualWidth = firstSheet.offsetWidth;
                const actualColumnCount = window.getComputedStyle(firstSheet).columnCount;
                console.log(`After visibility restore - Sheet width: ${actualWidth}px, column-count: ${actualColumnCount}`);
                
                const expectedColumnCount = getColumnCount();
                if (parseInt(actualColumnCount) !== expectedColumnCount) {
                    console.warn(`After restore, sheet has column-count ${actualColumnCount}, expected ${expectedColumnCount} (viewport: ${window.innerWidth}px)`);
                    // Force it again with all vendor prefixes
                    firstSheet.style.setProperty('column-count', expectedColumnCount.toString(), 'important');
                    firstSheet.style.setProperty('-webkit-column-count', expectedColumnCount.toString(), 'important');
                    firstSheet.style.setProperty('-moz-column-count', expectedColumnCount.toString(), 'important');
                    
                    // Force another reflow
                    void firstSheet.offsetHeight;
                    const finalColumnCount = window.getComputedStyle(firstSheet).columnCount;
                    console.log(`After force fix, column-count: ${finalColumnCount}`);
                }
                
                // Set up periodic check to ensure column-count stays correct
                // Reduced frequency to improve performance - only check when needed
                const columnCheckInterval = setInterval(() => {
                    const targetColumnCount = getColumnCount();
                    let needsFix = false;
                    
                    sheets.forEach((sheet) => {
                        if (sheet.offsetParent !== null) { // Only check visible sheets
                            const computed = window.getComputedStyle(sheet);
                            const colCount = parseInt(computed.columnCount);
                            if (colCount !== targetColumnCount) {
                                needsFix = true;
                                console.warn(`Periodic check: Sheet has column-count ${colCount}, fixing to ${targetColumnCount} (viewport: ${window.innerWidth}px)`);
                                sheet.style.setProperty('column-count', targetColumnCount.toString(), 'important');
                                sheet.style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                                sheet.style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
                                // Force reflow to ensure change takes effect
                                void sheet.offsetHeight;
                            }
                        }
                    });
                    
                    // If no fixes needed for 5 seconds, increase interval to reduce CPU usage
                    if (!needsFix) {
                        // Keep interval but reduce logging
                    }
                }, 1000); // Reduced from 200ms to 1000ms (1 second) to improve performance
                
                // Store interval ID for cleanup (convert to string for dataset)
                contentElement.dataset.columnCheckInterval = columnCheckInterval.toString();
            }
        });
        
        // Create navigation controls
        const navControls = createNavigationControls(sheetContents.length, contentElement);
        
        // Position arrows on left/right sides of content area (vertically centered)
        // Find the content-grid or section to position arrows relative to
        const positioningContainer = contentElement.closest('.content-grid') || 
                                     contentElement.closest('.section') || 
                                     contentElement.parentElement;
        
        // Make positioning container relative if it isn't already
        const containerStyle = window.getComputedStyle(positioningContainer);
        if (containerStyle.position === 'static') {
            positioningContainer.style.position = 'relative';
        }
        // CRITICAL: Ensure overflow is visible so arrows positioned outside are visible
        if (containerStyle.overflow === 'hidden' || containerStyle.overflowX === 'hidden') {
            positioningContainer.style.overflow = 'visible';
            positioningContainer.style.overflowX = 'visible';
            console.log('[Arrow Visibility] Set positioning container overflow to visible');
        }
        
        // CRITICAL: Always add arrows to positioning container, even for single-sheet pages
        // Arrows should always be visible, but grayed out when disabled (single sheet or at boundaries)
        positioningContainer.appendChild(navControls.prevArrow);
        positioningContainer.appendChild(navControls.nextArrow);
        
        // Function to update arrow positions based on viewport
        function updateArrowPositions() {
            const viewportWidth = window.innerWidth;
            const prevArrow = navControls.prevArrow;
            const nextArrow = navControls.nextArrow;
            
            // Ensure arrows are visible and properly positioned
            if (viewportWidth > 1024) {
                // Desktop: arrows outside
                prevArrow.style.left = '';
                prevArrow.style.right = '';
                nextArrow.style.left = '';
                nextArrow.style.right = '';
            } else {
                // Tablet/Mobile: arrows inside
                prevArrow.style.left = '8px';
                prevArrow.style.right = '';
                nextArrow.style.left = '';
                nextArrow.style.right = '8px';
            }
            
            // CRITICAL: Always show arrows, but respect disabled state for styling
            // Disabled arrows will be grayed out by CSS (:disabled selector with opacity: 0.3)
            prevArrow.style.display = 'flex';
            nextArrow.style.display = 'flex';
            prevArrow.style.visibility = 'visible';
            nextArrow.style.visibility = 'visible';
            // Don't force opacity - let CSS handle disabled state (opacity: 0.3 for disabled)
            // Only set opacity to 1 if arrow is NOT disabled, otherwise remove inline opacity to let CSS take over
            if (prevArrow.disabled) {
                prevArrow.style.opacity = ''; // Remove inline style, let CSS :disabled rule apply
            } else {
                prevArrow.style.opacity = '1';
            }
            if (nextArrow.disabled) {
                nextArrow.style.opacity = ''; // Remove inline style, let CSS :disabled rule apply
            } else {
                nextArrow.style.opacity = '1';
            }
        }
        
        // CRITICAL: Update positions and visibility immediately after appending
        // Use setTimeout to ensure DOM is ready
        setTimeout(() => {
            updateArrowPositions();
            // Double-check disabled state is set correctly for single-sheet pages
            if (sheetContents.length <= 1) {
                navControls.prevArrow.disabled = true;
                navControls.nextArrow.disabled = true;
                // Ensure opacity is cleared so CSS can apply disabled styling
                navControls.prevArrow.style.opacity = '';
                navControls.nextArrow.style.opacity = '';
                // Force visibility
                navControls.prevArrow.style.display = 'flex';
                navControls.nextArrow.style.display = 'flex';
                navControls.prevArrow.style.visibility = 'visible';
                navControls.nextArrow.style.visibility = 'visible';
                console.log(`[Arrow Visibility] Single sheet page (${sheetContents.length} sheet): arrows set to disabled (grayed out), display: flex, visibility: visible`);
            } else {
                console.log(`[Arrow Visibility] Multi-sheet page (${sheetContents.length} sheets): arrows enabled`);
            }
        }, 0);
        
        // Also update positions on initial load
        updateArrowPositions();
        
        // Update positions on resize
        window.addEventListener('resize', () => {
            updateArrowPositions();
        });
        
        // Indicators removed - navigation is handled by arrows only
        
        // Set up navigation
        let currentSheet = 0;
        // Use the sheets array we already created, not querySelectorAll
        // const sheets = sheetContainer.querySelectorAll('.' + SHEET_CLASS);
        const prevBtn = navControls.prevArrow;
        const nextBtn = navControls.nextArrow;
        
        function showSheet(index) {
            // Hide all sheets
            sheets.forEach((sheet, i) => {
                sheet.classList.remove(ACTIVE_SHEET_CLASS);
                sheet.style.display = 'none';
                // Ensure column-count is preserved even when hidden - use actual column count
                const targetColumnCount = getColumnCount();
                sheet.style.setProperty('column-count', targetColumnCount.toString(), 'important');
                sheet.style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                sheet.style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
            });
            
            // Show current sheet
            if (sheets[index]) {
                sheets[index].classList.add(ACTIVE_SHEET_CLASS);
                sheets[index].style.display = 'block';
                // CRITICAL: Force correct column count when showing sheet
                const targetColumnCount = getColumnCount();
                const viewportWidth = window.innerWidth;
                console.log(`[showSheet] Viewport: ${viewportWidth}px, Setting columns to: ${targetColumnCount}`);
                sheets[index].style.setProperty('column-count', targetColumnCount.toString(), 'important');
                sheets[index].style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                sheets[index].style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
                
                // Force reflow to ensure columns render
                void sheets[index].offsetHeight;
                
                // Verify after reflow
                setTimeout(() => {
                    const computed = window.getComputedStyle(sheets[index]);
                    const actualColCount = parseInt(computed.columnCount) || 0;
                    if (actualColCount !== targetColumnCount) {
                        console.warn(`[showSheet] Column count mismatch! Expected: ${targetColumnCount}, Got: ${actualColCount}. Forcing again...`);
                        sheets[index].style.setProperty('column-count', targetColumnCount.toString(), 'important');
                        sheets[index].style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                        sheets[index].style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
                    } else {
                        console.log(`[showSheet] Column count verified: ${actualColCount} columns`);
                    }
                }, 10);
                
                // Double-check after a brief delay (catches DevTools layout recalculation)
                setTimeout(() => {
                    const computed = window.getComputedStyle(sheets[index]);
                    const colCount = parseInt(computed.columnCount);
                    const expectedCount = getColumnCount();
                    if (colCount !== expectedCount) {
                        console.warn(`showSheet: Column-count changed to ${colCount} after display, fixing to ${expectedCount} (viewport: ${window.innerWidth}px)`);
                        sheets[index].style.setProperty('column-count', expectedCount.toString(), 'important');
                        sheets[index].style.setProperty('-webkit-column-count', expectedCount.toString(), 'important');
                        sheets[index].style.setProperty('-moz-column-count', expectedCount.toString(), 'important');
                        void sheets[index].offsetHeight;
                    }
                }, 50);
            }
            
            // Indicators removed - navigation is handled by arrows only
            
            // Update navigation buttons
            prevBtn.disabled = index === 0;
            nextBtn.disabled = index >= sheets.length - 1;
            
            // CRITICAL: Update opacity to respect disabled state
            // Disabled arrows should be grayed out (CSS handles this, but ensure inline styles don't override)
            if (prevBtn.disabled) {
                prevBtn.style.opacity = ''; // Let CSS handle disabled styling
            } else {
                prevBtn.style.opacity = '1';
            }
            if (nextBtn.disabled) {
                nextBtn.style.opacity = ''; // Let CSS handle disabled styling
            } else {
                nextBtn.style.opacity = '1';
            }
            
            currentSheet = index;
        }
        
        prevBtn.addEventListener('click', () => {
            if (currentSheet > 0) {
                showSheet(currentSheet - 1);
            }
        });
        
        nextBtn.addEventListener('click', () => {
            if (currentSheet < sheets.length - 1) {
                showSheet(currentSheet + 1);
            }
        });
        
        // Indicators removed - navigation is handled by arrows only
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            // Only handle if content element or its children have focus
            if (contentElement.contains(document.activeElement) || document.activeElement === document.body) {
                if (e.key === 'ArrowLeft' && currentSheet > 0) {
                    e.preventDefault();
                    showSheet(currentSheet - 1);
                } else if (e.key === 'ArrowRight' && currentSheet < sheets.length - 1) {
                    e.preventDefault();
                    showSheet(currentSheet + 1);
                }
            }
        });
        
        // Mark as initialized
        contentElement.dataset.paginationInitialized = 'true';
        
        // CRITICAL: Add MutationObserver to watch for any column-count changes on sheets
        // This ensures sheets always have correct column count even if something tries to change them
        // Use debouncing to avoid fighting with our own updates
        let mutationCheckTimeout;
        const observer = new MutationObserver((mutations) => {
            // Debounce to avoid checking too frequently
            clearTimeout(mutationCheckTimeout);
            mutationCheckTimeout = setTimeout(() => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                    const target = mutation.target;
                    if (target.classList.contains(SHEET_CLASS)) {
                            // Only check if sheet is visible (to avoid unnecessary checks)
                            if (target.offsetParent === null && !target.classList.contains(ACTIVE_SHEET_CLASS)) {
                                return;
                            }
                            
                        const computed = window.getComputedStyle(target);
                            const colCount = parseInt(computed.columnCount) || 0;
                            const expectedCount = getColumnCount();
                            
                            // Only fix if count is wrong AND we didn't just set it ourselves
                            if (colCount !== expectedCount && colCount > 0) {
                                // Check if our inline style says it should be correct
                                const inlineStyle = target.style.getPropertyValue('column-count');
                                const inlineColCount = inlineStyle ? parseInt(inlineStyle) : null;
                                
                                // If inline style says it should be correct but computed says wrong, CSS is overriding
                                if (inlineColCount === expectedCount || inlineColCount === null) {
                                    // CSS is overriding - force it again, but only log once per sheet
                                    if (!target.dataset.columnCountFixed) {
                                        console.warn(`[MutationObserver] Sheet column-count reverted to ${colCount}, forcing to ${expectedCount} (viewport: ${window.innerWidth}px)`);
                                        target.dataset.columnCountFixed = 'true';
                                        setTimeout(() => {
                                            delete target.dataset.columnCountFixed;
                                        }, 1000);
                                    }
                                    target.style.setProperty('column-count', expectedCount.toString(), 'important');
                                    target.style.setProperty('-webkit-column-count', expectedCount.toString(), 'important');
                                    target.style.setProperty('-moz-column-count', expectedCount.toString(), 'important');
                                    // Force reflow
                                    void target.offsetHeight;
                                }
                        }
                    }
                }
            });
            }, 100); // Debounce by 100ms
        });
        
        // Observe all sheets for style changes
        sheets.forEach((sheet) => {
            observer.observe(sheet, {
                attributes: true,
                attributeFilter: ['style', 'class']
            });
        });
        
        // Store observer reference for cleanup if needed
        contentElement.dataset.paginationObserver = 'active';
    }

    /**
     * Initialize all content-text elements with pagination
     */
    function initAllPagination() {
        const contentTextElements = document.querySelectorAll('.content-text');
        console.log('Found', contentTextElements.length, 'content-text elements');
        
        contentTextElements.forEach((element, idx) => {
            // Check if it has the 4-column layout (from CSS or inline style)
            const computedStyle = window.getComputedStyle(element);
            let columnCount = computedStyle.columnCount;
            
            // Fallback: check inline style
            if (!columnCount || columnCount === 'auto') {
                const inlineColumnCount = element.style.columnCount || 
                                        element.getAttribute('style')?.match(/column-count:\s*(\d+)/)?.[1];
                if (inlineColumnCount) {
                    columnCount = inlineColumnCount;
                }
            }
            
            // Fallback: check CSS property directly
            if (!columnCount || columnCount === 'auto') {
                columnCount = computedStyle.getPropertyValue('column-count') || 
                            computedStyle.getPropertyValue('-webkit-column-count') ||
                            computedStyle.getPropertyValue('-moz-column-count');
            }
            
            const colCount = parseInt(columnCount);
            const expectedCount = getColumnCount();
            console.log(`Element ${idx}: columnCount = ${colCount}, expected = ${expectedCount} (viewport: ${window.innerWidth}px)`);
            
            // Initialize pagination if element has multi-column layout (>= 2 columns on desktop/tablet, or 1 on mobile)
            if (colCount >= expectedCount || (expectedCount === 1 && colCount === 1)) {
                console.log(`Initializing pagination for element ${idx}`);
                // Use setTimeout to ensure layout is calculated
                setTimeout(() => {
                    initPagination(element);
                }, 200);
            } else {
                console.log(`Skipping element ${idx} - column count mismatch (got ${colCount}, expected ${expectedCount})`);
            }
        });
    }

    // Initialize when DOM is ready - reduced delay to prevent flash
    // CRITICAL: Wait for window to be fully loaded to ensure accurate viewport measurement
    // This prevents incorrect column count detection during initial load
    function initializePaginationWhenReady() {
        const viewportWidth = window.innerWidth;
        const columnCount = getColumnCount();
        console.log(`Initializing pagination - Viewport: ${viewportWidth}px, Column count: ${columnCount}`);
        
        // Small delay to ensure styles are applied and layout is stable
        setTimeout(() => {
            initAllPagination();
            // Enforce columns immediately after initialization
            setTimeout(() => {
                enforceColumnCount();
                console.log('Pagination initialized, columns enforced');
            }, 50);
        }, 100);
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOMContentLoaded - waiting for full load');
            if (document.readyState === 'complete') {
                initializePaginationWhenReady();
            } else {
                window.addEventListener('load', initializePaginationWhenReady);
            }
        });
    } else {
        console.log('DOM already ready - checking load state');
        if (document.readyState === 'complete') {
            initializePaginationWhenReady();
        } else {
            window.addEventListener('load', initializePaginationWhenReady);
        }
    }

    // Re-initialize on window resize (with debounce)
    // BUT: Don't reset if it's just DevTools opening (small width change)
    let resizeTimeout;
    let lastWidth = window.innerWidth;
    let lastHeight = window.innerHeight;
    let lastColumnCount = getColumnCount();
    let lastWordsPerColumn = null; // Track words per column to detect changes
    // Track the "real" column count before minimize to prevent unnecessary re-init
    let preMinimizeColumnCount = null;
    let wasMinimized = false;
    // Track if initial load is complete to prevent premature re-initialization
    let initialLoadComplete = false;
    
    /**
     * Calculate words per column based on current viewport
     * This is a standalone version that can be called from resize handler
     */
    function calculateWordsPerColumnForViewport() {
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        // Get a sample content element to measure with
        const sampleElement = document.querySelector('.content-text');
        if (!sampleElement) return null;
        
        const computedStyle = window.getComputedStyle(sampleElement);
        const containerWidth = sampleElement.offsetWidth || sampleElement.clientWidth;
        if (!containerWidth || containerWidth === 0) return null;
        
        const currentColumnCount = getColumnCount();
        const columnGap = computedStyle.columnGap || computedStyle.getPropertyValue('column-gap') || '4rem';
        const singleColumnWidth = (containerWidth - (parseFloat(columnGap) || 64) * (currentColumnCount - 1)) / currentColumnCount;
        const lineHeight = parseFloat(computedStyle.lineHeight) || parseFloat(computedStyle.fontSize) * 1.9;
        
        // Calculate sheet height
        const navbar = document.querySelector('.navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : (viewportWidth < 768 ? 60 : 80);
        const section = sampleElement.closest('.section');
        const sectionPaddingTop = section ? parseFloat(window.getComputedStyle(section).paddingTop) || 0 : 0;
        const heading = sampleElement.parentElement.querySelector('h1');
        const headingHeight = heading ? heading.offsetHeight + parseFloat(window.getComputedStyle(heading).marginBottom) || 0 : 0;
        
        let reservedSpace = navbarHeight + sectionPaddingTop + headingHeight;
        if (viewportWidth < 480) {
            reservedSpace += 20;
        } else if (viewportWidth < 768) {
            reservedSpace += 30;
        } else {
            reservedSpace += 40;
        }
        
        const availableHeight = viewportHeight - reservedSpace;
        const minHeight = viewportWidth < 480 ? 200 : (viewportWidth < 768 ? 250 : 300);
        const sheetHeight = Math.max(minHeight, availableHeight);
        
        // Get responsive font size
        let responsiveFontSize = computedStyle.fontSize || '1.08rem';
        let responsiveLineHeight = computedStyle.lineHeight || '1.9';
        
        if (viewportWidth < 480) {
            responsiveFontSize = '0.9rem';
            responsiveLineHeight = '1.6';
        } else if (viewportWidth < 768) {
            responsiveFontSize = '0.95rem';
            responsiveLineHeight = '1.7';
        } else if (viewportWidth < 1024) {
            responsiveFontSize = '1rem';
            responsiveLineHeight = '1.8';
        }
        
        // Test with sample text to find words per column
        const testDiv = document.createElement('div');
        testDiv.style.cssText = `
            position: absolute;
            visibility: hidden;
            width: ${singleColumnWidth}px !important;
            column-count: 1 !important;
            font-size: ${responsiveFontSize} !important;
            line-height: ${responsiveLineHeight} !important;
            font-family: ${computedStyle.fontFamily || 'EB Garamond, serif'} !important;
            text-align: justify !important;
            height: ${sheetHeight}px !important;
            overflow: hidden !important;
            top: -9999px;
            left: -9999px;
            box-sizing: border-box !important;
        `;
        document.body.appendChild(testDiv);
        
        let bestFit = 75;
        if (viewportWidth < 768) {
            bestFit = 18;
        } else if (viewportWidth < 1024) {
            bestFit = 37;
        }
        
        let maxTestWords, startWords, stepSize;
        if (viewportWidth < 768) {
            maxTestWords = 30;
            startWords = 10;
            stepSize = 2;
        } else if (viewportWidth < 1024) {
            maxTestWords = 60;
            startWords = 20;
            stepSize = 3;
        } else {
            maxTestWords = 150;
            startWords = 50;
            stepSize = 5;
        }
        
        for (let testWords = startWords; testWords <= maxTestWords; testWords += stepSize) {
            const testContent = `<p>${"word ".repeat(testWords)}</p>`;
            testDiv.innerHTML = testContent;
            void testDiv.offsetHeight;
            const contentHeight = testDiv.offsetHeight;
            
            if (contentHeight <= sheetHeight * 1.05) {
                bestFit = testWords;
            } else {
                break;
            }
        }
        
        document.body.removeChild(testDiv);
        
        let minWords;
        if (viewportWidth < 768) {
            minWords = 15;
        } else if (viewportWidth < 1024) {
            minWords = 30;
        } else {
            minWords = 60;
        }
        
        return Math.max(bestFit, minWords);
    }
    
    // Mark initial load as complete after a delay to prevent resize handler from interfering
    setTimeout(() => {
        initialLoadComplete = true;
        console.log('Initial load complete, resize handler now active');
    }, 1000);
    
    /**
     * Update sheet heights based on current viewport height
     * Called when viewport height changes (e.g., DevTools opens/closes)
     */
    function updateSheetHeights() {
        const contentTextElements = document.querySelectorAll('.content-text[data-pagination-initialized="true"]');
        
        contentTextElements.forEach(contentElement => {
            const sheetContainer = contentElement.querySelector('.sheet-container');
            if (!sheetContainer) return;
            
            // Calculate new sheet height based on current viewport
            const newSheetHeight = calculateSheetHeight(contentElement);
            
            // Get current column count to adjust height if needed
            const currentColumnCount = getColumnCount();
            
            // Update all sheets in this container
            const sheets = sheetContainer.querySelectorAll('.' + SHEET_CLASS);
            sheets.forEach(sheet => {
                // Check if content actually fits in the calculated height
                const sheetContent = sheet.innerHTML;
                const tempDiv = document.createElement('div');
                tempDiv.style.cssText = `
                    position: absolute;
                    visibility: hidden;
                    width: ${sheet.offsetWidth}px;
                    column-count: ${currentColumnCount};
                    column-gap: ${window.getComputedStyle(sheet).columnGap || '4rem'};
                    font-size: ${window.getComputedStyle(sheet).fontSize};
                    line-height: ${window.getComputedStyle(sheet).lineHeight};
                    top: -9999px;
                `;
                tempDiv.innerHTML = sheetContent;
                document.body.appendChild(tempDiv);
                void tempDiv.offsetHeight;
                const contentHeight = tempDiv.offsetHeight;
                document.body.removeChild(tempDiv);
                
                // If content is taller than calculated height, allow it to expand
                const finalHeight = Math.max(newSheetHeight, contentHeight);
                
                // Use transition for smooth height change
                sheet.style.setProperty('transition', 'height 0.3s ease, max-height 0.3s ease', 'important');
                sheet.style.setProperty('height', `${finalHeight}px`, 'important');
                sheet.style.setProperty('max-height', `${finalHeight}px`, 'important');
                
                // Ensure scrolling is enabled so no content is cut off
                sheet.style.setProperty('overflow-y', 'auto', 'important');
                sheet.style.setProperty('overflow-x', 'hidden', 'important');
            });
            
            console.log(`Updated ${sheets.length} sheet(s) to height ${newSheetHeight}px (column count: ${currentColumnCount})`);
        });
    }
    
    // Aggressive column enforcement function - defined before use
    
    window.addEventListener('resize', () => {
        // CRITICAL: Don't process resize events during initial load
        // This prevents incorrect column count detection and unnecessary re-initialization
        if (!initialLoadComplete) {
            console.log('Resize during initial load, skipping to prevent interference');
            return;
        }
        
        const currentWidth = window.innerWidth;
        const currentHeight = window.innerHeight;
        const widthChange = Math.abs(currentWidth - lastWidth);
        const heightChange = Math.abs(currentHeight - lastHeight);
        
        // CRITICAL: If window is minimized (very small width), don't process resize
        // This prevents columns from disappearing during minimize
        if (currentWidth < 100 || currentHeight < 100) {
            console.log('Window appears minimized, skipping resize handling');
            wasMinimized = true;
            // Remember the column count before minimize
            if (preMinimizeColumnCount === null) {
                preMinimizeColumnCount = lastColumnCount;
            }
            return;
        }
        
        // Check if we're restoring from minimize
        const isRestoringFromMinimize = wasMinimized && currentWidth >= 100 && currentHeight >= 100;
        if (isRestoringFromMinimize) {
            console.log('Window restored from minimize, restoring previous column count and starting aggressive enforcement');
            // Restore the column count from before minimize
            lastColumnCount = preMinimizeColumnCount;
            wasMinimized = false;
            preMinimizeColumnCount = null;
            // Start aggressive enforcement during restore
            startAggressiveEnforcement(3000);
        }
        
        // Check if column count needs to change (crossed breakpoint)
        const newColumnCount = getColumnCount();
        // CRITICAL: If we're restoring from minimize and column count matches pre-minimize, don't re-init
        const actualColumnCountChanged = lastColumnCount !== newColumnCount;
        const shouldSkipReinit = isRestoringFromMinimize && preMinimizeColumnCount !== null && newColumnCount === preMinimizeColumnCount;
        const columnCountChanged = actualColumnCountChanged && !shouldSkipReinit;
        
        // CRITICAL: Always enforce column-count FIRST, before any other logic
        // This prevents columns from merging during resize
        // Also ensure all active sheets are visible
        document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
            sheet.style.display = 'block';
            sheet.style.visibility = 'visible';
            sheet.style.opacity = '1';
            // Force column count immediately
            const targetCount = getColumnCount();
            sheet.style.setProperty('column-count', targetCount.toString(), 'important');
            sheet.style.setProperty('-webkit-column-count', targetCount.toString(), 'important');
            sheet.style.setProperty('-moz-column-count', targetCount.toString(), 'important');
        });
        enforceColumnCount();
        
        // CRITICAL: If restoring from minimize, always start aggressive enforcement
        if (isRestoringFromMinimize) {
            startAggressiveEnforcement(3000);
        }
        // If this is a significant size change (likely minimize/restore), start aggressive enforcement
        // Lowered threshold to catch more cases
        if (widthChange > 100 || heightChange > 100) {
            startAggressiveEnforcement(2000);
        }
        
        // If only height changed (likely DevTools), update sheet heights dynamically
        if (widthChange < 50 && heightChange > 50) {
            // Height change detected - update sheet heights without re-initializing
            console.log(`Viewport height changed from ${lastHeight}px to ${currentHeight}px, updating sheet heights`);
            updateSheetHeights();
            lastHeight = currentHeight;
            lastWidth = currentWidth;
            // Enforce immediately and again after height update
            enforceColumnCount();
            setTimeout(enforceColumnCount, 10);
            setTimeout(enforceColumnCount, 50);
            setTimeout(enforceColumnCount, 150);
            return;
        }
        
        // CRITICAL: If column count changed, force full re-initialization (hard refresh)
        // This is necessary because words-per-column changes, so content must be re-split
        if (columnCountChanged && !isRestoringFromMinimize) {
            console.log(`🔄 Column count changed from ${lastColumnCount} to ${newColumnCount} (viewport: ${currentWidth}px) - FORCING FULL RE-INITIALIZATION`);
            
            // Find all content elements that have pagination initialized
            const contentTextElements = document.querySelectorAll('.content-text[data-pagination-initialized="true"]');
            
            contentTextElements.forEach(contentElement => {
                console.log(`[HARD REFRESH] Re-initializing pagination for element due to column count change`);
                
                // Remove existing sheets and navigation
                const sheetContainer = contentElement.querySelector('.sheet-container');
                if (sheetContainer) {
                    sheetContainer.remove();
                }
                
                // Remove navigation arrows
                const navArrows = contentElement.parentElement.querySelectorAll('.' + NAV_ARROW_CLASS);
                navArrows.forEach(arrow => arrow.remove());
                
                // Clear pagination initialization flag to allow re-initialization
                contentElement.dataset.paginationInitialized = 'false';
                delete contentElement.dataset.paginationInitialized;
                
                // Restore original content
                if (contentElement.dataset.originalContent) {
                    contentElement.innerHTML = contentElement.dataset.originalContent;
                }
                
                // Force a small delay to ensure DOM is clean, then re-initialize
                setTimeout(() => {
                    initPagination(contentElement);
                }, 50);
            });
            
            // Update tracking variables
            lastColumnCount = newColumnCount;
            lastWordsPerColumn = currentWordsPerColumn; // Update words per column tracking
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            clearTimeout(resizeTimeout);
            return; // Exit early - re-initialization will handle the rest
        }
        
        // Update words per column tracking even if no re-initialization needed
        if (currentWordsPerColumn !== null) {
            lastWordsPerColumn = currentWordsPerColumn;
        }
        
        // OLD CODE BELOW - keeping for reference but should not be reached when column count changes
        if (false) {
            // CRITICAL: First, try to update existing sheets without removing them
            const existingSheets = document.querySelectorAll('.' + SHEET_CLASS);
            const hasExistingSheets = existingSheets.length > 0;
            
            if (hasExistingSheets) {
                console.log(`[RESIZE] Found ${existingSheets.length} existing sheets, updating column count from ${lastColumnCount} to ${newColumnCount} without re-initialization`);
                
                // CRITICAL: Update column count on all existing sheets IMMEDIATELY
                existingSheets.forEach((sheet, idx) => {
                    // Force column count with maximum priority
                    sheet.style.cssText = sheet.style.cssText.replace(
                        /column-count\s*:\s*[^;!]+/gi,
                        ''
                    ).replace(
                        /-webkit-column-count\s*:\s*[^;!]+/gi,
                        ''
                    ).replace(
                        /-moz-column-count\s*:\s*[^;!]+/gi,
                        ''
                    );
                    
                    // Set column count with !important
                    sheet.style.setProperty('column-count', newColumnCount.toString(), 'important');
                    sheet.style.setProperty('-webkit-column-count', newColumnCount.toString(), 'important');
                    sheet.style.setProperty('-moz-column-count', newColumnCount.toString(), 'important');
                    // CRITICAL: Remove column-width to prevent columns from merging
                    sheet.style.removeProperty('column-width');
                    sheet.style.removeProperty('-webkit-column-width');
                    sheet.style.removeProperty('-moz-column-width');
                    
                    // Ensure visibility
                    if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                        sheet.style.display = 'block';
                        sheet.style.visibility = 'visible';
                        sheet.style.opacity = '1';
                    }
                    
                    // Update width if needed
                    const sheetContainer = sheet.parentElement;
                    if (sheetContainer && sheetContainer.classList.contains('sheet-container')) {
                        const containerWidth = sheetContainer.offsetWidth || sheetContainer.clientWidth;
                        if (containerWidth > 0) {
                            sheet.style.setProperty('width', `${containerWidth}px`, 'important');
                            sheet.style.setProperty('min-width', `${containerWidth}px`, 'important');
                            sheet.style.setProperty('max-width', `${containerWidth}px`, 'important');
                        }
                    }
                    
                    // Force reflow and verify
                    void sheet.offsetHeight;
                    const computed = window.getComputedStyle(sheet);
                    const actualColCount = parseInt(computed.columnCount) || 0;
                    if (actualColCount !== newColumnCount) {
                        console.warn(`[RESIZE] Sheet ${idx} column count mismatch: expected ${newColumnCount}, got ${actualColCount}. Forcing again...`);
                        // Force again more aggressively
                        sheet.style.cssText += ` column-count: ${newColumnCount} !important; -webkit-column-count: ${newColumnCount} !important; -moz-column-count: ${newColumnCount} !important;`;
                        void sheet.offsetHeight;
                    } else {
                        console.log(`[RESIZE] Sheet ${idx} column count verified: ${actualColCount}`);
                    }
                });
                
                // CRITICAL: When column count reduces (4->2 or 2->1), content needs more vertical space
                // Ensure sheets can accommodate the content by allowing overflow or increasing height
                existingSheets.forEach(sheet => {
                    // When columns reduce, content needs more height - ensure scrolling works
                    sheet.style.setProperty('overflow-y', 'auto', 'important');
                    sheet.style.setProperty('overflow-x', 'hidden', 'important');
                    
                    // If column count reduced, temporarily increase max-height to show all content
                    if (newColumnCount < lastColumnCount) {
                        const currentHeight = parseFloat(sheet.style.height) || sheet.offsetHeight;
                        // Allow sheet to grow to accommodate content (up to 2x current height)
                        sheet.style.setProperty('max-height', `${currentHeight * 2}px`, 'important');
                        // Force reflow to let content redistribute
                        void sheet.offsetHeight;
                    }
                });
                
                // Update heights (this will recalculate based on viewport)
                updateSheetHeights();
                
                // CRITICAL: Start aggressive enforcement when updating existing sheets
                startAggressiveEnforcement(2000);
                
                // Enforce multiple times
                enforceColumnCount();
                lastColumnCount = newColumnCount;
                lastWidth = currentWidth;
                lastHeight = currentHeight;
                
                setTimeout(() => {
                    enforceColumnCount();
                    existingSheets.forEach(sheet => {
                        if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                            sheet.style.display = 'block';
                            sheet.style.visibility = 'visible';
                            // Double-check column count
                            const targetCount = getColumnCount();
                            sheet.style.setProperty('column-count', targetCount.toString(), 'important');
                            sheet.style.setProperty('-webkit-column-count', targetCount.toString(), 'important');
                            sheet.style.setProperty('-moz-column-count', targetCount.toString(), 'important');
                        }
                    });
                }, 10);
                setTimeout(enforceColumnCount, 50);
                setTimeout(enforceColumnCount, 150);
                setTimeout(enforceColumnCount, 300);
                
                return; // Skip re-initialization, we updated existing sheets
            }
        }
        
        // If no existing sheets or column count didn't change, proceed with re-initialization
        if (false) {
            console.log('No existing sheets found, re-initializing pagination');
            
            // CRITICAL: Start aggressive enforcement during re-initialization
            startAggressiveEnforcement(3000);
            
            // CRITICAL: Keep enforcing columns during re-initialization to prevent disappearing
            const enforceInterval = setInterval(() => {
                enforceColumnCount();
                // Also ensure sheets are visible
                document.querySelectorAll('.' + SHEET_CLASS).forEach(sheet => {
                    if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                        sheet.style.display = 'block';
                        sheet.style.visibility = 'visible';
                        sheet.style.opacity = '1';
                    }
                });
            }, 50); // Enforce every 50ms during re-initialization
            
            lastColumnCount = newColumnCount;
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                // CRITICAL: Before removing sheets, ensure we have a backup
                const sheetsToPreserve = new Map();
                document.querySelectorAll('.content-text[data-pagination-initialized="true"]').forEach(element => {
                    const sheetContainer = element.querySelector('.sheet-container');
                    if (sheetContainer) {
                        const activeSheet = sheetContainer.querySelector('.' + ACTIVE_SHEET_CLASS);
                        if (activeSheet) {
                            sheetsToPreserve.set(element, {
                                content: activeSheet.innerHTML,
                                index: parseInt(activeSheet.getAttribute('data-sheet-index') || '0')
                            });
                        }
                    }
                });
                
                // Stop the enforcement interval
                clearInterval(enforceInterval);
                
                // Reset and re-initialize
                document.querySelectorAll('.content-text').forEach(element => {
                    if (element.dataset.paginationInitialized === 'true' && element.dataset.originalContent) {
                        // Remove existing pagination
                        const navContainer = element.parentElement.querySelector('.' + PAGINATION_CONTAINER_CLASS);
                        if (navContainer) {
                            navContainer.remove();
                        }
                        // Remove navigation arrows
                        const prevArrow = element.parentElement.querySelector('.' + NAV_ARROW_CLASS + '--prev');
                        const nextArrow = element.parentElement.querySelector('.' + NAV_ARROW_CLASS + '--next');
                        if (prevArrow) prevArrow.remove();
                        if (nextArrow) nextArrow.remove();
                        // Restore original content
                        element.innerHTML = element.dataset.originalContent;
                        delete element.dataset.paginationInitialized;
                    }
                });
                // Re-initialize
                setTimeout(() => {
                    initAllPagination();
                    // Restore active sheet if we preserved it
                    sheetsToPreserve.forEach((preserved, element) => {
                        const sheetContainer = element.querySelector('.sheet-container');
                        if (sheetContainer) {
                            const targetSheet = sheetContainer.querySelector(`.${SHEET_CLASS}[data-sheet-index="${preserved.index}"]`);
                            if (targetSheet) {
                                // Show the preserved sheet
                                document.querySelectorAll(`.${SHEET_CLASS}`).forEach(s => {
                                    s.classList.remove(ACTIVE_SHEET_CLASS);
                                    s.style.display = 'none';
                                });
                                targetSheet.classList.add(ACTIVE_SHEET_CLASS);
                                targetSheet.style.display = 'block';
                            }
                        }
                    });
                    // Enforce one more time after re-initialization
                    setTimeout(enforceColumnCount, 50);
                    setTimeout(enforceColumnCount, 100);
                    setTimeout(enforceColumnCount, 300);
                }, 100);
            }, 300);
            return;
        }
        
        // If restoring from minimize and column count is the same, just enforce without re-init
        if (isRestoringFromMinimize && preMinimizeColumnCount !== null && newColumnCount === preMinimizeColumnCount) {
            console.log('Restoring from minimize - enforcing columns without re-initialization');
            // CRITICAL: Ensure all sheets are visible and have correct column count
            document.querySelectorAll('.' + SHEET_CLASS).forEach(sheet => {
                sheet.style.setProperty('column-count', newColumnCount.toString(), 'important');
                sheet.style.setProperty('-webkit-column-count', newColumnCount.toString(), 'important');
                sheet.style.setProperty('-moz-column-count', newColumnCount.toString(), 'important');
                if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                }
            });
            enforceColumnCount();
            updateSheetHeights();
            lastColumnCount = newColumnCount;
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            // Enforce multiple times to ensure it sticks
            setTimeout(() => {
                enforceColumnCount();
                document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                });
            }, 10);
            setTimeout(enforceColumnCount, 50);
            setTimeout(enforceColumnCount, 150);
            setTimeout(enforceColumnCount, 300);
            return;
        }
        
        // For ANY width change, try to update existing sheets first
        // Only re-initialize if absolutely necessary (no sheets exist)
        const allSheets = document.querySelectorAll('.' + SHEET_CLASS);
        const hasSheets = allSheets.length > 0;
        
        // If we have sheets, ALWAYS update them instead of removing
        if (hasSheets && widthChange < 500) {
            // Small to medium change - just enforce column-count and update heights
            // CRITICAL: Ensure sheets remain visible during resize
            if (allSheets.length > 0) {
                allSheets.forEach(sheet => {
                    // Update column count on all sheets to match current viewport
                    sheet.style.setProperty('column-count', newColumnCount.toString(), 'important');
                    sheet.style.setProperty('-webkit-column-count', newColumnCount.toString(), 'important');
                    sheet.style.setProperty('-moz-column-count', newColumnCount.toString(), 'important');
                    // CRITICAL: Remove column-width to prevent columns from merging
                    sheet.style.removeProperty('column-width');
                    sheet.style.removeProperty('-webkit-column-width');
                    sheet.style.removeProperty('-moz-column-width');
                    
                    // Ensure visibility
                    if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                        sheet.style.display = 'block';
                        sheet.style.visibility = 'visible';
                        sheet.style.opacity = '1';
                    }
                    
                    // Update width if needed
                    const sheetContainer = sheet.parentElement;
                    if (sheetContainer && sheetContainer.classList.contains('sheet-container')) {
                        const containerWidth = sheetContainer.offsetWidth || sheetContainer.clientWidth;
                        if (containerWidth > 0) {
                            sheet.style.setProperty('width', `${containerWidth}px`, 'important');
                            sheet.style.setProperty('min-width', `${containerWidth}px`, 'important');
                            sheet.style.setProperty('max-width', `${containerWidth}px`, 'important');
                        }
                    }
                    
                    // Force reflow
                    void sheet.offsetHeight;
                });
            }
            
            enforceColumnCount(); // Enforce immediately
            updateSheetHeights();
            lastColumnCount = newColumnCount;
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            // Enforce multiple times to ensure it sticks
            setTimeout(() => {
                enforceColumnCount();
                // Ensure visibility again
                document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                    // Double-check column count
                    const targetCount = getColumnCount();
                    sheet.style.setProperty('column-count', targetCount.toString(), 'important');
                    sheet.style.setProperty('-webkit-column-count', targetCount.toString(), 'important');
                    sheet.style.setProperty('-moz-column-count', targetCount.toString(), 'important');
                });
            }, 10);
            setTimeout(enforceColumnCount, 50);
            setTimeout(enforceColumnCount, 150);
            setTimeout(enforceColumnCount, 300);
            return;
        }
        
        // Very large width change (>500px) - but still try to update existing sheets first
        if (hasSheets) {
            console.log(`Large width change (${widthChange}px) but sheets exist - updating instead of removing`);
            // Update all sheets with new column count
            allSheets.forEach(sheet => {
                sheet.style.setProperty('column-count', newColumnCount.toString(), 'important');
                sheet.style.setProperty('-webkit-column-count', newColumnCount.toString(), 'important');
                sheet.style.setProperty('-moz-column-count', newColumnCount.toString(), 'important');
                // CRITICAL: Remove column-width to prevent columns from merging
                sheet.style.removeProperty('column-width');
                sheet.style.removeProperty('-webkit-column-width');
                sheet.style.removeProperty('-moz-column-width');
                
                if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                }
                
                const sheetContainer = sheet.parentElement;
                if (sheetContainer && sheetContainer.classList.contains('sheet-container')) {
                    const containerWidth = sheetContainer.offsetWidth || sheetContainer.clientWidth;
                    if (containerWidth > 0) {
                        sheet.style.setProperty('width', `${containerWidth}px`, 'important');
                        sheet.style.setProperty('min-width', `${containerWidth}px`, 'important');
                        sheet.style.setProperty('max-width', `${containerWidth}px`, 'important');
                    }
                }
                void sheet.offsetHeight;
            });
            
            enforceColumnCount();
            updateSheetHeights();
            lastColumnCount = newColumnCount;
            lastWidth = currentWidth;
            lastHeight = currentHeight;
            
            setTimeout(() => {
                enforceColumnCount();
                allSheets.forEach(sheet => {
                    if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                        sheet.style.display = 'block';
                        sheet.style.visibility = 'visible';
                    }
                });
            }, 10);
            setTimeout(enforceColumnCount, 50);
            setTimeout(enforceColumnCount, 150);
            setTimeout(enforceColumnCount, 300);
            return;
        }
        
        // Only re-initialize if no sheets exist at all
        console.log('No sheets found, re-initializing pagination');
        const enforceInterval = setInterval(() => {
            enforceColumnCount();
        }, 200); // Reduced from 50ms to 200ms to improve performance
        
        lastColumnCount = newColumnCount;
        lastWidth = currentWidth;
        lastHeight = currentHeight;
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            clearInterval(enforceInterval);
            // Reset and re-initialize only if really needed
            document.querySelectorAll('.content-text').forEach(element => {
                if (element.dataset.paginationInitialized === 'true' && element.dataset.originalContent) {
                    // Remove existing pagination
                    const navContainer = element.parentElement.querySelector('.' + PAGINATION_CONTAINER_CLASS);
                    if (navContainer) {
                        navContainer.remove();
                    }
                    // Remove navigation arrows
                    const prevArrow = element.parentElement.querySelector('.' + NAV_ARROW_CLASS + '--prev');
                    const nextArrow = element.parentElement.querySelector('.' + NAV_ARROW_CLASS + '--next');
                    if (prevArrow) prevArrow.remove();
                    if (nextArrow) nextArrow.remove();
                    // Restore original content
                    element.innerHTML = element.dataset.originalContent;
                    delete element.dataset.paginationInitialized;
                }
            });
            // Re-initialize
            setTimeout(() => {
                initAllPagination();
                // Enforce after re-initialization
                setTimeout(enforceColumnCount, 100);
                setTimeout(enforceColumnCount, 300);
            }, 100);
        }, 300);
    });
    
    /**
     * CRITICAL: Aggressively enforce correct column count on all sheets based on viewport
     * Called frequently to prevent column merging on maximize/resize
     */
    function enforceColumnCount() {
        const targetColumnCount = getColumnCount();
        const viewportWidth = window.innerWidth;
        
        // Get all sheets - use querySelectorAll to catch all, even during re-initialization
        const allSheets = document.querySelectorAll('.' + SHEET_CLASS);
        
        if (allSheets.length === 0) {
            // No sheets yet, nothing to enforce
            return;
        }
        
        // Debug logging
        if (allSheets.length > 0 && viewportWidth > 0) {
            console.log(`[enforceColumnCount] Viewport: ${viewportWidth}px, Target columns: ${targetColumnCount}, Sheets found: ${allSheets.length}`);
            
            // CRITICAL: On desktop, ensure we're targeting 4 columns, not 3
            if (viewportWidth >= 1024 && targetColumnCount !== 4) {
                console.error(`🚨 CRITICAL: Desktop viewport (${viewportWidth}px) but targetColumnCount is ${targetColumnCount}, not 4!`);
            }
        }
        
        allSheets.forEach(sheet => {
            // Skip if sheet is not in DOM (being removed during re-initialization)
            if (!sheet.parentElement || !document.body.contains(sheet)) {
                return;
            }
            
            // CRITICAL: Ensure sheet is visible before enforcing columns
            // This prevents columns from disappearing during minimize/maximize
            if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                sheet.style.display = 'block';
                sheet.style.visibility = 'visible';
                sheet.style.opacity = '1';
            }
            
            // Get current computed column count
            const computed = window.getComputedStyle(sheet);
            const currentColCount = parseInt(computed.columnCount) || 0;
            
            // Enforce correct column count based on viewport width
            sheet.style.setProperty('column-count', targetColumnCount.toString(), 'important');
            sheet.style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
            sheet.style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
            // CRITICAL: Remove column-width to prevent columns from merging
            sheet.style.removeProperty('column-width');
            sheet.style.removeProperty('-webkit-column-width');
            sheet.style.removeProperty('-moz-column-width');
            
            // Ensure width is maintained for proper column rendering
            const sheetContainer = sheet.parentElement;
            if (sheetContainer && sheetContainer.classList.contains('sheet-container')) {
                const containerWidth = sheetContainer.offsetWidth || sheetContainer.clientWidth;
                if (containerWidth > 0) {
                    sheet.style.setProperty('width', `${containerWidth}px`, 'important');
                    sheet.style.setProperty('min-width', `${containerWidth}px`, 'important');
                    sheet.style.setProperty('max-width', `${containerWidth}px`, 'important');
                    
                    // CRITICAL: On desktop, verify container width is sufficient for 4 columns
                    if (viewportWidth >= 1024 && targetColumnCount === 4) {
                        const columnGap = parseFloat(window.getComputedStyle(sheet).columnGap) || 64; // Default 4rem = 64px
                        const minWidthFor4Cols = (columnGap * 3) + 100; // Minimum width needed for 4 columns
                        if (containerWidth < minWidthFor4Cols) {
                            console.warn(`⚠️ Container width (${containerWidth}px) may be too narrow for 4 columns with gap ${columnGap}px. Minimum needed: ${minWidthFor4Cols}px`);
                        }
                    }
                }
            }
            
            // Force reflow to ensure styles are applied
            void sheet.offsetHeight;
            
            // Double-check after reflow
            const afterComputed = window.getComputedStyle(sheet);
            const afterColCount = parseInt(afterComputed.columnCount) || 0;
            if (afterColCount !== targetColumnCount) {
                console.warn(`⚠️ Column count enforcement failed: expected ${targetColumnCount}, got ${afterColCount} (viewport: ${viewportWidth}px). Retrying...`);
                
                // CRITICAL: If we're on desktop (>1024px) and seeing 3 columns, force 4 columns
                if (viewportWidth >= 1024 && afterColCount === 3) {
                    console.error(`🚨 CRITICAL: Desktop viewport (${viewportWidth}px) showing 3 columns instead of 4! Forcing fix...`);
                    // Remove all column-related styles and reapply
                    sheet.style.removeProperty('column-count');
                    sheet.style.removeProperty('-webkit-column-count');
                    sheet.style.removeProperty('-moz-column-count');
                    sheet.style.removeProperty('column-width');
                    sheet.style.removeProperty('-webkit-column-width');
                    sheet.style.removeProperty('-moz-column-width');
                    // Force reflow
                    void sheet.offsetHeight;
                    // Reapply with maximum priority
                    sheet.style.setProperty('column-count', '4', 'important');
                    sheet.style.setProperty('-webkit-column-count', '4', 'important');
                    sheet.style.setProperty('-moz-column-count', '4', 'important');
                    // Force another reflow
                    void sheet.offsetHeight;
                    const finalComputed = window.getComputedStyle(sheet);
                    const finalColCount = parseInt(finalComputed.columnCount) || 0;
                    if (finalColCount === 4) {
                        console.log(`✓ Fixed: Column count now ${finalColCount}`);
                    } else {
                        console.error(`✗ Still showing ${finalColCount} columns after fix attempt`);
                    }
                } else {
                    // Force again with even more aggressive approach
                    sheet.style.cssText = sheet.style.cssText.replace(
                        /column-count\s*:\s*[^;!]+/gi,
                        `column-count: ${targetColumnCount} !important`
                    );
                    sheet.style.setProperty('column-count', targetColumnCount.toString(), 'important');
                    sheet.style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                    sheet.style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
                    void sheet.offsetHeight;
                }
            } else if (viewportWidth >= 1024 && afterColCount === 4) {
                // Log success for desktop
                console.log(`✓ Sheet has correct column count: ${afterColCount} (viewport: ${viewportWidth}px)`);
            }
        });
        
        // Also enforce on content-text parent to prevent inheritance issues
        document.querySelectorAll('.content-text').forEach(contentText => {
            if (contentText.querySelector('.' + SHEET_CLASS)) {
                // When sheets exist, parent should have column-count: 1
                contentText.style.setProperty('column-count', '1', 'important');
                contentText.style.setProperty('-webkit-column-count', '1', 'important');
                contentText.style.setProperty('-moz-column-count', '1', 'important');
            }
        });
    }
    
    // Periodic column enforcement - reduced frequency to improve performance
    // Run every 2 seconds instead of 50ms to reduce CPU usage
    // Store interval ID for potential cleanup
    const columnEnforcementInterval = setInterval(() => {
        // Only enforce if there are sheets on the page
        const hasSheets = document.querySelectorAll('.' + SHEET_CLASS).length > 0;
        if (hasSheets) {
            enforceColumnCount();
        }
    }, 2000); // Reduced from 50ms to 2000ms (2 seconds) to improve performance
    
    // Enforce when window becomes visible again (after minimize/maximize)
    // This is critical for fixing the minimize/maximize issue
    // CRITICAL: Aggressive enforcement interval during window state changes
    let aggressiveEnforcementInterval = null;
    let aggressiveEnforcementTimeout = null;
    
    function startAggressiveEnforcement(duration = 2000) {
        // Clear any existing aggressive enforcement
        if (aggressiveEnforcementInterval) {
            clearInterval(aggressiveEnforcementInterval);
        }
        if (aggressiveEnforcementTimeout) {
            clearTimeout(aggressiveEnforcementTimeout);
        }
        
        console.log('Starting aggressive column enforcement for', duration, 'ms');
        
        // Enforce immediately
        enforceColumnCount();
        
        // Enforce every 50ms during the duration
        aggressiveEnforcementInterval = setInterval(() => {
            enforceColumnCount();
            // Ensure all active sheets are visible
            document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                sheet.style.display = 'block';
                sheet.style.visibility = 'visible';
                sheet.style.opacity = '1';
                const targetCount = getColumnCount();
                sheet.style.setProperty('column-count', targetCount.toString(), 'important');
                sheet.style.setProperty('-webkit-column-count', targetCount.toString(), 'important');
                sheet.style.setProperty('-moz-column-count', targetCount.toString(), 'important');
            });
        }, 50);
        
        // Stop after duration
        aggressiveEnforcementTimeout = setTimeout(() => {
            if (aggressiveEnforcementInterval) {
                clearInterval(aggressiveEnforcementInterval);
                aggressiveEnforcementInterval = null;
            }
            console.log('Stopped aggressive column enforcement');
        }, duration);
    }
    
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            // Window became visible - enforce columns immediately and aggressively
            console.log('Window became visible, starting aggressive column enforcement');
            
            // CRITICAL: Ensure all active sheets are visible when window is restored
            document.querySelectorAll('.' + SHEET_CLASS).forEach(sheet => {
                if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                    // Force column count immediately
                    const targetColumnCount = getColumnCount();
                    sheet.style.setProperty('column-count', targetColumnCount.toString(), 'important');
                    sheet.style.setProperty('-webkit-column-count', targetColumnCount.toString(), 'important');
                    sheet.style.setProperty('-moz-column-count', targetColumnCount.toString(), 'important');
                }
            });
            
            // Start aggressive enforcement for 3 seconds
            startAggressiveEnforcement(3000);
            
            // Also enforce at specific intervals
            const enforceSchedule = [10, 25, 50, 100, 200, 400, 600, 1000, 1500, 2000];
            enforceSchedule.forEach(delay => {
                setTimeout(() => {
                    enforceColumnCount();
                    document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                        sheet.style.display = 'block';
                        sheet.style.visibility = 'visible';
                        sheet.style.opacity = '1';
                    });
                }, delay);
            });
        }
    });
    
    // Enforce on focus (window maximize often triggers focus)
    window.addEventListener('focus', () => {
        console.log('Window focused, starting aggressive column enforcement');
        // Start aggressive enforcement for 2 seconds
        startAggressiveEnforcement(2000);
        // Also enforce at specific intervals
        const enforceSchedule = [10, 25, 50, 100, 200, 400, 600];
        enforceSchedule.forEach(delay => {
            setTimeout(() => {
                enforceColumnCount();
                document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                });
            }, delay);
        });
    });
    
    // Handle window resize events that might be missed (e.g., minimize/maximize)
    // Use a more aggressive approach for window state changes
    let lastWindowState = {
        width: window.innerWidth,
        height: window.innerHeight,
        visible: !document.hidden
    };
    
    // Check window state periodically to catch minimize/maximize
    // Reduced frequency to improve performance
    setInterval(() => {
        const currentState = {
            width: window.innerWidth,
            height: window.innerHeight,
            visible: !document.hidden
        };
        
        // Skip if window is minimized (too small)
        if (currentState.width < 100 || currentState.height < 100) {
            return;
        }
        
        // If window became visible or size changed significantly, enforce columns
        if (currentState.visible && (!lastWindowState.visible || 
            Math.abs(currentState.width - lastWindowState.width) > 100 ||
            Math.abs(currentState.height - lastWindowState.height) > 100)) {
            console.log('Window state changed significantly, enforcing column count and visibility');
            
            // CRITICAL: Ensure all sheets are visible when window is restored
            document.querySelectorAll('.' + SHEET_CLASS).forEach(sheet => {
                if (sheet.classList.contains(ACTIVE_SHEET_CLASS)) {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                    sheet.style.opacity = '1';
                }
            });
            
            enforceColumnCount();
            setTimeout(() => {
                enforceColumnCount();
                // Double-check visibility
                document.querySelectorAll('.' + SHEET_CLASS + '.' + ACTIVE_SHEET_CLASS).forEach(sheet => {
                    sheet.style.display = 'block';
                    sheet.style.visibility = 'visible';
                });
            }, 10);
            setTimeout(enforceColumnCount, 50);
            setTimeout(enforceColumnCount, 150);
            setTimeout(enforceColumnCount, 300);
        }
        
        lastWindowState = currentState;
    }, 2000); // Reduced from 100ms to 2000ms (2 seconds) to improve performance
    
    // REMOVED: Continuous requestAnimationFrame loop was causing severe performance issues
    // Column enforcement is now handled by:
    // 1. Resize events (debounced)
    // 2. Visibility change events
    // 3. Focus events
    // 4. Periodic interval (2 seconds)
    // 5. Window state check (2 seconds)
    // This is sufficient and much more performant
    
    // Also use ResizeObserver to catch layout changes and enforce columns
    // Note: ResizeObserver doesn't detect viewport changes directly, so we rely on window resize listener above
    if (typeof ResizeObserver !== 'undefined') {
        const resizeObserver = new ResizeObserver((entries) => {
            // Enforce columns immediately on any resize
            enforceColumnCount();
            // Layout changed, enforce column-count
            enforceColumnCount();
        });
        
        // Observe all sheet containers
        document.querySelectorAll('.sheet-container').forEach(container => {
            resizeObserver.observe(container);
        });
        
        // Also observe when new containers are added
        const containerObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && node.classList && node.classList.contains('sheet-container')) {
                        resizeObserver.observe(node);
                    }
                });
            });
        });
        
        containerObserver.observe(document.body, { childList: true, subtree: true });
    }
})();


