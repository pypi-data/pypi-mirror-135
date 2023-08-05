"""
Created on 10.05.2021

@author: baier
"""
from accessOutlookEmail import create_account, save_attachment


def main():
    account = create_account('kreutmair@orcacapital.de', 'jar54Cet$cosh45')
    save_attachment('Steubing', r'W:\01. ORCA Depot\Z InputConfirms\Steubing', account)


if __name__ == '__main__':
    main()
