# LDES Corporate Body Feed

LDES feed for EU Publications Office Corporate Body Authority Table

This is a proof-of-concept [RDF-Connect](https://rdf-connect.github.io/) pipeline to produce an [LDES (Linked Data Event Stream)](https://semiceu.github.io/LinkedDataEventStreams/) from the EU Publications Office's Corporate Body Authority Table, available at <https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/corporate-body>.

The pipeline is executed periodically to:
1. Fetch the latest version of the Corporate Body SKOS vocabulary (`corporatebodies-skos.rdf`)
2. Detect any changes compared to the previous version
3. Write detected changes to the LDES feed for downstream consumers to ingest

The LDES feed is kept as a collection of static documents which can be served via GitHub Pages or any static hosting platform.

## How it works

The pipeline uses [RDF-Connect](https://rdf-connect.github.io/) processors to:
1. **Fetch** the `corporatebodies-skos.rdf` file from the EU Publications Office
2. **Detect changes** by comparing with previous state stored in LevelDB
3. **Generate ActivityStreams** events (Create, Update, Delete) for changed SKOS concepts
4. **Bucketize** events using time-based fragmentation (monthly buckets)
5. **Write** to disk as static LDES fragments

## Setup

### Prerequisites
- Node.js 22 or higher
- npm

### Local development

cd pipeline
npm install
npx @rdfc/js-runner rdfc-pipeline.ttl

## Architecture

[EU Publications Office - Corporate Body Authority Table]
    (corporatebodies-skos.rdf)
                ↓
       [HttpFetch Processor]
                ↓
      [DumpsToFeed Processor] → [LevelDB State]
                ↓
        [Sdsify Processor]
                ↓
       [Bucketize Processor] → [Feed State JSON]
                ↓
     [LdesDiskWriter Processor]
                ↓
         [docs/ directory] → [Static Hosting / GitLab Pages]

## Data Source

The Corporate Body Authority Table is maintained by the EU Publications Office as part of the EU Vocabularies. It contains standardized identifiers and labels for EU institutions, bodies, agencies, and other organizations.

- **Dataset**: [Corporate Body Authority Table](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/corporate-body)
- **Format**: SKOS (Simple Knowledge Organization System)
- **Source file**: `corporatebodies-skos.rdf`

## Additional Resources

- [RDF-Connect Documentation](https://rdf-connect.github.io/)
- [LDES Specification](https://semiceu.github.io/LinkedDataEventStreams/)
- [EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies)
- [SKOS Reference](https://www.w3.org/TR/skos-reference/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Pages Documentation](https://docs.gitlab.com/ee/user/project/pages/)

## Support

For issues specific to:

- **RDF-Connect pipeline**: Check [RDF-Connect GitHub](https://github.com/rdf-connect)
- **Corporate Body Authority Table data**: Contact [EU Publications Office](https://op.europa.eu/en/web/eu-vocabularies/contact)

## License

MIT
