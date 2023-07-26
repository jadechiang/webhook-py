from abc import abstractmethod, ABC


class WebhookRepository(ABC):
    @abstractmethod
    def get_webhooks(self):
        pass

    @abstractmethod
    def find_by_id(self, webhook_id):
        pass

    @abstractmethod
    def remove(self, webhook_id):
        pass
