import datetime
from django.conf import settings
from .models_field_enums import *
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import rest_framework.authtoken.models
from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AHJ(models.Model):
    AHJPK = models.AutoField(db_column='AHJPK', primary_key=True)
    AHJID = models.CharField(db_column='AHJID', unique=True, max_length=36)
    AHJCode = models.CharField(db_column='AHJCode', max_length=20, blank=True)
    AHJLevelCode = models.ForeignKey('AHJLevelCode', on_delete=models.DO_NOTHING, db_column='AHJLevelCodeID', null=True)
    PolygonID = models.ForeignKey('Polygon', on_delete=models.DO_NOTHING, db_column='PolygonID', null=True)
    AddressID = models.ForeignKey('Address', on_delete=models.DO_NOTHING, db_column='AddressID', null=True)
    AHJName = models.CharField(db_column='AHJName', max_length=100)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    DocumentSubmissionMethodNotes = models.CharField(db_column='DocumentSubmissionMethodNotes', max_length=255, blank=True)
    PermitIssueMethodNotes = models.CharField(db_column='PermitIssueMethodNotes', max_length=255, blank=True)
    EstimatedTurnaroundDays = models.IntegerField(db_column='EstimatedTurnaroundDays', null=True)
    FileFolderURL = models.CharField(db_column='FileFolderURL', max_length=255, blank=True)
    URL = models.CharField(db_column='URL', max_length=2048, blank=True)
    BuildingCode = models.ForeignKey('BuildingCode', on_delete=models.DO_NOTHING, db_column='BuildingCodeID', null=True)
    BuildingCodeNotes = models.CharField(db_column='BuildingCodeNotes', max_length=255, blank=True)
    ElectricCode = models.ForeignKey('ElectricCode', on_delete=models.DO_NOTHING, db_column='ElectricCodeID', null=True)
    ElectricCodeNotes = models.CharField(db_column='ElectricCodeNotes', max_length=255, blank=True)
    FireCode = models.ForeignKey('FireCode', on_delete=models.DO_NOTHING, db_column='FireCodeID', null=True)
    FireCodeNotes = models.CharField(db_column='FireCodeNotes', max_length=255, blank=True)
    ResidentialCode = models.ForeignKey('ResidentialCode', on_delete=models.DO_NOTHING, db_column='ResidentialCodeID', null=True)
    ResidentialCodeNotes = models.CharField(db_column='ResidentialCodeNotes', max_length=255, blank=True)
    WindCode = models.ForeignKey('WindCode', on_delete=models.DO_NOTHING, db_column='WindCodeID', null=True)
    WindCodeNotes = models.CharField(db_column='WindCodeNotes', max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'AHJ'


    def get_contacts(self):
        return [contact.ContactID for contact in AHJContactRepresentative.objects.filter(AHJPK=self.AHJPK) if contact.ContactStatus is True]

    def get_unconfirmed(self):
        return [contact.ContactID for contact in AHJContactRepresentative.objects.filter(AHJPK=self.AHJPK) if contact.ContactStatus is None]

    def get_comments(self):
        return [comment for comment in Comment.objects.filter(AHJPK=self.AHJPK).order_by('-Date')]

    def get_inspections(self):
        return [ins for ins in AHJInspection.objects.filter(AHJPK=self.AHJPK) if ins.InspectionStatus is True]

    def get_unconfirmed_inspections(self):
        return [ins for ins in AHJInspection.objects.filter(AHJPK=self.AHJPK) if ins.InspectionStatus is None]


    def get_document_submission_methods(self):
        return [dsm for dsm in AHJDocumentSubmissionMethodUse.objects.filter(AHJPK=self.AHJPK) if dsm.MethodStatus is True]

    def get_uncon_dsm(self):
        return [dsm for dsm in AHJDocumentSubmissionMethodUse.objects.filter(AHJPK=self.AHJPK) if dsm.MethodStatus is None]

    def get_permit_submission_methods(self):
        return [pim for pim in AHJPermitIssueMethodUse.objects.filter(AHJPK=self.AHJPK) if pim.MethodStatus is True]

    def get_uncon_pim(self):
        return [pim for pim in AHJPermitIssueMethodUse.objects.filter(AHJPK=self.AHJPK) if pim.MethodStatus is None]

    def get_err(self):
        return[err for err in EngineeringReviewRequirement.objects.filter(AHJPK=self.AHJPK) if err.EngineeringReviewRequirementStatus is True]

    def get_uncon_err(self):
        return[err for err in EngineeringReviewRequirement.objects.filter(AHJPK=self.AHJPK) if err.EngineeringReviewRequirementStatus is None]

    def get_fee_structures(self):
        return [fs for fs in FeeStructure.objects.filter(AHJPK=self.AHJPK) if fs.FeeStructureStatus is True]

    def get_uncon_fs(self):
        return [fs for fs in FeeStructure.objects.filter(AHJPK=self.AHJPK) if fs.FeeStructureStatus is None]

    SERIALIZER_EXCLUDED_FIELDS = ['Polygon', 'AHJPK', 'Comments', 'UnconfirmedContacts', 'UnconfirmedEngineeringReviewRequirements', 'UnconfirmedDocumentSubmissionMethods', 'UnconfirmedPermitIssueMethods', 'UnconfirmedInspections', 'UnconfirmedFeeStructures']

class Comment(models.Model):
    CommentID = models.AutoField(db_column='CommentID', primary_key=True)
    UserID = models.ForeignKey('User', on_delete=models.DO_NOTHING, db_column='UserID')
    CommentText = models.TextField(db_column='CommentText', null=True, blank=True)
    AHJPK = models.IntegerField(db_column='AHJPK', null=True)
    Date = models.DateTimeField(db_column='Date', default=now)
    ReplyingTo = models.IntegerField(db_column='ReplyingTo', null=True)

    def get_replies(self):
        return [comment for comment in Comment.objects.filter(ReplyingTo=self.CommentID).order_by('-Date')]

    class Meta:
        managed = True
        db_table = 'Comment'

class Address(models.Model):
    AddressID = models.AutoField(db_column='AddressID', primary_key=True)
    LocationID = models.ForeignKey('Location', models.DO_NOTHING, db_column='LocationID', null=True)
    AddrLine1 = models.CharField(db_column='AddrLine1', max_length=100, blank=True)
    AddrLine2 = models.CharField(db_column='AddrLine2', max_length=100, blank=True)
    AddrLine3 = models.CharField(db_column='AddrLine3', max_length=100, blank=True)
    City = models.CharField(db_column='City', max_length=100, blank=True)
    Country = models.CharField(db_column='Country', max_length=100, blank=True)
    County = models.CharField(db_column='County', max_length=100, blank=True)
    StateProvince = models.CharField(db_column='StateProvince', max_length=100, blank=True)
    ZipPostalCode = models.CharField(db_column='ZipPostalCode', max_length=100, blank=True)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    AddressType = models.ForeignKey('AddressType', on_delete=models.DO_NOTHING, db_column='AddressTypeID', null=True)

    class Meta:
        managed = True
        db_table = 'Address'

    SERIALIZER_EXCLUDED_FIELDS = ['AddressID']

class Contact(models.Model):
    ContactID = models.AutoField(db_column='ContactID', primary_key=True)
    AddressID = models.ForeignKey(Address, models.DO_NOTHING, db_column='AddressID', null=True)
    FirstName = models.CharField(db_column='FirstName', max_length=255, blank=True)
    MiddleName = models.CharField(db_column='MiddleName', max_length=255, blank=True)
    LastName = models.CharField(db_column='LastName', max_length=255, blank=True)
    HomePhone = models.CharField(db_column='HomePhone', max_length=31, blank=True)
    MobilePhone = models.CharField(db_column='MobilePhone', max_length=31, blank=True)
    WorkPhone = models.CharField(db_column='WorkPhone', max_length=31, blank=True)
    ContactType = models.ForeignKey('ContactType', on_delete=models.DO_NOTHING, db_column='ContactTypeID', null=True)
    ContactTimezone = models.CharField(db_column='ContactTimezone', max_length=255, blank=True)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    Email = models.CharField(db_column='Email', max_length=50, blank=True)
    Title = models.CharField(db_column='Title', max_length=255, blank=True)
    URL = models.CharField(db_column='URL', max_length=255, blank=True)
    PreferredContactMethod = models.ForeignKey('PreferredContactMethod', on_delete=models.DO_NOTHING, db_column='PreferredContactMethodID', null=True)

    class Meta:
        managed = True
        db_table = 'Contact'

    SERIALIZER_EXCLUDED_FIELDS = ['ContactID']

    def create_relation_to(self, to):
        status_fields = {
            'ContactID': self,
            'ContactStatus': None
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJContactRepresentative.objects.create(**status_fields)
        elif to.__class__.__name__ == 'AHJInspection':
            status_fields['InspectionID'] = to
            return AHJInspectionContact.objects.create(**status_fields)
        else:
            raise ValueError('\'Contact\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        status_fields = {
            'ContactID': self,
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJContactRepresentative.objects.get(**status_fields)
        elif to.__class__.__name__ == 'AHJInspection':
            status_fields['InspectionID'] = to
            return AHJInspectionContact.objects.get(**status_fields)
        else:
            raise ValueError('\'Contact\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'ContactStatus'

class AHJContactRepresentative(models.Model):
    RepresentativeID = models.AutoField(db_column='RepresentativeID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    ContactID = models.ForeignKey('Contact', models.DO_NOTHING, db_column='ContactID')
    ContactStatus = models.BooleanField(db_column='ContactStatus', null=True)

    def get_relation_status_field(self):
        return 'ContactStatus'

    class Meta:
        managed = True
        db_table = 'AHJContactRepresentative'
        unique_together = (('AHJPK', 'ContactID'),)

class AHJInspection(models.Model):
    InspectionID = models.AutoField(db_column='InspectionID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    InspectionType = models.ForeignKey('InspectionType', on_delete=models.DO_NOTHING, db_column='InspectionTypeID', null=True)
    AHJInspectionName = models.CharField(db_column='AHJInspectionName', max_length=255)
    AHJInspectionNotes = models.CharField(db_column='AHJInspectionNotes', max_length=255, blank=True)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    FileFolderURL = models.CharField(db_column='FileFolderURL', max_length=255, blank=True)
    TechnicianRequired = models.BooleanField(db_column='TechnicianRequired', null=True)
    InspectionStatus = models.BooleanField(db_column='InspectionStatus', null=True)

    def get_contacts(self):
        return [contact.ContactID for contact in AHJInspectionContact.objects.filter(InspectionID=self.InspectionID) if contact.ContactStatus == 1]
    
    def get_uncon_con(self):
        return [contact.ContactID for contact in AHJInspectionContact.objects.filter(InspectionID=self.InspectionID) if contact.ContactStatus == 0]

    def create_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            self.InspectionStatus = None
            return self
        else:
            raise ValueError('\'AHJInspection\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            return self
        else:
            raise ValueError('\'AHJInspection\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'InspectionStatus'

    class Meta:
        managed = True
        db_table = 'AHJInspection'
        unique_together = (('AHJPK', 'AHJInspectionName'),)

    SERIALIZER_EXCLUDED_FIELDS = ['InspectionID', 'UnconfirmedContacts', 'InspectionStatus']

class AHJInspectionContact(models.Model):
    RepresentativeID = models.AutoField(db_column='RepresentativeID', primary_key=True)
    InspectionID = models.ForeignKey('AHJInspection', models.DO_NOTHING, db_column='InspectionID')
    ContactID = models.ForeignKey('Contact', models.DO_NOTHING, db_column='ContactID')
    ContactStatus = models.BooleanField(db_column='ContactStatus', null=True)

    def get_relation_status_field(self):
        return 'ContactStatus'



    class Meta:
        managed = True
        db_table = 'AHJInspectionContact'
        unique_together = (('InspectionID', 'ContactID'),)

class FeeStructure(models.Model):
    FeeStructurePK = models.AutoField(db_column='FeeStructurePK', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    FeeStructureID = models.CharField(db_column='FeeStructureID', max_length=36) # UUIDField
    FeeStructureName = models.CharField(db_column='FeeStructureName', unique=True, max_length=255)
    FeeStructureType = models.ForeignKey('FeeStructureType', on_delete=models.DO_NOTHING, db_column='FeeStructureTypeID', null=True)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    FeeStructureStatus = models.BooleanField(db_column='FeeStructureStatus', null=True)

    class Meta:
        managed = True
        db_table = 'FeeStructure'
        unique_together = (('FeeStructureID', 'AHJPK'),)

    SERIALIZER_EXCLUDED_FIELDS = ['FeeStructurePK', 'FeeStructureStatus']

    def create_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            self.FeeStructureStatus = None
            return self
        else:
            raise ValueError('\'FeeStructure\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            return self
        else:
            raise ValueError('\'FeeStructure\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'FeeStructureStatus'

class Edit(models.Model):
    EditID = models.AutoField(db_column='EditID', primary_key=True)
    ChangedBy = models.ForeignKey('User', models.DO_NOTHING, db_column='ChangedBy', related_name='related_primary_edit')
    ApprovedBy = models.ForeignKey('User', models.DO_NOTHING, db_column='ApprovedBy', null=True, related_name='related_secondary_edit')
    AHJPK = models.ForeignKey('AHJ', models.DO_NOTHING, db_column='AHJPK', null=True)
    InspectionID = models.ForeignKey('AHJInspection', models.DO_NOTHING, db_column='InspectionID', null=True)
    SourceTable = models.CharField(db_column='SourceTable', max_length=255)
    SourceColumn = models.CharField(db_column='SourceColumn', max_length=255)
    SourceRow = models.IntegerField(db_column='SourceRow')
    # status is P = pending, R = rejected, A = approved
    ReviewStatus = models.CharField(db_column='ReviewStatus', max_length=1, default='P')
    Comments = models.CharField(db_column='Comments', max_length=255, blank=True)
    OldValue = models.CharField(db_column='OldValue', max_length=255, blank=True, null=True)
    NewValue = models.CharField(db_column='NewValue', max_length=255, blank=True, null=True)
    DateRequested = models.DateField(db_column='DateRequested')
    DateEffective = models.DateField(db_column='DateEffective', blank=True, null=True)
    #Edit type: A = addition, D = deletion, U = update
    EditType = models.CharField(db_column='EditType', max_length=1, default='U')
    DataSourceComment = models.CharField(db_column='DataSourceComment', max_length=255)

    class Meta:
        managed = True
        db_table = 'Edit'

class Location(models.Model):
    LocationID = models.AutoField(db_column='LocationID', primary_key=True)
    Altitude = models.DecimalField(db_column='Altitude', max_digits=15, decimal_places=6, null=True)
    Elevation = models.DecimalField(db_column='Elevation', max_digits=17, decimal_places=8, null=True)
    Latitude = models.DecimalField(db_column='Latitude', max_digits=10, decimal_places=8, null=True)
    Longitude = models.DecimalField(db_column='Longitude', max_digits=11, decimal_places=8, null=True)
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    LocationDeterminationMethod = models.ForeignKey('LocationDeterminationMethod', on_delete=models.DO_NOTHING, db_column='LocationDeterminationMethodID', null=True)
    LocationType = models.ForeignKey('LocationType', on_delete=models.DO_NOTHING, db_column='LocationTypeID', null=True)

    class Meta:
        managed = True
        db_table = 'Location'

    SERIALIZER_EXCLUDED_FIELDS = ['LocationID']

class EngineeringReviewRequirement(models.Model):
    EngineeringReviewRequirementID = models.AutoField(db_column='EngineeringReviewRequirementID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    Description = models.CharField(db_column='Description', max_length=255, blank=True)
    EngineeringReviewType = models.ForeignKey('EngineeringReviewType', on_delete=models.DO_NOTHING, db_column='EngineeringReviewTypeID', null=True)
    RequirementLevel = models.ForeignKey('RequirementLevel', on_delete=models.DO_NOTHING, db_column='RequirementLevelID', null=True)
    RequirementNotes = models.CharField(db_column='RequirementNotes', max_length=255, blank=True)
    StampType = models.CharField(db_column='StampType', choices=STAMP_TYPE_CHOICES, max_length=7)
    EngineeringReviewRequirementStatus = models.BooleanField(db_column='EngineeringReviewRequirementStatus', null=True)

    class Meta:
        managed = True
        db_table = 'EngineeringReviewRequirement'

    SERIALIZER_EXCLUDED_FIELDS = ['EngineeringReviewRequirementID', 'EngineeringReviewRequirementStatus']

    def create_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            self.EngineeringReviewRequirementStatus = None
            return self
        else:
            raise ValueError('\'EngineeringReviewRequirement\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        if to.__class__.__name__ == 'AHJ':
            return self
        else:
            raise ValueError('\'EngineeringReviewRequirement\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'EngineeringReviewRequirementStatus'

class DocumentSubmissionMethod(models.Model):
    DocumentSubmissionMethodID = models.AutoField(db_column='DocumentSubmissionMethodID', primary_key=True)
    Value = models.CharField(db_column='Value', choices=DOCUMENT_SUBMISSION_METHOD_CHOICES, unique=True, max_length=11)

    def create_relation_to(self, to):
        status_fields = {
            'DocumentSubmissionMethodID': self,
            'MethodStatus': None
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJDocumentSubmissionMethodUse.objects.create(**status_fields)
        else:
            raise ValueError('\'DocumentSubmissionMethod\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        status_fields = {
            'DocumentSubmissionMethodID': self,
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJDocumentSubmissionMethodUse.objects.get(**status_fields)
        else:
            raise ValueError('\'DocumentSubmissionMethod\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'MethodStatus'

class AHJDocumentSubmissionMethodUse(models.Model):
    UseID = models.AutoField(db_column='UseID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    DocumentSubmissionMethodID = models.ForeignKey('DocumentSubmissionMethod', models.DO_NOTHING, db_column='DocumentSubmissionMethodID')
    MethodStatus = models.BooleanField(db_column='MethodStatus', null=True)

    class Meta:
        managed = True
        db_table = 'AHJDocumentSubmissionMethodUse'
        unique_together = (('AHJPK', 'DocumentSubmissionMethodID'),)

    SERIALIZER_EXCLUDED_FIELDS = ['UseID']

    def get_value(self):
        return self.DocumentSubmissionMethodID.Value

    def get_relation_status_field(self):
        return 'MethodStatus'

class PermitIssueMethod(models.Model):
    PermitIssueMethodID = models.AutoField(db_column='PermitIssueMethodID', primary_key=True)
    Value = models.CharField(db_column='Value', choices=PERMIT_ISSUE_METHOD_CHOICES, unique=True, max_length=11)

    def create_relation_to(self, to):
        status_fields = {
            'PermitIssueMethodID': self,
            'MethodStatus': None
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJPermitIssueMethodUse.objects.create(**status_fields)
        else:
            raise ValueError('\'PermitIssueMethod\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_to(self, to):
        status_fields = {
            'PermitIssueMethodID': self,
        }
        if to.__class__.__name__ == 'AHJ':
            status_fields['AHJPK'] = to
            return AHJPermitIssueMethodUse.objects.get(**status_fields)
        else:
            raise ValueError('\'PermitIssueMethod\' cannot be related to \'{to_model}\''.format(to_model=to.__class__.__name__))

    def get_relation_status_field(self):
        return 'MethodStatus'

class AHJPermitIssueMethodUse(models.Model):
    UseID = models.AutoField(db_column='UseID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    PermitIssueMethodID = models.ForeignKey('PermitIssueMethod', models.DO_NOTHING, db_column='PermitIssueMethodID')
    MethodStatus = models.BooleanField(db_column='MethodStatus', null=True)

    class Meta:
        managed = True
        db_table = 'AHJPermitIssueMethodUse'
        unique_together = (('AHJPK', 'PermitIssueMethodID'),)

    SERIALIZER_EXCLUDED_FIELDS = ['UseID']

    def get_value(self):
        return self.PermitIssueMethodID.Value

    def get_relation_status_field(self):
        return 'MethodStatus'

class Polygon(models.Model):
    PolygonID = models.AutoField(db_column='PolygonID', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=100)
    GEOID = models.CharField(db_column='GEOID', max_length=10)
    Polygon = models.MultiPolygonField(db_column='Polygon')
    LandArea = models.BigIntegerField(db_column='LandArea')
    WaterArea = models.BigIntegerField(db_column='WaterArea')
    InternalPLatitude = models.DecimalField(db_column='InternalPLatitude', max_digits=10, decimal_places=8)
    InternalPLongitude = models.DecimalField(db_column='InternalPLongitude', max_digits=11, decimal_places=8)

    class Meta:
        managed = True
        db_table = 'Polygon'

class StatePolygon(models.Model):
    PolygonID = models.OneToOneField(Polygon, models.DO_NOTHING, db_column='PolygonID', primary_key=True)
    FIPSCode = models.CharField(db_column='FIPSCode', max_length=2)

    class Meta:
        managed = True
        db_table = 'StatePolygon'

class CountyPolygon(models.Model):
    PolygonID = models.OneToOneField('Polygon', models.DO_NOTHING, db_column='PolygonID', primary_key=True)
    StatePolygonID = models.ForeignKey('StatePolygon', models.DO_NOTHING, db_column='StatePolygonID')
    LSAreaCodeName = models.CharField(db_column='LSAreaCodeName', max_length=100)

    class Meta:
        managed = True
        db_table = 'CountyPolygon'

class CityPolygon(models.Model):
    PolygonID = models.OneToOneField('Polygon', models.DO_NOTHING, db_column='PolygonID', primary_key=True)
    StatePolygonID = models.ForeignKey('StatePolygon', models.DO_NOTHING, db_column='StatePolygonID')
    LSAreaCodeName = models.CharField(db_column='LSAreaCodeName', max_length=100)

    class Meta:
        managed = True
        db_table = 'CityPolygon'

class CountySubdivisionPolygon(models.Model):
    PolygonID = models.OneToOneField('Polygon', models.DO_NOTHING, db_column='PolygonID', primary_key=True)
    StatePolygonID = models.ForeignKey('StatePolygon', models.DO_NOTHING, db_column='StatePolygonID')
    LSAreaCodeName = models.CharField(db_column='LSAreaCodeName', max_length=100)

    class Meta:
        managed = True
        db_table = 'CountySubdivisionPolygon'

class UserManager(BaseUserManager):
    use_in_migrations = True

    # eventually handle first name and last name into contact table, for now handles username and password
    def _create_user(self, email, password, **extra_fields):
        # save to user
        ContactID = Contact.objects.create(Email=email)
        
        User = User.objects.create()
        # save to authuser
        user = self.model(email=email, **extra_fields)
        #user.set_password(password)

    def create_user(self, **extra_fields):
        Email = extra_fields.get('Email', '')
        Username = extra_fields.get('Username', '')
        password = extra_fields.get('password', '')
        ContactID = Contact.objects.create(Email=Email, AddressID=Address.objects.create())

        user = self.model(
            Email=self.normalize_email(Email),
            ContactID=ContactID,
            Username=Username,
            SignUpDate=datetime.date.today(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(**extra_fields)

class User(AbstractBaseUser):
    UserID = models.AutoField(db_column='UserID', primary_key=True)
    ContactID = models.ForeignKey(Contact, models.DO_NOTHING, db_column='ContactID', null=True)
    Username = models.CharField(db_column='Username', unique=True, max_length=254)
    password = models.CharField(max_length=128)
    Email = models.CharField(db_column='Email', unique=True, max_length=254)
    is_staff = models.BooleanField(db_column='IsStaff', default=False)
    is_active = models.BooleanField(db_column='IsActive', default=False)
    SignUpDate = models.DateField(db_column='SignUpDate', blank=True)
    PersonalBio = models.CharField(db_column='PersonalBio', max_length=255, blank=True)
    URL = models.CharField(db_column='URL', max_length=255, blank=True, null=True)
    CompanyAffiliation = models.CharField(db_column='CompanyAffiliation', max_length=255, blank=True)
    Photo = models.CharField(db_column='Photo', max_length=255, blank=True, null=True)
    IsPeerReviewer = models.IntegerField(db_column='IsPeerReviewer', null=True, default=False)
    NumReviewsDone = models.IntegerField(db_column='NumReviewsDone', default=0)
    AcceptedEdits = models.IntegerField(db_column='NumAcceptedEdits', default=0)
    SubmittedEdits = models.IntegerField(db_column='NumSubmittedEdits', default=0)
    CommunityScore = models.IntegerField(db_column='CommunityScore', default=0)
    SecurityLevel = models.IntegerField(db_column='SecurityLevel', default=3)

    USERNAME_FIELD = 'Email'
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, core):
        return self.is_superuser
    
    def get_email_field_name(self=None):
        return 'Email'

    def get_maintained_ahjs(self):
        return [ahjpk.AHJPK.AHJPK for ahjpk in AHJUserMaintains.objects.filter(UserID=self).filter(MaintainerStatus=True)]

    class Meta:
        db_table = 'User'
        managed = True

class AHJUserMaintains(models.Model):
    MaintainerID = models.AutoField(db_column='MaintainerID', primary_key=True)
    AHJPK = models.ForeignKey(AHJ, models.DO_NOTHING, db_column='AHJPK')
    UserID = models.ForeignKey(User, models.DO_NOTHING, db_column='UserID')
    MaintainerStatus = models.BooleanField(db_column='MaintainerStatus')

    class Meta:
        managed = True
        db_table = 'AHJUserMaintains'
        unique_together = (('AHJPK', 'UserID'),)

class WebpageToken(rest_framework.authtoken.models.Token):
     key = models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')
     created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
     user = models.OneToOneField(on_delete=models.CASCADE, related_name='webpage_token', to=settings.AUTH_USER_MODEL, verbose_name='User')

     def get_user(self):
         return self.user

class APIToken(rest_framework.authtoken.models.Token):
     key = models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')
     created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
     user = models.OneToOneField(on_delete=models.CASCADE, related_name='api_token', to=settings.AUTH_USER_MODEL, verbose_name='User')

class StateTemp(models.Model):
    GEOID = models.CharField(max_length=2)
    NAME = models.CharField(max_length=100)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAME

# Census county shapefile model
class CountyTemp(models.Model):
    STATEFP = models.CharField(max_length=2)
    GEOID = models.CharField(max_length=5)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAMELSAD

# Census cousub shapefile model
class CousubTemp(models.Model):
    STATEFP = models.CharField(max_length=2)
    GEOID = models.CharField(max_length=10)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAMELSAD

# Census place shapefile model
class CityTemp(models.Model):
    STATEFP = models.CharField(max_length=2)
    GEOID = models.CharField(max_length=7)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAMELSAD
