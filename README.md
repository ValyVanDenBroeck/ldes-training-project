Linked Data Event StreamsA hands-on implementation guide for the EU Corporate Body VocabularyA guide to a hands-on implementation of a Linked Data Event Stream (LDES) feed for the EU Corporate Body authority table, built as part of the online course Publishing Data with Linked Data Event Streams: Why and How on the Interoperable Europe Academy.What we will buildWe will take a static SKOS vocabulary the EU Corporate Body authority table, published by the Publications Office of the European Union, and transform it into a Linked Data Event Stream.Each corporate body in the vocabulary becomes a tracked member. When the pipeline runs (periodically), it compares the current state of the vocabulary against the previous one and generates ActivityStreams events:
as:Create : when a new corporate body appears
as:Update : when an existing corporate body is modified
as:Delete : when a corporate body is removed
These events are organized into time-based fragments and published as a collection of static documents. To keep things simple, we do not use an LDES server. Instead, the feed is served directly via GitHub Pages.Once deployed, the entry point to the LDES will be hosted on your own repository.How it worksEU Publications Office           RDF-Connect Pipeline             GitHub Pages
┌─────────────────────┐       ┌─────────────────────────┐       ┌────────────────┐
│    SKOS RDF/XML     │──────>│     Fetch > Diff >      │──────>│   Static LDES  │
│    (data dump)      │       │    Events > Fragment     │       │   TriG files   │
└─────────────────────┘       └─────────────────────────┘       └────────────────┘
The pipeline performs the following steps:
Fetches the full SKOS dump from the EU Publications Office
Detects changes by comparing with previous state stored in LevelDB
Generates events: as:Create for new, as:Update for changed, as:Delete for removed
Fragments the events into time-based buckets (max 100 per page) using the TREE specification
Writes static TriG files to docs/, which GitHub Pages serves as your live LDES
On the first run, every entity is new, so the pipeline generates a Create event for each one. On subsequent runs, only actual changes produce new events.Implementation GuidePrerequisites
Git and a GitHub account
Node.js v22 or higher
npm (comes with Node.js)
Setup the environment1. Create a new GitHub repository (e.g. ldes-my-first-feed), clone it locally and create the repository structure.git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
mkdir -p pipeline docs
2. Set up the pipeline and install the required dependenciesCreate pipeline/package.json:{
    "name": "ldes-training",
    "version": "1.0.0",
    "description": "LDES for EU Corporate Body Vocabulary",
    "type": "module",
    "author": "<AUTHOR NAME>",
    "contributors": ["<CONTRIBUTOR NAME>"],
    "license": "MIT",
    "dependencies": {
      "@rdfc/js-runner": "^1.0.0",
      "@rdfc/dumps-to-feed-processor-ts": "^1.2.0",
      "@rdfc/http-utils-processor-ts": "^0.1.2",
      "@rdfc/file-utils-processors-ts": "^0.6.0",
      "@rdfc/sds-processors-ts": "^1.4.2"
    }
}
Then install the dependencies:cd pipeline
npm install
3. Create the pipeline configuration filesFilePurposerdfc-pipeline-corporate-body.ttlPipeline definition: fetching, diffing, fragmenting, writingshape.ttlSHACL shape targeting skos:Concept, it tells the pipeline which entities to trackfocusNodes.sparqlSPARQL query selecting all skos:Concept entities from the dumpmetadata.ttlStream metadata (title, publisher, timestamp path) for LDES clientsrun.mjsWindows workaround, patches backslash paths. Not needed on Linux/macOSpipeline/shape.ttl — defines which entities to track:@prefix sh:   <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<#ActivityShape> a sh:NodeShape ;
    rdfs:comment "Shape targeting SKOS Concepts in the Corporate Body vocabulary" ;
    sh:targetClass skos:Concept .
pipeline/focusNodes.sparql — tells the pipeline how to find entities in the dump:PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?entity
WHERE {
    ?entity a skos:Concept .
}
pipeline/metadata.ttl — describes the LDES stream (replace <your-username> and <your-repo>):@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix p-plan: <http://purl.org/net/p-plan#> .
@prefix sds:    <https://w3id.org/sds#> .
@prefix dcat:   <https://www.w3.org/ns/dcat#> .
@prefix ldes:   <https://w3id.org/ldes#> .
@prefix as:     <https://www.w3.org/ns/activitystreams#> .

