#!/usr/bin/env node

/**
 * Puppeteer Font Weight Analysis Script
 * Analyzes computed font styles from browser for Paytone One font-weight investigation
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function analyzeFontWeight() {
    console.log('🔍 Starting Puppeteer font weight analysis...');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Navigate to the website
        console.log('📄 Navigating to http://localhost:4321/');
        await page.goto('http://localhost:4321/', {
            waitUntil: 'networkidle0',
            timeout: 30000
        });

        // Wait for fonts to load
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Analyze the brand-text element
        console.log('🎨 Analyzing h1.brand-text computed styles...');

        const fontAnalysis = await page.evaluate(() => {
            const element = document.querySelector('h1.brand-text.font-semibold');

            if (!element) {
                return { error: 'Element h1.brand-text.font-semibold not found' };
            }

            const computed = getComputedStyle(element);

            // Get all relevant font properties
            const analysis = {
                // Core font properties
                fontFamily: computed.fontFamily,
                fontSize: computed.fontSize,
                fontWeight: computed.fontWeight,
                fontStyle: computed.fontStyle,
                fontStretch: computed.fontStretch,

                // Font synthesis properties
                fontSynthesis: computed.fontSynthesis || 'N/A',
                fontSynthesisWeight: computed.fontSynthesisWeight || 'N/A',
                fontSynthesisStyle: computed.fontSynthesisStyle || 'N/A',
                fontSynthesisSmallCaps: computed.fontSynthesisSmallCaps || 'N/A',

                // Text effects that might create bold appearance
                textShadow: computed.textShadow,
                webkitTextStroke: computed.webkitTextStroke || 'N/A',
                webkitTextStrokeWidth: computed.webkitTextStrokeWidth || 'N/A',
                webkitTextStrokeColor: computed.webkitTextStrokeColor || 'N/A',

                // Font smoothing
                webkitFontSmoothing: computed.webkitFontSmoothing || 'N/A',
                mozOsxFontSmoothing: computed.mozOsxFontSmoothing || 'N/A',

                // Font features
                fontFeatureSettings: computed.fontFeatureSettings,
                fontVariationSettings: computed.fontVariationSettings || 'N/A',
                fontKerning: computed.fontKerning || 'N/A',

                // Transform and positioning
                transform: computed.transform,

                // Element text content for reference
                textContent: element.textContent,

                // Additional context
                elementClasses: element.className,
                elementTagName: element.tagName,

                // CSS Custom Properties (if any)
                customProperties: {}
            };

            // Try to get CSS custom properties
            try {
                const style = getComputedStyle(element);
                for (let i = 0; i < style.length; i++) {
                    const prop = style[i];
                    if (prop.startsWith('--font') || prop.startsWith('--text')) {
                        analysis.customProperties[prop] = style.getPropertyValue(prop);
                    }
                }
            } catch (e) {
                analysis.customProperties.error = e.message;
            }

            return analysis;
        });

        // Take a screenshot for visual reference
        console.log('📸 Taking screenshot for visual reference...');
        await page.screenshot({
            path: path.join(__dirname, '../data/outputs/font-analysis-screenshot.png'),
            fullPage: false,
            clip: {
                x: 0,
                y: 0,
                width: 800,
                height: 400
            }
        });

        // Save analysis results
        const outputPath = path.join(__dirname, '../data/outputs/font-weight-analysis.json');
        fs.writeFileSync(outputPath, JSON.stringify(fontAnalysis, null, 2));

        console.log('✅ Font weight analysis complete!');
        console.log('📊 Results:');
        console.log(`   Font Family: ${fontAnalysis.fontFamily}`);
        console.log(`   Font Weight: ${fontAnalysis.fontWeight}`);
        console.log(`   Font Synthesis: ${fontAnalysis.fontSynthesis}`);
        console.log(`   Font Synthesis Weight: ${fontAnalysis.fontSynthesisWeight}`);
        console.log(`   Text Shadow: ${fontAnalysis.textShadow}`);
        console.log(`   WebKit Text Stroke: ${fontAnalysis.webkitTextStroke}`);
        console.log(`   Element Classes: ${fontAnalysis.elementClasses}`);
        console.log(`📁 Full analysis saved to: ${outputPath}`);
        console.log(`📸 Screenshot saved to: font-analysis-screenshot.png`);

        return fontAnalysis;

    } catch (error) {
        console.error('❌ Error during analysis:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

// Run the analysis
if (require.main === module) {
    analyzeFontWeight()
        .then(result => {
            console.log('🎉 Analysis completed successfully');
            process.exit(0);
        })
        .catch(error => {
            console.error('💥 Analysis failed:', error.message);
            process.exit(1);
        });
}

module.exports = { analyzeFontWeight };
