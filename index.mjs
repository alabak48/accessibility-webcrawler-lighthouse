// index.mjs

import fs from 'fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';

async function runLighthouse(url, index) {
  const chrome = await launch({ chromeFlags: ['--headless'] });
  const options = { 
    logLevel: 'error', 
    output: 'json', 
    onlyCategories: ['accessibility'],
    port: chrome.port 
  };

  try {
    const runnerResult = await lighthouse(url, options);

    // JSON Report
    const requestedUrl = runnerResult.lhr.requestedUrl;
    const finalUrl = runnerResult.lhr.finalUrl;
    const audits = runnerResult.lhr.audits;
    const categories = runnerResult.lhr.categories;

    // Create an object with the extracted data
    const resultData = {
      requestedUrl,
      finalUrl,
      audits,
      categories,
    };

    // Convert the object to JSON and save to a file
    const resultJson = JSON.stringify(resultData, null, 2);
    fs.writeFileSync(index + '.json', resultJson);

    // ovdje ćemo slati podatke na API

    // `.lhr` is the Lighthouse Result as a JS object
    console.log('Report is done for', runnerResult.lhr.finalUrl);
  } catch (error) {
    console.error('Error url: ', url);
    console.error('Error running Lighthouse:', error);
  }
}

// Export the Lighthouse function
export { runLighthouse };