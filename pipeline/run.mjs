import path from "path";
const origJoin = path.join;
const origRelative = path.relative;
const origResolve = path.resolve;
path.join = (...args) => origJoin(...args).replaceAll("\\", "/");
path.relative = (...args) => origRelative(...args).replaceAll("\\", "/");
path.resolve = (...args) => origResolve(...args).replaceAll("\\", "/");
path.sep = "/";

await import("@rdfc/js-runner/bin/cli.js");
