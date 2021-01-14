import { generateFlux } from "./functions.js";

import alfgants from "../stores/1000gants.json"; // 658c1335-6441-4f3f-bdf1-a605b7e346e6
import boutiqueonly from "../stores/boutiqueonly.json"; // ac9f9c15-baca-4461-bf2c-29519590e104
import collection_t from "../stores/collection_t.json"; //  e975083f-3043-46c7-a69e-04e4025fa03f
// import destination_bio from '../stores/destination_bio.json'; //  e9096d7b-8afa-44de-99fb-2b1ac179668f
import eden_park from "../stores/eden_park.json"; // 992bc7b0-57c4-4823-9698-7e46ce7f9fc0
import gallico_fashion from "../stores/gallico_fashion.json"; // 30f72f2b-5127-4b0e-b6ea-7e11a611a954
import manuelabiocca from "../stores/manuelabiocca.json"; // c94e912d-5928-4bbc-9edd-1be532008a74
import plazaShoes from "../stores/plaza-shoes.json"; // 8ca8deca-22a0-4506-929c-7476b8edc82c
import originesteaandcoffee from "../stores/originesteaandcoffee.json"; // e9096d7b-8afa-44de-99fb-2b1ac179668f
import boucherieagricoledelivery from "../stores/boucherieagricoledelivery.json"; // e9096d7b-8afa-44de-99fb-2b1ac179668f
import cannolive from "../stores/cannolive.json"; // 41f9e44d-cc27-460b-986d-54aaeced2087
import jeromedeoliveira from "../stores/jeromedeoliveira.json"; // cd3ee5de-c6f8-42b0-920d-aaf01aa1570c (patisserieintuitions)
import madeinrotin from "../stores/madeinrotin.json"; // 1c526bc8-62d2-4eb9-80e3-61e790b8225b
import mavillemoshopping from "../stores/mavillemoshopping.json"; // 71d8ce73-7c30-4715-9ce3-776e5b53b92c (Ogoni)
import mekanova from "../stores/mekanova.json"; // b3af0bf9-2530-488d-a01d-5f26c272afc1
import lagrandecoutellerie from "../stores/lagrandecoutellerie.json"; // 2b026c84-bda6-4f8b-9b49-cdae7faf0985 - 2 stores ???
import pepsCannes from "../stores/peps_cannes.json"; // 4a103f60-8805-4067-b900-8237964b25ce
import lenotre from "../stores/lenotre.json"; // e6e7007d-e06c-4dd0-b277-1708a205b550
import districtcannes from "../stores/districtcannes.json"; // ee8a4a59-822f-45f4-80e0-24d11136c7ed

/**
 * Here we execute the function
 * Example we execute the enrichment on the alfgants using the store id "9c41c89f-ba21-442c-8991-69ac6b4a0a77"
   And the Universe "Mode" which will be exported to the file "1000gants.json" on the workspaceDir directory
 * 
 * await generateFlux(alfgants, '1000gants.json', '9c41c89f-ba21-442c-8991-69ac6b4a0a77', 'Mode');
 */

// await generateFlux(
//   collection_t,
//   "collection_t.json",
//   "e975083f-3043-46c7-a69e-04e4025fa03f",
//   "Alimentation"
// );
