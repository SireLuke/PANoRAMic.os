import { fetchWikipedia } from "./fetchWikipedia";
import { translateUniversal } from "./translateUniversal";
import { classifyKnowledge } from "./classifyKnowledge";

export async function educationEngine(world, topic, language) {
    const wiki = await fetchWikipedia(topic);
    if (!wiki.success) {
        return { success: false, reason: "Wikipedia fetch failed" };
    }

    const translated = await translateUniversal(wiki.extract, language);
    const classified = classifyKnowledge(translated.translated);

    world.education = {
        topic,
        original: wiki.extract,
        translated: translated.translated,
        classification: classified,
        sourceUrl: wiki.url
    };

    return {
        success: true,
        data: world.education
    };
}
