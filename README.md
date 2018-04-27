### :lock: This repository has been archived

# CommCare HQ Prelogin

This site is visible before a user logs in to [CommCare HQ](http://www.commcarehq.org/home/)
or afterward by visiting `/home` directly.

## Enabling Development locally

1) Please follow the [steps for using LESS](https://github.com/dimagi/commcare-hq#using-less-3-options) and setting up Django Compressor in your local dev environment.

2) Set this flag in your `localsettings.py`

```
ENABLE_PRELOGIN_SITE = True
```

## PURGING THE CACHE

To purge the cache from a specific endpoint, run the following

```
curl -X PURGE -D – "https://www.commcarehq.org/<path>/<to>/<purge>"
```

So if we wanted to force purge the cache for `/home`, then run:

```
curl -X PURGE -D – "https://www.commcarehq.org/home/"
curl -X PURGE -D – "https://www.commcarehq.org/lang/en/home/"
curl -X PURGE -D – "https://www.commcarehq.org/lang/fra/home/"
```

## LICENSE

Dimagi owns copyright over this repository and reserves all rights.
