// engine/worldState.ts

export type WorldPopulation = {
    total: number;
    byRegion?: Record<string, number>;
};

export type WorldResources = {
    parSupply: number;
    parCap: number;
    renewables: number;
    nonRenewables: number;
};

export type WorldEconomy = {
    parSupply: number;
    parCap: number;
    stewardshipFund: number;
    humanitarianPool: number;
    taxLoad: number;
};

export type WorldEducation = {
    topic?: string;
    original?: string;
    translated?: string;
    qualityScore?: number;
    accessScore?: number;
    equityScore?: number;
};

export type WorldGovernance = {
    panitarianScore?: number;
    publicPool?: number;
    minimumThreshold?: number;
};

export type WorldHumanitarian = {
    needScore?: number;
    reliefScore?: number;
    accessScore?: number;
};

export type WorldStability = {
    stabilityScore?: number;
    volatilityScore?: number;
    dampeningScore?: number;
};

export type WorldCatastrophe = {
    impactScore?: number;
    severityScore?: number;
};

export type WorldMigration = {
    migrationScore?: number;
};

export type WorldTrafficking = {
    traffickingScore?: number;
};

export type WorldHarmIndex = {
    harmScore?: number;
};

export type WorldTravel = {
    poiCount?: number;
};

export type WorldState = {
    time: number;
    population: WorldPopulation;
    resources: WorldResources;
    economy: WorldEconomy;
    education: WorldEducation;
    governance: WorldGovernance;
    humanitarian: WorldHumanitarian;
    stability: WorldStability;
    catastrophe: WorldCatastrophe;
    migration: WorldMigration;
    trafficking: WorldTrafficking;
    harmindex: WorldHarmIndex;
    travel: WorldTravel;
};
