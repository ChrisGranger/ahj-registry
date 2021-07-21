from collections import OrderedDict

from djoser.compat import get_user_email, get_user_email_field_name
from django.conf import settings
from django.db import connection
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from djoser.serializers import UserCreateSerializer
from .models import *


class PolygonSerializer(geo_serializers.GeoFeatureModelSerializer):
    """
    Class to serialize Polygon objects into GeoJSON format
    plus extra properties in the properties section of
    the GeoJSON
    """
    AHJID = serializers.SerializerMethodField()

    class Meta:
        model = Polygon
        geo_field = 'Polygon'
        id_field = False
        fields = ['AHJID', 'LandArea', 'GEOID', 'InternalPLatitude', 'InternalPLongitude']

    def get_AHJID(self, instance):
        return self.context.get('AHJID', '')


class OrangeButtonSerializer(serializers.Field):
    """
    Custom serializer to add the Orange Button
    primitives to each field.
    "<field_name>": {
        "Value": "<value>,
        ...
    }
    """
    def get_attribute(self, instance):
        """
        Overridden method for correctly adding
        Orange Button primitives even when the
        field's value is null
        Otherwise, this class' to_representation
        will not be called by the caller serializer
        """
        attribute = super().get_attribute(instance)
        if attribute is None:
            return {'Value': None}
        else:
            return attribute

    def to_representation(self, value):
        if type(value) is dict and 'Value' in value and value['Value'] is None:
            return value
        ob_obj = {}
        ob_obj['Value'] = value
        return ob_obj

class EnumModelSerializer(serializers.Serializer):
    Value = serializers.CharField()

    def get_attribute(self, instance):
        attribute = super().get_attribute(instance)
        if attribute is None:
            return {'Value': ''}
        else:
            return attribute

    def to_representation(self, value):
        if type(value) is dict and 'Value' in value and value['Value'] == '':
            return value
        return super().to_representation(value)


class FeeStructureSerializer(serializers.Serializer):
    """
    Serializes Orange Button FeeStrucuture object to OrderedDict
    """
    FeeStructurePK = OrangeButtonSerializer()
    FeeStructureID = OrangeButtonSerializer()
    FeeStructureName = OrangeButtonSerializer()
    FeeStructureType = EnumModelSerializer()
    Description = OrangeButtonSerializer()
    FeeStructureStatus = OrangeButtonSerializer()

    def to_representation(self, feestructure):
        """
        Returns an OrderedDict representing an FeeStructure object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in FeeStructure.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(feestructure)


class LocationSerializer(serializers.Serializer):
    """
    Serializes Orange Button Location object to OrderedDict
    """
    LocationID = OrangeButtonSerializer()
    Altitude = OrangeButtonSerializer()
    Elevation = OrangeButtonSerializer()
    Latitude = OrangeButtonSerializer()
    Longitude = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    LocationDeterminationMethod = EnumModelSerializer()
    LocationType = EnumModelSerializer()

    def to_representation(self, location):
        """
        Returns an OrderedDict representing an Location object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in Location.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(location)


class AddressSerializer(serializers.Serializer):
    """
    Serializes Orange Button Address object to OrderedDict
    """
    AddressID = OrangeButtonSerializer()
    AddrLine1 = OrangeButtonSerializer()
    AddrLine2 = OrangeButtonSerializer()
    AddrLine3 = OrangeButtonSerializer()
    City = OrangeButtonSerializer()
    Country = OrangeButtonSerializer()
    County = OrangeButtonSerializer()
    StateProvince = OrangeButtonSerializer()
    ZipPostalCode = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    AddressType = EnumModelSerializer()
    Location = LocationSerializer(source='LocationID')

    def to_representation(self, address):
        """
        Returns an OrderedDict representing an Address object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in Address.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(address)


class ContactSerializer(serializers.Serializer):
    """
    Serializes Orange Button Contact object to OrderedDict
    """
    ContactID = OrangeButtonSerializer()
    FirstName = OrangeButtonSerializer()
    MiddleName = OrangeButtonSerializer()
    LastName = OrangeButtonSerializer()
    HomePhone = OrangeButtonSerializer()
    MobilePhone = OrangeButtonSerializer()
    WorkPhone = OrangeButtonSerializer()
    ContactType = EnumModelSerializer()
    ContactTimezone = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    Email = OrangeButtonSerializer()
    Title = OrangeButtonSerializer()
    URL = OrangeButtonSerializer()
    PreferredContactMethod = EnumModelSerializer()
    Address = AddressSerializer(source='AddressID')

    def to_representation(self, contact):
        """
        Returns an OrderedDict representing an Contact object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in Contact.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(contact)


