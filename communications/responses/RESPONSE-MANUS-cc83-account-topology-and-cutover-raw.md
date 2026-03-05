# Account Topology and Migration Plan

This document outlines the execution-ready account topology and migration plan for the three specified accounts, with the goal of centralizing organization control-plane ownership without operational downtime.

## 1. ACCOUNT_ROLE_TOPOLOGY

The following canonical roles are defined for the specified accounts to ensure a clear separation of duties and enhance security:

| Account | Canonical Role | Responsibilities |
|---|---|---|
| `syncrescendence@gmail.com` | **Control-Plane Owner** | Centralized administration, organization ownership, and primary point of control for all platforms and services. This account will hold the highest level of administrative privileges. |
| `truongphillipthanh@gmail.com` | **Primary User Account** | Day-to-day user account for accessing services and performing routine tasks. This account will have standard user-level permissions. |
| `icloud.truongphillipthanh@gmail.com` | **Legacy/Billing Account** | This account will be used to manage non-transferable paid subscriptions, such as the Google AI Pro student benefits, until they can be migrated or expire. It will also serve as a billing-only account where necessary. |
| `truongphillipthanh@icloud.com` | **Break-Glass Account** | Emergency access account with administrative privileges, to be used only in the event that the Control-Plane Owner account is inaccessible. This account should be secured with the highest level of security measures. |

## 2. TARGET_END_STATE

The following table outlines the explicit final target mapping for each platform family, centralizing ownership under the `syncrescendence@gmail.com` account:

| Platform Family | Target Owner Account | Notes |
|---|---|---|
| GitHub | `syncrescendence@gmail.com` | Organization ownership will be transferred to this account. |
| Slack | `syncrescendence@gmail.com` | Primary Workspace Ownership will be transferred to this account. |
| Discord | `syncrescendence@gmail.com` | Server ownership will be transferred to this account. |
| Cloudflare | `syncrescendence@gmail.com` | Super Administrator privileges will be held by this account. |
| Google Workspace/GCP/YouTube | `syncrescendence@gmail.com` | Centralized ownership of the Google Workspace organization, all GCP projects, and the YouTube Brand Account. |
| Claude/OpenAI/Gemini Model Subscriptions | `syncrescendence@gmail.com` | All new and transferable model subscriptions will be consolidated under this account. The Claude Pro subscription will be moved here. |
| Exocortex SaaS Set | `syncrescendence@gmail.com` | All other SaaS applications and services will be owned and managed by this account. |

## 3. MIGRATION_SEQUENCING

The migration is divided into three phases to ensure a controlled and reversible process, minimizing the risk of operational downtime.

### Phase 1: Preparation and Pre-migration

| Step | Action | Verification | Rollback |
|---|---|---|---|
| 1.1 | **Secure All Accounts:** Ensure multi-factor authentication (MFA) is enabled on all four accounts (`syncrescendence@gmail.com`, `truongphillipthanh@gmail.com`, `icloud.truongphillipthanh@gmail.com`, `truongphillipthanh@icloud.com`). | Confirm MFA status in the security settings of each account provider. | N/A |
| 1.2 | **Invite New Control-Plane Owner:** Invite `syncrescendence@gmail.com` as an administrator or owner to all relevant platforms (GitHub, Slack, Discord, Cloudflare, Google Workspace/GCP). | `syncrescendence@gmail.com` receives and accepts invitations, and appears in the member/admin list of each platform. | Revoke the invitation or remove the member from the platform. |
| 1.3 | **Document Current State:** Take screenshots or export configurations of critical settings (e.g., DNS records in Cloudflare, user roles in Slack, repository permissions in GitHub). | All critical configurations are documented and stored securely. | N/A |

### Phase 2: Ownership Transfer

| Step | Action | Verification | Rollback |
|---|---|---|---|
| 2.1 | **Transfer GitHub Ownership:** From the current owner account, transfer organization ownership to `syncrescendence@gmail.com`. | `syncrescendence@gmail.com` is listed as the sole "Organization owner" in GitHub settings. | The new owner can transfer ownership back to the original owner. |
| 2.2 | **Transfer Slack Primary Ownership:** From the current Primary Owner account, transfer Primary Ownership to `syncrescendence@gmail.com`. | `syncrescendence@gmail.com` is listed as the "Primary Owner" in Slack's "About this Workspace" section. | The new Primary Owner can transfer ownership back. |
| 2.3 | **Transfer Discord Server Ownership:** From the current server owner account, transfer server ownership to `syncrescendence@gmail.com`. | `syncrescendence@gmail.com` has the crown icon next to their name in the server's member list. | The new owner can transfer ownership back. |
| 2.4 | **Promote Cloudflare Super Administrator:** Log in as the current Super Administrator and grant `syncrescendence@gmail.com` the Super Administrator role. | `syncrescendence@gmail.com` can access all Cloudflare settings and manage other users. | The original Super Administrator can revoke the new one's privileges. |
| 2.5 | **Transfer Google Workspace/GCP/YouTube Ownership:** Transfer primary ownership of the Google Workspace organization, promote `syncrescendence@gmail.com` to owner on all GCP projects, and make it the Primary Owner of the YouTube Brand Account. | `syncrescendence@gmail.com` is listed as the primary administrator/owner in the respective consoles. | The new owner can transfer ownership back. |

