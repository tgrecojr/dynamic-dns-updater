
# About
`dynamic-dns-update` is a utility to be run locally that will update both a Route53 A record (Dynamic DNS) and your main AWS NACL for your VPC when your local DNS changes.

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
