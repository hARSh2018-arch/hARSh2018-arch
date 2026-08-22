# Setup Guide — Sun Breathing GitHub Profile

Everything you need is in this folder:

```
README.md
assets/hero-banner.svg
.github/workflows/snake.yml
.github/workflows/pacman.yml
```

## Step 1 — Create (or open) your profile repo

GitHub profile READMEs come from a special repo: one named **exactly** the same
as your username.

- Go to github.com/new
- Repository name: `hARSh2018-arch`
- Public
- Create it (skip this if it already exists)

## Step 2 — Upload the files

Keep the exact folder structure below when you upload — the README depends
on the `assets/` path and the workflow filenames.

```
hARSh2018-arch/
├── README.md
├── assets/
│   └── hero-banner.svg
└── .github/
    └── workflows/
        ├── snake.yml
        └── pacman.yml
```

Easiest way: on the repo page, click **Add file → Upload files**, drag in
`README.md` and the `assets` folder, commit. Then repeat for `.github/workflows`
(GitHub will let you create the nested folders as you drag files in).

## Step 3 — Give Actions write permission

The snake and pacman workflows need to push a generated SVG back into your repo.

1. Go to **Settings → Actions → General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Save

## Step 4 — Run both workflows once manually

1. Go to the **Actions** tab
2. Click **generate snake animation** in the left sidebar → **Run workflow** → **Run workflow**
3. Click **generate pacman contribution graph** → **Run workflow** → **Run workflow**
4. Wait ~1–2 minutes for each to finish (green check)

Each workflow pushes its SVG to a new branch called `output` — that's what the
README's `<img>` tags point at. After this first manual run, both are scheduled
to auto-refresh once a day, so your graphs stay current without you touching
anything.

## Step 5 — Fill in your real links

Open `README.md` and replace the three `#` placeholders near the bottom:

```md
[![Portfolio](...)](#)   → your portfolio URL
[![LinkedIn](...)](#)    → your LinkedIn URL
[![Mail](...)](#)        → mailto:you@email.com
```

## Step 6 — Check it renders

Visit `github.com/hARSh2018-arch` — the README should now show:

- the animated flame banner (embers, flickering flame shapes, glowing title)
- your stats, streak, top languages, and trophy row
- the live activity graph
- the flame-colored snake and Pac-Man contribution animations
- the honors table (edit this directly in `README.md` as you add real achievements)

## Troubleshooting

**Banner doesn't show** — double check the file is at exactly
`assets/hero-banner.svg` (case-sensitive) in the `main` branch.

**Snake/Pac-Man image is broken** — the `output` branch only exists after
the workflow runs successfully at least once. Check the Actions tab for
red X's and open the log to see the error.

**Workflow fails with a permissions error** — you skipped Step 3. Go back
and confirm "Read and write permissions" is selected and saved.

**Want different flame colors** — edit the hex codes directly in
`snake.yml` (`color_snake`, `color_dots`) and in the badge URLs throughout
`README.md` (all built around `#1A0500`, `#D62828`, `#F77F00`, `#FCA311`).
