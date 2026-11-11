---
name: wine-preferences
description: "Remember how the user buys wine, their usual budget and the wines they like or avoid, so other answers fit them, and let them show, change or clear that saved note. Use when the user asks to save, remember, show, change, update or forget their wine preferences, buying habits, budget or taste: \"remember that I mostly buy Burgundy under $150\", \"what preferences have you saved for me\", \"forget my budget\", \"I don't like oaky Chardonnay, remember that\", \"记住我喜欢香槟\". Not for pricing a wine, list or offer; those belong to the other WineAuction skills."
---

# Wine preferences

Keep one short note about how the user buys wine, their usual budget and the wines they like or avoid. Write to the user in their language and keep each question to one line.

## Steps

1. Call `get_preference` ([fields](../wineauction-reference/references/tools/preference.md)) without announcing it. `AUTH_REQUIRED` → tell the user to sign in to the WineAuction connector in their client's connector settings and stop.
2. Work out what the user wants:
   - **Show**: show the saved note, or say none is saved.
   - **Save or change**: apply what the user said to the saved note.
   - **Clear**: only when the user asks to forget or clear everything.
   - **Remove one thing** (for example "forget my budget"): drop that line and keep the rest.
3. When the user asks to save but gave little, ask in one go, letting them skip any:
   - How they buy wine (several allowed): retail shops and online, restaurants, auctions, something else.
   - Usual price per bottle: under $50, $50 to $150, $150 to $500, over $500. They may add a split, such as "restaurants up to $200, auctions up to $1,000".
   - Wines they like or avoid, in their words.
4. Write the note (format below) and show it. Call `save_preference` only after the user agrees to that exact text. Then say it is saved and can be edited at https://wineauction.ai/settings.
5. On a clear, call `save_preference` with an empty string after the user confirms, then say the note is cleared.

Use the saved note afterwards to fit answers, such as the price range and the wines the user likes, without repeating it back.

## The note

Plain text, at most 5,000 characters, the user's own words kept. One line per topic, in the user's language:

```
Buys wine: retail, auctions
Price range: usually $50–150 a bottle; up to $500 at auction
Likes: white Burgundy (Roulot, Coche-Dury), Champagne; not much New World red
Updated: 2026-10-31 (WineAuction)
```

Put today's date on the Updated line, not the example's. Leave out a line the user did not give, and never add anything they did not say. `save_preference` replaces the whole note, so when updating, send the full note with the change applied. An empty string clears it, only when the user asks to clear it.

These tools cannot buy, bid or contact a seller. The only thing they write is this preference note.
