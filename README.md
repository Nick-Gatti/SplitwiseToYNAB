
# SplitwiseToYNAB
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/nickgatti)

This script allows for an easy way to keep Splitwise and You Need A Budget (YNAB) up to date without having to manually import each purchase made on your behalf. An example of this can be found in option two of the [YNAB Blog post on utilizing Splitwise](https://support.youneedabudget.com/en_us/splitwise-and-ynab-a-guide-H1GwOyuCq#register) in your budget.

In short, it adds a new $0 transaction into a "Splitwise" account in YNAB each time a new expense comes into Splitwise. This is split into subtransactions- one that goes into a "Splitwise" category (as an inflow) and one that has the category left blank (With the same amount as an outflow). You'd then want to update the category to what the expense would be if you had paid for it, and then approve it.




## Environment Variables

To run this project, you will need to add the following environment variables to your .env file, or as variables in your `docker run` command.
An .env.example file is included.

### From Splitwise

`SPLITWISE_API_KEY`- Your Splitwise API key, generated in your [Splitwise Apps](https://secure.splitwise.com/apps) page under "Register your application"

### From YNAB
`YNAB_API_KEY`- Your YNAB API key- generated in the [YNAB Developer Settings](https://app.youneedabudget.com/settings/developer) and clicking on the "New Token" button.

`YNAB_BUDGET_NAME`(Optional)- The name of the YNAB budget you want to use. Defaults to your most recently used budget.

`YNAB_SPLITWISE_ACCOUNT_NAME`(Optional)- The name of an unlinked "Splitwise" account in your budget. Defaults to "Splitwise".

`YNAB_SPLITWISE_CATEGORY_NAME`(Optional)-  The name of your Splitwise category in YNAB. Defaults to "Splitwise".

### General

`NAME`(Optional)- Your name. Used for formatting memo in YNAB.

`DAYS`(Optional)- How many days back you want to check for new expenses. Defaults to 7.

`SLEEP`(Optional)- How long (in minutes) you want the script to sleep between checks. Defaults to 15 minutes.
## Run Locally

Clone the project

```bash
  git clone https://github.com/Nick-Gatti/SplitwiseToYNAB.git
```

Go to the project directory

```bash
  cd SplitwiseToYNAB
```

Copy .env file and set up environment
```bash
  cp .env.example .env
  nano .env
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start

```bash
  python SplitwiseToYNAB.py
```


## To Do

- Add logic to update/delete expenses in YNAB when they're updated/deleted in Splitwise
- Add support for more than one person being repaid (This may work already, I haven't tested.)
