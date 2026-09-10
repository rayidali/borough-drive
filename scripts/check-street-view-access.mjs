// Local, bounded access check. Never import this script into the public game.
// Metadata only: node scripts/check-street-view-access.mjs
// Metadata + one potentially billable image: add --image.
import { readFile, mkdtemp, writeFile, chmod } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { parseEnv } from 'node:util';

const args = process.argv.slice(2);
if (args.some(arg => arg !== '--image')) {
  console.log('Usage: node scripts/check-street-view-access.mjs [--image]');
  process.exit(2);
}

let key = '';
function safe(message) {
  return String(message).split(key || '\0').join('[REDACTED]')
    .replace(/AIza[\w-]+/g, '[REDACTED]');
}

async function request(endpoint, parameters) {
  const url = new URL(`https://maps.googleapis.com/maps/api/streetview${endpoint}`);
  for (const [name, value] of Object.entries(parameters)) url.searchParams.set(name, value);
  url.searchParams.set('key', key);
  // Do not log URLs, request objects or exception stacks: they can contain the key.
  return fetch(url, { redirect: 'error', signal: AbortSignal.timeout(20000) });
}

async function main() {
  let config;
  try {
    config = parseEnv(await readFile(new URL('../.env', import.meta.url), 'utf8'));
  } catch {
    console.error('Cannot read the local .env file. Keep it as a plain-text file in the repository root.');
    process.exitCode = 2;
    return;
  }
  key = (config.GOOGLE_MAPS_API_KEY || '').trim();
  if (!key || /\s/.test(key) || /^(YOUR_|PASTE_)/i.test(key)) {
    console.error('Paste a key after GOOGLE_MAPS_API_KEY= in .env and save; no request sent.');
    process.exitCode = 2;
    return;
  }

  const response = await request('/metadata', {
    location: '40.7269445,-73.9856404', radius: '50', source: 'outdoor',
  });
  if (!response.ok) {
    console.error(`Metadata HTTP ${response.status}: ${safe(await response.text()).slice(0, 2000)}`);
    process.exitCode = 1;
    return;
  }
  const metadata = await response.json();
  console.log(JSON.stringify({
    checkedAt: new Date().toISOString(),
    requestedLocation: 'First Avenue and East 7th Street, Manhattan',
    status: metadata.status, imageryDate: metadata.date || 'not supplied',
    location: metadata.location, panoramaId: metadata.pano_id, attribution: metadata.copyright,
    ...(metadata.error_message ? { error: safe(metadata.error_message) } : {}),
  }, null, 2));
  if (metadata.status !== 'OK' || !metadata.pano_id) {
    process.exitCode = 1;
    return;
  }
  if (!args.includes('--image')) return;

  const imageResponse = await request('', {
    pano: metadata.pano_id, size: '640x640', heading: '29.72', pitch: '5', fov: '90',
    return_error_code: 'true',
  });
  if (!imageResponse.ok) {
    console.error(`Image HTTP ${imageResponse.status}: ${safe(await imageResponse.text()).slice(0, 2000)}`);
    process.exitCode = 1;
    return;
  }
  const contentType = imageResponse.headers.get('content-type') || '';
  if (!contentType.startsWith('image/jpeg')) {
    console.error('Image response was not JPEG; access is not confirmed.');
    process.exitCode = 1;
    return;
  }
  const bytes = Buffer.from(await imageResponse.arrayBuffer());
  const directory = await mkdtemp(join(tmpdir(), 'borough-street-view-'));
  await chmod(directory, 0o700);
  const imagePath = join(directory, 'first-seventh-access-test.jpg');
  await writeFile(imagePath, bytes, { mode: 0o600 });
  console.log(JSON.stringify({ imageStatus: imageResponse.status, bytes: bytes.length, imagePath }));
  console.log('Inspect the temporary image to confirm visual access, then delete it. No image is saved in the game.');
}

main().catch(() => {
  console.error('Access check failed while connecting, reading a response or writing the temporary preview. No credentials logged.');
  process.exitCode = 1;
});
