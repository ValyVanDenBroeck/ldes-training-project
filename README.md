<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README — LDES Training Project</title>
    <style>
        :root {
            --primary: #0366d6;
            --text: #24292e;
            --muted: #586069;
            --bg: #ffffff;
            --code-bg: #f6f8fa;
            --border: #e1e4e8;
            --info-bg: #dbedff;
            --info-border: #0366d6;
            --warn-bg: #fffbdd;
            --warn-border: #e36209;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            max-width: 880px;
            margin: 0 auto;
            padding: 32px 24px;
            line-height: 1.6;
            color: var(--text);
        }
        h1 { font-size: 2em; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 16px; }
        h2 { font-size: 1.5em; margin-top: 40px; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
        h3 { font-size: 1.15em; margin-top: 24px; margin-bottom: 8px; }
        p { margin-bottom: 12px; }
        ul, ol { padding-left: 24px; margin-bottom: 12px; }
        li { margin-bottom: 6px; }
        a { color: var(--primary); text-decoration: none; }
        a:hover { text-decoration: underline; }
        code {
            background: var(--code-bg);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.85em;
        }
        pre {
            background: var(--code-bg);
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.85em;
            line-height: 1.45;
            margin: 12px 0;
            border: 1px solid var(--border);
        }
        pre code { background: none; padding: 0; font-size: 1em; }
        table { width: 100%; border-collapse: collapse; margin: 12px 0; }
        th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
        th { background: var(--code-bg); }
        .note {
            background: var(--info-bg);
            border-left: 4px solid var(--info-border);
            padding: 12px 16px;
            margin: 16px 0;
            border-radius: 0 4px 4px 0;
        }
        .warn {
            background: var(--warn-bg);
            border-left: 4px solid var(--warn-border);
            padding: 12px 16px;
            margin: 16px 0;
            border-radius: 0 4px 4px 0;
        }
        blockquote {
            border-left: 4px solid var(--border);
            padding: 0 16px;
            color: var(--muted);
            margin: 12px 0;
        }
        .badge { background: var(--primary); color: white; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; text-decoration: none; }
    </style>
</head>
<body>

<h1>🔗 LDES Hands-On — EU Corporate Body Vocabulary</h1>

<blockquote>
    <p>A hands-on exercise to build your first <strong>Linked Data Event Stream (LDES)</strong>. You will transform a real EU vocabulary into a live, change-tracking event stream — hosted entirely as static files on GitHub Pages.</p>
</blockquote>

<h2>What you will build</h2>

<p>The goal of this exercise is to guide you through creating your first LDES from scratch.</p>

<p>You will take a static <strong>SKOS vocabulary</strong> — the <a href="https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/corporate-body">EU Corporate Body authority table</a>, published by the Publications Office of the European Union — and transform it into a <strong>Linked Data Event Stream</strong>: an immutable, append-only feed that tracks changes over time.</p>

<p>Each corporate body in the vocabulary becomes a tracked entity. When the pipeline runs, it compares the current state of the vocabulary against the previous one and generates <strong>ActivityStreams events</strong>:</p>

<ul>
    <li><code>as:Create</code> — when a new corporate body appears</li>
    <li><code>as:Update</code> — when an existing corporate body is modified</li>
    <li><code>as:Delete</code> — when a corporate body is removed</li>
</ul>

<p>These events are organized into time-based fragments and published as a collection of static documents. To keep things simple, <strong>we do not use an LDES server</strong> — instead, the feed is served directly via <strong>GitHub Pages</strong>.</p>

<p>Once deployed, the entry point to your LDES will be:</p>
<pre><code>https://&lt;your-github-username&gt;.github.io/&lt;your-repo-name&gt;/</code></pre>

<h2>How it works</h2>

<pre><code>EU Publications Office     RDF-Connect Pipeline        GitHub Pages
┌──────────────────┐     ┌────────────────────┐     ┌──────────────┐
│  SKOS RDF/XML    │────▶│  Fetch → Diff →    │────▶│  Static LDES │
│  (9.6 MB dump)   │     │  Events → Fragment │     │  TriG files  │
└──────────────────┘     └────────────────────┘     └──────────────┘</code></pre>

<p>The pipeline performs the following steps:</p>

<ol>
    <li><strong>Fetches</strong> the full SKOS dump from the EU Publications Office</li>
    <li><strong>Detects changes</strong> by comparing each entity's RDF against a previously stored hash (LevelDB)</li>
    <li><strong>Generates events</strong> — <code>as:Create</code> for new entities, <code>as:Update</code> for modified ones, <code>as:Delete</code> for removed ones</li>
    <li><strong>Fragments</strong> the events into time-based buckets (max 100 per page) using the TREE specification</li>
    <li>
