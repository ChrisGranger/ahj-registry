from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .authentication import WebpageTokenAuth
from .models import AHJ,Edit
from .serializers import AHJSerializer, EditSerializer
from .utils import get_multipolygon, get_multipolygon_wkt, get_str_location, \
    filter_ahjs, order_ahj_list_AHJLevelCode_PolygonLandArea, get_location_gecode_address_str


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def webpage_ahj_list(request):
    """
    Functional view for the WebPageAHJList
    """
    # By default select all the AHJs
    # filter by the latitude, longitude
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


def translate(s):
    if s == "AHJDocumentSubmissionMethodUse":
        return "DocumentSubmissionMethod"
    if s == "AHJPermitIssueMethodUse":
        return "PermitIssueMethod"
    return s

def translate_id(s):
    if s == "AHJDocumentSubmissionMethodUse":
        return "Use"
    if s == "AHJPermitIssueMethodUse":
        return "Use"
    return s

@api_view(['GET'])
def get_single_ahj(request):
    """
    Endpoint to get a single ahj given an AHJPK
    """
    AHJPK = request.GET.get('AHJPK')
    ahj = AHJ.objects.filter(AHJPK=AHJPK)
    context = {'fields_to_drop': []}
    serialized_ahj = AHJSerializer(ahj, context=context,many=True).data[0]
    r_type = request.query_params.get('view')
    Fields = {"AHJInspection","Contact","FeeStructure","EngineeringReviewRequirement"}
    SearchFields = {"Address", "Location"}
    changed = set()
    if r_type == "latest" or r_type == "latest-accepted":
        query = None
        if r_type == "latest":
            query = EditSerializer(Edit.objects.filter(AHJPK=AHJPK, ReviewStatus="P").order_by('-DateRequested')[:10],many=True).data
        if r_type == "latest-accepted":
            query = EditSerializer(Edit.objects.filter(AHJPK=AHJPK, ReviewStatus="P", EditStatus="A").order_by('-DateRequested')[:10],many=True).data
        for x in query:
            if not (x['SourceColumn'],x['SourceRow']) in changed:
                if x['EditType'] == "U":
                    if x['SourceTable'] in Fields:
                        for y in serialized_ahj[x['SourceTable'] + "s"]:
                            if x['SourceTable'] == "AHJInspection":
                                if y['InspectionID'] == x['SourceRow']:
                                    y[x['SourceColumn']] = x['NewValue']
                                    changed.add((x['SourceColumn'],x['SourceRow']))
                                    break
                            else:
                                if y[x['SourceTable'] + "ID"] == x['SourceRow']:
                                    y[x['SourceColumn']] = x['NewValue']
                                    changed.add((x['SourceColumn'],x['SourceRow']))
                                    break
                        continue
                    elif x['SourceTable'] in SearchFields:
                        if x['SourceTable'] == "Address" and serialized_ahj['Address']['AddressID'] == x['SourceRow']:
                            serialized_ahj["Address"][x['SourceColumn']] = x['NewValue']
                            changed.add((x['SourceColumn'],x['SourceRow'])) 
                            continue
                        if x['SourceTable'] == "Location" and serialized_ahj['Address']['Location']['LocationID'] == x['SourceRow']:
                            serialized_ahj["Address"]['Location'][x['SourceColumn']] = x['NewValue']
                            changed.add((x['SourceColumn'],x['SourceRow'])) 
                            continue
                        for y in contact:
                            if x['SourceTable'] == "Address" and y['Address']['AddressID'] == x['SourceRow']:
                                y["Address"][x['SourceColumn']] = x['NewValue']
                                changed.add((x['SourceColumn'],x['SourceRow'])) 
                                continue
                            if x['SourceTable'] == "Location" and y['Address']['Location']['LocationID'] == x['SourceRow']:
                                y["Address"]['Location'][x['SourceColumn']] = x['NewValue']
                                changed.add((x['SourceColumn'],x['SourceRow'])) 
                                continue
                    elif x['SourceTable'] != 'AHJ':
                        serialized_ahj[x['SourceTable']][x['SourceColumn']] = x['NewValue']
                        changed.add((x['SourceColumn'],x['SourceRow'])) 
                elif x['EditType'] == "A":
                    if x['SourceTable'] == "AHJInspection":
                        for y in range(len(serialized_ahj['UnconfirmedInspections'])):
                            if serialized_ahj['UnconfirmedInspections'][y]['InspectionID'] == x['SourceRow']:
                                insp = serialized_ahj['UnconfirmedInspections'].pop(y)
                                serialized_ahj['AHJInspections'].append(insp)
                                break
                    else:
                        for y in range(len(serialized_ahj['Unconfirmed' + translate(x['SourceTable']) + 's'])):
                            if serialized_ahj['Unconfirmed' + translate(x['SourceTable']) + 's'][y][translate_id(x['SourceTable']) + 'ID'] == x['SourceRow']:
                                insp = serialized_ahj['Unconfirmed' + translate(x['SourceTable']) + 's'].pop(y)
                                serialized_ahj[translate(x['SourceTable']) + 's'].append(insp)
                                break
                else:
                    if x['SourceTable'] == "AHJInspection":
                        for y in range(len(serialized_ahj['AHJInspections'])):
                            if serialized_ahj['AHJInspections'][y]['InspectionID'] == x['SourceRow']:
                                insp = serialized_ahj['AHJInspections'].pop(y)
                                break
                    else:
                        for y in range(len(serialized_ahj[translate(x['SourceTable'])+'s'])):
                            if serialized_ahj[translate(x['SourceTable'])+'s'][y][translate_id(x['SourceTable']) + 'ID'] == x['SourceRow']:
                                insp = serialized_ahj[translate(x['SourceTable'])+'s'].pop(y)
                                break


                
    return Response(serialized_ahj, status=status.HTTP_200_OK)
