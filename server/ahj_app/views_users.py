import json
import os

from djoser.conf import settings as djoser_settings
from djoser.compat import get_user_email
from django.utils.timezone import now
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.conf import settings

from .authentication import WebpageTokenAuth
from .models import AHJUserMaintains, AHJ, User, APIToken, Contact, WebpageToken, PreferredContactMethod, SunspecAllianceMemberDomain, AHJOfficeDomain
from .permissions import IsSuperuser
from .serializers import UserSerializer, ContactSerializer
from djoser.views import UserViewSet, TokenCreateView, TokenDestroyView
from djoser import signals
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings

from .utils import get_enum_value_row, filter_dict_keys, ENUM_FIELDS

class ActivateUser(UserViewSet):

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        maintainedAHJ = self.get_maintained_ahj(user.Email)
        if (maintainedAHJ):
            AHJUserMaintains.objects.create(AHJPK=maintainedAHJ, UserID=user, MaintainerStatus=1)
        user.is_active = True
        user.MemberID = self.get_member_id(user.Email)
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.confirmation(self.request, context).send(to)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Returns the sunspec alliance member id if domain matches a registered member. Returns None otherwise.
    def get_member_id(self, email):
        domain = SunspecAllianceMemberDomain.objects.filter(Domain=email[email.index('@') + 1 : ])
        return domain[0].MemberID if domain.exists() else None
    
    # Returns the AHJ that corresponds to the domain of the user's email. Returns None if no AHJ matches.
    def get_maintained_ahj(self, email):
        domain = AHJOfficeDomain.objects.filter(Domain=email[email.index('@') + 1 : ]).first()
        return AHJ.objects.filter(AHJID=domain.AHJID.AHJID).first() if domain else None

class ConfirmPasswordReset(UserViewSet):

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        """
        Overridden Djoser endpoint for sending a rest password confirmation email.
        This was overridden to let users activate their account by resetting their password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.is_active = True # The purpose of overwriting this endpoint is to set users as active if performing password reset confirm.
        serializer.user.save()           # The user had to access their email account to perform a password reset.

        if djoser_settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            djoser_settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def get_active_user(request):
    """
    Returns the user of the requesting user authenticated by their WebpageToken.
    """
    return Response(UserSerializer(request.user, context={'is_public_view': False}).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_user(request, username):
    """
    Function view for getting a user with the specified username.
    """
    context = {'is_public_view': True}
    if request.auth is not None and request.user.Username == username:
        context['is_public_view'] = False
    try:
        user = User.objects.get(Username=username)
        return Response(UserSerializer(user, context=context).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def user_update(request):
    """
    Update the user profile associated with the requesting user. These are the fields that can be changed:

    ======= ======
    Table   Fields
    ======= ======
    User    Username, PersonalBio, URL, CompanyAffiliation
    Contact FirstName, LastName, URL, WorkPhone, PreferredContactMethod, Title
    ======= ======

    """
    changeable_user_fields = {'Username', 'PersonalBio', 'URL', 'CompanyAffiliation'}
    changeable_contact_fields = {'FirstName', 'LastName', 'URL', 'WorkPhone', 'PreferredContactMethod', 'Title'}
    user_data = filter_dict_keys(request.data, changeable_user_fields)
    contact_data = filter_dict_keys(request.data, changeable_contact_fields)
    for field in ENUM_FIELDS.intersection(contact_data.keys()):
        contact_data[field] = get_enum_value_row(field, contact_data[field])
    user = request.user
    User.objects.filter(UserID=user.UserID).update(**user_data)
    Contact.objects.filter(ContactID=user.ContactID.ContactID).update(**contact_data)
    return Response('Success', status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def create_api_token(request): 
    try:
        user = request.user
        with transaction.atomic():
            APIToken.objects.filter(user=user).delete()
            api_token = APIToken.objects.create(user=user, is_active=False)
        return Response({'auth_token': api_token.key}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated, IsSuperuser])
def set_ahj_maintainer(request):
    """
    Endpoint for Superusers to assign a user as a data maintainer of an AHJ.
    Expects a ``Username`` and ``AHJPK``.
    """
    try:
        username = request.data['Username']
        ahjpk = request.data['AHJPK']
        user = User.objects.get(Username=username)
        ahj = AHJ.objects.get(AHJPK=ahjpk)
        maintainer_record = AHJUserMaintains.objects.filter(AHJPK=ahj, UserID=user)
        if maintainer_record.exists():
            maintainer_record.update(MaintainerStatus=True)
        else:
            AHJUserMaintains.objects.create(UserID=user, AHJPK=ahj, MaintainerStatus=True)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated, IsSuperuser])
def remove_ahj_maintainer(request):
    """
    Endpoint for Superusers to revoke a user as a data maintainer of an AHJ.
    Expects a ``Username`` and ``AHJPK``.
    """
    try:
        username = request.data['Username']
        ahjpk = request.data['AHJPK']
        user = User.objects.get(Username=username)
        ahj = AHJ.objects.get(AHJPK=ahjpk)
        AHJUserMaintains.objects.filter(AHJPK=ahj, UserID=user).update(MaintainerStatus=False)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
