from abc import ABCMeta, abstractmethod


class Saveable:

    @abstractmethod
    def save_settings(self):
        """
        This method is an absract method to be implemented to savable object that can save the current state of the object.
        """
        pass

    @abstractmethod
    def load_settings(self):
        """
        This method is an absract method to be implemented to savable object that can load a state of the object.
        """
        pass
