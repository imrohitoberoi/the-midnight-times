class MultiSerializerClassViewSetMixin:
    """
    Multiple Serializers can be defined for a ViewSet using this Mixin.
    serializer_classes:
        takes a dict as input with actions defined as keys and the respective serializer to use as their values
    """
    serializer_classes = None

    def get_serializer_class(self):
        if hasattr(self, 'action'):
            return self.serializer_classes.get(self.action)
