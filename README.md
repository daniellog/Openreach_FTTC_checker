# Openreach_FTTC_checker
A Python script to check when FTTC is available in your area.

### Prerequisites

You will need some python libaries for this script to work.

```
pip install mechanize
pip install BeautifulSoup
```

### Using the script

The script just requires a UK BT landline number that then pushes to the BT DSL checker website and scrapes the data back to find out if its avaliable of not.

Example:
```
Openreach_FTTC_checker.py -n 01132823658
```

If you are going to be running this as a cronjob and only want output when its avaliable then use the '-a' flag.

Example:
```
Openreach_FTTC_checker.py -n 01132823658 -a
```
