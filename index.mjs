// index.mjs

import fs from 'fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';

async function runLighthouse(url, index) {
  const chrome = await launch({ chromeFlags: ['--headless'] });
  const options = { 
    logLevel: 'error', 
    output: 'json',
    port: chrome.port 
  };

  try {
    const runnerResult = await lighthouse(url, options);

    // JSON Report
    const reportJson = runnerResult.report;

    fs.writeFileSync(index + '.json', reportJson);

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