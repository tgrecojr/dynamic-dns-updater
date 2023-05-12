
# About
`Dynamic DNS Updater` is a utility to be run locally that will update both a Route53 A record (Dynamic DNS) and your main AWS NACL for your VPC when your local DNS changes. The intention is to alter your AWS environments so that they are accessable only to your local home network under the assumption that you are dynamically assigned an IP from your ISP.  This application is intended to work for IPv4 only.


# Required Environment Variables

The Following environment variables are used in this application.  All environment variables are prefaced with "DDNSU" for the application

| NAME                                | Description                          | Default |
| :----------------                   | :------                              | :---- |
| DDNSU_TIME_BETWEEN_CHECKS_IN_SECONDS|   Number of seconds between checks   | 300 |
| DDNSU_ROUTE53_HOST_NAME             |   Host name for the Route53 Record   | N/A |
| DDNSU_ROUTE53_ZONEID                |   Route53 Hosted Zone ID             | N/A |
| DDNSU_ROUTE53_TTL                   |   The TTL for the A record           | N/A |
| AWS_ACCESS_KEY_ID                   |   AWS Access Key ID                  | N/A |
| AWS_SECRET_ACCESS_KEY               |   AWS Secret Access Key              | N/A |
| AWS_DEFAULT_REGION                  |   AWS Default Region                 | N/A |
| DDNSU_NACL_ID                       |   AWS NACL ID (from VPC)             | N/A |
| DDNSU_SG_INFO                       |   JSON String of SG Details          | N/A |

# DDNSU_SG_INFO Details

Multiple Security groups can be updated at the same time using the following format:

[{"sg": "sgid","to": 443,"from": 443}, {"sg": "sgid2","to": 3306,"from": 3306}]



