from collections import OrderedDict
import datetime


from django.apps import apps
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, throttle_classes, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .throttles import MemberRateThrottle
from rest_framework.response import Response

from .authentication import APITokenAuth
from .models import APIToken
from .serializers import AHJSerializer
from .utils import order_ahj_list_AHJLevelCode_PolygonLandArea, filter_ahjs, get_str_location, \
    get_public_api_serializer_context, get_ob_value_primitive, get_str_address, get_location_gecode_address_str, check_address_empty


def deactivate_expired_api_tokens():
    """
    Sets the ``is_active`` field to ``False`` for APIToken rows whose ``expires`` date has passed.
    """
    APIToken.objects.filter(is_active=True, expires__lte=timezone.now()).update(is_active=False)


@api_view(['POST'])
@authentication_classes([APITokenAuth])
@permission_classes([IsAuthenticated])
@throttle_classes([MemberRateThrottle])
def ahj_list(request):
    """
    Public API endpoint for AHJ Search. See the API documentation for more information.
    """
    str_location = None
    try:
        ob_location = request.data.get('Location', None)
        if ob_location is not None:
            str_location = get_str_location(ob_location)
    except (TypeError, KeyError, ValueError) as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    # Process sent Address object if no location provided
    try:
        if ob_location is None:
            ob_address = request.data.get('Address', None)
            if ob_address is not None:
                str_address = get_str_address(ob_address)
                json_location = get_location_gecode_address_str(str_address)
                str_location = get_str_location(location=json_location)
    except TypeError:
        return Response('Invalid Address, all values must be strings', status=status.HTTP_400_BAD_REQUEST)
    ahjs = filter_ahjs(
        AHJName=get_ob_value_primitive(request.data, 'AHJName', throw_exception=False),
        AHJID=get_ob_value_primitive(request.data, 'AHJID', throw_exception=False),
        AHJCode=get_ob_value_primitive(request.data, 'AHJCode', throw_exception=False),
        AHJLevelCode=get_ob_value_primitive(request.data, 'AHJLevelCode', throw_exception=False),
        BuildingCode=get_ob_value_primitive(request.data, 'BuildingCodes', throw_exception=False, exception_return_value=[]),
        ElectricCode=get_ob_value_primitive(request.data, 'ElectricCodes', throw_exception=False, exception_return_value=[]),
        FireCode=get_ob_value_primitive(request.data, 'FireCodes', throw_exception=False, exception_return_value=[]),
        ResidentialCode=get_ob_value_primitive(request.data, 'ResidentialCodes', throw_exception=False, exception_return_value=[]),
        WindCode=get_ob_value_primitive(request.data, 'WindCodes', throw_exception=False, exception_return_value=[]),
        StateProvince=get_ob_value_primitive(request.data, 'StateProvince', throw_exception=False),
        location=str_location)

    serializer = AHJSerializer
    paginator = LimitOffsetPagination()
    context = get_public_api_serializer_context()
    page = paginator.paginate_queryset(ahjs, request)

    if str_location is not None:
        page = order_ahj_list_AHJLevelCode_PolygonLandArea(page)
    payload = serializer(page, many=True, context=context).data

    # Mimics implementation of LimitOffsetPagination.get_paginated_response(data)
    return Response(OrderedDict([
        ('count', paginator.count),
        ('next', paginator.get_next_link()),
        ('previous', paginator.get_previous_link()),
        ('AuthorityHavingJurisdictions', payload)  # Match Array name of AuthorityHavingJurisdiction
    ]))


@api_view(['POST'])
@authentication_classes([APITokenAuth])
@permission_classes([IsAuthenticated])
@throttle_classes([MemberRateThrottle])
def ahj_geo_location(request):
    """
    Public API endpoint for searching AHJs by Location.
    This endpoint is from AHJ Registry 1.0, and the AHJ Registry 2.0 ``ahj_list`` endpoint should be used instead.
    """
    ahjs_to_search = request.data.get('ahjs_to_search', None)

    # If sent an Orange Button Address containing Location
    ob_location = request.data.get('Location', None)
    if ob_location is None:
        # If sent an Orange Button Location
        ob_location = request.data

    try:
        str_location = get_str_location(ob_location)
        if (str_location == None):
            return Response('Location field(s) cannot be empty.', status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, KeyError, ValueError) as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    ahjs = filter_ahjs(location=str_location)

    # Only include ahjs whose AHJID is in ahjs_to_search, if ahjs_to_search was given
    if ahjs_to_search is None:
        ahj_result = [ahj for ahj in ahjs]
    else:
        ahj_result = [ahj for ahj in ahjs if ahj.AHJID in ahjs_to_search]
    ahj_result = order_ahj_list_AHJLevelCode_PolygonLandArea(ahj_result)
    return Response(AHJSerializer(ahj_result, many=True, context=get_public_api_serializer_context()).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([APITokenAuth])
@permission_classes([IsAuthenticated])
@throttle_classes([MemberRateThrottle])
def ahj_geo_address(request):
    """
    Public API endpoint for searching AHJs by Address.
    This endpoint is from AHJ Registry 1.0, and the AHJ Registry 2.0 ``ahj_list`` endpoint should be used instead.
    """
    ahjs_to_search = request.data.get('ahjs_to_search', None)

    ob_address = request.data.get('Address', None)
    if ob_address is None:
        ob_address = request.data

    try:
        str_address = get_str_address(ob_address)
        if (check_address_empty(str_address) == None):
            return Response('Address field(s) cannot be empty.', status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response('Invalid Address, all values must be strings', status=status.HTTP_400_BAD_REQUEST)

    ob_location = get_location_gecode_address_str(str_address)
    str_location = get_str_location(ob_location)

    ahjs = filter_ahjs(location=str_location)

    # Only include ahjs whose AHJID is in ahjs_to_search, if ahjs_to_search was given
    if ahjs_to_search is None:
        ahj_result = [ahj for ahj in ahjs]
    else:
        ahj_result = [ahj for ahj in ahjs if ahj.AHJID in ahjs_to_search]
    ahj_result = order_ahj_list_AHJLevelCode_PolygonLandArea(ahj_result)
    return Response(AHJSerializer(ahj_result, many=True, context=get_public_api_serializer_context()).data, status=status.HTTP_200_OK)
