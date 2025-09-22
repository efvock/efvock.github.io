class NullContext:
    def __getattr__(self, *args, **kwargs):
        def wrap(*args, **kwargs):
            return self

        return wrap

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass


NULL_CONTEXT = NullContext()
