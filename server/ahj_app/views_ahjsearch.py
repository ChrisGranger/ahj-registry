from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .throttles import WebpageSearchThrottle
from .models import AHJ
from .serializers import AHJSerializer
from .utils import get_multipolygon, get_multipolygon_wkt, get_str_location, \
    filter_ahjs, order_ahj_list_AHJLevelCode_PolygonLandArea, get_location_gecode_address_str


@api_view(['POST'])
@throttle_classes([WebpageSearchThrottle])
def webpage_ahj_list(request):
    """
    Endpoint for the client app's AHJ Search.

    It is similar to to the public API endpoint documented in the API Documentation with these differences in filtering:
        - BuildingCode instead of BuildingCodes
        - ElectricCode instead of ElectricCodes
        - FireCode instead of FireCodes
        - ResidentialCode instead of ResidentialCodes
        - WindCode instead of WindCodes
        - Allows filtering with GeoJSON through the ``FeatureCollection`` parameter.

    See the AHJSearchPageFilter.vue and store.js for more information about how this endpoint is used.
    """
    json_location = get_location_gecode_address_str(request.data.get('Address', None))

    polygon = get_multipolygon(request=request, location=json_location)
    polygon_wkt = None
    if polygon is not None:
        polygon_wkt = get_multipolygon_wkt(multipolygon=polygon)
    str_location = get_str_location(location=json_location)
    ahjs = filter_ahjs(
        AHJName=request.data.get('AHJName', None),
        AHJID=request.data.get('AHJID', None),
        AHJPK=request.data.get('AHJPK', None),
        AHJCode=request.data.get('AHJCode', None),
        AHJLevelCode=request.data.get('AHJLevelCode', None),
        BuildingCode=request.data.get('BuildingCode', []),
        ElectricCode=request.data.get('ElectricCode', []),
        FireCode=request.data.get('FireCode', []),
        ResidentialCode=request.data.get('ResidentialCode', []),
        WindCode=request.data.get('WindCode', []),
        StateProvince=request.data.get('StateProvince', None),
        location=str_location, polygon=polygon_wkt)

    if polygon is not None and str_location is None:
        """
        If a polygon was searched, and a location was not,
        set the Location object returned to represent the center of the polygon.
        """
        polygon_center = polygon.centroid
        json_location = {'Latitude': {'Value': polygon_center[1]}, 'Longitude': {'Value': polygon_center[0]}}

    serializer = AHJSerializer
    paginator = LimitOffsetPagination()
    context = {'is_public_view': request.data.get('use_public_view', False)}
    page = paginator.paginate_queryset(ahjs, request)

    if str_location is not None or polygon is not None:
        """
        Sort the AHJs returned if a location or polygon was searched
        """
        page = order_ahj_list_AHJLevelCode_PolygonLandArea(page)

    payload = serializer(page, many=True, context=context).data

    return paginator.get_paginated_response({
        'Location': json_location,
        'ahjlist': payload
    })


@api_view(['GET'])
def get_single_ahj(request):
    """
    Endpoint to get a single AHJ given an ``AHJPK`` query parameter.
    """
    try:
        ahj = AHJ.objects.get(AHJPK=request.query_params.get('AHJPK'))
        return Response(AHJSerializer(ahj).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
