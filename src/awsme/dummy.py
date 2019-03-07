class DummyCloudWatch:

    def log(self, *args, **kwargs) -> None:
        pass

    def flush(self, complete: bool = True) -> None:
        pass
