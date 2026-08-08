# Checkpoint — ChatGPT Desktop / Codex Auth Split

Date: 2026-08-07

## What happened

The new combined ChatGPT desktop app suddenly lost the normal Chat surface after the app was quit and reopened. The top-left UI changed from the normal ChatGPT experience with Chat / Work plus Codex to an API-authenticated state showing only Work / Codex. The account area also stopped showing the normal ChatGPT account identity and instead showed "Logged in with API key."

## What we verified

- ChatGPT Classic still provides the normal conversational interface.
- The new combined desktop app normally supports Chat + Work + Codex when signed in with the user's regular ChatGPT account.
- The desktop app also supports an alternate API-key login path.
- Codex CLI in VS Code reported: `Logged in using an API key`.
- Codex CLI in macOS Terminal reported the same API-key login and the same project-key suffix.
- After logging the desktop app out of API-key mode and back in using normal ChatGPT user credentials, the old/full app layout immediately returned, including Chat / Work and normal account identity.
- After that desktop login, `codex login status` in Terminal changed from API-key auth to `Logged in using ChatGPT`.

## Conclusion

The desktop app and the default Codex CLI installation are sharing persisted auth state. Switching the default Codex auth to API-key mode can cause the combined desktop app to relaunch in API-key identity mode, which changes the visible feature set and removes the normal Chat surface. Logging the desktop app back into ChatGPT also flips the default CLI auth back to ChatGPT.

This was reproducible enough to treat the auth-state switch as the practical cause of the disappearing Chat UI, even though OpenAI's documentation does not clearly describe the missing-Chat behavior as intentional.

## Current state

- ChatGPT desktop app: signed in with normal ChatGPT user credentials.
- Normal Chat / Work layout: restored.
- Default `codex login status`: now reports ChatGPT login.
- VS Code: close it for now rather than keep multiple Codex clients fighting over one shared auth store.
- Terminal will be the first place to isolate API-key Codex usage.

## Intended next setup

Keep the default Codex home for the desktop app / ChatGPT account:

```text
~/.codex
  auth = ChatGPT
```

Create a separate Codex home for Terminal API-key usage:

```text
~/.codex-api
  auth = API key
```

The proposed Terminal pattern is:

```bash
CODEX_HOME="$HOME/.codex-api" codex
```

and the API-key login would be performed only inside that alternate `CODEX_HOME`, not against the default profile.

## Important rule

Do NOT run a normal/default `codex login --with-api-key` again while the desktop app is using the default `~/.codex` auth store. That would risk flipping the desktop app back into API-key mode and losing the normal Chat interface again.

## Next move

Set up the isolated Terminal `CODEX_HOME` one step at a time and verify both auth states can coexist:

1. default `codex login status` should remain ChatGPT;
2. alternate `CODEX_HOME="$HOME/.codex-api" codex login status` should eventually report API key;
3. confirm the desktop app keeps Chat / Work after the alternate Terminal auth is established;
4. only after that, research how much effort it will take to make VS Code use the isolated API-key profile without disturbing the desktop app.

## Research already done

Current OpenAI docs and recent user / GitHub reports were checked. They support the existence of separate ChatGPT and API-key auth modes, shared/persisted Codex auth behavior, and using separate `CODEX_HOME` roots as the practical way to isolate auth/config state. VS Code isolation is not yet verified and should be treated as a separate follow-up task.
