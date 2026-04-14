# LDES Hands-On Implementation guide for EU Corporate Body Vocabulary

A guide to a hands-on implementation of a [Linked Data Event Stream (LDES)](https://w3id.org/ldes/specification) feed for the [EU Corporate Body authority table](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/corporate-body), built as part of the online course **Publishing Data with Linked Data Event Streams: Why and How** on the [Interoperable Europe Academy](https://interoperable-europe.ec.europa.eu/collection/interoperable-europe-academy/solution/publishing-data-linked-data-event-streams-why-and-how).


## What you will build

The goal is to guide you through creating your first LDES.

We will take a static **SKOS vocabulary** — the [EU Corporate Body authority table](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/corporate-body), published by the Publications Office of the European Union, and transform it into a **Linked Data Event Stream**: an immutable, append-only feed that tracks changes over time.

Each corporate body in the vocabulary becomes a tracked member. When the pipeline runs, it compares the current state of the vocabulary against the previous one and generates **ActivityStreams events**:

- `as:Create` — when a new corporate body appears
- `as:Update` — when an existing corporate body is modified
- `as:Delete` — when a corporate body is removed

These events are organized into time-based fragments and published as a collection of static documents. To keep things simple, **we do not use an LDES server** — instead, the feed is served directly via **GitHub Pages**.

Once deployed, the entry point to the LDES will be hosted on your own repository.

## How it works

```
EU Publications Office           RDF-Connect Pipeline             GitHub Pages
┌─────────────────────┐       ┌─────────────────────────┐       ┌────────────────┐
│    SKOS RDF/XML     │──────>│     Fetch > Diff >      │──────>│   Static LDES  │
│    (data dump)      │       │    Events > Fragment    │       │   TriG files   │
└─────────────────────┘       └─────────────────────────┘       └────────────────┘
```

The pipeline performs the following steps:

1. **Fetches** the full SKOS dump from the EU Publications Office
2. **Detects changes** by comparing with previous state stored in LevelDB
3. **Generates events** — `as:Create` for new, `as:Update` for changed, `as:Delete` for removed
4. **Fragments** the events into time-based buckets (max 100 per page) using the TREE specification
5. **Writes** static TriG files to `docs/`, which GitHub Pages serves as your live LDES

On the first run, every entity is new, so the pipeline generates a `Create` event for each one. On subsequent runs, only actual changes produce new events.

_________

## Setup

### Prerequisites

- **Git** and a **GitHub account**
- **Node.js** v22 or higher
- **npm** (comes with Node.js)

### Local development

On Linux:

```bash
cd pipeline
npm install
npx @rdfc/js-runner rdfc-pipeline.ttl
```

On Windows: 

```bash
cd pipeline
npm install
node run.mjs rdfc-pipeline-corporate-body.ttl
```






