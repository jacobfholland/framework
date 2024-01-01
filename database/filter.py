from sqlalchemy.orm import contains_eager


class Filter:
    def __init__(self, cls, **data) -> None:
        self.filter = []
        self.cls = cls

        for key, value in data.items():
            attribute_parts = key.split(".")
            if len(attribute_parts) == 2 and self.is_relationship(attribute_parts[0]):
                # Handle relationship attributes.
                self.handle_relationship(attribute_parts, value)
            elif hasattr(cls, key):
                # Handle direct attributes.
                self.filter.append(getattr(cls, key) == value)
        print(self.filter)
        for filter in self.filter:
            print(vars(filter), "\n")

    def is_relationship(self, attr):
        return hasattr(getattr(self.cls, attr, None), 'property')

    def handle_relationship(self, key_parts, value):
        """Handle filters for relationships."""
        relationship_name, attribute_name = key_parts
        relationship_attr = getattr(self.cls, relationship_name)

        # Check if it's a collection relationship (one-to-many or many-to-many)
        if relationship_attr.property.uselist:
            # Create a condition where any member of the collection matches the criterion
            condition = relationship_attr.any(**{attribute_name: value})
            self.filter.append(condition)
        else:
            # For one-to-one relationships, directly compare the attribute.
            related_cls = relationship_attr.property.mapper.class_
            self.filter.append(getattr(related_cls, attribute_name) == value)
