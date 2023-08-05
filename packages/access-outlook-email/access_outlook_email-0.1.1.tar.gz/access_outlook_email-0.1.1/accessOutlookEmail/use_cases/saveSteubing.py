"""
Created on 10.05.2021

@author: baier
"""
from accessOutlookEmail import create_account, save_attachment

account = create_account('kreutmair@orcacapital.de', 'ubeRr@schun9')

save_attachment('Steubing', r'W:\01. ORCA Depot\Z InputConfirms\Steubing', account)
