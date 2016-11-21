from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account

        # fields that you want to send to the Client except for ones defined
        # above with their required value set to False
        fields = ('id', 'email', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password', 'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.email = validated_data.get('email', instance.email)
            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            # update user's session authentication hash so he/she doesn't
            # have to login on their next request

            update_session_auth_hash(self.context.get('request'), instance)
            return instance
