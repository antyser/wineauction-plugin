---
name: setup
description: "Get a new WineAuction user to a useful answer in the first minute: ask what wine, offer or list they are looking at (or show a live example), answer it with real prices, then offer to remember how they buy wine and their budget. Use when the user has just installed WineAuction, runs setup, asks to set it up, get started or see what it can do, or asks to save, remember, show, change or clear their wine preferences or taste profile: \"set up WineAuction\", \"what can this do?\", \"remember that I mostly buy Burgundy under $150\", \"what preferences have you saved for me\", \"帮我设置一下\", \"记住我喜欢香槟\". Not for pricing a wine, list or offer the user already brought without asking for setup; those belong to the other WineAuction skills."
---

# Setup

Show value first: one question, a real answer, then an offer to remember. Write to the user in their language, keep each question to one line, and let them skip anything.

## Asking

Use the client's own question tool when it has one: `AskUserQuestion` in Claude Code and Cowork (options plus the automatic "Other" free-text answer), `request_user_input` in Codex. Without one, ask in plain text with numbered options and accept a free answer.

## Steps

0. Call `get_preference` ([fields](../wineauction-reference/references/tools/preference.md)) without announcing it. A saved note shapes the example and the suggestions below. `AUTH_REQUIRED` → tell the user to sign in to the WineAuction connector (Claude Code: `/mcp`) and stop.
   - When the user only wants to see, change or clear their saved preferences, skip to [Saved preferences](#saved-preferences).
1. Ask one question: "What wine, offer or list are you looking at? Paste it, attach a photo, or I can show you an example." Options:
   - Show me an example
   - A wine and a price I was quoted
   - A restaurant wine list
   - Bottles I own
2. Answer right away with a tool call; do not ask anything else first. If the user picked a kind of input without giving it (no wine, price, list or photo yet), ask in one line for the paste or photo, then answer.
   - **Example**: call `list_offers` with `offer_type: auction`, `house: klwines`, `status: live`, `max_price_usd: 100`, `min_discount_pct: 20`, `mixed_lot: exclude`, `sort: discount_vs_auction` ([fields](../wineauction-reference/references/tools/list_offers.md)). If the saved note names a colour or region, pass it too. Pick the first lot below both references whose retail rests on at least 2 offers and whose auction median on at least 3 sales; nothing qualifies → the first lot below the auction median. No qualifying K&L lot (an empty result) → take the soonest live auction from `list_auctions` and repeat the call with its `auction_slug` in place of `house`, keeping the other filters; still nothing → say in one line that no example is live right now and go to step 3. Show that one lot: wine and vintage, bottles, price per 750 ml with the buyer's premium, both references with their counts, when it ends, and the `wineapp_url` and seller `url`. Say in one line that the current bid can still rise. Then add one line: "Send me any wine, price or list and I'll check it the same way."
   - **A wine and a price, or a merchant email**: follow [merchant-offer-check](../merchant-offer-check/SKILL.md).
   - **A wine without a price**: follow [wine-info](../wine-info/SKILL.md).
   - **A restaurant list**: follow [restaurant-wine-list](../restaurant-wine-list/SKILL.md).
   - **Bottles they own**: follow [cellar-valuation](../cellar-valuation/SKILL.md).
   - **Auction lots or a sale**: follow [auction-lots](../auction-lots/SKILL.md).
3. Offer to remember, in one line: "Want me to remember how you buy wine and your budget, so answers fit you next time?" Skip this step when the saved note already covers both.
   - On yes, ask both in one go when the question tool takes several questions, else one after the other:
     - How they buy wine (several allowed): retail shops and online, restaurants, auctions, something else.
     - Usual price per bottle: under $50, $50 to $150, $150 to $500, over $500. They may add a split, such as "restaurants up to $200, auctions up to $1,000".
   - Add what the user said in this conversation about wines they like or avoid, in their words. Write the note (format below), show it, and call `save_preference` only after they agree. Then say it is saved and can be edited at https://wineauction.ai/settings.
   - On no or skip, move on without asking again.
4. End with exactly three suggested next questions the user can send as written, fitted to what they asked, the saved note and today's live data, and not repeating the question just answered. Mix the jobs, for example:
   - "Is $120 a fair price for Barolo 2016 at my shop?"
   - "Which bottles on this list are least marked up?" (with a photo of a list)
   - "Show me lots under $100 ending today that sell below retail."
   When the client can search an email inbox and schedule a recurring task, make one of the three "Watch my inbox for good wine deals" (see [Deal watch](#deal-watch)).

## The note

Plain text, at most 5,000 characters, the user's own words kept. One line per topic, in the user's language:

```
Buys wine: retail, auctions
Price range: usually $50–150 a bottle; up to $500 at auction
Likes: white Burgundy (Roulot, Coche-Dury), Champagne; not much New World red
Updated: 2026-10-31 (WineAuction setup)
```

Put today's date on the Updated line, not the example's. Leave out a line the user did not give, and never add anything they did not say. `save_preference` replaces the whole note, so when updating, send the full note with the change applied. An empty string clears it, only when the user asks to clear it.

## Saved preferences

When the user asks to see, change or clear their preferences: show the saved note (or say none is saved), apply the change they ask for, show the result, and save it after they agree.

## Deal watch

Only when the user asks for it. The watch runs in the user's own client: their email stays with their agent and is never sent to WineAuction, except the wine names and prices of each offer for comparison.

1. Check what this client can do: an email connector (Gmail, Outlook or similar) it can search, and a way to schedule a recurring task. If either is missing, say which one in one line and stop; do not set up a partial watch.
2. Explain in two sentences: on a schedule, search the inbox for new wine merchant emails and newsletters, compare each offered wine with retail and auction prices, and report only clearly good deals.
3. Ask how often (daily or weekly) and what counts as a good deal (default: at least 20% below the retail reference; or below the auction median).
4. Create the scheduled task with the client's scheduling tool. Its prompt follows the "Inbox deal watch" section of [merchant-offer-check](../merchant-offer-check/SKILL.md), with the threshold, the frequency and, when saved, the price range and likes from the note to rank results.
5. Tell the user the task's name and how to pause or delete it.

These tools cannot buy, bid or contact a seller. The only thing they write is this preference note.
