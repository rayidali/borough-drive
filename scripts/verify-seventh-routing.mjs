// Exercise the configured static-file and miss routes against the shipped files.
// Production CDN behavior is checked separately by verify-seventh-hosted.mjs.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {immutableCache, mutableCache} from './seventh-hosting.mjs';

const config = JSON.parse(await fs.readFile(new URL('../vercel.json', import.meta.url), 'utf8'));
const root = new URL('../dist/', import.meta.url);
const build = JSON.parse(await fs.readFile(new URL('seventh/build.json', root), 'utf8'));
const routes = config.routes;
assert(Array.isArray(routes), 'Explicit filesystem/miss routing is required');
assert(!config.headers && !config.rewrites, 'Keep routing order in one list');
assert.equal(routes.filter(route => route.handle === 'filesystem').length, 1);
await assert.rejects(fs.access(new URL('index.html', root)), 'Root must retain the Seventh shell');

async function exists(url) {
  try { return (await fs.stat(new URL(url.slice(1), root))).isFile(); }
  catch { return false; }
}
async function resolve(url) {
  const headers = {};
  for (const route of routes) {
    if (route.handle === 'filesystem') {
      if (await exists(url)) return {status: 200, file: url, headers};
      continue;
    }
    assert(route.src && !route.handle, 'Unsupported routing phase');
    if (!new RegExp(route.src).test(url)) continue;
    Object.assign(headers, route.headers);
    if (route.continue) continue;
    if (route.dest) return {status: await exists(route.dest) ? 200 : 404, file: route.dest, headers};
    return {status: route.status, headers};
  }
  return {status: 404, headers};
}

for (const [url, file] of [['/', '/seventh/index.html'], ['/index.html', '/legacy.html'], ['/legacy.html', '/legacy.html']]) {
  const result = await resolve(url);
  assert.equal(result.status, 200, url);
  assert.equal(result.file, file, url);
  assert.equal(result.headers['Cache-Control'], mutableCache, url);
}
for (const file of Object.keys(build.files)) {
  const url = '/seventh/' + file, result = await resolve(url);
  assert.equal(result.status, 200, url);
  assert.equal(result.file, url, url);
  assert.equal(result.headers['Cache-Control'], file.startsWith('areas/') ? immutableCache : mutableCache, url);
}
const absent = ['/seventh/areas/assets/' + '0'.repeat(64) + '.scn',
  '/seventh/areas/manifest-' + '0'.repeat(64) + '.json',
  '/seventh/areas/assets/unversioned.scn', '/seventh/areas/manifest-current.json'];
for (const url of absent) {
  const result = await resolve(url);
  assert.equal(result.status, 404, url);
  assert.equal(result.headers['Cache-Control'], 'no-store', url);
}
console.log(`Hosting route contract: ${Object.keys(build.files).length} files, root/legacy mapping and four uncached missing-file cases pass.`);
