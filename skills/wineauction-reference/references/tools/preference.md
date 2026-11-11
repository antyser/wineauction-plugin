# get_preference and save_preference

The signed-in user's wine preference note: one block of plain text about how they buy wine, their price range and the wines they like. The user can view and edit the same note at https://wineauction.ai/settings.

## get_preference

No inputs. Returns `{preference, updated_at}`: the note as text and its last change as an ISO 8601 time, both `null` when nothing is saved.

## save_preference

| Input | Type | Notes |
| --- | --- | --- |
| `preference` | string, required | The whole note, at most 5,000 characters (an emoji counts as 2). Replaces the saved note; an empty string clears it. |

Returns the saved `{preference, updated_at}`, with leading and trailing spaces trimmed; after a clear both are `null`. Show the user the returned text. Call only after the user agrees to the exact text.

Both tools need a signed-in account; without one they return `AUTH_REQUIRED`. A note over the limit returns `invalid_input`. `PREFERENCE_UNAVAILABLE` means the store failed: try once more, then tell the user it could not be saved and that they can paste the note at https://wineauction.ai/settings.
