# ClickPattern Knowledge Base: agent instructions

Customer help center for ClickPattern, built on [Mintlify](https://mintlify.com). Read `README.md` for structure, writing rules and screenshot rules; they apply to every edit.

- Pages are MDX with `title` and `description` frontmatter. Navigation lives in `docs.json`; add every new page there.
- Use the app's exact UI labels in **bold**.
- Never state plan limits or prices; link to https://www.clickpattern.com/pricing.
- Campaign IDs in examples are plain UUID v4, never `camp_…`.
- Outside backticks, escape `{`, `}` and `<` (`\{`, `\}`, `&lt;`).
- Run `python3 scripts/check_docs.py` before committing.
