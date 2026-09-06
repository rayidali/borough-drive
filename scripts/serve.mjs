import http from 'node:http';
import {createReadStream} from 'node:fs';
import {stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

// Serve only the game directory, bound to this computer's loopback interface.
const root = fileURLToPath(new URL('../dist/', import.meta.url));
const port = Number(process.argv[2] ?? 5173);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  console.error('Choose a port between 1 and 65535: npm run dev -- 5174');
  process.exit(1);
}
const types = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.wasm': 'application/wasm', '.glb': 'model/gltf-binary',
  '.gltf': 'model/gltf+json', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.hdr': 'application/octet-stream',
  '.txt': 'text/plain; charset=utf-8', '.md': 'text/plain; charset=utf-8'
};

const server = http.createServer(async (req, res) => {
  const fail = (status, message) => {
    res.writeHead(status, {'Content-Type': 'text/plain; charset=utf-8'});
    res.end(req.method === 'HEAD' ? undefined : message);
  };
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.setHeader('Allow', 'GET, HEAD');
    return fail(405, 'Method not allowed');
  }
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  } catch {
    return fail(400, 'Invalid URL');
  }
  if (pathname.includes('\0') || pathname.includes('\\')) return fail(400, 'Invalid path');
  const filename = path.resolve(root, '.' + (pathname.endsWith('/') ? pathname + 'index.html' : pathname));
  const relative = path.relative(root, filename);
  if (relative.startsWith('..') || path.isAbsolute(relative)) return fail(403, 'Forbidden');
  try {
    const info = await stat(filename);
    if (!info.isFile()) return fail(404, 'File not found');
    const stream = createReadStream(filename);
    stream.on('error', () => {
      if (res.headersSent) res.destroy();
      else fail(500, 'Unable to read file');
    });
    res.writeHead(200, {
      'Content-Type': types[path.extname(filename).toLowerCase()] ?? 'application/octet-stream',
      'Content-Length': info.size,
      'Cache-Control': 'no-cache',
      'X-Content-Type-Options': 'nosniff'
    });
    if (req.method === 'HEAD') {
      stream.destroy();
      return res.end();
    }
    res.on('close', () => stream.destroy());
    stream.pipe(res);
  } catch (error) {
    fail(error.code === 'ENOENT' || error.code === 'ENOTDIR' ? 404 : 500, 'File unavailable');
  }
});
server.on('error', error => {
  console.error(error.code === 'EADDRINUSE'
    ? `Port ${port} is busy. Try: npm run dev -- ${port < 65535 ? port + 1 : 5173}`
    : error.message);
  process.exitCode = 1;
});
server.listen(port, '127.0.0.1', () => {
  console.log(`Borough Drive: http://127.0.0.1:${port}`);
  console.log('Press Ctrl+C to stop. Files are served from dist/.');
});
