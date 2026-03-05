# Webshell Decision — CC84

**Date**: 2026-03-04  
**Status**: active  
**Class**: risk and tradeoff decision

## Chosen Path

Use a **private-first webshell**:

1. local-only bind (`127.0.0.1`)
2. read-only status/docs endpoints available immediately
3. callback write endpoints disabled by default
4. callback write endpoints enabled only when explicit token is configured

## Why this is best now

1. You are still in account/ownership migration windows and do not need public write ingress yet.
2. You asked for autonomous progress while not wanting security footguns.
3. This gives immediate operational visibility with minimal blast radius.
4. It preserves momentum without requiring immediate decisions on signature verification, WAF policy, and webhook hardening.

## Tradeoffs

Benefits:

1. safest default
2. no accidental public callback ingestion
3. simple mental model while migration is in progress

Costs:

1. not yet internet-addressable for third-party webhook providers
2. requires one explicit token to enable callback writes
3. true public callback automation is deferred to a later hardening tranche

## Promotion condition to external stage

Promote from private-first to public callback ingress only when all are true:

1. ownership transfer waves are stable (Slack/Discord/GitHub)
2. Cloudflare path routing for `/ops/*` is ready
3. per-provider signature validation policy is defined
4. callback replay protection policy is defined
