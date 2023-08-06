# BigQuery query - bqq 
> "Simplified, enriched `bq query`"

- prompted queries (billed project, cost, size), using dry run
- synchronize jobs from cloud (results linked with console.cloud.google.com)
- super fast search through query job history
- download and preview result data

## Requirements
- python >= 3.6

- fzf - https://github.com/junegunn/fzf (required)
```bash
brew install fzf
```
- gcloud - https://cloud.google.com/sdk/docs/install (recommended)
```bash
brew install --cask google-cloud-sdk
```

## Installation

- Using [pypi](https://pypi.org/project/bqq/)

```bash
pip install bqq
```

## Usage

### 1. Initialize bqq

```
bqq --init
```

### 2. Set up default credentials
> Underlying BigQuery client relies on [application-default](https://cloud.google.com/sdk/gcloud/reference/auth/application-default) credentials
```bash
gcloud auth application-default login
```


## Examples

```
Usage: bqq [OPTIONS] [SQL]

  BiqQuery query.

Options:
  -f, --file FILENAME  File containing SQL
  -y, --yes            Automatic yes to prompt
  -h, --history        Search local history
  -d, --delete         Delete job from history (local & cloud)
  -i, --info           Show gcloud configuration
  --clear              Clear local history
  --sync               Sync history from cloud
  --init               Initialize bqq environment
  --version            Show the version and exit.
  --help               Show this message and exit.
```


Query 
```bash
bqq "SELECT repository.url, repository.created_at FROM bigquery-public-data.samples.github_nested LIMIT 100"
Billing project = my-google-project
Estimated size = 150.3 MiB
Estimated cost = +0.00 $
Do you want to continue? [y/N]: y
```

Query in file
```
bqq -f query.sql
```

Synchronize
```
bqq --sync
Syncing jobs information  [####################################]
```

Search history
```
bqq -h
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Creation time = 2020-01-01 00:00:00
Project = my-google-project
Account = account@google.com
Query cost = +0.00 $
Slot time =
Console link = https://console.cloud.google.com/bigquery?project=my-google-project&j=bq:US:3ff1f9b0-ae38-4d83-a711-7f28f74ff769&page=queryresults
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
SELECT repository.url, repository.created_at FROM bigquery-public-data.samples.github_nested LIMIT 100
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Download result ? [y/N]:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ url                                                            ┃ created_at                ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ https://github.com/liferay/liferay-plugins                     ┃ 2009/09/25 15:56:21 -0700 ┃
┃ https://github.com/plataformatec/simple_form                   ┃ 2009/12/28 06:23:48 -0800 ┃
┃ https://github.com/cakephp/datasources                         ┃ 2009/12/02 21:07:40 -0800 ┃
┃ https://github.com/ezsystems/ezfind                            ┃ 2010/10/19 13:46:09 -0700 ┃
┃ https://github.com/EightMedia/hammer.js                        ┃ 2012/03/02 04:58:28 -0800 ┃
┃ https://github.com/saasbook/hw3_rottenpotatoes                 ┃ 2012/02/03 10:33:06 -0800 ┃
┃ https://github.com/JetBrains/kotlin                            ┃ 2012/02/13 09:29:58 -0800 ┃
┃ https://github.com/php/php-src                                 ┃ 2011/06/15 18:52:25 -0700 ┃
┃ https://github.com/saasbook/hw4_rottenpotatoes                 ┃ 2012/02/17 13:23:02 -0800 ┃
┃ https://github.com/AFNetworking/AFNetworking                   ┃ 2011/05/31 14:28:44 -0700 ┃
┃ https://github.com/php/php-src                                 ┃ 2011/06/15 18:52:25 -0700 ┃
┃ https://github.com/mono/MonoGame                               ┃ 2011/04/06 17:23:40 -0700 ┃
...
```