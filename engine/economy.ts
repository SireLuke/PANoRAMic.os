// engine/economy.ts

import { WorldState } from "./worldState";
import { dynamicFloat } from "../core/economy/src/dynamicFloat";
import { digitalIssuance } from "../core/economy/src/digitalIssuance";
import { physicalMintingRules } from "../core/economy/src/physicalMintingRules";
import { physicalPAR } from "../core/economy/src/physicalPAR";
import { realAssetEquivalence } from "../core/economy/src/realAssetEquivalence";
import { nationFactors } from "../core/economy/src/nationFactors";
import { humanitarianPool } from "../core/economy/src/humanitarianPool";
import { taxAllotment } from "../core/economy/src/taxAllotment";
import { freedomAllotment } from "../core/economy/src/freedomAllotment";
import { stewardshipFund } from "../core/economy/src/stewardshipFund";
import { stewardshipGovernance } from "../core/economy/src/stewardshipGovernance";

export function applyEconomy(world: WorldState): WorldState {
    let next = { ...world };

    // Dynamic float update
    next.economy.parSupply = dynamicFloat({
        worldPopulation: next.population.total,
        resourceParValue: next.resources.renewables,
        totalParSupply: next.economy.parSupply
    });

    // Digital issuance
    next.economy.parSupply = digitalIssuance({
        currentSupply: next.economy.parSupply,
        governanceScore: next.governance.panitarianScore ?? 1
    });

    // Physical minting rules
    next.economy.parCap = physicalMintingRules({
        renewables: next.resources.renewables,
        nonRenewables: next.resources.nonRenewables
    });

    // Physical PAR verification
    next.economy.parSupply = physicalPAR({
        parSupply: next.economy.parSupply,
        parCap: next.economy.parCap
    });

    // Real asset equivalence
    next.economy.parSupply = realAssetEquivalence({
        parSupply: next.economy.parSupply,
        renewables: next.resources.renewables
    });

    // Nation factors
    next.economy.taxLoad = nationFactors({
        population: next.population.total,
        parSupply: next.economy.parSupply
    });

    // Humanitarian pool
    next.economy.humanitarianPool = humanitarianPool({
        taxLoad: next.economy.taxLoad,
        needScore: next.humanitarian.needScore ?? 0
    });

    // Tax allotment
    next.economy.taxLoad = taxAllotment({
        parSupply: next.economy.parSupply,
        governanceScore: next.governance.panitarianScore ?? 1
    });

    // Freedom allotment
    next.economy.parSupply = freedomAllotment({
        parSupply: next.economy.parSupply,
        stabilityScore: next.stability.stabilityScore ?? 1
    });

    // Stewardship fund
    next.economy.stewardshipFund = stewardshipFund({
        renewables: next.resources.renewables,
        parSupply: next.economy.parSupply
    });

    // Stewardship governance
    next.economy.stewardshipFund = stewardshipGovernance({
        fund: next.economy.stewardshipFund,
        governanceScore: next.governance.panitarianScore ?? 1
    });

    return next;
}
