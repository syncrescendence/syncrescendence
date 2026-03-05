# Syncrescendence Identity Cutover — Migration Capability Report

**Prepared by:** Manus AI
**Date:** 2026-03-05
**Target identity:** `syncrescendence@gmail.com`
**Classification:** Internal — Migration Design

---

## Executive Summary

This report provides a platform-by-platform analysis of what can be automated and what must remain a human-owner action when migrating ownership of thirteen service surfaces to `syncrescendence@gmail.com`. The analysis is grounded in official documentation and public API references for each platform. The central finding is that **only three platforms (GitHub, Google/GCP, and Slack on Enterprise Grid) expose APIs sufficient to automate the ownership grant step**; all others require the incumbent owner to take a manual, authenticated UI action. Accordingly, the migration strategy should treat automation as a pre-flight and post-flight verification harness, while the ownership mutation itself is orchestrated as a human-in-the-loop ceremony for most platforms.

---

## 1. Automation Envelope Matrix

The table below classifies each platform across five dimensions. "Can automate now" means that a script running under the current owner's credentials can programmatically grant the target account an equivalent ownership role without any UI interaction. "Must be human owner" means the incumbent owner must perform at least one authenticated UI action that cannot be replicated via API.

| Platform | Can Automate Now | Must Be Human Owner | Risk Level | Why |
| :--- | :---: | :---: | :---: | :--- |
| **GitHub (org + billing)** | Partial | Yes (billing) | Low | The REST API endpoint `PUT /orgs/{org}/memberships/{username}` with `"role": "admin"` can programmatically promote `syncrescendence` to org owner. However, billing contact and payment method updates have no API surface and require a human to log in to the billing settings. [1][2] |
| **Cloudflare (zone + Super Admin)** | No | Yes | Medium | There is no API endpoint to change the Super Administrator role. The official process requires the current Super Admin to add the new user via the dashboard and assign the Super Administrator role manually. Zone migration between accounts is also a manual nameserver-swap process. [3][4] |
| **Google Workspace (Super Admin)** | Partial | Yes (final removal) | Medium | The Admin SDK Directory API (`admin.googleapis.com`) can assign the Super Admin role to a new user programmatically. However, removing the old Super Admin requires the new Super Admin to perform that action — meaning the final step is always a human action by the newly promoted account. [5][6] |
| **GCP (project/org IAM)** | Yes | No | Low | The Resource Manager API `projects.setIamPolicy` can add `syncrescendence@gmail.com` as `roles/owner` on any project where the caller holds the Owner role. The old owner can be removed in the same API call. This is fully scriptable. [7] |
| **Slack (workspace/org owner)** | Yes (Enterprise Grid only) | Yes (non-EG plans) | Medium | The `admin.users.setOwner` API method can programmatically promote any member to workspace or org owner. This method is **exclusively available on Enterprise Grid plans**. On free, Pro, or Business+ plans, the current Primary Owner must use the UI. [8] |
| **Discord (server ownership)** | No | Yes | Low | Server ownership transfer is a UI-only action: right-click a member → "Transfer Ownership." No REST API endpoint exists for this operation. [9] |
| **Discord (app/bot team)** | No | Yes | Low | Developer Team ownership transfer requires the current team owner to navigate to the Developer Portal → Team Settings and initiate the transfer. Identity verification (Stripe) may be required. [10] |
| **Notion (workspace)** | No | Yes | Medium | The Notion public API does not expose any endpoint for managing member roles or workspace ownership. The workspace owner must manually change roles via Settings → People. [11] |
| **Coda (workspace/doc)** | No | Yes | Low | Doc ownership can be transferred by the current owner via the doc settings UI. Workspace-level admin transfer is also UI-only. Enterprise org admins can bulk-transfer docs from deprovisioned users, but this is still a UI action. [12][13] |
| **Confluence Cloud (Atlassian org)** | Partial | Yes | High | Atlassian provides an Organizations REST API for user management, but the "Transfer all apps" flow between organizations is a manual, multi-step process requiring org admin access in both source and destination organizations. Orgs with centralized user management must contact Atlassian Support. [14] |
| **Jira Cloud (Atlassian org)** | Partial | Yes | High | Same as Confluence — both products share the Atlassian organization layer. Adding a new org admin via `admin.atlassian.com` is a UI action; the Organizations REST API can enumerate users but not change org-level admin roles directly. [14] |
| **Linear (workspace)** | No | Yes | Medium | The Workspace Owner role is only available on the Enterprise plan. Role changes are made via Settings → Administration → Members in the UI. The Linear GraphQL API does not expose a mutation for changing workspace ownership. [15] |
| **ClickUp (workspace)** | No | Yes | Low | Only the current Workspace Owner can transfer ownership via Settings → Danger Zone → Select new owner. There is no ClickUp API endpoint for this action. [16] |
| **Basecamp (account)** | No | Yes | Low | The current account owner grants co-owner powers via Adminland → Add/remove account owners. If the owner account is inaccessible, Basecamp support can assist with verified proof of organizational authority, but this takes several days. [17] |
| **Airtable (workspace/base)** | Partial | Yes | Low | Enterprise admins can transfer workspace ownership via the Admin Panel UI. Individual base ownership can be transferred by upgrading a collaborator's permission to Owner. Neither action is available via the Airtable REST API. [18] |

