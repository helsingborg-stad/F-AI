from src.modules.notification.protocols.INotificationService import INotificationService


class ConsoleNotificationService(INotificationService):
    async def send(self, recipient: str, payload: str):
        print(f'(ConsoleNotificationService) {recipient=}, {payload=}')
