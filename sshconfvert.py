import yaml

# Load the Ansible inventory file
def load_inventory(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Convert inventory data to SSH config
def generate_ssh_config(inventory, static_content=None):
    ssh_config_lines = []
    
    # Add static content if provided
    if static_content:
        ssh_config_lines.append(f"# Static Content Start\n{static_content}\n# Static Content End\n\n")

    if 'hosts' in inventory['all']:
        for host, data in inventory['all']['hosts'].items():
            ssh_config_lines.append(f"Host {host}\n")
            ssh_config_lines.append(f"Hostname {data['ansible_host']}\n")
            ssh_config_lines.append(f"Port {data.get('ansible_port', 22)}\n")  # Default to port 22 if not specified
            ssh_config_lines.append("###\n")
    
    return ssh_config_lines

# Write the SSH config to a file
def write_ssh_config(file_path, ssh_config_lines):
    with open(file_path, 'w') as file:
        file.write("".join(ssh_config_lines))
    print(f"SSH config file written to: {file_path}")

# Main function to run the script
def main():
    inventory_file = "inventory.yml"  # Path to your Ansible inventory
    ssh_config_file = "config"    # Path to the SSH config output file

    static_content = """
### Update with Gitlab CI - ansible-inventory Devops project pipeline ###
Include config.d/* 
IdentityFile ~/.ssh/id_rsa
addKeysToAgent yes
StrictHostKeyChecking no
UserKnownHostsFile=/dev/null
User devops
    """
    # Load the Ansible inventory
    inventory = load_inventory(inventory_file)

    # Generate SSH config lines
    ssh_config = generate_ssh_config(inventory, static_content)

    # Write SSH config to the file
    write_ssh_config(ssh_config_file, ssh_config)

if __name__ == "__main__":
    main()