---

## 2. Pre-Cutover Snapshot Checklist

Before any ownership mutation is executed, the following artifacts must be captured and stored in a secure, version-controlled location. These snapshots serve as the authoritative baseline for rollback and post-cutover verification.

### GitHub

The following must be exported before any role change: a complete list of organization members and their current roles (obtainable via `GET /orgs/{org}/members`); a list of all teams, their members, and repository permissions; a list of all installed GitHub Apps and OAuth Apps with their permission scopes; the current billing plan, payment method last-four digits, and billing email; and a full repository list with visibility settings. The GitHub CLI command `gh api /orgs/{org}/members --paginate` provides a machine-readable snapshot.

### Cloudflare

Export the full DNS zone file for every domain via Dashboard → DNS → Export. Capture screenshots or API-exported JSON of all Firewall Rules, Page Rules, Workers Routes, SSL/TLS settings, and Rate Limiting rules. Record the current Super Administrator email address and all member email addresses with their roles. Note the billing plan and renewal date for each zone.

### Google Workspace / GCP

Export the full IAM policy for each GCP project using `gcloud projects get-iam-policy {PROJECT_ID} --format=json > iam_snapshot.json`. From the Workspace Admin console, export the user list including admin role assignments. Record all verified domains, the primary domain, and any configured SAML/SSO identity providers. Capture the billing account ID and linked projects.

### Slack

Export the member list via the `users.list` API method, noting the `is_owner` and `is_primary_owner` flags. If on a paid plan, export the full workspace data via Workspace Settings → Import/Export. Record all installed apps, their OAuth scopes, and the user accounts they are authorized under.

### Discord

Export the server template via Server Settings → Server Template. Record the full member list with roles. For each bot application, capture the Application ID, Client ID, and the team it belongs to. Note the current team owner's Discord account.

### Exocortex Platforms (Notion, Coda, Confluence, Linear, Jira, ClickUp, Basecamp, Airtable)

For each platform, export all workspace data using the platform's native export function. Record all workspace members and their permission levels. Capture any active integrations, automation configurations, and API keys or tokens that are scoped to the current owner's account, as these will break upon ownership transfer.

---

## 3. Rollback Design

Rollback feasibility is highest when the legacy owner account remains active and retains at least one elevated role in the platform. The critical constraint for every platform is: **do not remove the legacy owner until the new owner has been independently verified to have full access**.

