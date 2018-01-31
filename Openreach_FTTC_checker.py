#!/usr/bin/python
import re
import getopt
import sys
import mechanize
from bs4 import BeautifulSoup

def main(argv):

  if not argv:
    print "Openreach_FTTC_checker.py -n <telephoneNumber>"
    print "-n --telephoneNumber  - UK BT landline telephone number"
    print "-a --avaliable        - Only print output if FTTC is avaliable (For cron jobs)"
    sys.exit(2)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "han:", ["help", "avaliable", "telephoneNumber="])
  except getopt.GetoptError:
    print "Openreach_FTTC_checker.py -n <telephoneNumber>"
    print "-n --telephoneNumber  - UK BT landline telephone number"
    print "-a --avaliable        - Only print output if FTTC is avaliable (For cron jobs)"
    sys.exit(2)

  telephoneNumber = None
  onlyAvaliable = False

  for opt, arg in opts:
    if opt in ("-n", "--telephoneNumber"):
      if re.match('^(?:0|\+?44)(?:\d\s?){9,10}$', arg ) is not None:
        telephoneNumber = arg 
      else:
        print('Telephone number invalid')
        sys.exit(2)
    elif opt in ("-a", "--avaliable"):
      onlyAvaliable = True
    elif opt in ("-h", "--help"):
      print "Openreach_FTTC_checker.py -n <telephoneNumber>"
      print "-n --telephoneNumber  - UK BT landline telephone number"
      print "-a --avaliable        - Only print output if FTTC is avaliable (For cron jobs)"
      sys.exit(2)
    else:
      print "Openreach_FTTC_checker.py -n <telephoneNumber>"
      print "-n --telephoneNumber  - UK BT landline telephone number"
      print "-a --avaliable        - Only print output if FTTC is avaliable (For cron jobs)"
      sys.exit(2)

  url = 'http://www.dslchecker.bt.com/'
  br = mechanize.Browser()
  br.set_handle_robots(False) # ignore robots
  br.open(url)
  br.select_form(nr=0)
  br["TelNo"] = telephoneNumber
  res = br.submit()
  content = res.read()
 
  soup = BeautifulSoup(content,"html.parser") 
  try:
    VDSL_Range_A_status = soup('table')[3].findAll('tr')[2].findAll('td')[6].string
    VDSL_Range_B_status = soup('table')[3].findAll('tr')[3].findAll('td')[6].string
  except:
    print "There is no data available for this number. This could be either because it is not a BT line or it is a new BT number that has just been provided. Most new numbers will appear on the checker 24 hours after BT has installed the line."
    sys.exit(2)
 
  if VDSL_Range_A_status == 'Available':
    print "** FTTC available! **"
    print "" 
    print "** VDSL Range A (Clean) **"
    print "Speed Downstream (Mbps) High: " + soup('table')[3].findAll('tr')[2].findAll('td')[0].string
    print "Speed Downstream (Mbps) Low: " + soup('table')[3].findAll('tr')[2].findAll('td')[1].string
    print "Speed Upstream (Mbps) High: " + soup('table')[3].findAll('tr')[2].findAll('td')[2].string
    print "Speed Upstream (Mbps) Low: " + soup('table')[3].findAll('tr')[2].findAll('td')[3].string
    print ""
    print "** VDSL Range B (Impacted) **"
    print "Speed Downstream (Mbps) High: " + soup('table')[3].findAll('tr')[3].findAll('td')[0].string
    print "Speed Downstream (Mbps) Low: " + soup('table')[3].findAll('tr')[3].findAll('td')[1].string
    print "Speed Upstream (Mbps) High: " + soup('table')[3].findAll('tr')[3].findAll('td')[2].string
    print "Speed Upstream (Mbps) Low: " + soup('table')[3].findAll('tr')[3].findAll('td')[3].string
  else:
   if onlyAvaliable == False:  
    print "** FTTC not available :( **"
    print "VDSL Range A Availability Status: " + VDSL_Range_A_status
    print "VDSL Range B Availability Status: " + VDSL_Range_B_status
    
if __name__ == "__main__":
  main(sys.argv[1:])
