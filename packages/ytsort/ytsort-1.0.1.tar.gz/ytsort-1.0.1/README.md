# YTSort

This program sorts the already downloaded youtube videos present in a folder by renaming them and adding serial number before their names.

# Requirements

Youtube Data API v3 is required. Get it from [here](https://console.cloud.google.com/apis/library/youtube.googleapis.com?supportedpurview=project)

# Install 

```
pip install ytsort
```

# Usage

Set Youtube API Key to the environment variable 'YOUTUBE_DATA_API_KEY' (for ease of use, but not required).

### Execute:
```
ytsort
```
ytsort [Options]

Options:

    -c, --character TEXT   Character after serial.

    -p, --padded-zero      Padded zero.

    -np, --no-padded-zero  No padded zero.

    --help                 Show help.

If -p & -np both are passed simultaneously then default from config.py will be used.


# Install from source

1. Install the packages in requirements.txt by running:

   ```
   python -m pip install -r requirements.txt
   ```

2. Not required but for ease of use
 
   a) Set Youtube API Key to the environment variable 'YOUTUBE_DATA_API_KEY'

   or
 
   b) edit the `config.py`:

      `'api_key': os.environ.get('YOUTUBE_DATA_API_KEY'),` to `'api_key': <Your Youtube API key>,`

## Run

cd into the folder containing youtube videos and execute:
```
python <path of YTSort folder>
```
