import ftplib
import gnupg
import os
from datetime import datetime, timedelta



def get_dates_between(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    formatted_dates = []

    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y%m%d')
        formatted_dates.append(formatted_date)
        current_date += timedelta(days=1)
    
    return formatted_dates

def decrypt_file(gpg_file, output_file):
    gpg = gnupg.GPG(binary='/Users/simi/Documents/startups/turntablecharts/datapipeline/gpnug/bin/gpg')
    with open(gpg_file, 'rb') as f:
        decrypted_data = gpg.decrypt_file(f, passphrase=GPG_PASSPHRASE)

        if decrypted_data.ok:
            print('Decrypting ~ '+gpg_file)
            with open(output_file, 'wb') as outfile:
                outfile.write(decrypted_data.data)
            print('Decrypting completed ~ '+gpg_file)
        else:
            print("Decryption failed:", decrypted_data.status)

def download_files(files):
    print('Connecting to FTP')
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    ftp.encoding = "utf-8"
    print('FTP - welcome ~ '+ftp.getwelcome())

    for i in range(0, len(files)):
        filename = files[i]
        print("Downloading ~ "+filename)
        with open(filename, 'wb') as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
        print("Download completed for ~ "+filename)

        if filename.startswith('audiomack'):
            decrypt_file(filename, filename[:-4])


def generate_file_names(file_dates):
    result = []
    for i in range(0, len(file_dates)):
        #boomplay_name = "Boomplay_NG_"+file_dates[i]+'.csv'
        audiomack_name = 'audiomack_streams_'+file_dates[i]+'.csv.asc'

        #result.append(boomplay_name)
        result.append(audiomack_name)
    return result


def get_files(start_date, end_date):
    download_files(generate_file_names(get_dates_between(start_date, end_date)))
    print('Download completed...')


if __name__=="__main__":
    get_files('2023-07-21', '2023-07-22')

