# Presentation and repository discovery

## Technical abstract

Meme Intelligence is an experimental Solana research toolkit by Luca Celebrano (@Lukecele). It combines historical transaction ingestion, heuristic first-buyer attribution, SQLite provenance fields, wallet clustering and scoring modules. Fisher exact and out-of-sample checks support exploratory cohort analysis; they require acquired, reviewed historical data and do not establish trading performance. A separate Next.js dashboard presents exports and market API data, including simulation views. The repository provides a reproducible empty-data diagnostic and makes missing-data states explicit through `DATA_INCOMPLETE`.

## GitHub settings handoff

These are proposed settings, **not applied**. The task runtime rejected the repository API write because it owns remote delivery. No alternative write path was attempted. The existing homepage is empty; no public demo was verified.

| Setting | Proposed value | Action remaining |
| --- | --- | --- |
| About description | Experimental Solana research toolkit for wallet clustering, liquidity analysis and data-driven backtesting. Built by Lukecele. | Replace the current institutional claim through the repository About gear. |
| Topics | `solana`, `on-chain-analytics`, `crypto-research`, `wallet-analysis`, `liquidity`, `python`, `data-science`, `backtesting` | Replace current topics through the About gear. |
| Homepage | Empty | Keep empty until a public homepage or demo is verified. |
| Social preview | [social-card.png](assets/social-card.png) | Repository Settings → General → Social preview → Edit → Upload an image. |

The eight proposed topics describe implemented research areas. They satisfy GitHub's documented maximum of 20 topics, 50 characters per topic and lowercase letters/numbers/hyphens. See [GitHub topic guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).

## Sharing asset

- [PNG](assets/social-card.png): 1280 × 640, opaque dark background for consistent display on light and dark pages.
- [Editable SVG source](assets/social-card.svg): original typography and geometric artwork; no external images or new logo. Colors follow the dashboard's dark background and emerald accents.
- Text: “Explore Solana wallets, liquidity & market data” and “by Lukecele”.
- Render with a system DejaVu Sans font and CairoSVG: `cairosvg docs/assets/social-card.svg -o docs/assets/social-card.png`. Rendering tools are optional documentation tooling, not application dependencies.

A README image does not configure GitHub's social preview. The PNG meets the [documented preview format](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview): under 1 MB, with the recommended 1280 × 640 dimensions.
