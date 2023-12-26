import { runLighthouse } from './index.mjs';
import { argv, exit } from 'process';

var websites = [
    'https://www.mefos.unios.hr/index.php/hr/',
    'https://www.biologija.unios.hr/',
    'https://www.kemija.unios.hr/',
    'https://www.pravos.unios.hr/',
    'http://www.uaos.unios.hr/',
    'http://www.efos.unios.hr/',
    'https://www.ferit.unios.hr/',  
    'https://www.fdmz.hr/index.php/hr/',
    'https://www.foozos.hr/',
    'https://www.ffos.unios.hr/'
];


async function main() {
  try {
    const url = argv[2]; // Retrieve the URL from command-line arguments
    const index = parseInt(argv[3]); // Convert index to an integer
    console.info("URL:", url);
    console.info("Index:", index);

    await runLighthouse(url, index);
  } catch (error) {
    console.error("ERROR:", error);
    exit(1);
  }

  exit(0);
}


// Call the main function
main();