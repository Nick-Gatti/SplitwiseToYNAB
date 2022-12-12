import datetime
import json
import logging
import os
import re
import time
from decimal import Decimal
from sys import stdout

import requests
from dotenv import load_dotenv

import getAccountInfo

load_dotenv()
logger=logging.getLogger('logger')
logLevel = os.getenv('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=logLevel)
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#Splitwise variables
splitwiseKey= os.getenv('SPLITWISE_API_KEY')
splitwiseUserID=getAccountInfo.getSplitwiseUserID()

#YNAB Variables
ynabKey=os.getenv('YNAB_API_KEY')
ynabBudgetID=getAccountInfo.getYNABBudgetID(ynabKey,os.getenv('YNAB_BUDGET_NAME',default='last-used'))
ynabSplitwiseAccountID=getAccountInfo.getYNABSplitwiseAccountID(os.getenv('YNAB_SPLITWISE_ACCOUNT_NAME', default='Splitwise'),ynabBudgetID,ynabKey)
ynabSplitwiseCategoryID=getAccountInfo.getYNABSplitwiseCategoryID(os.getenv('YNAB_SPLITWISE_CATEGORY_NAME',default='Splitwise'),ynabBudgetID,ynabKey)
ynabServerKnowledge=0
#General variables
userName=os.getenv('NAME', default='you')
days=int(os.getenv('DAYS',default=7))
sleep=int(os.getenv('SLEEP', default=15))

logger.info("Starting...")



while True:
    daysBack = datetime.datetime.now()-datetime.timedelta(days)
    #Get data from Splitwise/YNAB
    ynabTransactions=json.loads(requests.get('https://api.youneedabudget.com/v1/budgets/'+ynabBudgetID+'/accounts/'+ynabSplitwiseAccountID+'/transactions', headers={'Authorization':'Bearer '+ynabKey}, params={'since_date':daysBack}).content)['data']['transactions']
    splitwiseData=json.loads(requests.get('https://secure.splitwise.com/api/v3.0/get_expenses',headers={'Authorization': 'Bearer '+splitwiseKey}, params={'updated_after':daysBack}).content)
    ynabImportIds=[]
    for transaction in ynabTransactions:
        if transaction['import_id']:
            ynabImportIds.append(transaction['import_id'])
    newExpenses=[]
    for expense in splitwiseData["expenses"]:
        expenseId=(expense['id'])
        if(str(expenseId) in ynabImportIds):
            ##TODO: Add logic for updated/deleted expenses
            logger.debug('Skipping previously added import ID ' +str(expense['id']))
            continue
        else:
            for i in range(len(expense['repayments'])):
                if int(expense['repayments'][i-1]['from'])==splitwiseUserID:
                    expenseDate=expense['date'].split('T')[0]
                    newExpenses.append({'id':expenseId,'date':expenseDate,'description':expense["description"],'amount':expense['repayments'][i-1]['amount']})  


    #Add new YNAB transactions
    ynabNewTransactions=[]
    for newExpense in newExpenses:
        ynabNewTransactions.append({
          "import_id": str(newExpense["id"]),
          "account_id": ynabSplitwiseAccountID,
          "date": newExpense['date'],
          "amount": 0,
          "memo": newExpense['description']+', '+userName+  (' owe ' if userName=='you' else ' owes ') +'{0:.2f}'.format(Decimal(re.sub(r'[^\d\-.]', '', newExpense['amount']))),
          "cleared": "cleared",
          "subtransactions":[
            {
                "amount": int(Decimal(re.sub(r'[^\d\-.]', '', newExpense['amount']))*1000),#This is probably the second worst way to go about this but I'm doing it anyway
                "category_id":ynabSplitwiseCategoryID
            },
            {
                "amount":-int(Decimal(re.sub(r'[^\d\-.]', '', newExpense['amount']))*1000)
            }
            ]
            })
        logger.info('Added new expense "'+newExpense['description']+'"')
    if len(ynabNewTransactions)>0:
        ynabNewTransactions={"transactions":ynabNewTransactions}
        response=requests.post('https://api.youneedabudget.com/v1/budgets/'+ynabBudgetID+'/transactions',headers={'Authorization':'Bearer '+ynabKey},params={'budget_id':ynabBudgetID},json=ynabNewTransactions)
        logger.debug(response.content)
    else:
        logger.info('No new transactions. Sleeping.')
    time.sleep(sleep*60)



