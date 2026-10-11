FILES: index.html, editorials.html, games.html, connect.html, styles.css, app.js, states.js, map.js, logo.png, data/, scripts/, .github/
EDIT NAME/EMAIL/INSTAGRAM/SHEET: top of app.js.
STATE PANELS (years in power + points): states.js. These are editorial readings; verify each before publishing.
MAP: indiamap.js holds state outlines traced from the wall-poster image you supplied (low resolution, so shapes are approximate). map.js colours them by party using the data in app.js. Delhi, Goa, Puducherry, Andaman and Lakshadweep are dots. Make sure you have the right to use the poster's outline, and for a final version consider a high-resolution official Survey of India map.
DAILY UPDATE: needs a GitHub repo connected to Netlify and a repository secret ANTHROPIC_API_KEY. scripts/update.py + .github/workflows/daily.yml
 write 10 headlines and 4 editorials each morning (06:00 IST). AUTO_PUBLISH "false" saves a draft in data/editorial.draft.json instead.
