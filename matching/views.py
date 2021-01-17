from .models import MatchingEntry
from .serializers import MatchingEntrySerializer
from rest_framework import generics, mixins, permissions


class MyMatchingEntryDetail(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    queryset = MatchingEntry.objects.all()
    serializer_class = MatchingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = generics.get_object_or_404(queryset, user=self.request.user)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
