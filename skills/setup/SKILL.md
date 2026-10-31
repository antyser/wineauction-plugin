---
name: setup
description: "Set up WineAuction for this user: ask how they buy wine, their price range and the wines they like, save that as their preference note, and offer a recurring check of their inbox for good merchant deals. Use when the user has just installed WineAuction, asks to set it up, get started or onboard, or asks to save, remember, show, change or clear their wine preferences or taste profile: \"set up WineAuction\", \"remember that I mostly buy Burgundy under $150\", \"what preferences have you saved for me\", \"帮我设置一下\", \"记住我喜欢香槟\". Not for pricing a wine, list or offer; those belong to the other WineAuction skills."
---

# Setup

Ask one question at a time, keep each question to one line, and let the user skip any of them. Write to the user in their language.

## Asking

Use the client's own question tool when it has one: `AskUserQuestion` in Claude Code and Cowork (options plus the automatic "Other" free-text answer), `request_user_input` in Codex. Without one, ask in plain text with numbered options and accept a free answer. Never ask all the questions in one message.

## Steps

0. Call `get_preference` ([fields](../wineauction-reference/references/tools/preference.md)). If a note is saved, show it and ask: keep it, update it, or start over. Keep → go to step 4. Update → ask only what the user wants to change. `AUTH_REQUIRED` → tell the user to sign in to the WineAuction connector (Claude Code: `/mcp`) and stop.
1. How they buy wine (several allowed):
   - Retail: shops and online stores
   - Restaurants
   - Auctions
   - Something else (their words)
2. Price range per bottle (one choice; offer a free-text addition when they buy in more than one way, such as "restaurants up to $200, auctions up to $1,000"):
   - Under $50
   - $50 to $150
   - $150 to $500
   - Over $500
3. Wines they like, in their words: regions, producers, grapes or specific bottles, and anything they avoid. Free text; skippable.
4. Write the note (format below), show it, and ask to save. On yes, call `save_preference` with the whole note. Then say it is saved and that they can view or edit it at https://wineauction.ai/settings. Never call `save_preference` before the user agrees, and never add anything they did not say.
5. Offer the deal watch, below.

## The note

Plain text, at most 5,000 characters, the user's own words kept. One line per topic, in the user's language:

```
Buys wine: retail, auctions
Price range: usually $50–150 a bottle; up to $500 at auction
Likes: white Burgundy (Roulot, Coche-Dury), Champagne; not much New World red
Updated: 2026-10-31 (WineAuction setup)
```

Leave out a line the user skipped. `save_preference` replaces the whole note, so when updating, send the full note with the change applied. An empty string clears it, only when the user asks to clear it.

## Deal watch

Offer this once, after the note. The watch runs in the user's own client: their email stays with their agent and is never sent to WineAuction, except the wine names and prices of each offer for comparison.

1. Check what this client can do: an email connector (Gmail, Outlook or similar) it can search, and a way to schedule a recurring task. If either is missing, say which one in one line and where they might turn it on, and stop here; do not set up a partial watch.
2. Explain in two sentences: on a schedule, search the inbox for new wine merchant emails and newsletters, compare each offered wine with retail and auction prices, and tell them only about clearly good deals.
3. Ask: turn it on? How often (daily or weekly)? What counts as a good deal (default: at least 20% below the retail reference; or below the auction median)?
4. On yes, create the scheduled task with the client's scheduling tool. Its prompt follows the "Inbox deal watch" section of the [merchant-offer-check](../merchant-offer-check/SKILL.md) skill, with the threshold, the frequency and, when saved, the user's price range and likes from the note to rank results.
5. Tell the user the task's name and how to pause or delete it.

When the user declines, or the client cannot do it, leave it; do not ask again in this conversation.

These tools cannot buy, bid or contact a seller. The only thing they write is this preference note.
