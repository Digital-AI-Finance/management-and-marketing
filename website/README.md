# Management & Marketing Jekyll Website

A professional, Springer-inspired academic journal website built with Jekyll.

## Structure

```
website/
├── _config.yml              # Jekyll configuration
├── _layouts/                # HTML templates
│   └── default.html         # Base layout template
├── _includes/               # Reusable components
│   ├── header.html          # Site header with branding
│   ├── nav.html             # Navigation menu
│   └── footer.html          # Site footer
├── _data/                   # Data files (JSON/YAML)
│   ├── journal.json         # Journal metadata
│   ├── editors.json         # Editorial board data
│   └── articles.json        # Published articles data
├── assets/
│   └── css/
│       └── main.css         # Springer-inspired styling
├── index.html               # Homepage
├── aims-and-scope.md        # Journal scope page
├── editorial-board.md       # Editorial board page
├── articles.md              # Articles listing page
├── about.md                 # About page
└── Gemfile                  # Ruby dependencies
```

## Design Philosophy

The website features a **Springer-inspired professional academic design** with:

- **Color Palette**:
  - Primary: #0070A8 (Springer blue)
  - Secondary: #333333 (dark gray)
  - Background: #FFFFFF (white)
  - Accent: #E6F3FF (light blue)

- **Typography**: Clean, readable sans-serif fonts optimized for academic content
- **Layout**: Mobile-first responsive design
- **Components**: Article cards, editorial board grid, hero banners

## Local Development

### Prerequisites

- Ruby 2.7+
- Bundler gem

### Installation

```bash
cd website
bundle install
```

### Running Locally

```bash
bundle exec jekyll serve
```

Visit `http://localhost:4000/management-and-marketing/` in your browser.

### Building for Production

```bash
bundle exec jekyll build
```

Output will be in `_site/` directory.

## Data Files

The site dynamically pulls content from `_data/` directory:

### `_data/journal.json`
```json
{
  "title": "Management & Marketing",
  "description": "Journal description...",
  "publisher": "Bucharest University of Economic Studies",
  "issn": "1842-0206"
}
```

### `_data/editors.json`
```json
[
  {
    "name": "Prof. Dr. Name",
    "role": "Editor-in-Chief",
    "affiliation": "University Name",
    "country": "Country",
    "featured": true
  }
]
```

### `_data/articles.json`
```json
[
  {
    "title": "Article Title",
    "authors": "Author 1, Author 2",
    "volume": "18",
    "issue": "1",
    "year": "2023",
    "pages": "1-20",
    "doi": "10.1234/mm.2023.001",
    "type": "Research Article",
    "abstract": "Article abstract...",
    "keywords": ["keyword1", "keyword2"],
    "url": "https://doi.org/..."
  }
]
```

## Customization

### Colors

Edit CSS variables in `assets/css/main.css`:

```css
:root {
    --primary-color: #0070A8;
    --secondary-color: #333333;
    /* ... */
}
```

### Navigation

Edit `_includes/nav.html` to add/remove menu items.

### Content

- Update pages by editing corresponding `.md` files
- Modify layouts in `_layouts/`
- Update components in `_includes/`

## GitHub Pages Deployment

1. Push to GitHub repository
2. Enable GitHub Pages in repository settings
3. Set source to `main` branch, `/website` folder (or configure baseurl)
4. Site will be available at `https://yourusername.github.io/management-and-marketing/`

## Features

- Responsive mobile-first design
- Open Access badge and ISSN display
- Article cards with metadata
- Editorial board grid layout
- Hero sections with call-to-action
- SEO-optimized with jekyll-seo-tag
- RSS feed support with jekyll-feed

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

Design and code: MIT License
Content: CC BY 4.0 (or as specified by journal)

## Credits

Built with Jekyll. Design inspired by Springer Nature academic journals.
