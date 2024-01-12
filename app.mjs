import { runLighthouse } from './index.mjs';
import { argv, exit } from 'process';

async function main() {
// ovdje ćemo ući u beskonačnu petlju koja dohvaća popis od 10 mrežnih mjesta s API i obrađuje ih
  try {
    const url = argv[2]; // Retrieve the URL from command-line arguments
    const index = parseInt(argv[3]); // Convert index to an integer
    //console.info("URL:", url);
    //console.info("Index:", index);
    await runLighthouse(url, index);
    console.log('Gotov node', url, ' - ', index);
  } catch (error) {
    console.error("ERROR:", error);
    exit(1); 
  }
  exit(0);
}
// Call the main function
main();