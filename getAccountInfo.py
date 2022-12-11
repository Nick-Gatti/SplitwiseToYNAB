import requests,json,os
def getYNABBudgetID(ynabKey,ynabBudgetName):
    if ynabBudgetName=='last-used':
        return 'last-used'
    budgets=json.loads(requests.get('https://api.youneedabudget.com/v1/budgets/', headers={'Authorization':'Bearer '+ynabKey}).content)['data']['budgets']
    for budget in budgets:
        if budget['name']==ynabBudgetName:
            return budget['id']
    raise RuntimeError('Splitwise account not found in YNAB.')
def getYNABSplitwiseCategoryID(splitwiseCategoryName,ynabBudgetID,ynabKey):
    categoryGroups= json.loads(requests.get('https://api.youneedabudget.com/v1/budgets/'+ynabBudgetID+'/categories', headers={'Authorization':'Bearer '+ynabKey}).content)['data']['category_groups']
    for categoryGroup in categoryGroups:
        for category in categoryGroup['categories']:
            if category['name']==splitwiseCategoryName:
                return(category['id'])
    raise RuntimeError('Splitwise category not found in YNAB.')            

def getYNABSplitwiseAccountID(splitwiseAccountName,ynabBudgetID,ynabKey):
    accounts=json.loads(requests.get('https://api.youneedabudget.com/v1/budgets/'+ynabBudgetID+'/accounts',headers={'Authorization':'Bearer '+ynabKey}).content)['data']['accounts']
    for account in accounts:
        if account['name']==splitwiseAccountName:
            return account['id']
    raise RuntimeError('Splitwise account not found in YNAB.')

def getSplitwiseUserID():
    splitwiseUserID=json.loads(requests.get('https://secure.splitwise.com/api/v3.0/get_current_user', headers={'Authorization': 'Bearer '+os.getenv('SPLITWISE_API_KEY')}, params={}).content)['user']['id']
    return(splitwiseUserID)