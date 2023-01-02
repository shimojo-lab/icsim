import textwrap

# hosts = [{
#     'host_name': 'h1', 
#     'host_ip': '192.168.2.2',
# }]

def gen_ssh_config_file(hosts, pubkey_filename):
    config_file_content = ""
    for host in hosts:
        host_config = f"""
        Host {host['host_name']}
            User user
            identitiesOnly yes
            HostName {host['host_ip']}
            identityFile {pubkey_filename}
        """
        config_file_content += host_config
    return textwrap.dedent(config_file_content)[1:-1]

def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    