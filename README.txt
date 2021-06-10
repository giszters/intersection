I want to see the number of tiles required to cover my area

When user provides the definition of area to be covered by observation, we're dealing with a Polygon object (provided through GeoJSON features)

We need the ability to find out which tiles cover the area provided by user (for specific date or date range - we need to check whether the specific tiles change and if yes - how frequently)

The data we're interested in fetching is made available on a public (requester-pays) AWS S3 bucket.

Some links:

    https://registry.opendata.aws/sentinel-1/ - AWS S3 bucket info

    https://roda.sentinel-hub.com/sentinel-s1-l1c/GRD/readme.html - data structure description

    https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-1-sar/products-algorithms/level-1-product-formatting - product naming convention

When we're able to properly find out which products need to be fetched from S3 for specific area (polygon), we need to make this information available quickly and via some kind of an API - to be used by the backend / frontend application when setting up orders and calculating prices.
Sample AWS S3 output

aws s3 ls s3://sentinel-s1-l1c/GRD/2021/5/10/IW/DH/ --request-payer requester
    PRE S1A_IW_GRDH_1SDH_20210510T095149_20210510T095218_037824_0476E1_A70E/
    PRE S1A_IW_GRDH_1SDH_20210510T095218_20210510T095243_037824_0476E1_419B/
    PRE S1A_IW_GRDH_1SDH_20210510T095243_20210510T095308_037824_0476E1_3701/
    (...)


aws s3 ls s3://sentinel-s1-l1c/GRD/2021/5/10/IW/DH/S1B_IW_GRDH_1SDH_20210510T090734_20210510T090801_026840_0334D1_5317/ --request-payer requester
                           PRE annotation/
                           PRE measurement/
                           PRE preview/
                           PRE support/
2021-05-10 14:10:19      21645 manifest.safe
2021-05-10 14:10:30       3078 productInfo.json
2021-05-10 14:10:19      15010 report-20210510T111552.pdf
