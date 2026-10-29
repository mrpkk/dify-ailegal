# AILegal — Dify plugin

Source repository: **https://github.com/mrpkk/dify-ailegal**

Verified legal provisions and citation checks for six jurisdictions: Russia (`ru`), India (`in`),
the United States (`us`), the United Kingdom (`uk`), Canada (`ca`) and Hong Kong (`hk`).

The plugin never invents a provision: when the verified corpus has no norm for the question it
returns an explicit refusal (`refused: true` / `found: false`).

## Setup

1. Install the plugin in Dify (Marketplace or local package `dify-ailegal.difypkg`).
2. Open the provider credentials and set **API base URL** if you do not want the default:
   - default: `https://ailegal.legal`
   - any compatible self-hosted base URL is accepted, but it must be an absolute `http(s)` URL.
3. No API key is required for the free tier. The provider validates connectivity by calling
   `GET {api_base}/api/v2/oracle/stats` (free, no quota consumed).

## Usage

### `legal_breakdown`

Describe a situation and the tool returns the provisions that apply, each with a link to the
official text.

- `text` (required) — the situation, in the user's words;
- `jurisdiction` (required) — `ru`, `in`, `us`, `uk`, `ca`, `hk`;
- `locale` (optional) — `en` or `ru`, answer language.

Example input: `My employer has not paid my salary for two months in India` with `jurisdiction=in`
returns the Code on Wages provision and the `indiacode.gov.in` link.

### `verify_citation`

Checks whether a code/article pair exists in the verified corpus.

- `code` (required), e.g. `Code on Wages`;
- `article` (optional), e.g. `s. 17`;
- `jurisdiction` (optional) — narrows the search.

Returns `found: true/false`, `verified`, and the official `source_url`. A `found: false` answer
means: do not rely on this citation.

## API and credentials

- **Base URL:** `https://ailegal.legal` (configurable via `api_base`).
- **Free tier:** 120 calls/hour, no account, no key.
- **Credential handling:** the plugin stores no credentials. `api_base` is kept by Dify as provider
  configuration. No secret is sent anywhere.
- **Connection requirements:** outbound HTTPS to the configured `api_base` (and only that host).
  Timeouts: 10 s for validation, 60 s for `legal_breakdown`, 30 s for `verify_citation`.

## Privacy

See [PRIVACY.md](PRIVACY.md). In short: the situation text and citation parameters are sent to the
configured API to produce the answer; the plugin itself stores nothing.

## Local validation

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -c "import provider.ailegal, tools.legal_breakdown, tools.verify_citation; print('imports ok')"
```

The packaged archive was rebuilt after these checks. The hosted endpoint was verified separately:
`initialize` returns 200 and `verify_citation` answers `found=true` for `Code on Wages s.17`.

Legal information, not legal advice.
