// Compare the deployed bytes with the reviewed local release, without rebuilding.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const origin = new URL(process.argv[2] || 'https://www.drivearound.nyc').origin;
const output = process.argv[3] || 'model-source/publication-2026-10-24/hosting.json';
const build = JSON.parse(await fs.readFile('dist/seventh/build.json', 'utf8'));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const report = {date: new Date().toISOString(), origin, build: build.generatedAt || build.builtAt,
  pack: build.files['index.pck'], routes: [], runtime: [], errors: [], complete: false};

async function inspect(url, expected, kind) {
  const response = await fetch(origin + url, {signal: AbortSignal.timeout(120000)});
  const bytes = Buffer.from(await response.arrayBuffer());
  const row = {url, status: response.status, bytes: bytes.length, sha256: hash(bytes),
    cacheControl: response.headers.get('cache-control'), contentType: response.headers.get('content-type')};
  report[kind].push(row);
  assert.equal(response.status, 200, url);
  assert.equal(row.bytes, expected.bytes, url + ' size');
  assert.equal(row.sha256, expected.sha256, url + ' hash');
  if (/\/areas\/(assets\/|manifest-)/.test(url)) {
    assert.match(row.cacheControl || '', /max-age=31536000/, url + ' cache lifetime');
    assert.match(row.cacheControl || '', /immutable/, url + ' immutable content');
  }
  if (url.endsWith('.scn') || url.endsWith('.pck')) assert.match(row.contentType || '', /application\/octet-stream/);
  if (url.endsWith('.wasm')) assert.match(row.contentType || '', /application\/wasm/);
}

for (const [url, file] of [['/', 'seventh/index.html'], ['/seventh/', 'seventh/index.html'],
  ['/index.html', 'legacy.html'], ['/legacy.html', 'legacy.html'], ['/seventh/build.json', 'seventh/build.json']]) {
  const bytes = await fs.readFile(path.join('dist', file));
  try { await inspect(url, {bytes: bytes.length, sha256: hash(bytes)}, 'routes'); }
  catch (error) { report.errors.push({url, message: error.message}); }
}

const queue = Object.entries(build.files);
await Promise.all(Array.from({length: 6}, async () => {
  while (queue.length) {
    const [file, expected] = queue.shift();
    try { await inspect('/seventh/' + file, expected, 'runtime'); }
    catch (error) { report.errors.push({file, message: error.message}); }
  }
}));
try {
  const response = await fetch(origin + '/seventh/areas/assets/' + '0'.repeat(64) + '.scn');
  report.missingScene = {status: response.status, cacheControl: response.headers.get('cache-control')};
  assert.equal(response.status, 404, 'Missing scenes must return 404');
  assert(!/immutable|max-age=31536000/.test(report.missingScene.cacheControl || ''), 'Missing scene must not inherit immutable caching');
} catch (error) { report.errors.push({missingScene: true, message: error.message}); }
report.runtime.sort((a, b) => a.url.localeCompare(b.url));
report.complete = report.errors.length === 0;
await fs.mkdir(path.dirname(output), {recursive: true});
await fs.writeFile(output, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({origin, routes: report.routes.length, runtimeFiles: report.runtime.length,
  complete: report.complete, errors: report.errors, output}, null, 2));
if (!report.complete) process.exitCode = 1;
