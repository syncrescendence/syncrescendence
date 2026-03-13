#!/usr/bin/env node

const http = require("http");
const fs = require("fs");

const DEFAULT_HOST = "127.0.0.1";
const DEFAULT_PORT = 18792;
const DEFAULT_HEADER = "x-openclaw-relay-token";
const DEFAULT_TOKEN = "0a8962ae5789cca85855084b1e847af7a05d71912aac4b28";

function fail(message) {
  console.error(message);
  process.exit(1);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function requestJson({ path, host, port, header, token }) {
  return new Promise((resolve, reject) => {
    const req = http.request(
      {
        host,
        port,
        path,
        headers: {
          [header]: token,
        },
      },
      (res) => {
        let data = "";
        res.setEncoding("utf8");
        res.on("data", (chunk) => {
          data += chunk;
        });
        res.on("end", () => {
          if (res.statusCode && res.statusCode >= 400) {
            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
            return;
          }
          try {
            resolve(JSON.parse(data));
          } catch (error) {
            reject(new Error(`Invalid JSON from ${path}: ${data}`));
          }
        });
      },
    );
    req.on("error", reject);
    req.end();
  });
}

class CdpClient {
  constructor({ host, port, header, token }) {
    this.host = host;
    this.port = port;
    this.header = header;
    this.token = token;
    this.nextId = 1;
    this.pending = new Map();
    this.ws = null;
  }

  async connect() {
    const WebSocketImpl = globalThis.WebSocket;
    if (!WebSocketImpl) {
      fail("Node runtime does not expose WebSocket.");
    }
    this.ws = new WebSocketImpl(`ws://${this.host}:${this.port}/cdp`, {
      headers: { [this.header]: this.token },
    });
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.id && this.pending.has(message.id)) {
        const { resolve, reject } = this.pending.get(message.id);
        this.pending.delete(message.id);
        if (message.error) reject(new Error(JSON.stringify(message.error)));
        else resolve(message.result);
      }
    };
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
    });
  }

  send(method, params = {}, sessionId = undefined) {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      this.pending.set(id, { resolve, reject });
      const payload = { id, method, params };
      if (sessionId) payload.sessionId = sessionId;
      this.ws.send(JSON.stringify(payload));
    });
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function listTabs(config) {
  const tabs = await requestJson({ ...config, path: "/json/list" });
  console.log(JSON.stringify(tabs, null, 2));
}

function chooseTab(tabs, args) {
  if (args["target-id"]) {
    return tabs.find((tab) => tab.id === args["target-id"]);
  }
  if (args["match-url"]) {
    return tabs.find((tab) => tab.url.includes(args["match-url"]));
  }
  if (args["match-title"]) {
    return tabs.find((tab) => tab.title.includes(args["match-title"]));
  }
  return tabs[0];
}

async function evalInTab(config, args) {
  const tabs = await requestJson({ ...config, path: "/json/list" });
  const tab = chooseTab(tabs, args);
  if (!tab) {
    fail(`No tab matched target-id=${args["target-id"] || ""} match-url=${args["match-url"] || ""} match-title=${args["match-title"] || ""}`);
  }
  let expression = args.expr || "";
  if (args["expr-file"]) {
    expression = fs.readFileSync(args["expr-file"], "utf8");
  }
  if (!expression) {
    fail("Provide --expr or --expr-file.");
  }
  const client = new CdpClient(config);
  await client.connect();
  try {
    const { sessionId } = await client.send("Target.attachToTarget", {
      targetId: tab.id,
      flatten: true,
    });
    await client.send("Runtime.enable", {}, sessionId);
    const result = await client.send(
      "Runtime.evaluate",
      {
        expression,
        awaitPromise: true,
        returnByValue: !args["return-remote-object"],
      },
      sessionId,
    );
    console.log(JSON.stringify({ tab, result }, null, 2));
  } finally {
    client.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  if (!command) {
    fail("usage: relay_cdp.js <list-tabs|eval> [--match-url ... | --target-id ...] [--expr ... | --expr-file ...]");
  }
  const config = {
    host: args.host || DEFAULT_HOST,
    port: Number(args.port || DEFAULT_PORT),
    header: args.header || DEFAULT_HEADER,
    token: args.token || process.env.OPENCLAW_RELAY_TOKEN || DEFAULT_TOKEN,
  };

  if (command === "list-tabs") {
    await listTabs(config);
    return;
  }
  if (command === "eval") {
    await evalInTab(config, args);
    return;
  }
  fail(`unknown command: ${command}`);
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
