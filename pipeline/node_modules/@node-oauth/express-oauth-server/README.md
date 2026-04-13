<div align="center">
  <h1>Express OAuth Server</h1>
</div>

<p align="center">
Complete, compliant and well tested module for implementing an OAuth2 Server/Provider with <a alt="express" href="https://github.com/expressjs/express">express</a> in <a alt="node.js" href="http://nodejs.org/">Node.js</a>.
</p>

<div align="center">

[![Tests](https://github.com/node-oauth/express-oauth-server/actions/workflows/tests.yml/badge.svg)](https://github.com/node-oauth/express-oauth-server/actions/workflows/tests.yml)
[![CodeQL](https://github.com/node-oauth/express-oauth-server/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/node-oauth/express-oauth-server/actions/workflows/github-code-scanning/codeql)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![npm Version](https://img.shields.io/npm/v/@node-oauth/express-oauth-server?label=version)](https://www.npmjs.com/package/@node-oauth/oauth2-server)
[![npm Downloads/Week](https://img.shields.io/npm/dw/@node-oauth/express-oauth-server)](https://www.npmjs.com/package/@node-oauth/oauth2-server)
![GitHub](https://img.shields.io/github/license/node-oauth/express-oauth-server)

</div>

<div align="center">

[API Docs](https://node-oauth.github.io/express-oauth-server/)
·
[NPM Link](https://www.npmjs.com/package/@node-oauth/express-oauth-server)
·
[Node OAuth2 Server](https://github.com/node-oauth/node-oauth2-server)

</div>

## About

This package wraps the [@node-oauth/oauth2-server](https://github.com/node-oauth/node-oauth2-server) into an
express compatible middleware.
It's a maintained and up-to-date fork from the former
[oauthjs/express-oauth-server](https://github.com/oauthjs/express-oauth-server).


## Installation

```shell
$ npm install @node-oauth/express-oauth-server
```

## Quick Start

The module provides two middlewares - one for granting tokens and another to authorize them. 
`@node-oauth/express-oauth-server` and, consequently `@node-oauth/oauth2-server`,
expect the request body to be parsed already.
The following example uses `body-parser` but you may opt for an alternative library.

```js
const bodyParser = require('body-parser');
const express = require('express');
const OAuthServer = require('@node-oauth/express-oauth-server');

const app = express();

app.oauth = new OAuthServer({
  model: {}, // See https://github.com/node-oauth/node-oauth2-server for specification
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(app.oauth.authorize());

app.use(function(req, res) {
  res.send('Secret area');
});

app.listen(3000);
```

## Options

> Note: The following options **extend** the default options from `@node-oauth/oauth2-server`!
> You can read more about all possible options in the
> [@node-oauth/oauth2-server documentation](https://node-oauthoauth2-server.readthedocs.io/en/master/api/oauth2-server.html)
 
```
const options = { 
  useErrorHandler: false, 
  continueMiddleware: false,
}
```

- `useErrorHandler`
(_type: boolean_ default: false)

  If false, an error response will be rendered by this component.
  Set this value to true to allow your own express error handler to handle the error.

- `continueMiddleware`
(_type: boolean default: false_)

  The `authorize()` and `token()` middlewares will both render their 
  result to the response and end the pipeline.
  next() will only be called if this is set to true.

  **Note:** You cannot modify the response since the headers have already been sent.

  `authenticate()` does not modify the response and will always call next()

## Migration notes

Beginning with **version 4.0** this package brings some potentially breaking changes:

- dropped old es5 code; moved to native async/await
- requires node >= 16
- ships with [@node-oauth/oauth2-server](https://github.com/node-oauth/node-oauth2-server) 5.x
- no express version pinned but declared as `'*'` peer dependency, so it should not cause conflicts with your express version

## More Examples

For more examples, please visit [our dedicated "examples" repo](https://github.com/node-oauth/node-oauth2-server-examples)
, which also contains express examples.

## License

MIT, see [license file](./LICENSE).
