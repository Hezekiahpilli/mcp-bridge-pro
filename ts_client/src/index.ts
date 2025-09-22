
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const CMD = process.env.MCP_CMD || "python";
const ARGS = (process.env.MCP_ARGS || "python_server/server.py").split(" ");

async function main() {
  const transport = new StdioClientTransport({ command: CMD, args: ARGS });
  const client = new Client({ name: "bridge-client", version: "0.1.0" });
  await client.connect(transport);

  const tools = await client.listTools();
  console.log("Tools:", tools.tools.map(t => t.name));

  const echoRes = await client.callTool({ name: "echo", arguments: { text: "hello" } });
  console.log("echo:", echoRes.content);

  const calcRes = await client.callTool({ name: "calc", arguments: { expr: "2*(3+4)" } });
  console.log("calc:", calcRes.content);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
