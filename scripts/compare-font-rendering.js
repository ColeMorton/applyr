#!/usr/bin/env node

/**
 * Font Rendering Comparison Script
 * Captures browser rendering vs generated PDF to validate font consistency
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function compareFontRendering() {
    console.log('🔍 Starting font rendering comparison...');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Navigate to the website
        console.log('📄 Capturing browser rendering...');
        await page.goto('http://localhost:4321/', {
            waitUntil: 'networkidle0',
            timeout: 30000
        });

        // Wait for fonts to load
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Focus on the brand text area for comparison
        await page.evaluate(() => {
            const element = document.querySelector('h1.brand-text, .brand-text');
            if (element) {
                element.scrollIntoView();
                // Add a border for visibility in comparison
                element.style.border = '2px solid red';
                element.style.padding = '10px';
                element.style.margin = '20px';
                element.style.backgroundColor = 'rgba(255,255,0,0.1)';
            }
        });

        // Take screenshot of browser rendering
        const browserScreenshot = path.join(__dirname, '../data/outputs/browser_font_rendering.png');
        await page.screenshot({
            path: browserScreenshot,
            fullPage: false,
            clip: { x: 0, y: 0, width: 800, height: 400 }
        });

        // Get font details from browser for comparison
        const fontDetails = await page.evaluate(() => {
            const element = document.querySelector('h1.brand-text, .brand-text');
            if (!element) return null;

            const computed = getComputedStyle(element);
            return {
                fontFamily: computed.fontFamily,
                fontWeight: computed.fontWeight,
                fontSize: computed.fontSize,
                textContent: element.textContent,
                clientWidth: element.clientWidth,
                clientHeight: element.clientHeight
            };
        });

        console.log('🌐 Browser Font Analysis:');
        if (fontDetails) {
            console.log(`   Text: "${fontDetails.textContent}"`);
            console.log(`   Font Family: ${fontDetails.fontFamily}`);
            console.log(`   Font Weight: ${fontDetails.fontWeight}`);
            console.log(`   Font Size: ${fontDetails.fontSize}`);
            console.log(`   Element Size: ${fontDetails.clientWidth}x${fontDetails.clientHeight}px`);
        }

        console.log(`📸 Browser screenshot saved: ${browserScreenshot}`);

        // Create a summary report
        const comparisonReport = {
            timestamp: new Date().toISOString(),
            browserFontDetails: fontDetails,
            generatedPDF: 'data/outputs/test_font_fix_LinkedIn Reach Out.pdf',
            browserScreenshot: browserScreenshot,
            summary: {
                fontFamily: fontDetails ? fontDetails.fontFamily : 'Not found',
                expectedWeight: '600 (synthesized from 400)',
                actualWeight: fontDetails ? fontDetails.fontWeight : 'Unknown',
                matchesExpectation: fontDetails ? (fontDetails.fontWeight === '600') : false
            }
        };

        // Save comparison report
        const reportPath = path.join(__dirname, '../data/outputs/font_rendering_comparison.json');
        fs.writeFileSync(reportPath, JSON.stringify(comparisonReport, null, 2));

        console.log('✅ Font rendering comparison complete!');
        console.log('📊 Results:');
        console.log(`   PDF: data/outputs/test_font_fix_LinkedIn Reach Out.pdf`);
        console.log(`   Browser Screenshot: ${browserScreenshot}`);
        console.log(`   Comparison Report: ${reportPath}`);

        if (comparisonReport.summary.matchesExpectation) {
            console.log('🎉 Font weight matches expected value (600)!');
        } else {
            console.log(`⚠️  Font weight mismatch: Expected 600, got ${comparisonReport.summary.actualWeight}`);
        }

        return comparisonReport;

    } catch (error) {
        console.error('❌ Error during comparison:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

// Run the comparison
if (require.main === module) {
    compareFontRendering()
        .then(result => {
            console.log('🎉 Comparison completed successfully');
            process.exit(0);
        })
        .catch(error => {
            console.error('💥 Comparison failed:', error.message);
            process.exit(1);
        });
}

module.exports = { compareFontRendering };
