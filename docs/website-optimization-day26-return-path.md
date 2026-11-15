# Day 26 Return Path Review

- Date: 2026-11-13
- Scope: RSS discovery, update summaries, and subscription-intent paths
- Status: Completed

## What Was Checked

- The production RSS endpoint returned HTTP 200 with XML content.
- The local feed contains 17 items for 17 published guides, with 17 unique GUIDs and 17 distinct descriptions.
- All 17 guide pages expose RSS autodiscovery metadata and a visible `Follow via RSS` link.
- The guides index exposes RSS autodiscovery plus visible RSS and weekly-digest contact paths.
- The weekly-digest path is a user-initiated `mailto:` action. JavaScript records an `Email Contact` event, then leaves the request in the user's mail client.

## Issue Found

The feed items were written in source-file order instead of update order. The newest guide, dated 2026-11-03, appeared in the middle of the feed while an older 2026-08-05 guide appeared first. Some feed readers use the first items to determine what is new, so this could hide a recent update from returning readers.

## Fix

- Sort RSS items by each guide's `lastmod` date in descending order in the guide generator.
- Reorder the current `feed.xml` so the 2026-11-03 Big Agnes comparison is first.
- Add a regression test that requires descending dates and unique GUIDs.

## Permission Boundary

No mailing list was purchased, created, or populated. No visitor was subscribed automatically, and no email delivery result is claimed. The email-digest path remains a manual request that requires the user to send an email and the site owner to operate a consent and unsubscribe process before any recurring mailing.

## Outcome

The site now presents its newest guide first to RSS readers while preserving the existing no-account return path. No new pages, redirects, index controls, affiliate links, messages, or third-party submissions were created.

## Next Step

Day 27 should review whether the site's trust and conversion explanations are still accurate. Current GA4, GSC, and referring-domain exports are still needed for the data-dependent backlog.
