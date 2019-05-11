# policyBuilder
A policy builder interface for Trusted Capsules. Integrates key management capabilities

## Requirements:
- python 3.6+
- yarn
- capsule_gen (bundled for Linux x86-64, for other platforms please recompile)

## Background:
- Slides: https://docs.google.com/presentation/d/1h1r1BICwu2tbnsBMdahuZV4tx1Q5xVw0yfxkWo3Eexw/edit#slide=id.g592028f938_0_86
- Registration flow: [pdf](docs/registration_flow.pdf)

## Getting started
1. Install [yarn](https://yarnpkg.com/en/docs/install) and [python](https://www.anaconda.com/distribution/#download-section)
2. From the git root, run
```bash
yarn install #get React (for drag and drop), webpack (for library bundling), dependencies
pip3 install requirements.txt --user
```
3. Run webpack, typescript transpiler and python server with `yarn start`

Nonce flow:
- Server gets registration request
- Server generates random byte nonce, saves hex(nonce) as a string
- Server responds to client with enc_nonce = hex(pubkey(nonce)) 
- Client sends dec_nonce = hex(decrypt(fromhex(enc_nonce)))
- Server validates this in db

Open your web browser to http://localhost:5000/ for policy creation

### Notes
#### Frontend
Built with:
- [react](https://reactjs.org/) (for abstraction of components)
- [typescript](https://www.typescriptlang.org/) (for type sanity)
- [webpack](https://webpack.js.org/) (for js import support in the browser)
- [webpack-dev-server](https://webpack.js.org/configuration/dev-server/) (for auto refresh when doing front end dev work)
- [react-fontawesome](https://github.com/FortAwesome/react-fontawesome) (for nice icons)
- [superagent](https://github.com/visionmedia/superagent) (for post request and attachment handling)
- [react-dropzone](https://github.com/react-dropzone/react-dropzone) (for drag and drop files)
- [react-beautiful-dnd](https://github.com/atlassian/react-beautiful-dnd) (not used currently)

### Backend
Built with: 
- flask (web server)
- sqlite (persistent store)
- sqlalchemy (ORM for easy data marshalling)
- pytest (for unit tests)
- jsonschema (validate client requests)
- pycryptodomex (key generation and encrypt/decrypt tasks)