| Platform | Rollback Prerequisites | Rollback Mechanism | Time Window |
| :--- | :--- | :--- | :--- |
| **GitHub** | Legacy owner account still active and a member of the org. | New owner uses the API or UI to re-grant the legacy account the `admin` role. | Immediate; no propagation delay. |
| **Cloudflare** | Legacy Super Admin account still active. | Legacy Super Admin logs in and reassigns the Super Administrator role to themselves or another account. | Immediate; but DNS propagation for any zone changes may take up to 48 hours. |
| **Google Workspace** | Legacy Super Admin account still active. | New Super Admin uses the Admin console to re-assign the Super Admin role to the legacy account. | Typically minutes; up to 24 hours per Google's documentation. [6] |
| **GCP (IAM)** | Legacy owner account still has the `roles/owner` binding on the project. | Call `projects.setIamPolicy` to restore the original policy from the JSON snapshot. | Immediate via API. |
| **Slack** | Legacy Primary Owner account still active in the workspace. | On Enterprise Grid, call `admin.users.setOwner` to restore. On other plans, the current owner must use the UI. | Immediate. |
| **Discord (server)** | New server owner account is accessible. | New owner uses the UI to transfer ownership back. | Immediate. |
| **Discord (app/bot)** | New team owner account is accessible. | New team owner uses the Developer Portal to transfer ownership back. | Immediate; identity re-verification may be required. |
| **Notion** | New workspace owner account is accessible. | New owner uses Settings → People to restore the legacy account's Workspace Owner role. | Immediate. |
| **Coda** | New workspace admin account is accessible. | New admin uses the Admin Panel to transfer doc ownership back. | Immediate. |
| **Atlassian (Confluence/Jira)** | New org admin account is accessible. The "Transfer all apps" operation is **permanent and cannot be undone**. | If only admin roles were changed (not a full org transfer), the new admin can re-add the legacy account as an org admin. A full org transfer has no rollback path. | Admin role changes: immediate. Org transfer: no rollback. [14] |
| **Linear** | New workspace owner account is accessible. | New owner uses Settings → Administration → Members to restore the legacy account's role. | Immediate. |
| **ClickUp** | New workspace owner account is accessible. | New owner uses Settings → Danger Zone to transfer ownership back. | Immediate. |
| **Basecamp** | New account owner account is accessible. | New owner uses Adminland → Add/remove account owners to restore. | Immediate. |
| **Airtable** | New workspace owner account is accessible. | New owner uses the workspace settings or Enterprise Admin Panel to transfer ownership back. | Immediate. |

**Critical note on Atlassian:** The "Transfer all apps to another organization" flow is explicitly documented as permanent and irreversible. [14] If the migration involves a full Atlassian organization transfer (rather than simply adding a new org admin), there is no rollback path. This must be treated as a one-way gate and should be the last Atlassian action taken, only after all other platforms have been verified.

---

## 4. Order of Operations

The recommended sequence is ordered by blast radius (impact if something goes wrong) and reversibility. Platforms with fully reversible ownership changes and no production traffic dependency are executed first. Platforms that control DNS, email, or identity infrastructure are executed last.

**Phase A — Exocortex and Collaboration Tools (lowest blast radius)**

Execute ownership transfers for Basecamp, ClickUp, Airtable, Coda, and Notion first. These platforms hold content and project data but do not gate authentication or DNS for other services. Failures here are contained and easily reversed.

**Phase B — Issue Tracking and Documentation (Atlassian, Linear)**

Transfer Linear workspace ownership next, followed by adding `syncrescendence@gmail.com` as an Atlassian org admin for Jira and Confluence. **Do not execute the Atlassian "Transfer all apps" flow at this stage.** The goal is to establish dual-admin access, not to complete the irreversible org transfer.

**Phase C — Communication Platforms (Discord, Slack)**

Transfer Discord server ownership and Discord Developer Team ownership. Then transfer Slack workspace ownership. These platforms are production communication surfaces, so transfers should be scheduled during a low-traffic window with the team notified in advance.

**Phase D — Source Control (GitHub)**

Use the GitHub REST API to promote `syncrescendence@gmail.com` to org owner. Verify access. Then manually update billing information. Do not remove the legacy owner until billing is confirmed.

**Phase E — Cloud Identity and Infrastructure (Google Workspace, GCP)**

This is the highest-risk phase because Google Workspace controls the email identity that underpins authentication for many other services (OAuth "Sign in with Google"). Execute in this sub-order:

1. Add `syncrescendence@gmail.com` as a Super Admin in Google Workspace.
2. Verify the new Super Admin can log in and access the Admin console.
3. Use the GCP Resource Manager API to add `syncrescendence@gmail.com` as `roles/owner` on each project.
4. Verify GCP access.
5. Remove the legacy account from the Super Admin role (human action by the new Super Admin).
6. Update GCP billing account ownership.

