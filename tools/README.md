1. Run [scunpacked](https://github.com/StarCitizenWiki/scunpacked).\
   Data should be extracted to `LIVE_EXTRACT` and loaded to `LIVE_EXTRACT2`, one directory level above the repository:
   ```
    $ ls -1
    LIVE_EXTRACT
    LIVE_EXTRACT2
    all-slain
   ```

2. From the repo directory, run `python -m tools.extract`, `python -m tools.extract_actors`, etc.
