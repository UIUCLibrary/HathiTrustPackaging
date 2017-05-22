import abc


class AbsComponentTesterFactory(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def technical_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def metadata_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def completeness_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def naming_checker():
        pass


class AbsPackageFactory(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def all_components_checker():
        pass


class AbsValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, path):
        pass

    @staticmethod
    @abc.abstractmethod
    def validator_name():
        pass