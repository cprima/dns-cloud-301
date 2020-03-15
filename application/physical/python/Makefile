.PHONY: gae-set-config gae-deploy-nopromote local-gunicorn

gae-set-config:
	cp gcloud_config_wbigcloud ~/.config/gcloud/configurations/config_wbigcloud
	gcloud config configurations activate wbigcloud

gae-deploy-nopromote:
	gcloud app deploy app-cname-cloud-301.yaml --quiet
	gcloud app deploy dispatch.yaml --quiet

local-gunicorn:
	GOOGLE_APPLICATION_CREDENTIALS=~/Documents/IT-Security/gcloudserviceaccount_wbi-gcloud.json FLASK_APP=app-cname-cloud-301:app FLASK_ENV=development python -m flask run --host=localhost
