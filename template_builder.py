from jinja2 import FileSystemLoader, Environment
import uuid

ASTERISK_SERVER_IP = '192.168.19.202'
SECOND_EXTENSION_ADD = 10
INTERCOM_EXTENSION = 400

templateLoader = FileSystemLoader(searchpath='./templates')
templateEnv = Environment(loader=templateLoader)

sip_template = "sip_custom_post.conf.template"
template = templateEnv.get_template(sip_template)

sip_template_data = {
    'second_extension_add': SECOND_EXTENSION_ADD,
    'intercom_extension': INTERCOM_EXTENSION,
    'base_extensions': [ 101, 102, 103, 104, 105, 106, 107 ]
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
        'base_extension_secret': '',
        'phone_label': 'Kitchen'
    },
    {
        'mac_address': '00425ac6268b',
        'base_extension': 102,
        'base_extension_secret': '',
        'phone_label': 'Library'
    }
]

for dataset in sepmac_template_data:
    dataset['guid'] = uuid.uuid1()
    dataset['server_ip'] = ASTERISK_SERVER_IP
    dataset['second_extension'] = dataset['base_extension'] + SECOND_EXTENSION_ADD
    dataset['intercom_extension'] = INTERCOM_EXTENSION
    outputText = template.render(dataset)  # this is where to put args to the template renderer

    filename = 'SEP' + dataset['mac_address'].upper() + '.cnf.xml'
    with open('./build/' + filename, 'w') as f:
        f.write(outputText)
