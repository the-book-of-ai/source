// Rebuild appendices/_ai-tools-static.md from appendices/ai-tools.csv.
// Quarto's HTML page reads the CSV directly. PDF and EPUB include this file.
const csvPath = "appendices/ai-tools.csv";
const outPath = "appendices/_ai-tools-static.md";

const text = Deno.readTextFileSync(csvPath).replace(/^\uFEFF/, "");
const records = parseCsv(text);
const header = records.shift();
if (!header) {
  throw new Error(`${csvPath} is empty`);
}
const index = Object.fromEntries(header.map((name, i) => [name, i]));
for (const name of ["Tool", "URL", "Section", "Category", "License", "Platform", "Strength", "Limitation", "Note"]) {
  if (index[name] === undefined) {
    throw new Error(`${csvPath} is missing the ${name} column`);
  }
}

const lines = ["<!-- Generated from ai-tools.csv. Do not edit by hand. -->", ""];
let section: string | undefined;
for (const record of records) {
  if (record.every((cell) => cell === "")) continue;
  const next = record[index.Section];
  if (next !== section) {
    if (section !== undefined) lines.push("");
    section = next;
    lines.push(`## ${section}`, "");
    lines.push("| Tool | Category | License | Platform | Strength | Limitation | Note |");
    lines.push("| --- | --- | --- | --- | --- | --- | --- |");
  }
  const tool = record[index.Tool];
  const url = record[index.URL];
  const toolCell = url ? `[${tool}](${url})` : tool;
  lines.push("| " + [
    toolCell,
    record[index.Category],
    record[index.License],
    record[index.Platform],
    record[index.Strength],
    record[index.Limitation],
    record[index.Note],
  ].map(escapeCell).join(" | ") + " |");
}
lines.push("");
const output = lines.join("\n");

let previous = "";
try {
  previous = Deno.readTextFileSync(outPath);
} catch (_error) {
  previous = "";
}
if (previous !== output) {
  Deno.writeTextFileSync(outPath, output);
  console.log(`Wrote ${outPath}`);
} else {
  console.log(`${outPath} unchanged`);
}

function escapeCell(value: string): string {
  return value.replace(/\|/g, "\\|").replace(/\r?\n/g, " ");
}

function parseCsv(input: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < input.length; i++) {
    const char = input[i];
    if (quoted) {
      if (char === '"') {
        if (input[i + 1] === '"') {
          cell += '"';
          i++;
        } else {
          quoted = false;
        }
      } else {
        cell += char;
      }
      continue;
    }
    if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
    } else if (char !== "\r") {
      cell += char;
    }
  }
  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }
  return rows;
}