**Phase F — DNS and Edge (Cloudflare)**

Execute last, as Cloudflare controls DNS for all domains. The Super Administrator change is a manual UI action. After the new Super Admin is confirmed, move each zone to the new account following the nameserver-swap procedure. Maintain the old account in read-only status for at least 7 days (the period before Cloudflare marks a moved zone as "Deleted") to allow for emergency rollback. [3]

**Phase G — Atlassian Full Org Transfer (if required)**

Only after all other platforms are confirmed stable, execute the Atlassian "Transfer all apps" flow if a full org consolidation is required. This is the only irreversible action in the entire migration.

---

## 5. Post-Cutover Verification Tests

Each test below is deterministic: it produces a binary pass/fail result that can be logged as evidence of successful ownership transfer.

### GitHub

Run `gh api /orgs/{org}/memberships/syncrescendence` and assert that the response contains `"role": "admin"` and `"state": "active"`. Run `gh api /orgs/{org}/memberships/{legacy_account}` and assert that the legacy account is either absent or has `"role": "member"`. Attempt to access the organization's Billing settings page while authenticated as `syncrescendence` and confirm the payment method reflects the new owner's card.

### Cloudflare

Log in to the Cloudflare dashboard as `syncrescendence@gmail.com` and confirm the account-level "Super Administrator" badge is present. Run `curl -H "Authorization: Bearer {NEW_TOKEN}" https://api.cloudflare.com/client/v4/user` and assert that `"email"` matches `syncrescendence@gmail.com`. For each zone, run `dig +short {domain} NS` and confirm nameservers resolve to Cloudflare's assigned nameservers for the new account.

### Google Workspace / GCP

Call `GET https://admin.googleapis.com/admin/directory/v1/users/syncrescendence@{domain}` and assert that `isAdmin: true` is present in the response. For each GCP project, call `gcloud projects get-iam-policy {PROJECT_ID} --format=json` and assert that `syncrescendence@gmail.com` appears in the `roles/owner` binding. Confirm that the legacy account is absent from the `roles/owner` binding.

### Slack

Call `GET https://slack.com/api/users.info?user={USER_ID}` for the `syncrescendence` Slack user and assert that `"is_owner": true` is present in the response. Attempt to access Workspace Settings as `syncrescendence` and confirm full administrative access.

### Discord

Log in to Discord as `syncrescendence` and navigate to Server Settings. Confirm the "Transfer Ownership" option is available (only visible to the current server owner). For each bot application, log in to the Discord Developer Portal and confirm `syncrescendence`'s team is listed as the owner.

### Exocortex Platforms

For each platform, log in as `syncrescendence@gmail.com` and navigate to the workspace or account settings. Confirm that the account is listed as Owner or Admin. Attempt to perform an owner-only action (e.g., invite a new member, change a billing setting) and confirm it succeeds without a permission error.

---

## 6. Open Questions

The following items require manual confirmation before a migration runbook can be finalized.

**Slack plan tier.** The `admin.users.setOwner` API is exclusively available on Enterprise Grid. If the Syncrescendence Slack workspace is on a free, Pro, or Business+ plan, the ownership transfer cannot be automated and must be a manual UI action by the current Primary Owner. The current plan must be confirmed before scripting this step.

**Atlassian centralized user management status.** The Atlassian "Transfer all apps" flow is blocked for organizations that have the centralized user management experience enabled. If this is the case, Atlassian Support must be contacted to perform the transfer. The current organization configuration at `admin.atlassian.com` must be checked.

**Cloudflare Registrar domains.** Domains registered through Cloudflare Registrar require a separate inter-account transfer process that involves both the source and destination accounts confirming the transfer. [19] The list of Cloudflare Registrar-registered domains must be identified separately from domains merely using Cloudflare DNS.

**GCP Organization vs. project-level ownership.** The `projects.setIamPolicy` API can transfer project-level ownership, but GCP Organization-level IAM (the `resourcemanager.organizations.setIamPolicy` permission) requires the Organization Administrator role, which is tied to the Google Workspace super admin. Confirm whether there is a GCP Organization node above the projects, as this changes the sequencing dependency between Google Workspace and GCP steps.

