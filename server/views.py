from rest_framework import viewsets
from rest_framework.response import Response
from .models import Server, Category
from .serializers import ServerSerializer
from rest_framework.status import HTTP_201_CREATED
from rest_framework.exceptions import ValidationError
from django.db.models import Count


class ServerListViewSet(viewsets.ViewSet):
    """
    A viewset for listing and filtering Server objects based on various query parameters.

    Query Parameters:
    - `category` (str): Filter servers by category name.
    - `quantity` (int): Limit the number of servers returned in the response.
    - `by_user` (bool): If true, filter servers associated with the current user.
    - `server_id` (int): Filter servers by a specific server ID.
    - `by_num_member` (bool): If true, annotate each server with the number of associated members.

    This viewset supports multiple filters and annotations to provide flexible server listings.
    The response is a serialized representation of the filtered and/or annotated Server objects.

    Raises:
    - `ValidationError`: If any query parameter has an invalid value or if the server ID does not exist.

    Returns:
    - Response: A serialized list of Server objects matching the query parameters.
    """

    queryset = Server.objects.all()

    def list(self, request):
        category_param = request.query_params.get("category")
        quantity_param = request.query_params.get("quantity")
        by_user_param = request.query_params.get("by_user") == "true"
        server_id_param = request.query_params.get("server_id")
        num_members_param = request.query_params.get("by_num_member") == "true"

        if category_param:
            self.queryset = self.queryset.filter(category__name=category_param)

        if by_user_param:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if num_members_param:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if quantity_param:
            try:
                self.queryset = self.queryset[: int(quantity_param)]
            except ValueError:
                raise ValidationError(detail="Invalid quantity value")

        if server_id_param:
            try:
                self.queryset = self.queryset.filter(id=server_id_param)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {server_id_param} does not exist"
                    )
            except ValueError:
                raise ValidationError("Invalid server id")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": num_members_param}
        )
        return Response(serializer.data)
