class MultiSerializerClassViewSetMixin:
    """
    A mixin to use with DRF ViewSets for supporting multiple serializers based on actions.
    """
    serializer_classes = None

    def get_serializer_class(self):
        if hasattr(self, 'action'):
            return self.serializer_classes.get(self.action)
