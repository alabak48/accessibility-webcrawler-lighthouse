// index.mjs

import fs from 'fs';
import { launch } from 'chrome-launcher';
import lighthouse from 'lighthouse';
import util from 'util';


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
    console.log('Krenuo Lighthouse');
    const runnerResult = await lighthouse(url, options);
    console.log('Odradio Lighthouse');
    // JSON Report
    const reportJson = runnerResult.report;

   // fs.writeFileSync(index + '.json', reportJson);
/*
   const writeFile = util.promisify(fs.writeFile);
   writeFile(index + '.json', reportJson)
   .then(() =>{
    console.log('Zapisao sam file na disk, idem ubiti Chrome');
    chrome.kill();
    console.log('Ubio Chrome');
   })
   .catch((err)=>{
    console.log(err);
   });
*/
    console.log('Idem spremiti JSON',new Date().getMilliseconds());
    fs.writeFileSync(index + '.json', reportJson);

    console.log('Spremio JSON',new Date().getMilliseconds());
    chrome.kill();
    console.log('Ubio Chrome',new Date().getMilliseconds());

    // `.lhr` is the Lighthouse Result as a JS object
    console.log('Report is done for', runnerResult.lhr.finalUrl);
  } catch (error) {
    console.error('Error url: ', url);
    console.error('Error running Lighthouse:', error);
  }
}

// Export the Lighthouse function
export { runLighthouse };