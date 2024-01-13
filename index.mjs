// index.mjs

import fs from 'fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';

async function runLighthouse(url, index) {
  const chrome = await launch({ chromeFlags: ['--headless'] });
  //const chrome = await launch();
  const options = { 
    logLevel: 'error', 
    output: 'json',
     formFactor: 'desktop',
    screenEmulation: {
        mobile: false,
        width: 1350,
        height: 940,
        deviceScaleFactor: 1,
        disabled: false,
    },
    emulatedUserAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    port: chrome.port
  };

  try {
    const runnerResult = await lighthouse(url, options);

    // JSON Report
    const reportJson = runnerResult.report;

   // fs.writeFileSync(index + '.json', reportJson);

    fs.writeFile(index + '.json', reportJson, (err) => {
      if (err) {
        console.log(err);
      }
      chrome.kill();
    });



    // `.lhr` is the Lighthouse Result as a JS object
    console.log('Report is done for', runnerResult.lhr.finalUrl);
  } catch (error) {
    console.error('Error url: ', url);
    console.error('Error running Lighthouse:', error);
  }
}

// Export the Lighthouse function
export { runLighthouse };