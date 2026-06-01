import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const command = process.argv[2] ?? "dev";
const args = process.argv.slice(3);
const astroBin = fileURLToPath(new URL("../node_modules/astro/astro.js", import.meta.url));

const child = spawn(process.execPath, [astroBin, command, ...args], {
  stdio: "inherit",
  shell: false,
  env: {
    ...process.env,
    ASTRO_TELEMETRY_DISABLED: "1"
  }
});

child.on("exit", (code) => {
  process.exit(code ?? 1);
});
