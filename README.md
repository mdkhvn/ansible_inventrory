
# 📘 Ansible Inventory and sshConfig Generator from vCenter (GitOps Workflow)

This repository automatically generates a static Ansible inventory from VMs in VMware vCenter, using:

- Ansible

- Jinja2 templating

- GitLab CI

- GitOps workflow (auto commit & push)

- python

VM names must end with the `last two octets of the VM’s IP`:


```text
vm-machine-65.40
vm-test-70.21
```

The inventory generator:

- Extracts the IP from VM name → 172.13.65.40

- Cleans VM name → vm-machine

- Appends the domain → vm-machine.test.local

- Organizes VMs into groups based on vCenter folder

- Creates a static output_inventory.yml file

- Commits changes automatically via GitLab CI

- Convert output inventory to config for using sshConfig

## 📁 Repository Structure
```
inventory-generator/
├── ansible.cfg
├── generate_inventory.yml
├── inventory.yml.j2
├── group_vars/
│   └── all.yml
├── requirements.yml
├── .gitlab-ci.yml
└── README.md
└── sshconfvert.py
```
## 🚀 How It Works
#### 1. The Ansible Playbook (generate_inventory.yml)

Uses vmware.vmware.vms to gather all VMs from vCenter, groups them by folder, and renders inventory.yml using inventory.yml.j2.

#### 2. Jinja2 Template (inventory.yml.j2)

Outputs inventory in this structure:
```yaml
all:
  children:
    <folder_name>:
      hosts:
        <vm_name>:

  hosts:
    <vm_name>:
      ansible_host: <ip>
```
#### 3. sshconfvert templating sshConfig
this python script give you two file names, one input ansible inventory and second for output ssh config
```
inventory_file = "inventory.yml"
ssh_config_file = "config"
```
#### 4. GitLab CI (.gitlab-ci.yml)

The pipeline:

- Installs Ansible + VMware collection

- Runs the generator

- Check syntax

- Run the sshconfvert

- Commits any changes to the repo automatically

# 🔧 Configuration

#### 1. Set vCenter credentials using GitLab CI Variables

Go to:
GitLab → Settings → CI/CD → Variables

Add:

| Variable Name  | Description     |
| -------------- | --------------- |
| `VCENTER_HOST` | vCenter FQDN/IP |
| `VCENTER_USER` | Username        |
| `VCENTER_PASS` | Password        |

> [!note]
> These values are not stored in the repo.

#### 2. group_vars/all.yml

Adjust shared settings here:
```
fixed_ip_prefix: "172.13"
domain: "test.local"
vcenter_hostname: "{{ lookup('env', 'VCENTER_HOST') }}"
vcenter_username: "{{ lookup('env', 'VCENTER_USER') }}"
vcenter_password: "{{ lookup('env', 'VCENTER_PASS') }}"
```
# 📦 Requirements
Install the VMware collection:
```
ansible-galaxy collection install vmware.vmware
```
Install Python dependencies:
```
pip install ansible
```
# 🏃 Running Locally

To debug or run locally:
```
ansible-playbook generate_inventory.yml
```
The result will be generated at:
```
inventory.yml
```
# 🤖 GitLab CI Automation

The .gitlab-ci.yml automatically:

#### Inventory Generator Job
1. Runs the playbook

2. Generates inventory.yml

3. Checks if there are changes

4. Commits and pushes them

#### syntax check Job

- Check yml file linting

#### SSH config generator Job

1. Pull config file
2. Replace with new file
3. Git commit and push new file

> [!tip]
>No manual action required.
# 🧩 VM Naming Rules
For IP extraction and hostname generation:
```
<name>-<octet3>.<octet4>
```
Examples:
| VM Name                | Output Hostname             | ansible_host   |
| ---------------------- | --------------------------- | -------------- |
| `vm-machine-65.40`     | `vm-machine.test.local`     | `172.13.65.40` |
| `vm-test-70.21`        | `vm-test.test.local`        | `172.13.70.21` |

# 📬 Support / Improvements

Possible enhancements:

- Multi-level vCenter folder hierarchy

- Additional grouping (dev/stage/prod)

- Direct commit to a central GitOps environment repo

- Automatically regenerate inventory on VM creation events

# 🏁 Summary

This system provides:

✔ Fully automated inventory generation

✔ Clean GitOps workflow

✔ Zero manual updates

✔ vCenter → Ansible bridge

✔ Safe credential handling

✔ Stable, repeatable output