from abc import ABC, abstractmethod

class Processor(ABC):
    """
    An abstract base class for file processors.
    """
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    @abstractmethod
    def process(self):
        """
        This method should be implemented by subclasses to handle the specific file type.
        """
        pass
