# Get config via pyyaml
import yaml

list_login_data = [
    {
        'celonis_url' : 'some.celonis.cloud',
        'celonis_api_token': '1234567890',
        'id_or_name_of_data_pool': 'abcd12-and-so-on',
        'sftp_hostname': 'sftp.host.name',
        'sftp_username': 'admin',
        'sftp_password': 'password',
        'sftp_location': 'public',
        'sftp_file': 'filename',
    }
]

# write
# TODO: remove after creation:
#with open("logindata.yaml", 'w') as yamlfile:
#    data = yaml.dump(list_login_data, yamlfile)
#    print("Write successful")


with open("logindata.yaml", "r") as yamlfile:
    list_login_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    # TODO: eventually this is not necessary
    dict_login_data = list_login_data[0]
    dld = dict_login_data
    print("Read successful")
print(dld)


# Get files using SFTP
import pysftp

with pysftp.Connection(dld['sftp_hostname'], username=dld['sftp_username'], password=dld['sftp_password']) as sftp:
    with sftp.cd(dld['sftp_location']):             # temporarily chdir to public
        #sftp.put('/my/local/filename')  # upload file to public/ on remote
        sftp.get(dld['sftp_filename'])         # get a remote file


# pandas
# TODO: for test purposes / delete
import pandas as pd

df = pd.read_csv(dld['sftp_filename'])
df.head() #check it

# pycelonis
from pycelonis import get_celonis

celonis = get_celonis()

# ML workbench
login = {
    "celonis_url": "demo.eu-1.celonis.cloud",
    "api_token": "paste_here_your_api_token",
    #The following 2 lines are only necessary when connecting to CPM4.5, not for IBC:
    #"api_id": "paste_here_your_api_id",
    #"username": "paste_here_your_username",
}
celonis_manual = get_celonis(**login)

# push data
data_pool = celonis.pools.find(dld['id_or_name_of_data_pool'])

#
# celonis.pools
data_pool.push_table(df,"table_name", if_exists = 'replace')

