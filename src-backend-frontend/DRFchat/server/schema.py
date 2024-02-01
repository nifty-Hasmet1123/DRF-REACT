from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import ServerSerializer, ChannelSerializer

def open_api_parameter(name: str, parameter_type: str, description: str) -> OpenApiParameter:
    """
    Create an OpenAPI parameter definition.

    Args:
        name (str): The name of the parameter.
        parameter_type (str): The data type of the parameter.
        description (str): A description of the parameter.

    Returns:
        OpenApiParameter: An OpenAPI parameter object with the specified properties.
    """
    return OpenApiParameter(
        name = name,
        type = OpenApiTypes[parameter_type],
        location = OpenApiParameter.QUERY,
        description = description
    )

def generate_server_list_docs():
    """
    Generate OpenAPI documentation for the server list endpoint.

    Returns:
        dict: OpenAPI documentation containing response and parameter definitions 
        for the server list endpoint.
    """
    parameters = [
        open_api_parameter("category", "STR", "Category of servers to retrieve"),
        open_api_parameter("qty", "INT", "Number of servers to retrieve"),
        open_api_parameter("by_user", "BOOL", "Filter servers by the current authenticated user(True/False)"),
        open_api_parameter("server_id", "INT", "Include server by id"),
        open_api_parameter("number_of_members", "BOOL", "Include the number of members for each server in the response")
    ]

    return extend_schema(
        responses = ServerSerializer(many = True),
        parameters = parameters
    )

server_list_docs = generate_server_list_docs()
