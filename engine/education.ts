// engine/education.ts

import { WorldState } from "./worldState";

import {
    fetchWikipedia,
    translateUniversal,
    classifyKnowledge,
    accessScore,
    equityScore,
    qualityScore
} from "../core/education/src/index";

/**
 * The education tick engine:
 * - fetches knowledge (topic-based)
 * - translates it
 * - classifies it
 * - computes access, equity, quality metrics
 * - updates world.education
 */

export async function applyEducation(world: WorldState): Promise<WorldState> {
    const topic = world.education.topic ?? "Education";

    // 1. Fetch knowledge from Wikipedia
    const original = await fetchWikipedia(topic);

    // 2. Translate into universal language
    const translated = await translateUniversal(original);

    // 3. Classify the knowledge domain + safety
    const classification = classifyKnowledge(translated);

    // 4. Compute education metrics
    const access = accessScore(world.population.total);
    const equity = equityScore(world.population.total);
    const quality = qualityScore(translated);

    return {
        ...world,
        education: {
            topic,
            original,
            translated,
            classification,
            accessScore: access,
            equityScore: equity,
            qualityScore: quality
        }
    };
}