**Discord identity verification requirement.** Transferring ownership of a Discord Developer Team now requires Stripe identity verification by the new owner. [10] Confirm that `syncrescendence@gmail.com` has completed or is prepared to complete Stripe identity verification before scheduling the Discord Developer Team transfer.

**Linear plan tier.** The Workspace Owner role in Linear is only available on the Enterprise plan. On Free, Basic, or Business plans, all members are effectively admins and there is no distinct "owner" role to transfer. The current Linear plan must be confirmed to determine whether a formal ownership transfer is even applicable.

**Existing service-account tokens and OAuth grants.** Any integration that uses "Sign in with Google" or a personal access token scoped to the legacy owner's account will break silently after the legacy account loses its elevated roles. A full audit of all OAuth grants and API tokens across all platforms must be completed before cutover to identify integrations that require re-authorization.

**Basecamp organizational entity.** Basecamp's support team can reassign account management if the account is owned by a legal entity and sufficient proof of authority is provided. However, this process "will likely take several days." [17] If the legacy Basecamp account owner is unavailable, this path must be initiated well in advance of the target cutover date.

---

## References

[1] GitHub Docs — Transferring organization ownership: <https://docs.github.com/en/organizations/managing-organization-settings/transferring-organization-ownership>

[2] GitHub Docs — REST API endpoints for organization members: <https://docs.github.com/en/rest/orgs/members?apiVersion=2022-11-28>

[3] Cloudflare Docs — Move a domain between Cloudflare accounts: <https://developers.cloudflare.com/fundamentals/manage-domains/move-domain/>

[4] Cloudflare Docs — Change Super Administrator: <https://developers.cloudflare.com/fundamentals/account/change-super-admin/>

[5] Google Cloud Docs — Manage access to projects, folders, and organizations (IAM API): <https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access>

[6] Google Workspace Admin Help — Make a user an admin: <https://knowledge.workspace.google.com/admin/users/make-a-user-an-admin>

[7] Google Cloud Docs — Method: projects.setIamPolicy (Resource Manager API): <https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/setIamPolicy>

[8] Slack Developer Docs — admin.users.setOwner method: <https://docs.slack.dev/reference/methods/admin.users.setOwner>

[9] Discord Support — How do I transfer server ownership?: <https://support.discord.com/hc/en-us/articles/216273938-How-do-I-transfer-server-ownership>

[10] Discord Developer Support — How to Transfer Ownership of a Developer Team: <https://support-dev.discord.com/hc/en-us/articles/34905402845591-How-to-Transfer-Ownership-of-a-Developer-Team>

[11] Notion Help Center — Manage members & guests: <https://www.notion.com/help/add-members-admins-guests-and-groups>

[12] Coda Help Center — Change ownership of your Coda doc: <https://help.coda.io/hc/en-us/articles/39555803168013-Change-ownership-of-your-Coda-doc>

[13] Coda Help Center — Deactivate Enterprise users and transfer their docs: <https://help.coda.io/hc/en-us/articles/39555998877325-Deactivate-Enterprise-users-and-transfer-their-docs>

[14] Atlassian Support — Transfer all apps to another organization: <https://support.atlassian.com/organization-administration/docs/transfer-products-to-another-organization/>

[15] Linear Docs — Members and roles: <https://linear.app/docs/members-roles>

[16] ClickUp Help — Transfer Workspace ownership: <https://help.clickup.com/hc/en-us/articles/6310482663063-Transfer-Workspace-ownership>

[17] Basecamp Help — Add or Remove Other Owners: <https://3.basecamp-help.com/article/152-add-or-remove-other-owners>

[18] Airtable Support — Transferring Airtable workspace, base, and interface ownership: <https://support.airtable.com/docs/transferring-airtable-workspace-base-and-interface-ownership>

[19] Cloudflare Registrar Docs — Transfer a Cloudflare Registrar domain registration between accounts: <https://developers.cloudflare.com/registrar/account-options/inter-account-transfer/>
