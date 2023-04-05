from rest_framework import serializers

from service_lib.helper import AuthHelper


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        route = f'/internal/api/v1/account/login'
        helper = AuthHelper(route=route)
        helper.post_json(json=validated_data)
        return helper.response_json, helper.status_code


class ProfileSerializer(serializers.Serializer):

    def to_representation(self, instance):
        helper = AuthHelper()
        return {}


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(max_length=16, min_length=4)
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        route = f'/internal/api/v1/account/register'
        helper = AuthHelper(route=route)
        helper.post_json(json=validated_data)
        return helper.response_json, helper.status_code


class RegisterVerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=6)
    otp_token = serializers.CharField(max_length=32, min_length=32)

    def create(self, validated_data):
        route = f'/internal/api/v1/account/register_otp'
        helper = AuthHelper(route=route)
        helper.post_json(json=validated_data)
        return helper.response_json, helper.status_code
