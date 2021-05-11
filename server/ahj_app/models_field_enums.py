from django.contrib.gis.db import models


BUILDING_CODE_CHOICES = [
    ('2021IBC', '2021 IBC'),
    ('2018IBC', '2018 IBC'),
    ('2015IBC', '2015 IBC'),
    ('2012IBC', '2012 IBC'),
    ('2009IBC', '2009 IBC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]


class BuildingCode(models.Model):
    BuildingCodeID = models.AutoField(db_column='BuildingCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=BUILDING_CODE_CHOICES, max_length=18)


ELECTRIC_CODE_CHOICES = [
    ('2020NEC', '2020 NEC'),
    ('2017NEC', '2017 NEC'),
    ('2014NEC', '2014 NEC'),
    ('2011NEC', '2011 NEC'),
    ('2008NEC', '2008 NEC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]


class ElectricCode(models.Model):
    ElectricCodeID = models.AutoField(db_column='ElectricCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=ELECTRIC_CODE_CHOICES, max_length=18)


FIRE_CODE_CHOICES = [
    ('2021IFC', '2021 IFC'),
    ('2018IFC', '2018 IFC'),
    ('2015IFC', '2015 IFC'),
    ('2012IFC', '2012 IFC'),
    ('2009IFC', '2009 IFC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]


class FireCode(models.Model):
    FireCodeID = models.AutoField(db_column='FireCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=FIRE_CODE_CHOICES, max_length=18)


RESIDENTIAL_CODE_CHOICES = [
    ('2021IRC', '2021 IRC'),
    ('2018IRC', '2018 IRC'),
    ('2015IRC', '2015 IRC'),
    ('2012IRC', '2012 IRC'),
    ('2009IRC', '2009 IRC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]


class ResidentialCode(models.Model):
    ResidentialCodeID = models.AutoField(db_column='ResidentialCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=RESIDENTIAL_CODE_CHOICES, max_length=18)


WIND_CODE_CHOICES = [
    ('ASCE716', 'ASCE7-16'),
    ('ASCE710', 'ASCE7-10'),
    ('ASCE705', 'ASCE7-05'),
    ('SpecialWindZone', 'Special Wind Zone')
]


class WindCode(models.Model):
    WindCodeID = models.AutoField(db_column='WindCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=WIND_CODE_CHOICES, max_length=15)


AHJ_LEVEL_CODE_CHOICES = [
    ('040', 'State'),
    ('050', 'State County'),
    ('061', 'State County Minor Civil Division'),
    ('162', 'State Incorporated Place')
]


class AHJLevelCode(models.Model):
    AHJLevelCodeID = models.AutoField(db_column='AHJLevelCodeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=AHJ_LEVEL_CODE_CHOICES, max_length=3)


# DocumentSubmissionMethod model is in models.py
DOCUMENT_SUBMISSION_METHOD_CHOICES = [
    ('Epermitting', 'Epermitting'),
    ('Email', 'Email'),
    ('InPerson', 'In Person'),
    ('SolarApp', 'SolarAPP')
]


# PermitIssueMethod model is in models.py
PERMIT_ISSUE_METHOD_CHOICES = [
    ('Epermitting', 'Epermitting'),
    ('Email', 'Email'),
    ('InPerson', 'In Person'),
    ('SolarApp', 'SolarAPP')
]


ADDRESS_TYPE_CHOICES = [
    ('Mailing', 'Mailing'),
    ('Billing', 'Billing'),
    ('Installation', 'Installation'),
    ('Shipping', 'Shipping')
]


class AddressType(models.Model):
    AddressTypeID = models.AutoField(db_column='AddressTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=ADDRESS_TYPE_CHOICES, max_length=12)


LOCATION_DETERMINATION_METHOD_CHOICES = [
    ('GPS', 'GPS'),
    ('Survey', 'Survey'),
    ('AerialImage', 'Aerial Image'),
    ('EngineeringReport', 'Engineering Report'),
    ('AddressGeocoding', 'Address Geocoding'),
    ('Unknown', 'Unknown')
]


class LocationDeterminationMethod(models.Model):
    LocationDeterminationMethodID = models.AutoField(db_column='LocationDeterminationMethodID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=LOCATION_DETERMINATION_METHOD_CHOICES, max_length=17)


LOCATION_TYPE_CHOICES = [
    ('DeviceSpecific', 'Device Specific'),
    ('SiteEntrance', 'Site Entrance'),
    ('GeneralProximity', 'General Proximity'),
    ('Warehouse', 'Warehouse')
]


class LocationType(models.Model):
    LocationTypeID = models.AutoField(db_column='LocationTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=LOCATION_TYPE_CHOICES, max_length=16)


CONTACT_TYPE_CHOICES = [
    ('Homeowner', 'Homeowner'),
    ('OffTaker', 'Off Taker'),
    ('Inspector', 'Inspector'),
    ('Engineer', 'Engineer'),
    ('Originator', 'Originator'),
    ('Installer', 'Installer'),
    ('Investor', 'Investor'),
    ('PermittingOfficial', 'Permitting Official'),
    ('FireMarshal', 'Fire Marshal'),
    ('ProjectManager', 'Project Manager'),
    ('Salesperson', 'Salesperson')
]


class ContactType(models.Model):
    ContactTypeID = models.AutoField(db_column='ContactTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=CONTACT_TYPE_CHOICES, max_length=18)


PREFERRED_CONTACT_METHOD_CHOICES = [
    ('Email', 'Email'),
    ('WorkPhone', 'Work Phone'),
    ('CellPhone', 'Cell Phone'),
    ('HomePhone', 'Home Phone'),
    ('CellTextMessage', 'Cell Text Message'),
]


class PreferredContactMethod(models.Model):
    PreferredContactMethodID = models.AutoField(db_column='PreferredContactMethodID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=PREFERRED_CONTACT_METHOD_CHOICES, max_length=15)


ENGINEERING_REVIEW_TYPE_CHOICES = [
    ('StructuralEngineer', 'Structural Engineer'),
    ('ElectricalEngineer', 'Electrical Engineer'),
    ('PVEngineer', 'PV Engineer'),
    ('MasterElectrician', 'Master Electrician'),
    ('FireMarshal', 'Fire Marshal'),
    ('EnvironmentalEngineer', 'Environmental Engineer')
]


class EngineeringReviewType(models.Model):
    EngineeringReviewTypeID = models.AutoField(db_column='EngineeringReviewTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=ENGINEERING_REVIEW_TYPE_CHOICES, max_length=21)


REQUIREMENT_LEVEL_CHOICES = [
    ('Required', 'Required'),
    ('Optional', 'Optional'),
    ('ConditionallyRequired', 'Conditionally Required')
]


class RequirementLevel(models.Model):
    RequirementLevelID = models.AutoField(db_column='RequirementLevelID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=REQUIREMENT_LEVEL_CHOICES, max_length=21)


STAMP_TYPE_CHOICES = [
    ('Wet', 'Wet'),
    ('Digital', 'Digital'),
    ('Notary', 'Notary'),
    ('None', 'None')
]


class StampType(models.Model):
    StampTypeID = models.AutoField(db_column='StampTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=STAMP_TYPE_CHOICES, max_length=7)


FEE_STRUCTURE_TYPE_CHOICES = [
    ('Flat', 'Flat'),
    ('SystemSize', 'System Size')
]


class FeeStructureType(models.Model):
    FeeStructureTypeID = models.AutoField(db_column='FeeStructureTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=FEE_STRUCTURE_TYPE_CHOICES, max_length=10)


INSPECTION_TYPE_CHOICES = [
    ('RoughIn', 'Rough In'),
    ('Final', 'Final'),
    ('Windstorm', 'Windstorm'),
    ('Electrical', 'Electrical'),
    ('Structural', 'Structural')
]


class InspectionType(models.Model):
    InspectionTypeID = models.AutoField(db_column='InspectionTypeID', primary_key=True)
    Value = models.CharField(db_column='Value', unique=True, choices=INSPECTION_TYPE_CHOICES, max_length=10)
