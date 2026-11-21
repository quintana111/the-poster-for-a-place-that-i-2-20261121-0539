// ANCHORA — The Lighthouse Anchor (make.fun poster bounty entry).
// Copies the rendered entry.png next to this script to /output/entry.png,
// validating PNG magic, IHDR CRC, 1024x1024 dimensions and the 1 MiB cap.
// Node 22 stdlib only. No network.
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const OUT_DIR = "/output";
const OUT = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1048576;

function crc32(buf) {
  let table = crc32.table;
  if (!table) {
    table = crc32.table = new Int32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      table[n] = c;
    }
  }
  let c = 0xffffffff;
  for (const b of buf) c = table[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function fail(msg) {
  console.error("entry validation failed:", msg);
  process.exit(1);
}

const data = readFileSync(SRC);
if (data.length > MAX_BYTES) fail(`entry.png is ${data.length} bytes, over 1 MiB`);
const MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!data.subarray(0, 8).equals(MAGIC)) fail("not a PNG file");
if (data.readUInt32BE(8) !== 13 || data.toString("ascii", 12, 16) !== "IHDR") {
  fail("missing IHDR chunk");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`expected 1024x1024, got ${width}x${height}`);
}
const storedCrc = data.readUInt32BE(29);
const computedCrc = crc32(data.subarray(12, 29));
if (storedCrc !== computedCrc) fail("IHDR CRC mismatch");

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT);
const back = readFileSync(OUT);
if (back.length !== data.length) fail("read-back length mismatch");
const sha = createHash("sha256").update(back).digest("hex");
console.log(`entry.png ${width}x${height} ${back.length} bytes sha256=${sha}`);
console.log("wrote /output/entry.png");
