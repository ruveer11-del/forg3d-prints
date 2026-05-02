# Forg3d Prints

Amazon-inspired e-commerce storefront for Netlify using Next.js, Tailwind CSS, local product images, favorites, cart persistence, and a secure Netlify Function checkout email flow.

## Run locally

1. Install dependencies:
   `npm install`
2. Copy `.env.example` to `.env.local`
3. Add your secrets:
   - `EMAIL_API_KEY`
   - `EMAIL_FROM`
   - `ADMIN_EMAILS`
   - optional `API_KEY`
4. Start the app:
   `npm run dev`

## Deploy to Netlify

1. Push the project to GitHub.
2. Create a Netlify site from the repo.
3. Set environment variables in Netlify:
   - `EMAIL_API_KEY`
   - `EMAIL_FROM`
   - `ADMIN_EMAILS`
   - optional `API_KEY`
4. Netlify will use `npm run build` and the Next.js plugin from `netlify.toml`.
5. Orders submit through `/.netlify/functions/submit-order`.

## API key security

- Keep private keys only in `.env.local` locally and Netlify environment variables in production.
- Do not place secret keys in React components, `public` files, or client-side fetch responses.
- Access backend-only secrets from Netlify Functions with `process.env.API_KEY` or `process.env.EMAIL_API_KEY`.
- The Firebase web config you shared earlier is a public client config, but any real server secret must stay in Netlify Functions only.

## Email behavior

- Email sends only after successful checkout.
- One order creates one email.
- Multiple admin emails are handled as one recipient list from `netlify/functions/config.js`.
- Honeypot validation, blocked-term checks, and in-memory rate limiting are included to reduce spam.
