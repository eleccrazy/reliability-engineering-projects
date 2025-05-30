output "vm_public_ips" {
  description = "Public IP addresses for all VMs"
  value = {
    for vm_name, ip in azurerm_public_ip.vm :
    vm_name => ip.ip_address
  }
}
