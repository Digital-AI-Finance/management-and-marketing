---
layout: default
title: Editorial Board
description: Meet the distinguished scholars guiding Management & Marketing journal
---

<div class="container">

<div class="content-page">

# Editorial Board

Our editorial board comprises distinguished scholars from leading institutions worldwide, bringing diverse expertise in management, marketing, economics, and business studies. Their commitment to academic excellence ensures the highest quality standards for our journal.

</div>

{% if site.data.editors %}

<section class="section">
    <div class="section-header">
        <h2 class="section-title">Editor-in-Chief</h2>
    </div>
    <div class="board-grid">
        {% for editor in site.data.editors %}
            {% if editor.role == "Editor-in-Chief" %}
            <div class="editor-card">
                <span class="editor-role">{{ editor.role }}</span>
                <h3 class="editor-name">{{ editor.name }}</h3>
                <p class="editor-affiliation">{{ editor.affiliation }}</p>
                <p class="editor-country">{{ editor.country }}</p>
            </div>
            {% endif %}
        {% endfor %}
    </div>
</section>

<section class="section">
    <div class="section-header">
        <h2 class="section-title">Associate Editors</h2>
    </div>
    <div class="board-grid">
        {% for editor in site.data.editors %}
            {% if editor.role == "Associate Editor" %}
            <div class="editor-card">
                <span class="editor-role">{{ editor.role }}</span>
                <h3 class="editor-name">{{ editor.name }}</h3>
                <p class="editor-affiliation">{{ editor.affiliation }}</p>
                <p class="editor-country">{{ editor.country }}</p>
            </div>
            {% endif %}
        {% endfor %}
    </div>
</section>

<section class="section">
    <div class="section-header">
        <h2 class="section-title">Editorial Board Members</h2>
    </div>
    <div class="board-grid">
        {% for editor in site.data.editors %}
            {% if editor.role == "Editorial Board Member" or editor.role == "Board Member" %}
            <div class="editor-card">
                <span class="editor-role">Board Member</span>
                <h3 class="editor-name">{{ editor.name }}</h3>
                <p class="editor-affiliation">{{ editor.affiliation }}</p>
                <p class="editor-country">{{ editor.country }}</p>
            </div>
            {% endif %}
        {% endfor %}
    </div>
</section>

{% else %}

<div class="content-page">

## Editor-in-Chief

**Prof. Dr. [Name]**
Bucharest University of Economic Studies, Romania
*Email: editor@managementmarketing.ro*

## Associate Editors

The editorial team is currently being assembled. Please check back soon for updates.

## Editorial Board Members

We are building a distinguished international editorial board representing leading institutions worldwide.

</div>

{% endif %}

<div class="content-page">

## Roles & Responsibilities

### Editor-in-Chief
- Oversees all journal operations and editorial decisions
- Sets strategic direction for the journal
- Makes final decisions on manuscript acceptance
- Ensures ethical publication practices

### Associate Editors
- Handle manuscript assignments and peer review coordination
- Provide editorial recommendations
- Assist in developing journal policies
- Support special issue development

### Editorial Board Members
- Serve as expert peer reviewers
- Provide guidance on journal scope and direction
- Act as ambassadors for the journal
- Contribute to special issues and editorial initiatives

## Join Our Board

We welcome inquiries from distinguished scholars interested in joining our editorial board. Ideal candidates have:

- Strong publication record in relevant fields
- Experience in peer review and editorial work
- Commitment to advancing open access scholarship
- International research network and visibility

**Contact**: editorial@managementmarketing.ro

---

*Our editorial team is committed to maintaining the highest standards of academic publishing and fostering innovation in business research.*

</div>

</div>
