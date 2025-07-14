# Folkets AI - Frontend

## Developing

Installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```
## Translations

The app uses Paraglide from Inlang i18n library.

Translations are defined in "Messages" files `/frontend/messages/{locale}.json` as key-value pairs. 

### Naming conventions for Pragalide messages

#### Naming Pattern
`{route}_{section}_{element}_{property}`

#### Routes
- `settings_*` → /settings
- `chat_*` → /chat
- `some_new_route_*` → /some_new_route

#### Common Prefixes
- `common_*` → Shared across pages
- `nav_*` → Navigation elements