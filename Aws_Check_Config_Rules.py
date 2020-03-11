import boto3



accounts = []
region = []

def config_rules_check(accounts, region):
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        for location in region:
            print(acct + " " + location)
            configclient = session.client('config',region_name=location)

            count = 0
            nexttoken = {}
            while True:
                response = configclient.describe_config_rules(**nexttoken)
                for configrule in response['ConfigRules']:
                    count = count + 1
                    #print(configrule['ConfigRuleName'])
                    #print(response['NextToken'])
                if 'NextToken' in response:
                    nexttoken['NextToken'] = response['NextToken']
                else:
                    break
            print(count)




config_rules_check(accounts,region)
