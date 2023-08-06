# Arcane bing

This package is based on [bingads](https://docs.microsoft.com/en-us/advertising/guides/request-download-report?view=bingads-13).

## Get Started

```sh
pip install arcane-bing
```

## Example Usage

### Reporting

```python
bing_client = Client(
    credentials=Config.BING_ADS_CREDENTIALS,
    secrets_bucket=Config.SECRETS_BUCKET,
    refresh_token_location=Config.BING_ADS_REFRESH_TOKEN,
    storage_client=storage_client
)

reporting_service_manager, reporting_service = bing_client.get_bing_ads_api_client()

report_request = build_campaigns_report(reporting_service, bing_account_id)

result_file_path = bing_client.submit_and_download(report_request, reporting_service_manager)
```

### Campaign Service

:warning: For some API methods, you must provide the client's account id and the manager's customer id

```python
from arcane.bing import Client
from arcane.bing.helpers import parse_webfault_errors, parse_bing_response


bing_client = Client(
    credentials=Config.BING_ADS_CREDENTIALS,
    secrets_bucket=Config.SECRETS_BUCKET,
    refresh_token_location=Config.BING_ADS_REFRESH_TOKEN,
    storage_client=storage_client,
    customer_id=CUSTOMER_ID,
    account_id=ACCOUNT_ID
)

campaign_service = bing_client.get_service_client(service_name='CampaignManagement')

try:
    response = campaign_service.GetCampaignsByAccountId(AccountId=ACCOUNT_ID)
    all_campaigns = parse_bing_response(response)['Campaign']
    # do stuff with all_campaigns
except WebFault as e:
    bing_error = parse_webfault_errors(e)
    # do stuff with bing_error
```
