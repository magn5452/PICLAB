import pyvisa as visa

resource_manager = visa.ResourceManager()
resource_list = resource_manager.list_resources()
print(resource_list)
