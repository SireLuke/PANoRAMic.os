// core/education/src/fetchWikipedia.ts

export async function fetchWikipedia(topic: string) {
    const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(topic)}`;

    const res = await fetch(url);
    if (!res.ok) {
        return { success: false, content: null };
    }

    const data = await res.json();

    return {
        success: true,
        title: data.title,
        extract: data.extract,
        url: data.content_urls?.desktop?.page || null
    };
}
