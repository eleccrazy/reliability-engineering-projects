locals {
  vm_map = {
    "app-1"   = { role = "app", public_ip = false, private_ip = "10.0.1.4" }
    "app-2"   = { role = "app", public_ip = false, private_ip = "10.0.1.7" }
    "lb-db"   = { role = "load_balancer", public_ip = true, private_ip = "10.0.1.5" }
    "monitor" = { role = "monitoring", public_ip = true, private_ip = "10.0.1.6" }
  }
}

# Configure the Azure provider
provider "azurerm" {
  features {}
  # Use the subscription ID from the variable
  subscription_id = var.subscription_id
}

# Create a resource group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

# Create a virtual network
resource "azurerm_virtual_network" "main" {
  name                = "main-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
}

# Create a subnet within the virtual network
resource "azurerm_subnet" "main" {
  name                 = "main-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create a static public IP address for each VM that requires it
resource "azurerm_public_ip" "vm" {
  for_each = {
    for name, config in local.vm_map : name => config if config.public_ip
  }

  name                = "pubip-${each.key}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Basic"
}

# Creaete a network interface card (NIC) for each VM
resource "azurerm_network_interface" "vm" {
  for_each = local.vm_map

  name                = "nic-${each.key}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    private_ip_address            = each.value.private_ip
    public_ip_address_id          = each.value.public_ip ? azurerm_public_ip.vm[each.key].id : null
  }
    depends_on = [
        azurerm_subnet.main,
        azurerm_public_ip.vm
    ]
}

# NSG to allow SSH, HTTP, and HTTPS traffic
resource "azurerm_network_security_group" "main" {
  name                = "main-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "allow_ssh"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow_http"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow_https"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    role = "shared"
  }
}

# Associate the network security group with the subnet
resource "azurerm_subnet_network_security_group_association" "main" {
  subnet_id                 = azurerm_subnet.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_linux_virtual_machine" "vm" {
  for_each                        = local.vm_map
  name                            = each.key
  location                        = var.location
  resource_group_name             = azurerm_resource_group.main.name
  size                            = var.vm_size
  admin_username                  = var.admin_username
  network_interface_ids           = [azurerm_network_interface.vm[each.key].id]
  disable_password_authentication = true

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.ssh_public_key_path)
  }

  os_disk {
    name                 = "${each.key}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  tags = {
    environment = "demo"
    role        = each.value.role
  }

  depends_on = [azurerm_network_interface.vm]
}
