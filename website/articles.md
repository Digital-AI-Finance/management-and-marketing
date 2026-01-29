---
layout: default
title: All Articles
description: Browse all published research articles in Management & Marketing
---

<div class="container">

<div class="content-page">

# All Articles

Explore our complete collection of peer-reviewed research articles. All articles are published under open access and are freely available for reading, downloading, and sharing.

</div>

{% if site.data.articles %}

<section class="section">
    <div class="section-header">
        <h2 class="section-title">Published Articles ({{ site.data.articles | size }})</h2>
        <p class="section-description">Browse by volume, year, or topic</p>
    </div>

    <div class="articles-grid">
        {% for article in site.data.articles %}
        <article class="article-card">
            <span class="article-type">{{ article.type | default: "Research Article" }}</span>
            <h3 class="article-title">
                <a href="{{ article.url | default: '#' }}">{{ article.title }}</a>
            </h3>
            <p class="article-authors">{{ article.authors }}</p>
            <p class="article-meta">
                {% if article.volume %}Vol. {{ article.volume }}, {% endif %}
                {% if article.issue %}No. {{ article.issue }}, {% endif %}
                {{ article.year }}
                {% if article.pages %} | Pages {{ article.pages }}{% endif %}
                {% if article.doi %} | DOI: {{ article.doi }}{% endif %}
            </p>
            {% if article.abstract %}
            <p class="article-abstract">
                {{ article.abstract | truncate: 200 }}
            </p>
            {% endif %}
            {% if article.keywords %}
            <p class="article-meta">
                <strong>Keywords:</strong> {{ article.keywords | join: ", " }}
            </p>
            {% endif %}
            <a href="{{ article.url | default: '#' }}" class="article-link">Read Full Article</a>
        </article>
        {% endfor %}
    </div>
</section>

<!-- Volume & Issue Navigation -->
{% assign volumes = site.data.articles | map: "volume" | uniq | sort | reverse %}
{% if volumes.size > 0 %}
<section class="section">
    <div class="section-header">
        <h2 class="section-title">Browse by Volume</h2>
    </div>

    <div class="quick-links">
        {% for volume in volumes %}
        <a href="#volume-{{ volume }}" class="quick-link-card">
            <h3>Volume {{ volume }}</h3>
            <p>{{ site.data.articles | where: "volume", volume | size }} articles</p>
        </a>
        {% endfor %}
    </div>
</section>
{% endif %}

{% else %}

<div class="content-page">

## No Articles Available

Articles will be displayed here as they are published. Check back soon for our latest research.

### Recent Submissions

We are currently processing submissions for our upcoming issues. If you would like to submit your research, please visit our [Author Guidelines](#) page.

### Subscribe for Updates

Stay informed about new publications by subscribing to our journal alerts:

- Email notifications for new issues
- RSS feed for latest articles
- Social media updates

**Contact**: editorial@managementmarketing.ro

</div>

{% endif %}

<div class="content-page">

## Article Types

We publish several types of scholarly contributions:

### Research Articles
Full-length original research papers presenting novel findings and significant contributions to the field.

### Review Articles
Comprehensive syntheses of research on specific topics, including systematic reviews and meta-analyses.

### Case Studies
In-depth analyses of real-world business cases providing practical insights and theoretical contributions.

### Short Communications
Brief reports of preliminary findings or innovative methodologies.

### Special Issues
Thematically focused collections addressing emerging topics and contemporary challenges.

## Search & Filtering

*Advanced search functionality coming soon*

Browse articles by:
- Topic and keywords
- Author name
- Publication date
- Article type
- Volume and issue

## Citation Information

All articles include full citation metadata and are assigned DOIs for permanent identification. We support major citation formats including APA, MLA, Chicago, and Harvard.

## Open Access

All articles are published under **Creative Commons Attribution 4.0 International License (CC BY 4.0)**, meaning you are free to:

- **Share**: Copy and redistribute the material in any medium or format
- **Adapt**: Remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made

---

*For questions about specific articles, please contact the corresponding author listed in the article.*

</div>

</div>
