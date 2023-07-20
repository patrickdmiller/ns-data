import './common/env'
import {Nightscout} from "./nightscout";
const ns = new Nightscout()

async function main(){
  await ns.init();
  // const docs = await ns.fetch();
  // console.log(docs);
  await ns.close();
}

main()