from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.tools.auth import SecretsTokenAuthentication
from back_edesoft.models import User
from back_edesoft.serializers import UserSerializer


@extend_schema(tags=["User"])
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SecretsTokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def create(self, request, *args, **kwargs):
        cpf = request.data.pop("cpf")
        cnpj = request.data.pop("cnpj")
        phone = request.data.pop("phone")
        
        request.data["cpf"] = cpf.replace(".", "").replace("-", "")
        request.data["cnpj"] = cnpj.replace(".", "").replace("-", "").replace("/", "")
        request.data["phone"] = phone.replace("(", "").replace(")", "").replace("-", "")
        
        return super().create(request, *args, **kwargs)
