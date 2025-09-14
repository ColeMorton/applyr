#!/usr/bin/env node

/**
 * AstroFont Loading Investigation Script
 * Analyzes how AstroFont component loads Paytone One font in the browser
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function inspectAstroFontLoading() {
    console.log('🔍 Starting AstroFont loading investigation...');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Capture network requests to see font loading
        const requests = [];
        const responses = [];
        
        page.on('request', request => {
            requests.push({
                url: request.url(),
                method: request.method(),
                headers: request.headers(),
                resourceType: request.resourceType()
            });
        });
        
        page.on('response', response => {
            responses.push({
                url: response.url(),
                status: response.status(),
                headers: response.headers(),
                fromCache: response.fromCache()
            });
        });
        
        // Navigate to the website
        console.log('📄 Navigating to http://localhost:4321/');
        await page.goto('http://localhost:4321/', {
            waitUntil: 'networkidle0',
            timeout: 30000
        });
        
        // Wait for fonts to fully load
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Filter font-related requests
        const fontRequests = requests.filter(req => 
            req.url.includes('font') || 
            req.url.includes('Paytone') ||
            req.resourceType === 'font' ||
            req.url.includes('fonts.googleapis.com') ||
            req.url.includes('fonts.gstatic.com') ||
            req.url.includes('.woff') ||
            req.url.includes('.woff2') ||
            req.url.includes('.ttf')
        );
        
        const fontResponses = responses.filter(res => 
            res.url.includes('font') || 
            res.url.includes('Paytone') ||
            res.url.includes('fonts.googleapis.com') ||
            res.url.includes('fonts.gstatic.com') ||
            res.url.includes('.woff') ||
            res.url.includes('.woff2') ||
            res.url.includes('.ttf')
        );
        
        console.log('🌐 Analyzing network font requests...');
        console.log(`Found ${fontRequests.length} font-related requests`);
        
        // Get CSS stylesheets content
        const stylesheets = await page.evaluate(() => {
            const sheets = [];
            for (let i = 0; i < document.styleSheets.length; i++) {
                try {
                    const sheet = document.styleSheets[i];
                    const rules = [];
                    
                    if (sheet.cssRules) {
                        for (let j = 0; j < sheet.cssRules.length; j++) {
                            const rule = sheet.cssRules[j];
                            if (rule.cssText.includes('Paytone') || 
                                rule.cssText.includes('font-brand') ||
                                rule.cssText.includes('@font-face') ||
                                rule.cssText.includes('@import')) {
                                rules.push({
                                    cssText: rule.cssText,
                                    type: rule.type,
                                    selectorText: rule.selectorText || 'N/A'
                                });
                            }
                        }
                    }
                    
                    if (rules.length > 0) {
                        sheets.push({
                            href: sheet.href,
                            title: sheet.title,
                            rules: rules
                        });
                    }
                } catch (e) {
                    // Cross-origin stylesheets may not be readable
                    console.log('Stylesheet access denied:', sheet.href);
                }
            }
            return sheets;
        });
        
        // Get computed font information for brand text
        const brandTextAnalysis = await page.evaluate(() => {
            const element = document.querySelector('h1.brand-text, .brand-text');
            if (!element) return null;
            
            const computed = getComputedStyle(element);
            return {
                fontFamily: computed.fontFamily,
                fontWeight: computed.fontWeight,
                fontSize: computed.fontSize,
                actualFontFace: computed.getPropertyValue('font-family'),
                cssVariables: {
                    fontBrand: getComputedStyle(document.documentElement).getPropertyValue('--font-brand').trim()
                }
            };
        });
        
        // Get page HTML head to see font loading tags
        const headContent = await page.evaluate(() => {
            const head = document.head;
            const fontRelated = [];
            
            // Find font-related tags
            const links = head.querySelectorAll('link');
            links.forEach(link => {
                if (link.href.includes('font') || link.rel === 'preload' && link.as === 'font') {
                    fontRelated.push({
                        tag: 'link',
                        href: link.href,
                        rel: link.rel,
                        as: link.as,
                        type: link.type,
                        crossorigin: link.crossOrigin
                    });
                }
            });
            
            const styles = head.querySelectorAll('style');
            styles.forEach((style, index) => {
                if (style.textContent.includes('Paytone') || 
                    style.textContent.includes('font-brand') ||
                    style.textContent.includes('@font-face')) {
                    fontRelated.push({
                        tag: 'style',
                        index: index,
                        content: style.textContent.substring(0, 500) + '...' // Truncate for readability
                    });
                }
            });
            
            return fontRelated;
        });
        
        // Compile investigation results
        const investigation = {
            timestamp: new Date().toISOString(),
            url: 'http://localhost:4321/',
            fontRequests: fontRequests,
            fontResponses: fontResponses,
            stylesheets: stylesheets,
            brandTextAnalysis: brandTextAnalysis,
            headContent: headContent,
            summary: {
                totalRequests: requests.length,
                fontRequests: fontRequests.length,
                stylesheetsWithFonts: stylesheets.length,
                fontLoadingTags: headContent.length
            }
        };
        
        // Save investigation results
        const outputPath = path.join(__dirname, '../data/outputs/astro-font-investigation.json');
        fs.writeFileSync(outputPath, JSON.stringify(investigation, null, 2));
        
        // Take screenshot
        await page.screenshot({
            path: path.join(__dirname, '../data/outputs/astro-font-screenshot.png'),
            fullPage: false,
            clip: { x: 0, y: 0, width: 800, height: 400 }
        });
        
        console.log('✅ AstroFont investigation complete!');
        console.log('📊 Summary:');
        console.log(`   Total Network Requests: ${requests.length}`);
        console.log(`   Font-related Requests: ${fontRequests.length}`);
        console.log(`   Stylesheets with Fonts: ${stylesheets.length}`);
        console.log(`   Font Loading Tags: ${headContent.length}`);
        
        if (brandTextAnalysis) {
            console.log(`   Brand Text Font: ${brandTextAnalysis.fontFamily}`);
            console.log(`   CSS Variable --font-brand: ${brandTextAnalysis.cssVariables.fontBrand}`);
        }
        
        console.log('🔗 Key Font URLs Found:');
        fontRequests.forEach((req, i) => {
            console.log(`   ${i + 1}. ${req.url}`);
        });
        
        console.log(`📁 Full investigation saved to: ${outputPath}`);
        
        return investigation;
        
    } catch (error) {
        console.error('❌ Error during investigation:', error.message);
        throw error;
    } finally {
        await browser.close();
    }
}

// Run the investigation
if (require.main === module) {
    inspectAstroFontLoading()
        .then(result => {
            console.log('🎉 Investigation completed successfully');
            process.exit(0);
        })
        .catch(error => {
            console.error('💥 Investigation failed:', error.message);
            process.exit(1);
        });
}

module.exports = { inspectAstroFontLoading };