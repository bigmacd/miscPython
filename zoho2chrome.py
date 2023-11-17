
import argparse
import csv


# In:
# "Password Name","Description","Password URL","SecretData","Notes","CustomData","Tags","Classification","Favorite","TOTP","Folder Name"

# Out:
#name,url,username,password,note

# Parse this:
#"SecretType:Web Account
#User Name:bigmacd
#Password:alqp10ALQP!@
#"

def main(zohofile: str, protonfile: str) -> None:

    first = True
    with open(zohofile, 'r') as infile:

        with open(protonfile, 'w', newline="") as outfile:
            csv_reader = csv.reader(infile)
            csvwriter = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in csv_reader:
                if first:
                    newrow = ['name','url','username','password','note']
                    csvwriter.writerow(newrow)
                    first = False
                else:

                    # build the new row
                    newrow = []
                    newrow.append(row[0]) # name
                    newrow.append(row[2]) # url

                    # secret data
                    items = row[3].split('\n')
                    username = items[1].split(':')[1]
                    password = items[2].split(':')[1]
                    newrow.append(username)
                    newrow.append(password)

                    newrow.append(row[4]) # notes

                    # write data to the CSV file
                    csvwriter.writerow(newrow)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--zohofile", help="Name of export Zoho file", default='./ZohoVault_export.csv')
    parser.add_argument("--protonfile", help="Name of file to be imported", default='./protonpassimportfile.csv')
    args = parser.parse_args()

    main(args.zohofile, args.protonfile)
