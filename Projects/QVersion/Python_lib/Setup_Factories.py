from Python_lib.Arroyo import Arroyo
from Python_lib.Resource_Manager_Stub import Resource_Manager_Stub
from Python_lib.Thorlabs_PM100U import Thorlabs_PM100U
from Python_lib.Thorlabs_Stub import Thorlabs_Stub
from Python_lib.Toptica_CTL950 import Toptica_CTL950
from Python_lib.Toptica_Stub import Toptica_Stub
from Python_lib.EXFO import EXFO


import pyvisa as visa


class Setup_Stub_Factory:

    def __init__(self):
        pass

    def create_resource_manager(self):
        return Resource_Manager_Stub()

    def create_detector(self, resource_manager, thorlabs):
        return Thorlabs_Stub()

    def create_laser(self):
        return Toptica_Stub()


class Setup_Toptica_Factory:

    def __init__(self):
        pass

    def create_resource_manager(self):
        return visa.ResourceManager()

    def create_detector(self, resource_manager, thorlabs):
        return Thorlabs_PM100U(resource_manager, thorlabs)

    def create_laser(self):
        return Toptica_CTL950()

class Setup_EXFO_Factory:

    def __init__(self):
        pass

    def create_resource_manager(self):
        return visa.ResourceManager()

    def create_detector(self, resource_manager, thorlabs):
        return Thorlabs_PM100U(resource_manager, thorlabs)

    def create_laser(self, resource_manager):
        return EXFO(resource_manager)

class Setup_Arroyo_Factory:

    def __init__(self):
        pass

    def create_resource_manager(self):
        return visa.ResourceManager()

    def create_detector(self, resource_manager, thorlabs):
        return Thorlabs_PM100U(resource_manager, thorlabs)

    def create_laser(self, resource_manager, location_visa):
        return Arroyo(resource_manager, location_visa)