// main.ts — NIMBARA poster entry point (Node 22, stdlib only).
// Reads entry.png from this script's own folder (never a bare relative
// path, so the grader can run it from any working directory) and checks
// it is a 1024x1024 PNG under the 1 MiB limit before handing it off.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const bytes = readFileSync(source);

function fail(msg: string): never {
  throw new Error(`entry.png rejected: ${msg}`);
}

const MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (bytes.length < 8 || !MAGIC.every((b, i) => bytes[i] === b)) {
  fail("not a PNG file");
}
// Validate the IHDR chunk CRC so a truncated or corrupted header is
// caught even when the magic bytes and dimensions still look right.
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();
function crc32(buf: Buffer): number {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
if (bytes.length < 33 || bytes.toString("ascii", 12, 16) !== "IHDR") {
  fail("missing IHDR chunk");
}
const ihdrLen = bytes.readUInt32BE(8);
if (ihdrLen !== 13) {
  fail(`unexpected IHDR length: ${ihdrLen}`);
}
const storedCrc = bytes.readUInt32BE(29);
const actualCrc = crc32(bytes.subarray(12, 29));
if (storedCrc !== actualCrc) {
  fail(`IHDR CRC mismatch: ${storedCrc.toString(16)} != ${actualCrc.toString(16)}`);
}
if (bytes.length > 1024 * 1024) {
  fail(`too large: ${bytes.length} bytes (limit 1 MiB)`);
}
const w = bytes.readUInt32BE(16);
const h = bytes.readUInt32BE(20);
if (w !== 1024 || h !== 1024) {
  fail(`wrong size: ${w}x${h} (expected 1024x1024)`);
}
const digest = createHash("sha256").update(bytes).digest("hex");

// Copy the validated image to /output and prove the copy is identical.
const targetDir = "/output";
const target = join(targetDir, "entry.png");

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);

const again = readFileSync(target);
if (again.length !== bytes.length) {
  fail(`copy length mismatch: ${again.length} != ${bytes.length}`);
}
const digest2 = createHash("sha256").update(again).digest("hex");
if (digest2 !== digest) {
  fail(`copy sha256 mismatch: ${digest2} != ${digest}`);
}
console.log(`entry.png ${w}x${h} ${bytes.length} bytes sha256 ${digest}`);
console.log(`verified ${target} sha256 ${digest2}`);
