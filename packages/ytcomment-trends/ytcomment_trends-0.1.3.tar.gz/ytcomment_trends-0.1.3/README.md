# ytcomment_trends

[![PyPI version](https://badge.fury.io/py/ytcomment-trends.svg)](https://badge.fury.io/py/ytcomment-trends)

[![Python Versions](https://img.shields.io/pypi/pyversions/ytcomment-trends.svg)](https://pypi.org/project/ytcomment-trends/)

## Dependencies

Before install this library, you need to install mecab for NLP.

For macOS, run this command to install mecab and ipadic dictionary. For other OS, please follow the instructions from mecab official documentation.

```
brew install mecab mecab-ipadic
```

## How to use

### Get YouTube API Client Secret

Please refer to [Google's official documentation](https://developers.google.com/youtube/registering_an_application) for getting API keys. Make sure you create credentials with OAuth 2.0 Clients with type of "Desktop" app. Also, make sure you download JSON file to your local directory.

### Run command

Install this library with the following command:

```
pip install ytcomment_trends
```

If you are using virtual environment, please use the package manager of the virtual environment (e.g., `pipenv install`, `poetry add`).

After installation, run this command to analyze video. Make sure to check credentials JSON file path and video ID.

```
ytcomment_trends -t "./client_secret.json" -v pR2E2OatMTQ
```

If you are not sure about the arguments, run following command to check.

```
ytcomment_trends -h
```