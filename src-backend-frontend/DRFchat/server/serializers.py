from rest_framework import serializers
from .models import Server, Channel
from drf_spectacular.utils import extend_schema_field

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Server model.

    This serializer is used to convert Server model instances into JSON format and vice versa.
    It includes additional functionality for serializing the 'num_members' field, which is not
    directly part of the main Server model.

    Attributes:
        channel_server: A nested serializer for the 'channel_server' field.
        num_members: A field that is not part of the main model and is calculated using the
            'get_num_members' method.

    Meta:
        model: The Server model to be serialized.
        exclude: Fields to be excluded from the serialization (e.g., 'member').

    Methods:
        get_num_members(self, obj): A method that calculates the 'num_members' field. It should
        follow the naming convention 'get_<name-of-the-query.annotate>' used in the views.
        to_representation(self, instance): An instance method that is used for customizing the
        serialized output based on the 'num_members' context variable.
    """
    
    channel_server = ChannelSerializer(many=True)

    num_members = serializers.SerializerMethodField()

    class Meta:
        model = Server
        exclude = ("member", )

    @extend_schema_field(serializers.IntegerField)
    def get_num_members(self, obj):
        """
        Calculate the 'num_members' field for a server instance.

        This method calculates the 'num_members' field based on the value stored in the 'num_members'
        attribute of the server instance.

        Args:
            obj: The Server instance for which 'num_members' is calculated.

        Returns:
            int or None: The calculated 'num_members' value, or None if not available.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Customize the serialized output based on the 'num_members' context variable.

        This method is used to customize the serialized output by removing the 'num_members' field
        if it is not requested in the context.

        Args:
            instance: The Server instance to be serialized.

        Returns:
            dict: The serialized representation of the Server instance.
        """
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")

        if not num_members:
            data.pop("num_members", None)
        return data
    

# from rest_framework import serializers
# from .models import Server, Category, Channel
# from drf_spectacular.utils import extend_schema_field

# class ChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Channel
#         fields = "__all__"

# class ServerSerializer(serializers.ModelSerializer):
#     channel_server = ChannelSerializer(many = True)

#     # serializing a new column not directly inside the main models
#     # should match the name in the queryParamater inside the views.py
    
#     num_members = serializers.SerializerMethodField()
        
#     class Meta:
#         model = Server
#         exclude = ("member", )

#     @extend_schema_field(serializers.IntegerField)
#     def get_num_members(self, obj): # instance method should follow get_<name-of-the-query .annotate in the views.py>
#         # use a instance method to link the num_members query from the views.py to this serializer class

#         if hasattr(obj, "num_members"):
#             return obj.num_members
#         return None

#     def to_representation(self, instance):
#         # instance method used for 
#         data = super().to_representation(instance)
#         num_members = self.context.get("num_members") # return bool

#         if not num_members:
#             data.pop("num_members", None)
#         return data
