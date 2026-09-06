from rest_framework.response import Response
from rest_framework.views import APIView

from .dao import CitaDAO
from .serializers import CitaSerializer


class CitasActivasAPIView(APIView):
    """Devuelve las citas solicitadas o confirmadas usando la capa DAO."""

    def get(self, request):
        citas = CitaDAO.listar_activas()
        return Response(CitaSerializer(citas, many=True).data)
