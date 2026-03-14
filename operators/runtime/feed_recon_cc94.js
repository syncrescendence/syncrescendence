#!/usr/bin/env node

const http = require("http");

const RELAY_HOST = "127.0.0.1";
const RELAY_PORT = 18792;
const RELAY_HEADER = "x-openclaw-relay-token";
const RELAY_TOKEN =
  process.env.OPENCLAW_RELAY_TOKEN ||
  "0a8962ae5789cca85855084b1e847af7a05d71912aac4b28";

function requestJson(path) {
  return new Promise((resolve, reject) => {
    const req = http.request(
      {
        host: RELAY_HOST,
        port: RELAY_PORT,
        path,
        headers: { [RELAY_HEADER]: RELAY_TOKEN },
      },
      (res) => {
        let data = "";
        res.setEncoding("utf8");
        res.on("data", (chunk) => {
          data += chunk;
        });
        res.on("end", () => {
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

class CdpSession {
  constructor(target) {
    this.target = target;
    this.nextId = 1;
    this.pending = new Map();
    this.sessionId = null;
    this.ws = null;
  }

  async connect() {
    const WebSocketImpl = globalThis.WebSocket;
    this.ws = new WebSocketImpl(`ws://${RELAY_HOST}:${RELAY_PORT}/cdp`, {
      headers: { [RELAY_HEADER]: RELAY_TOKEN },
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
    const { sessionId } = await this.send("Target.attachToTarget", {
      targetId: this.target.id,
      flatten: true,
    });
    this.sessionId = sessionId;
    await this.send("Page.enable");
    await this.send("Runtime.enable");
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      this.pending.set(id, { resolve, reject });
      this.ws.send(
        JSON.stringify({
          id,
          sessionId: this.sessionId,
          method,
          params,
        }),
      );
    });
  }

  async evaluate(expression) {
    const result = await this.send("Runtime.evaluate", {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    return result.result?.value;
  }

  async navigate(url, waitMs = 2500) {
    await this.send("Page.navigate", { url });
    await this.wait(waitMs);
  }

  async wait(ms) {
    await new Promise((resolve) => setTimeout(resolve, ms));
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function getTabs() {
  return await requestJson("/json/list");
}

async function openSession(match) {
  const tabs = await getTabs();
  const candidates = tabs.filter((tab) => tab.url.includes(match));
  const score = (tab) => {
    if (match === "x.com") {
      if (tab.url.includes("/home")) return 100;
      if (tab.url === "https://x.com/" || tab.url === "https://x.com") return 90;
      if (/https:\/\/x\.com\/[^/]+$/.test(tab.url)) return 80;
      return 10;
    }
    if (match === "youtube.com") {
      if (tab.url.includes("/feed/channels")) return 100;
      if (tab.url === "https://www.youtube.com/" || tab.url === "https://www.youtube.com") return 90;
      return 10;
    }
    return 0;
  };
  const target = candidates.sort((a, b) => score(b) - score(a))[0];
  if (!target) throw new Error(`No tab matched ${match}`);
  const session = new CdpSession(target);
  await session.connect();
  return session;
}

async function listXAccounts(session) {
  await session.navigate("https://x.com/account/switch", 2000);
  return await session.evaluate(`(() => {
    const current = (document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]')?.innerText || '').trim();
    const currentHandle = (current.match(/@[A-Za-z0-9_]+/) || [null])[0];
    const switchers = [...document.querySelectorAll('button,[role="button"]')]
      .map((el) => ({
        aria: el.getAttribute('aria-label'),
        text: (el.innerText || el.textContent || '').trim(),
      }))
      .filter((entry) => /Switch to @/i.test(entry.aria || ''))
      .map((entry) => ({
        handle: ((entry.aria || '').match(/@[A-Za-z0-9_]+/) || [null])[0],
        aria: entry.aria,
        text: entry.text,
      }));
    return { currentHandle, currentRaw: current, switchers };
  })()`);
}

async function switchXAccount(session, handle) {
  const state = await listXAccounts(session);
  if (state.currentHandle === handle) return state;
  const clickTarget = async () =>
    await session.evaluate(`(() => {
      const target = [...document.querySelectorAll('button,[role="button"]')]
        .find((el) => (el.getAttribute('aria-label') || '') === 'Switch to ${handle}');
      if (!target) return { ok: false };
      target.click();
      return { ok: true };
    })()`);
  const clicked = await clickTarget();
  if (!clicked.ok) throw new Error(`Could not find X account switch target ${handle}`);
  for (let i = 0; i < 20; i += 1) {
    await session.wait(1500);
    const current = await session.evaluate(`(() => {
      const raw = (document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]')?.innerText || '').trim();
      return {
        handle: (raw.match(/@[A-Za-z0-9_]+/) || [null])[0],
        raw,
        url: location.href,
        title: document.title,
        bodyHandle: ((document.body.innerText || '').match(/@[A-Za-z0-9_]+/) || [null])[0],
      };
    })()`);
    if (current.handle === handle) return current;
    if (i === 4 || i === 10) {
      await session.navigate("https://x.com/account/switch", 2000);
    }
    if (i === 11) {
      await clickTarget();
    }
  }
  throw new Error(`X account switch did not settle to ${handle}`);
}

async function xProfileSnapshot(session, handle) {
  await session.navigate(`https://x.com/${handle.replace(/^@/, "")}`, 3000);
  return await session.evaluate(`(() => {
    const text = document.body.innerText || '';
    const metricLinks = [...document.querySelectorAll('a[href*="/following"], a[href*="/followers"], a[href*="/verified_followers"]')]
      .map((a) => ({ href: a.href, text: (a.innerText || a.textContent || '').trim() }));
    return {
      title: document.title,
      url: location.href,
      text: text.slice(0, 2000),
      metricLinks,
    };
  })()`);
}

async function listYoutubeAccounts(session) {
  await session.evaluate(`(() => {
    document.querySelector('#avatar-btn')?.click();
    return true;
  })()`);
  await session.wait(1200);
  await session.evaluate(`(() => {
    const link = [...document.querySelectorAll('a,tp-yt-paper-item')]
      .find((el) => /Switch account/i.test((el.innerText || el.textContent || '').trim()));
    if (link) link.click();
    return true;
  })()`);
  await session.wait(1200);
  return await session.evaluate(`(() => {
    const currentEmail = (document.querySelector('ytd-google-account-header-renderer #email')?.innerText || '').trim();
    const currentHandle = (document.querySelector('ytd-account-item-renderer yt-formatted-string')?.innerText || '').trim();
    const sections = [...document.querySelectorAll('ytd-account-item-section-renderer')]
      .map((section) => {
        const email = (section.querySelector('ytd-account-item-section-header-renderer yt-formatted-string')?.innerText || '').trim();
        const item = section.querySelector('ytd-account-item-renderer');
        const name = (item?.innerText || '').trim().split('\\n').map((line) => line.trim()).filter(Boolean);
        return { email, lines: name };
      })
      .filter((entry) => entry.email);
    return { currentEmail, currentHandle, sections };
  })()`);
}

async function switchYoutubeAccount(session, email) {
  const state = await youtubeSwitchState(session);
  if (!state.availableEmails.includes(email)) return state;
  const switched = await session.evaluate(`(() => {
    const sections = [...document.querySelectorAll('ytd-account-item-section-renderer')];
    for (const section of sections) {
      const emailText = (section.querySelector('ytd-account-item-section-header-renderer yt-formatted-string')?.innerText || '').trim();
      if (emailText !== ${JSON.stringify(email)}) continue;
      const item = section.querySelector('tp-yt-paper-icon-item, tp-yt-paper-item, ytd-account-item-renderer');
      if (item) {
        item.click();
        return { ok: true };
      }
    }
    return { ok: false };
  })()`);
  if (!switched.ok) throw new Error(`Could not switch YouTube account to ${email}`);
  await session.wait(3000);
  const next = await youtubeSwitchState(session);
  if (next.availableEmails.includes(email)) {
    throw new Error(`YouTube account switch did not settle to ${email}`);
  }
  return next;
}

async function currentYoutubeIdentity(session) {
  await session.evaluate(`(() => {
    document.querySelector('#avatar-btn')?.click();
    return true;
  })()`);
  await session.wait(800);
  const state = await session.evaluate(`(() => {
    const currentEmail = (document.querySelector('ytd-popup-container #email')?.innerText || '').trim();
    const currentHandle = (document.querySelector('ytd-popup-container #channel-handle')?.innerText || '').trim();
    return { currentEmail, currentHandle };
  })()`);
  await session.evaluate(`(() => {
    document.body.click();
    return true;
  })()`);
  return state;
}

async function youtubeSwitchState(session) {
  await session.evaluate(`(() => {
    document.querySelector('#avatar-btn')?.click();
    return true;
  })()`);
  await session.wait(800);
  await session.evaluate(`(() => {
    const link = [...document.querySelectorAll('a,tp-yt-paper-item')]
      .find((el) => /Switch account/i.test((el.innerText || el.textContent || '').trim()));
    if (link) link.click();
    return true;
  })()`);
  await session.wait(800);
  const state = await session.evaluate(`(() => {
    const sections = [...document.querySelectorAll('ytd-account-item-section-renderer')];
    const availableEmails = sections
      .map((section) => (section.querySelector('ytd-account-item-section-header-renderer yt-formatted-string')?.innerText || '').trim())
      .filter(Boolean);
    const currentSection = sections.find((section) => !(section.querySelector('ytd-account-item-section-header-renderer yt-formatted-string')?.innerText || '').trim());
    return {
      availableEmails,
      currentSectionText: (currentSection?.innerText || '').trim(),
    };
  })()`);
  return state;
}

async function scrapeYoutubeSubscriptions(session, email) {
  await switchYoutubeAccount(session, email);
  await session.navigate("https://www.youtube.com/feed/channels", 2500);
  return await session.evaluate(`(async () => {
    const seen = new Map();
    let stablePasses = 0;
    let lastSize = 0;
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const collect = () => {
      const rows = [...document.querySelectorAll('ytd-channel-renderer')];
      for (const row of rows) {
        const link = row.querySelector('a#main-link, a[href^="/@"], a[href^="/channel/"]');
        if (!link) continue;
        const href = link.href;
        if (!href) continue;
        const channelName = (row.querySelector('#text-container, #channel-title, #title')?.innerText || link.innerText || '').trim().replace(/\\s+/g, ' ');
        const handle = href.includes('/@') ? href.split('/@')[1]?.split(/[/?#]/)[0] || '' : '';
        seen.set(href, {
          source_account: ${JSON.stringify(email)},
          platform: 'youtube',
          channel_name: channelName,
          channel_handle: handle ? '@' + handle : '',
          channel_url: href,
          notes: '',
        });
      }
    };
    for (let i = 0; i < 60; i += 1) {
      collect();
      window.scrollTo(0, document.documentElement.scrollHeight);
      await sleep(1200);
      collect();
      if (seen.size === lastSize) stablePasses += 1;
      else stablePasses = 0;
      lastSize = seen.size;
      if (stablePasses >= 4) break;
    }
    return { items: [...seen.values()] };
  })()`);
}

async function scrapeXFollowing(session, handle) {
  const normalized = handle.replace(/^@/, "");
  await session.navigate(`https://x.com/${normalized}/following`, 3000);
  const expectedCount = await session.evaluate(`(() => {
    const text = document.body.innerText || '';
    const match = text.match(/([\\d,]+)\\s+Following/i);
    return match ? Number(match[1].replace(/,/g, '')) : null;
  })()`);
  const seen = new Map();
  let stablePasses = 0;
  let lastSize = 0;
  let lastY = -1;
  const diagnostics = [];
  for (let i = 0; i < 140; i += 1) {
    const batch = await session.evaluate(`(() => {
      const rows = [...document.querySelectorAll('[data-testid="UserCell"]')];
      const items = rows.map((cell) => {
        const rawText = (cell.innerText || '').trim();
        if (!/Following|Unfollow/i.test(rawText)) return null;
        const links = [...cell.querySelectorAll('a[href]')].map((a) => a.href).filter(Boolean);
        const profileHref = links.find((href) => /^https:\\/\\/x\\.com\\/[^/]+$/.test(href) && !href.includes('/status/'));
        if (!profileHref) return null;
        const path = new URL(profileHref).pathname.replace(/^\\//, '');
        if (!path || ['home', 'explore', 'messages', 'notifications'].includes(path)) return null;
        const lines = rawText.split('\\n').map((line) => line.trim()).filter(Boolean);
        const displayName =
          lines.find((line) => !line.startsWith('@') && !/Follow|Following|Unfollow|Follows you/i.test(line)) || '';
        return {
          source_account: ${JSON.stringify(handle)},
          platform: 'x',
          display_name: displayName,
          handle: '@' + path,
          profile_url: profileHref,
          bio: '',
          notes: '',
        };
      }).filter(Boolean);
      return {
        items,
        y: window.scrollY,
        scrollHeight: document.documentElement.scrollHeight,
        clientHeight: document.documentElement.clientHeight,
      };
    })()`);
    for (const item of batch.items) {
      seen.set(item.handle, item);
    }
    diagnostics.push({
      step: i,
      seen: seen.size,
      visible: batch.items.length,
      y: batch.y,
      scrollHeight: batch.scrollHeight,
    });
    if (expectedCount && seen.size >= expectedCount) break;
    const atBottom = batch.y + batch.clientHeight >= batch.scrollHeight - 8;
    if (seen.size === lastSize) stablePasses += 1;
    else stablePasses = 0;
    if (atBottom && stablePasses >= 8) break;
    if (batch.y === lastY && stablePasses >= 8) break;
    lastSize = seen.size;
    lastY = batch.y;
    await session.evaluate(`(() => {
      window.scrollBy(0, Math.max(900, Math.floor(window.innerHeight * 0.9)));
      return { y: window.scrollY };
    })()`);
    await session.wait(1500);
  }
  return {
    items: [...seen.values()],
    url: await session.evaluate("location.href"),
    title: await session.evaluate("document.title"),
    expectedCount,
    diagnostics,
  };
}

function diffBy(items, key) {
  return new Map(items.map((item) => [item[key], item]));
}

async function applyXFollows(session, destHandle, items) {
  await switchXAccount(session, destHandle);
  const results = [];
  for (const item of items) {
    await session.navigate(item.profile_url, 2500);
    const result = await session.evaluate(`(() => {
      const targetHandle = ${JSON.stringify(item.handle)};
      const buttons = [...document.querySelectorAll('button,[role="button"],div[role="button"]')];
      const candidate = buttons.find((el) => /Follow|Following|Unfollow/i.test((el.innerText || el.textContent || '').trim()) || /Follow @/i.test(el.getAttribute('aria-label') || ''));
      if (!candidate) return { status: 'button_not_found' };
      const label = ((candidate.innerText || candidate.textContent || '').trim() || candidate.getAttribute('aria-label') || '').trim();
      if (/Following|Unfollow/i.test(label)) return { status: 'already_following', label };
      if (!/Follow/i.test(label)) return { status: 'unexpected_button', label };
      candidate.click();
      return { status: 'clicked_follow', label };
    })()`);
    results.push({ handle: item.handle, profile_url: item.profile_url, ...result });
    await session.wait(1200);
  }
  return results;
}

async function applyYoutubeSubscriptions(session, email, items) {
  await switchYoutubeAccount(session, email);
  const results = [];
  for (const item of items) {
    await session.navigate(item.channel_url, 2500);
    const result = await session.evaluate(`(() => {
      const buttons = [...document.querySelectorAll('button, yt-button-shape button, tp-yt-paper-button, tp-yt-paper-subscribe-button')];
      const candidate = buttons.find((el) => {
        const text = ((el.innerText || el.textContent || '').trim() || el.getAttribute('aria-label') || '').trim();
        return /Subscribe|Subscribed/i.test(text);
      });
      if (!candidate) return { status: 'button_not_found' };
      const label = ((candidate.innerText || candidate.textContent || '').trim() || candidate.getAttribute('aria-label') || '').trim();
      if (/Subscribed/i.test(label)) return { status: 'already_subscribed', label };
      if (!/Subscribe/i.test(label)) return { status: 'unexpected_button', label };
      candidate.click();
      return { status: 'clicked_subscribe', label };
    })()`);
    results.push({ channel_url: item.channel_url, channel_name: item.channel_name, ...result });
    await session.wait(1500);
  }
  return results;
}

async function main() {
  const mode = process.argv[2] || "inspect";
  if (!["inspect", "capture", "migrate"].includes(mode)) {
    throw new Error(`Unsupported mode: ${mode}`);
  }
  const xSession = await openSession("x.com");
  const ySession = await openSession("youtube.com");
  try {
    const xAccounts = await listXAccounts(xSession);
    const youtubeAccounts = await listYoutubeAccounts(ySession);
    const xSourceHandle = "@truongphillipth";
    const xDestHandle = "@truongphillipt_";
    const ySourceEmail = "truongphillipthanh@gmail.com";
    const yDestEmail = "icloud.truongphillipthanh@gmail.com";
    const xSnapshots = [
      { handle: xSourceHandle, snapshot: await xProfileSnapshot(xSession, xSourceHandle) },
      { handle: xDestHandle, snapshot: await xProfileSnapshot(xSession, xDestHandle) },
    ];
    if (mode === "inspect") {
      console.log(
        JSON.stringify(
          {
            assumptions: {
              xSourceHandle,
            xDestHandle,
            ySourceEmail,
            yDestEmail,
          },
          xAccounts,
          xSnapshots,
          youtubeAccounts,
          youtubeSwitchState: await youtubeSwitchState(ySession),
        },
        null,
        2,
        ),
      );
      return;
    }
    await switchXAccount(xSession, xSourceHandle);
    const xSource = await scrapeXFollowing(xSession, xSourceHandle);
    await switchXAccount(xSession, xDestHandle);
    const xDest = await scrapeXFollowing(xSession, xDestHandle);
    const ySource = await scrapeYoutubeSubscriptions(ySession, ySourceEmail);
    const yDest = await scrapeYoutubeSubscriptions(ySession, yDestEmail);
    const xSourceMap = diffBy(xSource.items, "handle");
    const xDestMap = diffBy(xDest.items, "handle");
    const ySourceMap = diffBy(ySource.items, "channel_url");
    const yDestMap = diffBy(yDest.items, "channel_url");
    const xMissing = [...xSourceMap.values()].filter((item) => !xDestMap.has(item.handle));
    const yMissing = [...ySourceMap.values()].filter((item) => !yDestMap.has(item.channel_url));
    if (mode === "migrate") {
      const xApplied = await applyXFollows(xSession, xDestHandle, xMissing);
      const yApplied = await applyYoutubeSubscriptions(ySession, yDestEmail, yMissing);
      console.log(
        JSON.stringify(
          {
            assumptions: {
              xSourceHandle,
              xDestHandle,
              ySourceEmail,
              yDestEmail,
              xAccount1Handle: null,
              xInference:
                "X source/destination mapping inferred from live session reality: @truongphillipth is the larger legacy graph candidate and @truongphillipt_ is the sparse destination candidate. Account 1 X handle is not surfaced in-session.",
            },
            xSource,
            xDest,
            xMissing,
            xApplied,
            ySource,
            yDest,
            yMissing,
            yApplied,
          },
          null,
          2,
        ),
      );
      return;
    }
    console.log(
      JSON.stringify(
        {
          assumptions: {
            xSourceHandle,
            xDestHandle,
            ySourceEmail,
            yDestEmail,
            xAccount1Handle: null,
            xInference:
              "X source/destination mapping inferred from live session reality: @truongphillipth is the larger legacy graph candidate and @truongphillipt_ is the sparse destination candidate. Account 1 X handle is not surfaced in-session.",
          },
          xAccounts,
          xSnapshots,
          xSource,
          xDest,
          xMissing,
          youtubeAccounts,
          ySource,
          yDest,
          yMissing,
        },
        null,
        2,
      ),
    );
  } finally {
    xSession.close();
    ySession.close();
  }
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
