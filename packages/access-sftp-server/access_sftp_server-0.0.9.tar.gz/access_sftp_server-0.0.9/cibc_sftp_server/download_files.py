"""
Created on 10.05.2021
This is a script to automatically download every day the files from the SFTP Server of CIBC and 
put it into the folder structure of the settlement department.
@author: baier
"""
import datetime
import os
import time
from cibc_sftp_server import manipulate_reports

from accessOutlookEmail import create_account, send_email
from cibc_sftp_server.sftp_connection import establishConnection, sftpConnection
global sftp
global server

year_str = datetime.date.today().strftime("%Y")
account = create_account('baier@orcacapital.de', 'Malfurion321.')
destFold = rf"W:\CIBC\Bestände_CSV\{year_str}"
folders = os.listdir(destFold)

# a set of all types of reports, fileTypes and needed type of report
DateiFormat = {'posnm', 'posad', 'balnd', 'cshsm', 'balad', 'actim', 'cshim', 'intad', 'cshid', 'divas',
               'cshtd', 'posam', 'intam', 'balam', 'actid', 'posnd', 'balnm', 'divat', 'cshtm', 'cshsd'}
DateiEndung = {'.csv', '.pdf'}
ReportToFolder = {
    'balad.csv': 'Devisen',
    'cshtd.csv': 'Umsätze Kontobuchungen Letzter Tag',
    'posnd.csv': 'TD Holding',
    'cshsm.csv': 'Umsätze Gesamtumsatzaufstellung',
    'mrmrsd.pdf': 'Margin Report'
}

# DateiFormat = list(DateiFormat).sort() #wandel set in Liste und sortiere

# ziehe gestriges Datum bzw. das Datum vor dem Wochenende
today = datetime.date.today()
yesterday = (today - datetime.timedelta(1)).strftime("%Y%m%d")
weekend = (today - datetime.timedelta(3)).strftime("%Y%m%d")
todaysReports = set()


def get_risk_margin_pdf():
    src_fold = r'\pickup\RiskMargin'
    list_files = sftp.listdir(path=src_fold)
    list_files.remove('Archive')
    list_files.sort(reverse=True)  # dreht Liste um, da lexikografische Ordnung
    now = (datetime.datetime.now()).strftime('%d.%m.%Y %H:%M:%S')
    del list_files[2 * 4:]  # Erhalte die aktuellsten Reports

    # ziehe den aktuellen Monat für das File
    date_of_folder = list_files[0][13:15]
    for monat in folders:
        if monat[0:2] == date_of_folder:
            date_of_folder = monat
            break

    for item in list_files:  # gehe über jede Datei in dem SFTP
        for key in ReportToFolder.items():  # gehe über jedes Tuple im DICT
            if key[0] in item:
                sftppath = f'{src_fold}\\{item}'
                localpath = f'{destFold}\\{date_of_folder}\\{key[1]}\\{item}'

                # checke, ob die Datei bereits existiert
                if os.path.isfile(localpath):
                    print(f"At {now}: {item} already exists! File won't be saved")
                else:
                    print(f'At {now}: {item} was saved in {localpath}')
                    sftp.get(sftppath, localpath)

                todaysReports.add(item)


def get_cash_pb_csv():
    # get all files from FTP Server
    src_fold = r'\pickup\CashPB'
    list_files = sftp.listdir(path=src_fold)
    list_files.remove('Archive')
    list_files.sort(reverse=True)  # dreht Liste um, da lexikografische Ordnung
    now = (datetime.datetime.now()).strftime('%d.%m.%Y %H:%M:%S')
    del list_files[2 * 20:]  # Erhalte die aktuellsten Reports

    # ziehe den aktuellen Monat aus dem File und speichere in den jeweiligen Monatsordner
    date_of_folder = list_files[0][8:10]
    for monat in folders:
        if monat[0:2] == date_of_folder:
            date_of_folder = monat
            break

    for item in list_files:  # gehe über jede Datei in dem SFTP
        for key in ReportToFolder.items():  # gehe über jedes Tuple im DICT
            if key[0] in item:
                sftppath = f'{src_fold}\\{item}'
                localpath = f'{destFold}\\{date_of_folder}\\{key[1]}\\{item}'

                # checke, ob die Datei bereits existiert
                if os.path.isfile(localpath):
                    print(f"At {now}: {item} already exists! File won't be saved")
                else:
                    print(f'At {now}: {item} was saved in {localpath}')
                    sftp.get(sftppath, localpath)

                    # bearbeite die Datei cshsm.csv
                    if key[0] == 'cshsm.csv' or key[0] == 'cshtd.csv':
                        manipulate_reports.formatExcelcshsm(localpath)

                    # bearbeite die Datei cshsm.csv
                    if key[0] == 'posnd.csv':
                        manipulate_reports.formatExcelposnd(localpath)

                todaysReports.add(item)


def main():
    global sftp
    global server

    while len(todaysReports) < len(ReportToFolder):
        server = establishConnection("files.prd.cibcprime.com", 22, 'cli_orca_prd', 'JT4d%k8dw3P')
        sftp = sftpConnection(server)
        # get all files from FTP Server
        src_fold = r'\pickup\CashPB'
        list_files = sftp.listdir(path=src_fold)
        list_files.remove('Archive')
        list_files.sort(reverse=True)  # dreht Liste um, da lexikografische Ordnung
        date_of_report = list_files[38][4:12]
        now = (datetime.datetime.now()).strftime('%d.%m.%Y %H:%M:%S')

        if date_of_report != yesterday and date_of_report != weekend:
            print(f'Checked at {now}: no new reports found!')

            if sftp: sftp.close(), print('SFTP got disconnected')
            if server: server.close(), print('Transport Layer got disconnected\n')
            time.sleep(600)
        else:
            body = f"<p>Hallo zusammen, <br><br> \
                    Die CIBC Reports stehen nun im Laufwerk bereit.<br> \
                    Um {now} wurden die Files heruntergeladen.<br><br> \
                    Dies ist eine automatisierte Email.</p>"

            get_cash_pb_csv()
            get_risk_margin_pdf()
            if len(todaysReports) == len(ReportToFolder):
                send_email(account, 'CIBC Reports available', body, ['baier@orcacapital.de', 'settlement@orcacapital.de'])
            else:
                time.sleep(120)

    # Close
    if sftp: sftp.close(), print('SFTP got disconnected')
    if server: server.close(), print('Transport Layer got disconnected\n')


if __name__ == '__main__':
    main()
