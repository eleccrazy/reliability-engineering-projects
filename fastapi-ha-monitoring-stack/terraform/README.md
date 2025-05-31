# Terraform Infrastructure Setup

This module provisions a minimal multi-VM cloud system on Azure using:

- 2 App VMs (FastAPI + NGINX, private only)
- 1 Load Balancer + DB VM (HAProxy + PostgreSQL, public)
- 1 Monitoring VM (Prometheus + Grafana, public)

## Key Features

- Uses shared Virtual Network + Subnet
- Attaches NSG to subnet for SSH, HTTP, HTTPS
- Assigns public IPs conditionally (lb-db, monitor)
- Clean separation of concerns (infrastructure vs config)

## To Use

```bash
cd terraform
terraform init
terraform plan # optional, to review changes
terraform apply

# Follow prompts to confirm
```
## Cleanup
```bash
terraform destroy
```
## Requirements
- Terraform 1.0+
- Azure CLI configured with your account
- Azure subscription with sufficient permissions

## Notes
- Ensure your Azure account has permissions to create VMs, NSGs, and other resources.
- Adjust variables in `variables.tf` as needed for your environment.
- Use `terraform output` to get IPs and other details after deployment.
