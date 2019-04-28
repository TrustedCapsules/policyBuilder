# policyBuilder
A policy builder interface for Trusted Capsules

## Requirements:
- python 3.6+
- yarn
- capsule_gen

## Getting started
Install [yarn](https://yarnpkg.com/en/docs/install)
From the git root, run
```bash
#frontend stuff
yarn install #get React (for drag and drop), webpack (for library bundling), babel (browser compatible)
yarn build #runs webpack and typescript transpiler

#backend stuff
pip3 install requirements.txt --user
python3 server.py #runs the backend
```

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
- Flask
