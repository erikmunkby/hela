from abc import ABC, abstractmethod


class BaseDataType(ABC):
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def _spark_type(self):
        raise NotImplementedError

    @abstractmethod
    def _glue_type(self):
        raise NotImplementedError

    @abstractmethod
    def _json_type(self):
        raise NotImplementedError

    @abstractmethod
    def _bigquery_type(self):
        raise NotImplementedError

    def _desc_(self) -> str:
        return {'name': self.name, 'type': 'BaseDataType', 'desc': self.description}
