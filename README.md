# Management & Marketing Journal Website

A static website replicating the [Management & Marketing Springer journal](https://link.springer.com/journal/44491) using Python scraping and GitHub Pages. This project demonstrates a hybrid approach combining Springer's official APIs with web scraping, respecting robots.txt compliance and rate limiting best practices.

## Overview

**Journal**: Management & Marketing
**Publisher**: Springer Nature
**Journal ID**: 44491
**Focus**: Business development, management theory, marketing strategies
**Type**: Open access, peer-reviewed journal

This project creates a complete mirror of the journal website with:
- Automated data collection via Springer APIs and web scraping
- Static site generation with Jekyll
- Responsive design for all devices
- GitHub Pages deployment

## Quick Start

### Prerequisites

- **Python 3.8+** - For the scraper
- **Ruby 2.7+** - For Jekyll local development
- **Git 2.0+** - For version control
- **GitHub CLI (gh 2.0+)** - For repository management (optional but recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/josterri/management-and-marketing.git
cd management-and-marketing

# Install Python dependencies for scraper
cd scraper
pip install -r requirements.txt
cd ..

# Install Ruby dependencies for Jekyll
cd website
bundle install
cd ..
```

### 2. Configure Springer API (Optional but Recommended)

For the best results, register for a free Springer Nature API key:

1. Visit [https://dev.springernature.com/](https://dev.springernature.com/)
2. Create a free account
3. Navigate to **My Applications** → **Create New Application**
4. Select APIs:
   - Springer Metadata API
   - Springer Open Access API
5. Copy your API key
6. Create a `.env` file in the project root:
   ```
   SPRINGER_API_KEY=your_api_key_here
   ```

Without an API key, the scraper will fall back to web scraping, but API access is recommended for reliability and freshness.

### 3. Run the Scraper

```bash
cd scraper
python scraper.py
```

The scraper will:
- Fetch and parse `robots.txt` to ensure compliance
- Query Springer APIs (if API key configured)
- Fall back to web scraping for content not available via API
- Handle HTTP 303 redirects properly
- Save structured data to `data/` directory
- Respect rate limiting (2.5-second delays between requests)

**Output files**:
- `data/journal_info.json` - Journal metadata
- `data/articles.json` - Latest articles
- `data/editorial_board.json` - Editorial board members
- `data/aims_scope.json` - Journal aims and scope
- `data/debug/` - Raw HTML files for debugging

### 4. Run the Website Locally

```bash
cd website
bundle exec jekyll serve
```

Visit [http://localhost:4000/management-and-marketing](http://localhost:4000/management-and-marketing) in your browser.

### 5. Deploy to GitHub Pages

The website automatically deploys when you push to the `main` branch:

```bash
git add .
git commit -m "Update journal content"
git push origin main
```

Your site will be available at `https://<github-username>.github.io/management-and-marketing`

## Project Structure

```
management-and-marketing/
│
├── scraper/                      # Python web scraper
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration settings
│   ├── scraper.py               # Main scraping logic
│   ├── api_client.py            # Springer Nature API client
│   ├── robots_checker.py        # robots.txt compliance checker
│   └── requirements.txt          # Python dependencies
│
├── website/                      # Jekyll static site
│   ├── _config.yml              # Jekyll configuration
│   ├── Gemfile                  # Ruby dependencies
│   ├── _layouts/                # Page templates
│   │   ├── default.html         # Base layout
│   │   └── page.html            # Page layout
│   ├── _includes/               # Reusable components
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── nav.html
│   ├── _data/                   # Data files
│   │   ├── journal.yml          # Journal metadata
│   │   ├── editors.yml          # Editorial board
│   │   └── articles.yml         # Article listings
│   ├── assets/                  # Static assets
│   │   ├── css/
│   │   │   └── main.css         # Stylesheet
│   │   ├── js/                  # JavaScript
│   │   └── images/              # Images
│   ├── index.html               # Homepage
│   ├── aims-and-scope.md        # Journal aims page
│   ├── editorial-board.md       # Editorial board page
│   ├── articles.md              # Articles listing
│   ├── about.md                 # About page
│   └── submit.md                # Submission guidelines
│
├── data/                        # Scraped data (generated)
│   ├── journal_info.json
│   ├── articles.json
│   ├── editorial_board.json
│   ├── aims_scope.json
│   └── debug/                   # Debug HTML files
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Scraper Features

### Hybrid API + Scraping Approach

The scraper intelligently combines:

1. **Springer Nature APIs (Primary)**
   - More reliable and stable
   - Better structured data
   - No rate limiting concerns
   - Requires free API key

2. **Web Scraping (Fallback)**
   - Captures additional content not in APIs
   - Editorial board pages
   - Submission guidelines
   - Journal-specific sections

### Key Features

- **robots.txt Compliance**: Fetches and parses `robots.txt` before any requests
- **Rate Limiting**: 2.5-second delays between requests to be respectful
- **Academic User-Agent**: Identifies as academic research bot with contact info
- **Redirect Handling**: Properly handles HTTP 303 redirects from Springer
- **Error Handling**: Graceful degradation when elements are missing
- **Debug Output**: Saves raw HTML for troubleshooting
- **Structured Data**: JSON output for easy website integration

### Configuration

Edit `scraper/config.py` to customize:

```python
# Rate limiting
REQUEST_DELAY = 2.5  # Seconds between requests

# User-Agent (identifies your bot)
USER_AGENT = "Mozilla/5.0 (compatible; AcademicResearchBot/1.0; ...)"

# CSS Selectors (with fallback chains)
SELECTORS = {
    "journal_title": ["h1.c-article-title", "h1.page-title", ...],
    # ... more selectors
}

# Output directory
OUTPUT_DIR = "data"
```

## Website Features

### Responsive Design

The website is fully responsive and works on:
- Desktop (1920x1080+)
- Tablet (768x1024)
- Mobile (320x568)

### Springer-Inspired Design

Color scheme inspired by Springer:
- Primary: `#0070A8` (Springer blue)
- Secondary: `#333333`
- Background: `#FFFFFF`
- Accent: `#E6F3FF`

### Sections

1. **Homepage**: Journal overview, latest articles, quick links
2. **Aims & Scope**: Complete journal aims and scope statement
3. **Editorial Board**: Editor-in-Chief and board members
4. **Articles**: Browsable article listings with metadata
5. **About**: General information and attribution
6. **Submit**: Article submission guidelines

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Scraper** | Python 3.8+ | Data collection |
| **HTTP** | `requests` | HTTP requests with sessions and redirects |
| **Parsing** | BeautifulSoup 4 | HTML parsing and CSS selectors |
| **APIs** | Springer Nature APIs | Structured metadata access |
| **Configuration** | `python-dotenv` | Environment variable management |
| **Static Site** | Jekyll 4.0+ | Site generation |
| **Theme** | Minima | Base Jekyll theme |
| **Deployment** | GitHub Pages | Free hosting and deployment |
| **Version Control** | Git 2.0+ | Code management |

## Data Sources

### Primary: Springer Nature APIs

- **Metadata API** (`meta/v2/json`): Journal and article metadata
- **Open Access API** (`openaccess/json`): Full-text content for open access articles
- **Integro API** (`integro/v1`): Comprehensive journal information

Endpoints (free with API key):
- `https://api.springernature.com/meta/v2/json?q=journal:44491`
- `https://api.springernature.com/openaccess/json?q=doi:...`

### Fallback: Web Scraping

Scrapes from: `https://link.springer.com/journal/44491`

- Journal title and description
- Editorial board pages
- Aims and scope document
- Article listings and metadata

## API Integration

### Getting Started with Springer APIs

1. **Register** (Free): [dev.springernature.com](https://dev.springernature.com/)
2. **Create Application**: Select "My Applications" → "Create New Application"
3. **Choose APIs**:
   - Springer Metadata API (most important)
   - Springer Open Access API (optional, for full-text)
4. **Get API Key**: Copy from application details
5. **Add to .env**: `SPRINGER_API_KEY=your_key_here`

### API Endpoints

```python
# Journal metadata
GET https://api.springernature.com/meta/v2/json
?q=journal:44491
&api_key=YOUR_KEY

# Articles
GET https://api.springernature.com/meta/v2/json
?q=journalid:44491
&p=1  # Page (1-indexed)
&s=50  # Results per page (max 100)

# Open access content
GET https://api.springernature.com/openaccess/json
?q=doi:10.1007/...
&api_key=YOUR_KEY
```

### Response Format

```json
{
  "records": [
    {
      "title": "Article Title",
      "creators": ["Author 1", "Author 2"],
      "doi": "10.1007/...",
      "publicationDate": "2024-01-15",
      "abstract": "...",
      "url": "https://link.springer.com/article/..."
    }
  ],
  "totalResults": 152,
  "startRecord": 1
}
```

## robots.txt Compliance

The scraper respects Springer's `robots.txt` at `https://link.springer.com/robots.txt`:

- **Allowed paths**: `/journal*`, `/article/`, `/submission-guidelines`, `/about`
- **Blocked user agents**: GPTBot, ChatGPT-User, and other AI bots
- **Academic bots**: Allowed with proper User-Agent identification
- **Crawl delay**: Observed when specified (our default: 2.5 seconds)

The `RobotsChecker` class:
- Fetches `robots.txt` before scraping
- Caches it for 1 hour
- Checks each URL against rules
- Enforces allowed crawl delays

## Local Development

### Running the Full Pipeline

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env to add SPRINGER_API_KEY if available

# 2. Run scraper
cd scraper
python scraper.py
cd ..

# 3. Copy data to Jekyll
cp data/*.json website/_data/

# 4. Build and serve locally
cd website
bundle exec jekyll serve --baseurl="" --port 4000
```

### Troubleshooting

**API key not working?**
```bash
# Check environment
echo $SPRINGER_API_KEY  # Should not be empty

# Test API directly
curl "https://api.springernature.com/meta/v2/json?q=journal:44491&api_key=$SPRINGER_API_KEY"
```

**Jekyll build fails?**
```bash
cd website
bundle install --redownload
bundle exec jekyll build --verbose
```

**Scraper returns no data?**
```bash
# Run with verbose logging
cd scraper
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('scraper.py').read())
"
```

## Deployment

### GitHub Pages Setup

The site automatically deploys when you push to `main`:

```bash
# GitHub automatically builds and deploys
git push origin main

# Check deployment status
gh repo view  # Look for "Pages" section
```

**Site URL**: `https://<your-github-username>.github.io/management-and-marketing`

### Manual Deployment

If using GitHub Actions:

1. Go to repository Settings → Pages
2. Select source branch: `main`
3. Select folder: `website` (if using `docs/` folder)
4. Click "Save"
5. GitHub Pages URL appears in Settings

### Continuous Updates

To keep the site current:

```bash
# Set up cron job (daily updates)
0 0 * * * cd ~/management-and-marketing && python scraper/scraper.py && git add data/ && git commit -m "Daily journal update" && git push
```

Or use GitHub Actions to automate:

```yaml
name: Daily Update
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run scraper
        env:
          SPRINGER_API_KEY: ${{ secrets.SPRINGER_API_KEY }}
        run: |
          cd scraper
          pip install -r requirements.txt
          python scraper.py
      - name: Commit changes
        run: |
          git config --global user.email "action@github.com"
          git config --global user.name "GitHub Action"
          git add data/
          git commit -m "Daily journal update" || true
          git push
```

## Contributing

We welcome contributions! Areas for improvement:

- [ ] Additional journal sections
- [ ] Enhanced styling
- [ ] Search functionality
- [ ] Archive/historical data
- [ ] Export formats (BibTeX, RIS)
- [ ] Statistics and metrics

### Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and test locally
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature/my-feature`
6. Open a Pull Request with description

### Testing Your Changes

```bash
# Test scraper
cd scraper
python -m pytest tests/  # If tests exist

# Test website locally
cd website
bundle exec jekyll serve --baseurl=""

# Check for broken links
# Use Firefox devtools or online tools
```

## Troubleshooting

### Scraper Issues

| Issue | Solution |
|-------|----------|
| `robots.txt` blocking | Check `robots_checker.py` logs; ensure User-Agent is set |
| API returns 401 | Verify `SPRINGER_API_KEY` in `.env` file |
| No data in output | Run scraper with verbose logging: `python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('scraper.py').read())"` |
| Redirect errors | Check internet connection; Springer returns HTTP 303 redirects which are handled |
| Rate limit errors | Increase `REQUEST_DELAY` in `config.py` |

### Website Issues

| Issue | Solution |
|-------|----------|
| Site won't build | Run `bundle install` and `bundle exec jekyll build --verbose` |
| CSS not loading | Check `baseurl` in `_config.yml` matches GitHub Pages path |
| Data not displaying | Verify `_data/` files are valid YAML/JSON |
| 404 on subpages | Check `baseurl` and permalink settings |

## API vs Scraping Comparison

| Aspect | API | Scraping |
|--------|-----|----------|
| **Reliability** | High | Medium (depends on HTML stability) |
| **Rate Limits** | Generous | Must be careful (2-3 sec delays) |
| **Data Freshness** | Real-time | Snapshot from crawl time |
| **Content Coverage** | Articles + metadata | All visible content |
| **Setup Complexity** | Registration required (5 min) | None |
| **Cost** | Free | Free |
| **Best For** | Metadata, articles | Editorial board, guidelines |

**Recommendation**: Register for free API key (5 minutes) for best results. Scraper works without it but with lower reliability.

## Performance

- **Scraper runtime**: ~2-5 minutes (depends on API availability)
- **Data size**: ~1-2 MB JSON files
- **Site build time**: ~5-10 seconds
- **Page load time**: <1 second (static files)
- **API requests**: ~10-20 requests per run

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Attribution & Disclaimer

**Important**: This is an educational and research project.

- **Data Source**: Journal metadata sourced from [Springer Nature](https://www.springernature.com/)
- **Journal Link**: [Management & Marketing - Springer](https://link.springer.com/journal/44491)
- **Design**: Inspired by Springer's journal template; all styling is original
- **Images**: Uses placeholder/generic images (no copyrighted content)
- **Disclaimer**: This is not affiliated with Springer Nature. See [Springer's official page](https://link.springer.com/journal/44491) for authoritative information.

## Citation

If you use this project or its data in your research:

```bibtex
@misc{management-marketing-mirror,
  title={Management \& Marketing Journal Website Mirror},
  author={Osterrieder, Joerg},
  year={2024},
  url={https://github.com/josterri/management-and-marketing},
  note={Educational project replicating Springer journal website}
}
```

## Contact & Support

For issues, questions, or suggestions:

1. **GitHub Issues**: [Create an issue](https://github.com/josterri/management-and-marketing/issues)
2. **Discussions**: [Start a discussion](https://github.com/josterri/management-and-marketing/discussions)
3. **Email**: See contributor profile

## Related Resources

- [Springer Nature APIs](https://dev.springernature.com/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Management & Marketing Journal](https://link.springer.com/journal/44491)

---

**Last Updated**: January 2026
**Project Status**: Active
**Python Version**: 3.8+
**Jekyll Version**: 4.0+
