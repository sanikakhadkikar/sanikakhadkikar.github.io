# sanikakhadkikar.github.io

Personal website of Sanika Khadkikar, built with [Hugo Blox](https://hugoblox.com/) and deployed to GitHub Pages on every push to `main`. Publications are pulled from NASA ADS automatically by a daily GitHub Action.

Content lives in `content/` (news in `post/`, Food for Thought in `notes/`, the "It's Not Cringe to Be Nerdy" blog in `not-cringe/`), and custom layouts in `layouts/`. To write a new blog piece, copy an existing folder in `content/not-cringe/`, set `genre:` (op-ed, explainer, ...) and start with `draft: true`.

To preview locally, install Hugo extended 0.126.3 and Go, then run `hugo server -D` and open http://localhost:1313.
