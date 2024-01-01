from sqlalchemy import or_

from app.utils.printable import Printable


class Filter(Printable):
    def __init__(self, cls, *args, **filters) -> None:
        if len(args) == 1 and isinstance(args[0], dict):
            filters.update(args[0])
        self.conditions = []
        self.cls = cls
        # if "deleted_at" not in filters:
        #     filters["deleted_at"] = None
        for key, value in filters.items():
            attribute_parts = key.split(".")
            if len(attribute_parts) == 2 and self.is_relationship(attribute_parts[0]):
                self.handle_relationship(attribute_parts, value)
            elif hasattr(cls, key):
                self.handle_direct_attribute(key, value)

    def is_relationship(self, attr):
        return hasattr(getattr(self.cls, attr, None), 'property')

    def handle_direct_attribute(self, key, value):
        """Handle filters for direct attributes."""
        if isinstance(value, list):
            # If the value is a list, create an OR condition for each value in the list
            conditions = [getattr(self.cls, key) == v for v in value]
            self.conditions.append(or_(*conditions))
        else:
            # If the value is not a list, create a simple equality filter
            self.conditions.append(getattr(self.cls, key) == value)

    def handle_relationship(self, key_parts, value):
        """Handle filters for relationships."""
        relationship_name, attribute_name = key_parts
        relationship_attr = getattr(self.cls, relationship_name)

        if relationship_attr.property.uselist:
            if isinstance(value, list):
                # Create an OR condition for each value in the list
                conditions = [relationship_attr.any(
                    **{attribute_name: v}) for v in value]
                self.conditions.append(or_(*conditions))
            else:
                # Create a condition where any member of the collection matches the criterion
                condition = relationship_attr.any(**{attribute_name: value})
                self.conditions.append(condition)
        else:
            if isinstance(value, list):
                # For a one-to-one relationship with a list of values, use OR
                conditions = [getattr(
                    relationship_attr.property.mapper.class_, attribute_name) == v for v in value]
                self.conditions.append(or_(*conditions))
            else:
                # For one-to-one relationships, directly compare the attribute
                related_cls = relationship_attr.property.mapper.class_
                self.conditions.append(
                    getattr(related_cls, attribute_name) == value)
