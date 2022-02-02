const fs = require("fs");
const { parse } = require("path");

let config = {};

fs.readFile("conv.txt", "utf-8", parseConv);

function parseConv(_, data) {
  const rows = data
    .replace(/ /g, "")
    .replace(/#\S*/g, "")
    .replace(/\r/g, "")
    .split("\n");

  for (const r of rows) {
    if (r == "") {
      continue;
    }
    const [key, value] = r.split(";");
    config[key] = value;
  }

  fs.readFile("t1_in.txt", "utf-8", parseT1In);
}

function parseT1In(_, data) {
  const rows = data.replace(/ /g, "").replace(/#\S+/g, "").split("\n");
  let result = "";
  for (const r of rows) {
    if (isFinite(parseInt(r))) {
      result += `Ждем ${parseInt(r)} c\n`;
      continue;
    }

    if (r === "") {
      continue;
    }

    if (r.match(/\S+:\S+:\S+:?\S+/g)) {
      result += `${parseABCDRowFormat(r)}\n`;
      continue;
    }

    if (r.match(/\S+:\S+$/g)) {
      result += `${parseABRowFormat(r)}\n`;
      continue;
    }
  }

  fs.writeFile("t1_out.txt", result, "utf-8", () => {});
}

function parseABCDRowFormat(row) {
  let blocks = row.split(":");
  blocks[0] = config[blocks[0]] === undefined ? blocks[0] : config[blocks[0]];
  blocks[3] = blocks[3] === undefined ? 0 : 1;
  return blocks.join(":");
}

function parseABRowFormat(row) {
  let blocks = row.split(/:|;/);
  blocks[0] = config[blocks[0]];
  return blocks.slice(0, 2).join(":");
}
