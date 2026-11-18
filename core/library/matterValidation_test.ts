import { assertEquals, assert } from "jsr:@std/assert";
import { validateMatterCatalog } from "./matterValidation.ts";
import type { MatterCatalog } from "./types.ts";
const base = (): MatterCatalog => ({schema:"matter-catalog-v0",sources:[],nodes:[{id:"matter:molecule:H2",kind:"molecule",title:"Hydrogen",libraryNodeId:null,element:null,molecule:{formula:"H2",smiles:null,charge:0,bondName:"single",bondLengthAngstrom:0.74,angleName:null,bondAngleDegrees:null,sourceId:"unused"},v8:{h:null,R:null,u:null,d:null,tau:null,chi:null,s:null,f:null},v8Mapping:null,measured:[],views:[],sourceIds:[],claimLevel:"declared-hypothesis"}]});
Deno.test("MatterCatalog accepts signed chi",()=>{const c=base();c.nodes[0].v8.chi=-0.75;assertEquals(validateMatterCatalog(c),[]);});
Deno.test("MatterCatalog accepts positive chi endpoint",()=>{const c=base();c.nodes[0].v8.chi=1;assertEquals(validateMatterCatalog(c),[]);});
Deno.test("MatterCatalog rejects chi outside signed range",()=>{const c=base();c.nodes[0].v8.chi=1.01;assert(validateMatterCatalog(c).some(p=>p.includes("v8.chi=1.01 outside [-1, 1]")));});
Deno.test("MatterCatalog keeps other coordinates in [0,1]",()=>{const c=base();c.nodes[0].v8.h=-0.01;assert(validateMatterCatalog(c).some(p=>p.includes("v8.h=-0.01 outside [0, 1]")));});
