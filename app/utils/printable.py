class Printable:
    def __repr__(self):
        return f"<{self.__class__.__name__}({vars(self)})>"
