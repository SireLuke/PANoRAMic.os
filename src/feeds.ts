export async function initFeeds() {
  // Later: connect to real APIs (NASA, NOAA, USGS, WHO, etc.)
  // For now, just simulate a short sync delay.
  await new Promise((resolve) => setTimeout(resolve, 250));
}
