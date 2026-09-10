// Bounded, local Street View reference viewer. No credentials or photographs
// enter the public game. Delete temporary images after the visual review.
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {parseEnv} from 'node:util';
import {tmpdir} from 'node:os';
import {join} from 'node:path';

const location = process.argv[2] || '40.7269445,-73.9856404';
const headings = (process.argv[3] || '29.72,119.72,209.72,299.72').split(',').map(Number);
const pitch = Number(process.argv[4] || '17');
const fov = Number(process.argv[5] || '85');
if (!/^40\.72\d+,-73\.98\d+$/.test(location) || headings.length > 4 ||
    headings.some(h => !Number.isFinite(h) || h < 0 || h > 360) ||
    !Number.isFinite(pitch) || Math.abs(pitch) > 60 || !Number.isFinite(fov) || fov < 25 || fov > 120) {
  throw Error('Use a First & Seventh location, up to four headings, pitch and FOV.');
}
let key = '';
try {
  key = parseEnv(await readFile(new URL('../.env', import.meta.url), 'utf8')).GOOGLE_MAPS_API_KEY?.trim();
  if (!key) throw Error('Missing local key');
  const request = async (suffix, parameters) => {
    const url = new URL('https://maps.googleapis.com/maps/api/streetview' + suffix);
    url.search = new URLSearchParams({...parameters, key});
    return fetch(url, {redirect: 'error', signal: AbortSignal.timeout(20000)});
  };
  const response = await request('/metadata', {location, radius: '35', source: 'outdoor'});
  if (!response.ok) throw Error('Metadata HTTP ' + response.status);
  const metadata = await response.json();
  if (metadata.status !== 'OK') throw Error('Metadata status ' + metadata.status);
  const directory = join(tmpdir(), 'borough-first-seventh-reference-08');
  await mkdir(directory, {recursive: true, mode: 0o700});
  const result = {checkedAt: new Date().toISOString(), requestedLocation: location,
    panoramaId: metadata.pano_id, imageryDate: metadata.date, location: metadata.location,
    attribution: metadata.copyright, views: []};
  for (const heading of headings) {
    const image = await request('', {pano: metadata.pano_id, size: '640x640', heading: String(heading),
      pitch: String(pitch), fov: String(fov), return_error_code: 'true'});
    if (!image.ok || !image.headers.get('content-type')?.startsWith('image/jpeg')) throw Error('Image HTTP ' + image.status);
    const file = join(directory, `${metadata.pano_id}-${heading}-${pitch}-${fov}.jpg`);
    await writeFile(file, Buffer.from(await image.arrayBuffer()), {mode: 0o600});
    result.views.push({heading, pitch, fov, file});
  }
  console.log(JSON.stringify(result, null, 2));
} catch {
  // Do not print the exception: request details may contain a credential.
  console.error('Street View reference request failed; no credential or request URL logged.');
  process.exitCode = 1;
}
