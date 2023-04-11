
import os, sys, logging
from os import environ
import dns.resolver
from datetime import datetime
import time
import boto3
from botocore.config import Config

PREVIOUS_ADDRESS = None

logger = logging.getLogger("DynamicDNSUpdater")
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)

REQUIRED_ENV_VARS = {
    "DDNSU_ROUTE53_HOST_NAME", 
    "DDNSU_ROUTE53_ZONEID",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_DEFAULT_REGION",
}

def checkAndLoadEnvironmentVariables():

    diff = REQUIRED_ENV_VARS.difference(environ)
    if len(diff) > 0:
        sys.exit(f'Failed to start application because {diff} environment variables are not set')
        
def updateRoute53(ip_address):
    logger.info("Starting update of Route53 A record for {}".format(os.environ['DDNSU_ROUTE53_HOST_NAME']))
    client = boto3.client('route53')
    response = client.change_resource_record_sets(
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': os.environ['DDNSU_ROUTE53_HOST_NAME'],
                        'ResourceRecords': [
                            {
                                'Value': ip_address,
                            },
                        ],
                        'TTL': os.environ.get('DDNSU_ROUTE53_TTL',300),
                        'Type': 'A',
                    },
                },
            ],
            'Comment': 'Web Server',
        },
    HostedZoneId='Z1FNLVW1LDGPGV',
    )
    logger.info("Route 53 Record updated successfully")
def updateNACL(ip_address):
    pass
    """ response = client.replace_network_acl_entry(
        CidrBlock='string',
        DryRun=True|False,
        Egress=True|False,
        IcmpTypeCode={
            'Code': 123,
            'Type': 123
        },
        Ipv6CidrBlock='string',
        NetworkAclId='string',
        PortRange={
            'From': 123,
            'To': 123
        },
        Protocol='string',
        RuleAction='allow'|'deny',
        RuleNumber=123
    ) """

def getLocalIPAddress():
    logger.info("Getting IP Address")
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["208.67.222.222","208.67.220.220"]
    result = resolver.resolve('myip.opendns.com', 'A')
    logger.info(f"The local IP Addreess is {result[0].to_text()}")
    #there is only ever a single local ip address to hardcode the return of the first
    return result[0].to_text()
    

def main():
    checkAndLoadEnvironmentVariables()
    while True:
        global PREVIOUS_ADDRESS
        logger.info("Starting DynamicDNSUpdater")
        start_time = datetime.now()
        myip = getLocalIPAddress()
        if myip !=  PREVIOUS_ADDRESS:
            logger.info("IP Address has changed.  Performing update operations.")
            updateRoute53(myip)
            updateNACL(myip)
            #Only update the IP Address if we receive no errors. This ensures everything is always up to date
            PREVIOUS_ADDRESS = myip
        else:
            logger.info("IP Address has not changed.  No updates needed.")
        time_taken = datetime.now() - start_time
        logger.info(f"DynamicDNSUpdater completed in {time_taken}")
        time.sleep(int(os.environ.get('DDNSU_TIME_BETWEEN_CHECKS_IN_SECONDS', default=300)))

if __name__ == "__main__":
    main()
