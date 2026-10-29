# ClickPattern Knowledge Base

Customer help center for [ClickPattern](https://www.clickpattern.com), built with [Mintlify](https://mintlify.com).
Every page is an MDX file in this repo. Mintlify publishes the site whenever `main` changes.

## Structure

| Folder | Navigation group |
| --- | --- |
| `start-here/` | Guides → Start here |
| `core-concepts/` | Guides → Core concepts |
| `tracking/` | Guides → Tracking (4 sub-groups) |
| `automation/` | Guides → Automation and protection |
| `reports/` | Guides → Reports and analytics |
| `ai/` | Guides → AI assistants |
| `team/` | Guides → Team and account |
| `billing/` | Guides → Plans and billing |
| `integrations/` | Integrations tab |
| `troubleshooting/` | Troubleshooting and reference → Troubleshooting |
| `reference/` | Troubleshooting and reference → Reference |
| `images/` | Screenshots, by area |
| `docs.json` | Site settings and navigation |

`index.mdx` is the home page.

## Editing a page

1. Edit the `.mdx` file (or use the Mintlify web editor, which commits back to this repo).
2. Open a pull request. The **Docs checks** workflow looks for broken links and MDX problems.
3. Merge. Mintlify deploys automatically.

To add a page, create the file and add its path (without `.mdx`) to the right group in `docs.json`.

## Writing rules

- Each page starts with frontmatter: `title` and a one or two sentence `description` (shown under the title).
- Use the app's exact UI labels in **bold**. Menu paths use arrows: **Data Hub → Integrations**.
- Short sentences, active voice, second person.
- Put tokens, parameters and URLs in backticks: `{clickid}`, `cid`, `https://{domain}/postback`.
- Outside backticks, write `\{` and `\}` for braces and `&lt;` for a less-than sign (MDX treats them as code).
- Don't state plan limits or prices. Link to [pricing](https://www.clickpattern.com/pricing).
- End with **FAQ** (optional) and **Related articles** linking other pages.

## Screenshots

- Take them from the demo account with **This year** and **All workspaces** selected, 1440×900 window, visible screen only.
- Blur or pixelate IP addresses, ad account IDs, campaign IDs, pixel IDs and codes.
- Save under `images/<area>/` and embed with:

```mdx
<Frame>
  <img src="/images/<area>/<file>.jpg" alt="What the screenshot shows" />
</Frame>
```

Pages still waiting for a screenshot have an MDX comment: `{/* Screenshot to add: … */}`.

## Preview locally

```bash
npm i -g mint
mint dev                 # http://localhost:3000
mint broken-links
python3 scripts/check_docs.py
```