<https://<your-username>.github.io/<your-repo>/corporate-body/CorporateBodyStream>
    a                     sds:Stream ;
    p-plan:wasGeneratedBy [ a            p-plan:Activity ;
                            rdfs:comment "Pipeline to publish EU Corporate Body vocabulary as LDES" ] ;
    sds:carries           [ a sds:Member ] ;
    sds:shape             <https://<your-username>.github.io/<your-repo>/shape.ttl#ActivityShape> ;
    sds:dataset           [ a                  dcat:Dataset ;
                            dcat:title         "EU Corporate Body Vocabulary LDES Feed"@en ;
                            dcat:publisher     <http://publications.europa.eu/resource/authority/corporate-body> ;
                            ldes:timestampPath as:published ;
                            dcat:identifier    <http://publications.europa.eu/resource/dataset/corporate-body> ] .
pipeline/rdfc-pipeline-corporate-body.ttl — the main pipeline definition (replace <your-username> and <your-repo>):@prefix js:   <https://w3id.org/conn/js#>.
@prefix :     <https://w3id.org/conn#>.
@prefix owl:  <http://www.w3.org/2002/07/owl#>.
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#>.
@prefix tree: <https://w3id.org/tree#>.
@prefix as:   <https://www.w3.org/ns/activitystreams#>.
@prefix cb-as:  <https://<your-username>.github.io/<your-repo>/corporate-body/>.

<> owl:imports <./node_modules/@rdfc/js-runner/ontology.ttl>.
<> owl:imports <./node_modules/@rdfc/js-runner/channels/file.ttl>.
<> owl:imports <./node_modules/@rdfc/file-utils-processors-ts/processors.ttl>.
<> owl:imports <./node_modules/@rdfc/http-utils-processor-ts/processors.ttl>.
<> owl:imports <./node_modules/@rdfc/dumps-to-feed-processor-ts/processor.ttl>.
<> owl:imports <./node_modules/@rdfc/sds-processors-ts/configs/bucketizer.ttl>.
<> owl:imports <./node_modules/@rdfc/sds-processors-ts/configs/sdsify.ttl>.
<> owl:imports <./node_modules/@rdfc/sds-processors-ts/configs/ldes_disk_writer.ttl>.

# --- Channels ---

<raw/writer> a js:JsWriterChannel.
<raw/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <raw/reader>; :writer <raw/writer>.

<feed/writer> a js:JsWriterChannel.
<feed/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <feed/reader>; :writer <feed/writer>.

<sds/writer> a js:JsWriterChannel.
<sds/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <sds/reader>; :writer <sds/writer>.

<bucketized/writer> a js:JsWriterChannel.
<bucketized/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <bucketized/reader>; :writer <bucketized/writer>.

<metadata/writer> a js:JsWriterChannel.
<metadata/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <metadata/reader>; :writer <metadata/writer>.

<metadata/bucketized/writer> a js:JsWriterChannel.
<metadata/bucketized/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <metadata/bucketized/reader>; :writer <metadata/bucketized/writer>.

<shape/writer> a js:JsWriterChannel.
<shape/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <shape/reader>; :writer <shape/writer>.

<focusNodes/writer> a js:JsWriterChannel.
<focusNodes/reader> a js:JsReaderChannel.
[ ] a js:JsChannel; :reader <focusNodes/reader>; :writer <focusNodes/writer>.

# --- Processors ---

[ ] a js:HttpFetch;
    js:url "https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http%3A%2F%2Fpublications.europa.eu%2Fresource%2Fdistribution%2Fcorporate-body%2F20260318-0%2Frdf%2Fskos_core%2Fcorporatebodies-skos.rdf&fileName=corporatebodies-skos.rdf";
    js:writer <raw/writer>;
    js:options [ js:closeOnEnd true ].

[ ] a js:GlobRead;
    js:glob <./shape.ttl>;
    js:output <shape/writer>;
    js:closeOnEnd "true"^^xsd:boolean.

[ ] a js:GlobRead;
    js:glob <./focusNodes.sparql>;
    js:output <focusNodes/writer>;
    js:closeOnEnd "true"^^xsd:boolean.

[ ] a js:DumpsToFeed;
    js:dump <raw/reader>;
    js:output <feed/writer>;
    js:feedname "corporate-body";
    js:flush "false"^^xsd:boolean;
    js:dumpContentType "application/rdf+xml";
    js:focusNodesStrategy "sparql";
    js:nodeShapeIri "https://<your-username>.github.io/<your-repo>/shape.ttl#ActivityShape";
    js:nodeShape <shape/reader>;
    js:focusNodes <focusNodes/reader>;
    js:dbDir <./leveldb/>.

[ ] a js:Sdsify;
    js:input <feed/reader>;
    js:output <sds/writer>;
    js:stream cb-as:CorporateBodyStream;
    js:typeFilter as:Create, as:Update, as:Delete;
    js:shape """
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        @prefix as: <https://www.w3.org/ns/activitystreams#> .
        [ ] a sh:NodeShape ;
            sh:xone (
                [ a sh:NodeShape ; sh:targetClass as:Create ]
                [ a sh:NodeShape ; sh:targetClass as:Update ]
                [ a sh:NodeShape ; sh:targetClass as:Delete ]
            ).
    """.

[ ] a js:GlobRead;
    js:glob <./metadata.ttl>;
    js:output <metadata/writer>;
    js:closeOnEnd "true"^^xsd:boolean.

[ ] a js:Bucketize;
    js:channels [
          js:dataInput <sds/reader>;
          js:dataOutput <bucketized/writer>;
          js:metadataInput <metadata/reader>;
          js:metadataOutput <metadata/bucketized/writer>;
      ];
    js:bucketizeStrategy ( [
                               a tree:TimebasedFragmentation;
                               tree:timestampPath as:published;
                               tree:maxSize 100;
                               tree:k 4;
                               tree:minBucketSpan 2592000;
                           ]);
    js:savePath <./feed-state/buckets_save.json>;
    js:outputStreamId cb-as:CorporateBodyStream.

[ ] a js:LdesDiskWriter;
    js:dataInput <bucketized/reader>;
    js:metadataInput <metadata/bucketized/reader>;
    js:directory <../docs>.
pipeline/run.mjs — Windows runner (optional):This wrapper patches a known issue where the LDES disk writer generates Windows backslash paths that break the N3 RDF parser. It is not needed on Linux or macOS.import path from "path";
const origJoin = path.join;
const origRelative = path.relative;
path.join = (...args) => origJoin(...args).replaceAll("\\", "/");
path.relative = (...args) => origRelative(...args).replaceAll("\\", "/");
path.sep = "/";

await import("./node_modules/@rdfc/js-runner/bin/js-runner.js");
4. Run the pipelineOn Linux / macOS:cd pipeline
npx @rdfc/js-runner rdfc-pipeline-corporate-body.ttl
On Windows:cd pipeline
node run.mjs rdfc-pipeline-corporate-body.ttl
5. Verify the outputCheck that the LDES files were generated:ls ../docs/
You should see an index.trig file and a directory structure containing time-based fragments.6. Add a landing pageCreate docs/index.html so browsers display a human-readable page:<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=index.trig">
    <title>Corporate Body LDES Feed</title>
</head>
<body>
    <h1>EU Corporate Body Vocabulary — LDES Feed</h1>
    <p>Redirecting to <a href="index.trig">LDES entry point</a>...</p>
</body>
</html>
7. Add a .gitignoreCreate a .gitignore in the root of your repository:node_modules/
pipeline/leveldb/
pipeline/feed-state/
8. Deploy as GitHub static pagesGo to your repository Settings > Pages, set the source to the main branch and the /docs folder.Then commit and push:git add .
git commit -m "Initial LDES feed"
git push
Your first LDES feed will be live at: https://<your-username>.github.io/<your-repo>/9. Run again — observe change detectionRun the pipeline a second time. You should see Equal hashes messages — nothing changed in the source data, so no new events are generated. This is the power of LDES: only real changes produce new events.To see detailed logs:LOG_LEVEL=debug node run.mjs rdfc-pipeline-corporate-body.ttl
Project structure<your-repo>/
│
├── docs/                                     # Output: static LDES (served by GitHub Pages)
│   ├── index.html                            # Human-readable landing page
│   ├── index.trig                            # LDES entry point
│   └── .../                                  # Time-based fragment directories
│
├── pipeline/                                 # Pipeline configuration and runtime
│   ├── rdfc-pipeline-corporate-body.ttl      # Main pipeline definition
│   ├── metadata.ttl                          # Stream and dataset metadata
│   ├── shape.ttl                             # SHACL shape (targets skos:Concept)
│   ├── focusNodes.sparql                     # Custom SPARQL for entity selection
│   ├── package.json                          # npm dependencies
│   ├── run.mjs                               # Windows-compatible runner (optional)
│   ├── leveldb/                              # Entity state database (auto-generated)
│   └── feed-state/                           # Bucket state (auto-generated)
│
├── .gitignore
└── README.md
Troubleshooting"A sds:stream can only carry one specified shape, not 0"Harmless warning. The pipeline works correctly.Windows: Unexpected "<..\..\..\index.trig>" errorUse node run.mjs instead of npx @rdfc/js-runner. The wrapper patches Windows backslash paths.No events generatedMake sure:
focusNodes.sparql exists and contains the SPARQL query
nodeShapeIri in the pipeline matches the IRI in shape.ttl
The js:nodeShape and js:focusNodes channels are properly connected
DebuggingEnable verbose logging:LOG_LEVEL=debug node run.mjs rdfc-pipeline-corporate-body.ttl
Technologies & Further ReadingTechnologyRoleLDESLinked Data Event Streams specificationTREEFragmentation and paginationRDF-ConnectDeclarative pipeline frameworkSHACLShape-based entity selectionSKOSSource vocabulary modelActivityStreamsEvent types (Create, Update, Delete)GitHub PagesStatic hostingFurther reading
LDES DCAT-AP Feeds Specification
LDES Implementation Reports
EU Vocabularies Portal
RDF-Connect Documentation
Interoperable Europe Academy — LDES Course
License: MIT
