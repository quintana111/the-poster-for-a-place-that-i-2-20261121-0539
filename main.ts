import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const src = join(dir, "entry.png");
const outDir = "/output";
const out = join(outDir, "entry.png");

if (!existsSync(src)) throw new Error(`entry.png not found next to main.ts: ${src}`);
const buf = readFileSync(src);
if (buf.length > 1048576) throw new Error(`entry.png too large: ${buf.length} bytes`);
const magic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(magic)) throw new Error("entry.png is not a PNG");
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}
// IHDR CRC: CRC32 over the chunk type + data (bytes 12..28), stored at 29..32
const crcTable = (() => {
  const t = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c;
  }
  return t;
})();
const crc32 = (b: Buffer) => {
  let c = 0xffffffff;
  for (const byte of b) c = crcTable[(c ^ byte) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
if (buf.readUInt32BE(8) !== 13 || buf.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png has a malformed IHDR chunk");
}
if (crc32(buf.subarray(12, 29)) !== buf.readUInt32BE(29)) {
  throw new Error("entry.png IHDR CRC mismatch");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, out);
const back = readFileSync(out);
if (back.length !== buf.length) throw new Error("read-back length mismatch");
const sha = (b: Buffer) => createHash("sha256").update(b).digest("hex");
if (sha(back) !== sha(buf)) throw new Error("read-back sha256 mismatch");
console.log(`ok: /output/entry.png ${back.length} bytes sha256=${sha(back)}`);
