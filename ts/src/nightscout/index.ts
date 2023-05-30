import '../common/env'
import  { MongoClient, Db as MongoDb } from "mongodb";
import { logDebug, logError, logInfo } from "../common/log";

export class Nightscout{
  host: string = process.env.NSHOST || "localhost";
  port: string = process.env.NSPORT || "27017";
  db: string = process.env.NSDB || "Nightscout";
  user: string = process.env.NSUSER || "nightscout";
  pass: string = process.env.NSPASSWORD || "nightscout";
  connecturl: string = "";
  url: string = `mongodb://${this.user}:${this.pass}@${this.host}:${this.port}/${this.db}`;
  client : MongoClient;
  dbConnection : MongoDb
  constructor(){
    this.client = new MongoClient(this.url);
    this.dbConnection = this.client.db(this.db);
  }

  async init(){
    try{
      await this.client.connect();
      logInfo("ns connected and ready");
    }catch(err){
      logError(err);
    }

    logDebug("ns init complete")
    //list all collections
    const collections = await this.dbConnection.collections();
    logDebug("collections", collections.map(c=>c.collectionName));
  }

  async fetch(collection = "entries"){
    try{
      
      const coll = this.dbConnection.collection(collection);
      const docs = await coll.find().toArray();
      return docs;
    }catch(err){
      logError(err);
    }
  }

  close(){
    return this.client.close();
  }

}


// let client;
// let db;
// //build connection string

// module.exports = {
//   init: (props = {}) => {
//     for (let key in props) {
//       ns_mongo[key] = props[key];
//     }
//     client = new MongoClient(ns_mongo.url());
//     return client.connect().then(() => {
//       logger.info("ns connected and ready");
//       db = client.db("Nightscout");
//     });
//   },
//   close: ()=>{
//     return client.close()
//   },

//   fetchAll: ({ collection = "entries" }) => {
//     if (!client) {
//       throw new Error("client not initialized");
//     } else {
//       let coll = db.collection(collection);
//       return coll.find().toArray();
//     }
//   },
//   fetchAllEntries: () => {
//     return this.fetchAll({ collection: "entries" });
//   },

//   fetchEntriesFrom: ({ collection = "entries", after = -1, limit = null }) => {
//     logger.info("fetching after", after);
//     if (!client) {
//       throw new Error("client not initialized");
//     } else {
//       if (limit !== null) {
//         return db
//           .collection(collection)
//           .find({ date: { $gt: parseInt(after) } })
//           .limit(limit)
//           .toArray();
//       } else {
//         return db
//           .collection(collection)
//           .find({ date: { $gt: parseInt(after) } })
//           .toArray();
//       }
//     }
//   },

//   fetchAllTreatments: () => {
//     return this.fetchAll({ collection: "treatments" });
//   },

//   fetchTreatmentsFrom: ({ collection = "treatments", after = "1980-01-01T00:00:00.000Z" }) => {
//     logger.info("fetching after", after);
//     if (!client) {
//       throw new Error("client not initialized");
//     } else {
//       return db
//         .collection(collection)
//         .find({ $expr: { $gte: [{ $dateFromString: { dateString: "$created_at" } }, new Date(after)] } })
//         .toArray();
//     }
//   },
// };