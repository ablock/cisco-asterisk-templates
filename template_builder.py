from jinja2 import FileSystemLoader, Environment
import uuid

BASE_OCTETS = '192.168.19'
ASTERISK_SERVER_IP = f"{BASE_OCTETS}.202"
EXTENSION_PERMIT_IP = f"{BASE_OCTETS}.0"
BASE_EXTENSION = 100
SECOND_EXTENSION_NUMBER_JUMP = 10
INTERCOM_EXTENSION_NUMBER_JUMP = 300

templateLoader = FileSystemLoader(searchpath='./templates')
templateEnv = Environment(loader=templateLoader)

sip_template = "sip_custom_post.conf.template"
template = templateEnv.get_template(sip_template)

sip_template_data = {
    'second_extension_add': SECOND_EXTENSION_NUMBER_JUMP,
    'intercom_extension_add': INTERCOM_EXTENSION_NUMBER_JUMP,
    'base_extensions': [ 101, 102, 103, 104, 105, 106, 107 ],
    'permit_ip': EXTENSION_PERMIT_IP
}
outputText = template.render(sip_template_data)  # this is where to put args to the template renderer

with open('./build/sip_custom_post.conf', 'w') as f:
    f.write(outputText)

sepmac_template = "sepmac.cnf.xml.template"
template = templateEnv.get_template(sepmac_template)

sepmac_template_data = [
    {
        'mac_address': 'ac7e8a2bfaf9',
        'base_extension': 101,
        'base_extension_secret': 'MW]euuMj4oZtf7@RKMtFuiqGXfBV9a',
        'phone_label': 'Kitchen'
    },
    {
        'mac_address': '00425ac6268b',
        'base_extension': 102,
        'base_extension_secret': '2txddXTGJtTwFei4bokoGYsz3UsE',
        'phone_label': 'Master B/R'
    },
    {
        'mac_address': 'ac7e8a2bf1c1',
        'base_extension': 103,
        'base_extension_secret': 'JzmqC2y6XnDHBAaoDXxHfVWvnbT7sT',
        'phone_label': 'Office'
    },
    {
        'mac_address': 'ac7e8a2bf1bd',
        'base_extension': 104,
        'base_extension_secret': 'a79360e7d58575262508ab5a86282108',
        'phone_label': 'Lower TV'
    },
    {
        'mac_address': '38205618b1fb',
        'base_extension': 105,
        'base_extension_secret': '13aa4d2180ab9e8c1af2756c7169152d',
        'phone_label': 'Lower B/R'
    },
    {
        'mac_address': '38205618b21b',
        'base_extension': 106,
        'base_extension_secret': '004d89ac8b08585c43ccc37b17cc320b',
        'phone_label': 'Guest B/R'
    },
    {
        'mac_address': 'ac7e8a2bedc0',
        'base_extension': 107,
        'base_extension_secret': 'e89f169dbe7ffe40c6e066cb82e7ba6b',
        'phone_label': 'TBD'
    }
]

for dataset in sepmac_template_data:
    dataset['guid'] = uuid.uuid1()
    dataset['server_ip'] = ASTERISK_SERVER_IP
    dataset['second_extension'] = dataset['base_extension'] + SECOND_EXTENSION_NUMBER_JUMP
    dataset['intercom_extension'] = dataset['base_extension'] + INTERCOM_EXTENSION_NUMBER_JUMP
    outputText = template.render(dataset)  # this is where to put args to the template renderer

    filename = 'SEP' + dataset['mac_address'].upper() + '.cnf.xml'
    with open('./build/' + filename, 'w') as f:
        f.write(outputText)