class RecursiveField(serializers.Serializer):
    """
    Serializer that calls the caller serializer on the value
    of the field that was passed to it.
    Used for serializing Comments
    """
    def to_representation(self, value):
        """
        Calls the caller serializer that called this serializer
        """
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class UserSerializer(serializers.Serializer):
    """
    Serializes User to OrderedDict
    """
    UserID = serializers.IntegerField(read_only=True)
    ContactID = ContactSerializer()
    Username = serializers.CharField()
    Email = serializers.CharField()
    PersonalBio = serializers.CharField()
    CompanyAffiliation = serializers.CharField()
    Photo = serializers.CharField()
    AcceptedEdits = serializers.IntegerField()
    SubmittedEdits = serializers.IntegerField()
    CommunityScore = serializers.IntegerField()
    SignUpDate = serializers.DateField()
    MaintainedAHJs = serializers.ListField(source='get_maintained_ahjs')
    APIToken = serializers.CharField(source='get_API_token')
    is_superuser = serializers.BooleanField()

    def to_representation(self, user):
        """
        Returns an OrderedDict representing an User object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users. Unlike other
        serializers, the default is True to passively prevent
        sensitive data being serialized when it's not needed.
        """
        if self.context.get('is_public_view', True):
            for field in User.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(user)


class UserCreateSerializer(UserCreateSerializer):
    """
    Serializes User to Ordered Dict.
    Used when a new user is created.
    """
    FirstName = serializers.CharField()
    LastName = serializers.CharField()
    
    def validate(self, attrs):
        contact_fields = {field.name for field in Contact._meta.get_fields()}
        user_dict = OrderedDict({k: v for k, v in attrs.items() if k not in contact_fields})
        super().validate(user_dict)
        return attrs

    def to_representation(self, user):
        return UserSerializer(user).data

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('UserID',
                  'ContactID',
                  'Username',
                  'password',
                  'Email',
                  'is_staff',
                  'is_active',
                  'SignUpDate',
                  'PersonalBio',
                  'URL',
                  'CompanyAffiliation',
                  'Photo',
                  'CommunityScore',
                  'SecurityLevel',
                  'FirstName',
                  'LastName')


class CommentSerializer(serializers.Serializer):
    """
    Serializes Comment to OrderedDict.
    """
    CommentID = OrangeButtonSerializer()
    User = UserSerializer(source='UserID')
    CommentText = OrangeButtonSerializer()
    Date = OrangeButtonSerializer()
    Replies = RecursiveField(source='get_replies', many=True)


class DocumentSubmissionMethodUseSerializer(serializers.Serializer):
    """
    Serializes Orange Button DocumentSubmissionMethod object value to OrderedDict
    """
    UseID = serializers.IntegerField()
    Value = serializers.CharField(source='get_value')

    def to_representation(self, dsmu):
        if self.context.get('is_public_view', False):
            for field in AHJDocumentSubmissionMethodUse.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(dsmu)

class PermitIssueMethodUseSerializer(serializers.Serializer):
    """
    Serializes Orange Button PermitIssueMethod object value to OrderedDict
    """
    UseID = serializers.IntegerField()
    Value = serializers.CharField(source='get_value')

    def to_representation(self, pimu):
        if self.context.get('is_public_view', False):
            for field in AHJPermitIssueMethodUse.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(pimu)

class AHJInspectionSerializer(serializers.Serializer):
    """
    Serializes Orange Button AHJInspection object
    """
    InspectionID = OrangeButtonSerializer()
    InspectionType = EnumModelSerializer()
    AHJInspectionName = OrangeButtonSerializer()
    AHJInspectionNotes = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    FileFolderURL = OrangeButtonSerializer()
    TechnicianRequired = OrangeButtonSerializer()
    InspectionStatus = OrangeButtonSerializer()
    Contacts = ContactSerializer(source='get_contacts', many=True)
    UnconfirmedContacts = ContactSerializer(source='get_uncon_con', many=True)

    def to_representation(self, inspection):
        """
        Returns an OrderedDict representing an AHJInspection object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in AHJInspection.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(inspection)


class EngineeringReviewRequirementSerializer(serializers.Serializer):
    """
    Serializes Orange Button EngineeringReviewRequirement object to OrderedDict
    """
    EngineeringReviewRequirementID = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    EngineeringReviewType = EnumModelSerializer()
    RequirementLevel = EnumModelSerializer()
    RequirementNotes = OrangeButtonSerializer()
    StampType = EnumModelSerializer()
    EngineeringReviewRequirementStatus = OrangeButtonSerializer()

    def to_representation(self, err):
        """
        Returns an OrderedDict representing an EngineeringReviewRequirement object to OrderedDict
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in EngineeringReviewRequirement.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(err)


