"""
Created on 10.05.2021
This is a script to automatically upload every day the transaction file from the drive to the SFTP Server of CIBC.
@author: baier
"""
import os
import csv
import time
import random as rndm
import shutil
import datetime
from dotenv import load_dotenv
from accessOutlookEmail import create_account, send_email
from cibc_sftp_server.sftp_connection import establish_connection, sftp_connection

load_dotenv()
destFold = r'\drop\CashPB'
srcFold = r'W:\CIBC\upload'
archiveFold = f'{srcFold}\\Archive'
zusammenfassung = f'{archiveFold}\\0_zusammenfassung.txt'


def main():
    account = create_account(os.getenv('email_valentin'), os.getenv('password_valentin'))
    while True:
        now = (datetime.datetime.now()).strftime('%d.%m.%Y %H:%M:%S')
        list_files = os.listdir(path=srcFold)
        list_files.remove('Archive')

        if list_files:
            print(f"{list_files} has been found\n")

            server = establish_connection(os.getenv('cibc_server'), int(os.getenv('cibc_port')), os.getenv('cibc_user'),
                                          os.getenv('cibc_password'))
            sftp = sftp_connection(server)

            for file in list_files:
                new_filename = f'{file[:-4]}_{rndm.randint(0,100000)}{file[-4:]}'
                os.rename(f'{srcFold}\\{file}', f'{srcFold}\\{new_filename}')
                file = new_filename

                localpath = srcFold + '\\' + file
                sftp_file = destFold + '\\' + file

                with open(zusammenfassung, 'r', encoding='ISO-8859-1') as content:
                    save = content.readlines()[1:]

                with open(zusammenfassung, 'w', encoding='ISO-8859-1') as summary:
                    with open(localpath, 'r', encoding='ISO-8859-1') as upload_file:
                        reader = csv.reader(upload_file)
                        for row in reader:
                            for item in row:
                                summary.write(item + ',')
                            summary.write('\n')
                        summary.writelines(save)
                try:
                    if sftp.put(localpath, sftp_file):
                        print(f"{file} has been uploaded to CIBC")
                    if shutil.move(localpath, archiveFold):
                        body = f"""
                        <p>Die Datei {str(file)}, <br>
                        wurden versucht um  {now} ins Archive zu verschieben.<br>
                        Der Vorgang war ERFOLGREICH.<br><br>
                        Dies ist eine automatisierte Email.</p>"""
                        send_email(account, 'CIBC Upload/Move successful!', body,
                                   ['baier@orcacapital.de', 'settlement@orcacapital.de'])
                        print(f"{file} has been moved to {archiveFold}")
                except (shutil.Error, IOError) as err:
                    body = f"""
                    <p>Die Datei {str(file)}, <br>
                    wurden versucht um  {now} ins Archive zu verschieben.<br>
                    Der Vorgang SCHLUG FEHL. Schließe und lösche die Datei im UPLOAD-Ordner. Der Upload ist erfolgt.<br><br>
                    Caught following Error: {err}<br>
                    Dies ist eine automatisierte Email.</p>"""

                    send_email(account, 'CIBC Move failed!', body, ['baier@orcacapital.de', 'settlement@orcacapital.de',
                                                                    'kreutmair@orcacapital.de'])
                    print(f'Caught Permission Error: {err}')

            if sftp: sftp.close(), print('SFTP got disconnected')
            if server: server.close(), print('Transport Layer got disconnected')
        else:
            print('No new files')
            time.sleep(600)


if __name__ == '__main__':
    main()