### Phase 3: Post-migration and Cleanup

| Step | Action | Verification | Rollback |
|---|---|---|---|
| 3.1 | **Demote Old Accounts:** Downgrade the roles of `truongphillipthanh@gmail.com`, `icloud.truongphillipthanh@gmail.com`, and `truongphillipthanh@icloud.com` on all platforms to standard user, billing, or member roles as defined in the topology. The `truongphillipthanh@icloud.com` account should retain administrative access only where necessary for its break-glass function. | The old accounts have reduced permissions, and can no longer perform administrative actions (except for the break-glass account). | The Control-Plane Owner can re-promote the old accounts if needed. |
| 3.2 | **Update Billing Information:** Where possible, update billing profiles to be owned by `syncrescendence@gmail.com` or a dedicated billing administrator. | New invoices and billing communications are sent to the updated contact. | Revert billing information to the previous state. |
| 3.3 | **Final Verification:** Perform a full audit of all platforms to confirm that the new ownership structure is correctly implemented and that all services are fully operational. | All services are accessible and functioning as expected under the new ownership structure. | Execute rollback procedures from Phase 2 in reverse order. |

## 4. PAID_SUBSCRIPTION_STRATEGY

This strategy aims to preserve paid benefits while centralizing operational control.

| Subscription | Current Account | Strategy | Justification |
|---|---|---|---|
| **Google AI Pro** | `icloud.truongphillipthanh@gmail.com` | **Do Not Transfer.** Continue to use the benefits tied to this account until the subscription expires. All new Google-related subscriptions should be purchased with the `syncrescendence@gmail.com` account. | Google subscriptions are generally non-transferable. Attempting to move them risks losing the student benefits. |
| **Claude Pro** | `truongphillipthanh@icloud.com` | **Cancel and Re-subscribe.** Cancel the current subscription. Export all necessary chat history and data. Re-subscribe to Claude Pro using the `syncrescendence@gmail.com` account. | Anthropic does not currently support changing the email address associated with an account. This is the only viable method to align ownership with the new control plane. |

## 5. RISK_REGISTER

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy |
|---|---|---|---|---|
| R-01 | **Service Interruption:** Critical services become unavailable during the ownership transfer process. | Low | High | The phased migration approach with verification at each step is designed to minimize this. Perform migrations during low-traffic periods. |
| R-02 | **Loss of Access:** The new Control-Plane Owner account is locked out, or all administrative access is lost. | Low | Critical | The `truongphillipthanh@icloud.com` account is designated as a "break-glass" administrator. All accounts must have MFA and recovery methods properly configured. |
| R-03 | **Data Loss:** Loss of chat history or other data during the Claude Pro migration. | Medium | Medium | Export all important data from the existing Claude Pro account before canceling the subscription. |
| R-04 | **Incomplete Migration:** Some assets or permissions are not correctly transferred, leading to a fragmented control plane. | Medium | Medium | Conduct a thorough audit in the post-migration phase (Step 3.3) to ensure all resources are accounted for and correctly permissioned. |
| R-05 | **Loss of Paid Benefits:** The Google AI Pro student benefits are inadvertently lost. | Low | Medium | The subscription strategy explicitly avoids transferring the Google AI Pro subscription, leaving it on the existing account to preserve the benefits. |

## 6. OPERATOR_CHECKLIST

This checklist provides a concise sequence of actions for the human operator executing the migration.

**Phase 1: Preparation**
- [ ] Confirm MFA is active on all four Google/iCloud accounts.
- [ ] Invite `syncrescendence@gmail.com` as an administrator/owner to GitHub, Slack, Discord, Cloudflare, and Google Workspace.
- [ ] Verify `syncrescendence@gmail.com` has accepted all invitations.
- [ ] Backup/document critical settings for all platforms.

**Phase 2: Ownership Transfer**
- [ ] Transfer GitHub organization ownership to `syncrescendence@gmail.com`.
- [ ] Transfer Slack Primary Ownership to `syncrescendence@gmail.com`.
- [ ] Transfer Discord server ownership to `syncrescendence@gmail.com`.
- [ ] Grant `syncrescendence@gmail.com` the Super Administrator role in Cloudflare.
- [ ] Transfer Google Workspace, GCP, and YouTube primary ownership to `syncrescendence@gmail.com`.
- [ ] Verify `syncrescendence@gmail.com` is the new owner on all platforms.

**Phase 3: Subscriptions & Cleanup**
- [ ] Export data from the Claude Pro account on `truongphillipthanh@icloud.com`.
- [ ] Cancel the Claude Pro subscription on `truongphillipthanh@icloud.com`.
- [ ] Subscribe to Claude Pro using `syncrescendence@gmail.com`.
- [ ] Downgrade the roles of the three old accounts on all platforms per the defined topology.
- [ ] Update billing information where applicable.
- [ ] Perform a final audit to confirm all services are operational and correctly configured.
