// Verify the exact tracked browser package through its public hosting routes.
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const [origin, output] = process.argv.slice(2);
if (!origin || !output) throw Error('Usage: node scripts/verify-live-seventh.mjs <origin> <report.json>');
const build = JSON.parse(await fs.readFile('dist/seventh/build.json', 'utf8'));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const report = { date: new Date().toISOString(), origin, builtAt: build.builtAt, routes: [], runtime: [], complete: false };
async function request(url) {
  const response = await fetch(new URL(url, origin), { signal: AbortSignal.timeout(120000) });
  return { response, bytes: Buffer.from(await response.arrayBuffer()) };
}
try {
  for (const [url, file] of [['/', 'seventh/index.html'], ['/seventh/', 'seventh/index.html'], ['/index.html', 'legacy.html'], ['/legacy.html', 'legacy.html'], ['/seventh/build.json', 'seventh/build.json']]) {
    const { response, bytes } = await request(url);
    assert.equal(response.status, 200, url);
    assert.equal(hash(bytes), hash(await fs.readFile('dist/' + file)), url);
    report.routes.push({ url, bytes: bytes.length, sha256: hash(bytes), cacheControl: response.headers.get('cache-control') });
  }
  const queue = Object.entries(build.files);
  await Promise.all(Array.from({ length: 4 }, async () => {
    while (queue.length) {
      const [file, expected] = queue.shift();
      const { response, bytes } = await request('/seventh/' + file);
      assert.equal(response.status, 200, file);
      assert.equal(bytes.length, expected.bytes, file);
      assert.equal(hash(bytes), expected.sha256, file);
      const cacheControl = response.headers.get('cache-control');
      if (/^areas\/(?:assets\/[a-f0-9]{64}\.scn|manifest-[a-f0-9]{64}\.json)$/.test(file)) assert.match(cacheControl || '', /immutable/, file);
      report.runtime.push({ file, sha256: hash(bytes), cacheControl });
    }
  }));
  const { response } = await request('/seventh/areas/assets/' + '0'.repeat(64) + '.scn');
  assert.equal(response.status, 404);
  assert.match(response.headers.get('cache-control') || '', /no-store/);
  report.missingScene404NoStore = true;
  report.complete = true;
} catch (error) {
  report.error = String(error);
  process.exitCode = 1;
} finally {
  report.runtime.sort((a, b) => a.file.localeCompare(b.file));
  await fs.mkdir(path.dirname(output), { recursive: true });
  await fs.writeFile(output, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ complete: report.complete, routes: report.routes.length, runtime: report.runtime.length, error: report.error }));
}
