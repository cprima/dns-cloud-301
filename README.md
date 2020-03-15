# cname-cloud-301
The repo for cname-cloud-301.


# Google Cloud App Engine #

## Create a project

Go to https://console.cloud.google.com/projectcreate and create a new project.

With the gcloud CLI SDK installed, run `gcloud components update` for good measure and enable the CLI API at https://console.cloud.google.com/flows/enableapi?apiid=cloudfunctions

Check if a gcloud account is currently authenticated with `gloud auth list`, if not use `gloud auth login` to open a browser login window. Settings can be persisted in a configuration file (on Ubuntu at ~/.config/gcloud/configurations/config_* (the file needs to contain only alphanumerical characters after the underscore _)) and that config can be activated with `gcloud config configurations activate foobar` (with foobar being the part after the underscore _).

Example of a config file:
```

/.config/gcloud/configurations/config_sunlightmapdev
[core]
account = example@gmail.com
project = foobar
disable_usage_reporting = True

[compute]
zone = europe-west3-b
region = europe-west3

[app]
promote_by_default = true
```
Changes to the current config file can be made with `gcloud config set #..`.

The gcloud App Engine needs a "default" service set, deployment from this repo can be made with
```
cd ./application/physical/python
gcloud app deploy app-default.yaml
```

The code for a CNAME-based URL forwarder then lives in another service within this repo, deployment done with:

```
gcloud app deploy app-cname-cloud-301.yaml
gcloud app deploy dispatch.yaml
```

This deploys two services within the same gcloud App Engine project.

Custom domains can be configured at https://console.cloud.google.com/appengine/settings/domains?supportedpurview=project


## Functionality ##

The code in ./application/physical/python checks incoming HTTP requests for a match against entries in a dictionary config["redirect_urls"] and conditionally redirects with status 301 to the value of that entry.

### Location of the config file ###

The code handles three locations:

- inline

- googlestorage

- an own endpoint, which in turn loads from inline or googlestorage

To use Google Cloud Storage, the bucket and the filename must be configured with `storage_client_bucket` or `bucket_blob`.


# Python specifics #

pip freeze will not add gunicorn to requirements.txt, so manually added as per https://cloud.google.com/appengine/docs/flexible/python/runtime#application_startup
