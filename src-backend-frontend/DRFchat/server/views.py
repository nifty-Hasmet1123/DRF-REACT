from .models import Server
from .serializers import ServerSerializer
from .schema import server_list_docs
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
     
    def check_if_user_is_login(self, user, request):
        """
        Check if the user is logged in and return the user ID.

        Args:
            user (bool): Indicates whether the user should be checked for login.
            request: The HTTP request object.

        Returns:
            int: The user ID if the user is logged in, or None if not logged in.
        """
        if user and request.user.is_authenticated:
            user_id = request.user.id
        return user_id
        
    def get_query_conditions(self, request):
        """
        Get query conditions based on query parameters from the request.

        Args:
            request: The HTTP request object.

        Returns:
            tuple: A tuple containing the filtered queryset and a flag indicating whether to include the number of members.
        """
        queryset = self.queryset
        category = request.query_params.get("category")
        quantity = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("server_id")
        number_of_members = request.query_params.get("number_of_members") == "true"

        if request.user.is_authenticated:
            # set the by_user to true if user is logged in
            by_user = True 

        if category:
            queryset = queryset.filter(category=category)
        
        if by_user:
            user_id = self.check_if_user_is_login(by_user, request)
            queryset = queryset.filter(member=user_id)
        else:
            raise AuthenticationFailed(detail="Login to access JSON.")

        if number_of_members:
            queryset = self.queryset.annotate(num_members=Count("member"))

        if quantity:
            queryset = self.queryset[:int(quantity)]

        if by_server_id:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            
            try:
                queryset = self.queryset.filter(id=by_server_id)

                if not queryset.exists():
                    raise ValidationError(detail=f"Server with ID `{by_server_id}` not found")
            except ValueError as e:
                raise ValidationError({"valueError": f"{e}" })

        return queryset, number_of_members

    @server_list_docs
    def list(self, request):
        """
        List and filter server objects based on query parameters.

        This method handles HTTP GET requests to retrieve a list of server objects and allows for optional filtering based on
        various query parameters. It leverages the Spectacular schema for accurate API documentation.

        Args:
            self: The instance of the viewset.
            request: The HTTP request object.

        Returns:
            Response: A Response object containing the serialized server data.

        Raises:
            AuthenticationFailed: If the user is not authenticated, an exception is raised.

        Query Parameters:
            - `category` (str): Category of servers to retrieve.
            - `qty` (int): Number of servers to retrieve.
            - `by_user` (bool): Filter servers by the current authenticated user (True/False).
            - `server_id` (int): Include a server by its ID.
            - `number_of_members` (bool): Include the number of members for each server in the response.
        """
        queryset, number_members = self.get_query_conditions(request)
        serializer = ServerSerializer(queryset, many=True, context={"num_members": number_members})
        return Response(serializer.data)