class AHJSerializer(serializers.Serializer):
    """
    Serializes Orange Button AHJ object
    """
    AHJPK = OrangeButtonSerializer()
    AHJID = OrangeButtonSerializer()
    AHJCode = OrangeButtonSerializer()
    AHJLevelCode = EnumModelSerializer()
    AHJName = OrangeButtonSerializer()
    Description = OrangeButtonSerializer()
    DocumentSubmissionMethodNotes = OrangeButtonSerializer()
    PermitIssueMethodNotes = OrangeButtonSerializer()
    EstimatedTurnaroundDays = OrangeButtonSerializer()
    FileFolderURL = OrangeButtonSerializer()
    URL = OrangeButtonSerializer()
    BuildingCode = EnumModelSerializer()
    BuildingCodeNotes = OrangeButtonSerializer()
    ElectricCode = EnumModelSerializer()
    ElectricCodeNotes = OrangeButtonSerializer()
    FireCode = EnumModelSerializer()
    FireCodeNotes = OrangeButtonSerializer()
    ResidentialCode = EnumModelSerializer()
    ResidentialCodeNotes = OrangeButtonSerializer()
    WindCode = EnumModelSerializer()
    WindCodeNotes = OrangeButtonSerializer()
    Address = AddressSerializer(source='AddressID')
    Contacts = ContactSerializer(source='get_contacts', many=True)
    UnconfirmedContacts = ContactSerializer(source='get_unconfirmed', many=True)
    UnconfirmedInspections = AHJInspectionSerializer(source='get_unconfirmed_inspections', many=True)
    Polygon = serializers.SerializerMethodField()
    Comments = CommentSerializer(source='get_comments', many=True)
    AHJInspections = AHJInspectionSerializer(source='get_inspections', many=True)
    DocumentSubmissionMethods = DocumentSubmissionMethodUseSerializer(source='get_document_submission_methods', many=True)
    UnconfirmedDocumentSubmissionMethods = DocumentSubmissionMethodUseSerializer(source='get_uncon_dsm', many=True)
    PermitIssueMethods = PermitIssueMethodUseSerializer(source='get_permit_submission_methods', many=True)
    UnconfirmedPermitIssueMethods = PermitIssueMethodUseSerializer(source='get_uncon_pim', many=True)
    EngineeringReviewRequirements = EngineeringReviewRequirementSerializer(source='get_err', many=True)
    UnconfirmedEngineeringReviewRequirements = EngineeringReviewRequirementSerializer(source='get_uncon_err', many=True)
    FeeStructures = FeeStructureSerializer(source='get_fee_structures', many=True)
    UnconfirmedFeeStructures = FeeStructureSerializer(source='get_uncon_fs', many=True)

    def to_representation(self, ahj):
        """
        Returns an OrderedDict representing an AHJ object
        Note not every AHJ has every child object.
        If 'is_public_view' is True, will not serialize fields
        that are not meant for public api users.
        """
        if self.context.get('is_public_view', False):
            for field in AHJ.SERIALIZER_EXCLUDED_FIELDS:
                if field in self.fields:
                    self.fields.pop(field)
        return super().to_representation(ahj)

    def get_Polygon(self, instance):
        """
        Helper method to serialize the polygon associated with an AHJ
        """
        if instance.PolygonID is None:
            return None
        return PolygonSerializer(instance.PolygonID, context={'AHJID': instance.AHJID}).data


class EditSerializer(serializers.Serializer):
    """
    Serializes edits for the webpage AHJPage.
    """
    EditID = serializers.IntegerField(read_only=True)
    ChangedBy = UserSerializer()
    ApprovedBy = UserSerializer()
    AHJPK = serializers.IntegerField(source='AHJPK.AHJPK')
    SourceTable = serializers.CharField()
    SourceColumn = serializers.CharField()
    SourceRow = serializers.IntegerField()
    ReviewStatus = serializers.CharField()
    OldValue = serializers.CharField(read_only=True)
    NewValue = serializers.CharField()
    DateRequested = serializers.DateTimeField(read_only=True)
    DateEffective = serializers.DateTimeField(read_only=True)
    EditType = serializers.CharField()
    DataSourceComment = serializers.CharField()

    def to_representation(self, edit):
        if self.context.get('drop_users', False):
            """
            This gives the option for callers of the serializer to only serialize the username of the user.
            """
            self.fields['ChangedBy'] = serializers.CharField(source='ChangedBy.Username')
            if edit.ApprovedBy is None:
                self.fields['ApprovedBy'] = UserSerializer()
            else:
                self.fields['ApprovedBy'] = serializers.CharField(source='ApprovedBy.Username')
        return super().to_representation(edit)

    def create(self):
        """
        Creates an edit object without saving to database
        """
        return Edit(**self.validated_data)


class WebpageTokenSerializer(serializers.Serializer):
    """
    Serializes webpage token and user info when a user logs
    into the webpage.
    """
    auth_token = serializers.CharField(source='key')
    User = UserSerializer(source='get_user')


# Serializer used in Djoser's password reset endpoint. 
class UserFunctionsMixin:
    def get_user(self):
        try:
            user = User._default_manager.get(
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        if (
            settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
            or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            self.fail("email_not_found")

# Serializer used in Djoser's password reset endpoint
class SendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    default_error_messages = {
        "email_not_found": "User with given email does not exist."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()
