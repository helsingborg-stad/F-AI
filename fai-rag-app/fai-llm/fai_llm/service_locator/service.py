from fai_llm.service_locator.model import Services


class ServiceLocator:
    services: Services

    def __init__(self):
        self.services = Services()


global_locator = ServiceLocator()
