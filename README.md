# autoupdate

A small tool to automatically update AWS Lambda layers or other deployment artifacts.

## What this does
- Detects changes to a layer or artifact and publishes an updated Lambda layer.
- Intended for use in CI/CD pipelines (GitHub Actions, Jenkins, etc).

## Quick start
1. Clone the repo: `git clone https://github.com/4095495340/autoupdate.git`
2. Edit files as needed.
3. Run your update script (example): `python update_layer.py --help`

## How to contribute
1. Fork the repo, make a branch, then open a pull request.
2. Add clear commit messages and a short description of your change.

## License
MIT
