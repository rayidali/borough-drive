// Mirror the static-host contract for local integration checks. Only names
// containing their full content hash are immutable; errors must not be cached.
export const immutableCache = 'public, max-age=31536000, immutable';
export const mutableCache = 'public, max-age=0, must-revalidate';
export function seventhHeaders(pathname) {
  const headers = {'Cache-Control': mutableCache, 'X-Content-Type-Options': 'nosniff'};
  if (/^\/seventh\/areas\/(?:assets\/[a-f0-9]{64}\.scn|manifest-[a-f0-9]{64}\.json)$/.test(pathname)) {
    headers['Cache-Control'] = immutableCache;
  }
  if (pathname.endsWith('.scn') || pathname.endsWith('.pck')) headers['Content-Type'] = 'application/octet-stream';
  if (pathname.endsWith('.wasm')) headers['Content-Type'] = 'application/wasm';
  return headers;
}
