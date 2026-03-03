# MCP (Model Context Protocol) Configuration

## Overview
MCP enables Claude to interact with external services (GitHub, filesystem, databases) through a standardized protocol. This configuration supports multi-Claude coordination for Syncrescendence.

## Prerequisites
- Docker installed (for GitHub MCP server)
- Node.js 18+ (for local MCP servers)
- GitHub Personal Access Token with repo scope

## Server Configuration

### GitHub MCP Server
The official GitHub MCP server enables repository operations without manual git commands.

**Installation**:
```bash
# Pull the official image
docker pull ghcr.io/github/github-mcp-server

# Or use npx (requires Node.js)
npx @anthropic/github-mcp-server
```

**Configuration** (add to `~/.claude/.mcp.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "-e", "GITHUB_TOOLSETS=repos,issues,pull_requests",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
      }
    }
  }
}
```

**Available Toolsets**:
- `repos` - Repository management, file operations, branch creation
- `issues` - Issue creation, listing, commenting
- `pull_requests` - PR creation, review, merge
- `actions` - Workflow triggers, job logs

### Filesystem MCP Server
For direct filesystem operations across allowed paths.

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@modelcontextprotocol/server-filesystem",
        "/Users/YOUR_USERNAME/syncrescendence",
        "/Users/YOUR_USERNAME/syncrescendence-alpha",
        "/Users/YOUR_USERNAME/syncrescendence-beta",
        "/Users/YOUR_USERNAME/syncrescendence-gamma"
      ]
    }
  }
}
```

## Security Notes
- Never commit tokens to repository
- Use environment variables for secrets
- Restrict toolsets to minimum required
- Use `GITHUB_READ_ONLY=1` for read-only instances

## Verification
```bash
# Test GitHub MCP
docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# Check available tools
npx @anthropic/mcp-client list-tools
```

## Multi-Instance Coordination

When running multiple Claude instances, each should:
1. Use its own git worktree (see coordination.yaml)
2. Have zone-specific write permissions
3. Use branch prefixes (alpha/, beta/, gamma/)

See `engine/coordination.yaml` for zone ownership definitions.
