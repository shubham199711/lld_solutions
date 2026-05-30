from abc import ABC, abstractmethod

class ETLPipeline(ABC):

    def run(self):
        data = self.extract()
        transformed = self.transform(data)
        self.load(transformed)

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, data):
        pass

class SalesETL(ETLPipeline):

    def extract(self):
        return [1, 2, 3]

    def transform(self, data):
        return [x * 2 for x in data]

    def load(self, data):
        print(data)

SalesETL().run()