# Create your views here.
from rest_framework import viewsets

from app.models import Person, PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

