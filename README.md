# policyBuilder
A policy builder interface for Trusted Capsules

## Requirements:
- python 3.6+
- yarn
- capsule_gen

## Background:
Slides: https://docs.google.com/presentation/d/1h1r1BICwu2tbnsBMdahuZV4tx1Q5xVw0yfxkWo3Eexw/edit#slide=id.g592028f938_0_86

## Getting started
1. Install [yarn](https://yarnpkg.com/en/docs/install)
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

Open your web browser to http://localhost:5000/

### Notes
#### Frontend
Built with:
- react
- typescript
- [react-beautiful-dnd](https://github.com/atlassian/react-beautiful-dnd)

### Backend
Built with: 
- Flask (web server)
- SQLite (persistent store)
- SqlAlchemy (ORM for easy data marshalling)
