from django.contrib.auth import get_user_model
from ahj_app.models import *
from fixtures import *
import pytest
import datetime


def create_ahj(ahjpk, ahjid, mpoly_obj):
    polygon = Polygon.objects.create(Polygon=mpoly_obj, LandArea=1, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
    address = Address.objects.create()
    ahj = AHJ.objects.create(AHJPK=ahjpk, AHJID= ahjid, PolygonID=polygon, AddressID=address)
    return ahj

@pytest.fixture
def three_users(create_user):
    return create_user(Email='a@a.com'), create_user(Email='b@b.com'), create_user(Email='c@c.com')

@pytest.fixture
def two_ahjs(ahj_obj, mpoly_obj):
    return ahj_obj, create_ahj(2,2, mpoly_obj)

@pytest.fixture
def document_submission_methods():
    return DocumentSubmissionMethod.objects.create(Value='SolarApp'), DocumentSubmissionMethod.objects.create(Value='Email'), DocumentSubmissionMethod.objects.create(Value='InPerson')

@pytest.fixture
def permit_issue_methods():
    return PermitIssueMethod.objects.create(Value='SolarApp'), PermitIssueMethod.objects.create(Value='Email'), PermitIssueMethod.objects.create(Value='InPerson')

"""
    AHJ Model
"""

@pytest.mark.django_db
def test_ahj_get_confirmed_contacts(two_ahjs, three_users):
    ahj1, ahj2 = two_ahjs
    user1, user2, user3 = three_users
    assert len(ahj1.get_contacts()) == 0

    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=True) 
    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=True)
    assert len(ahj1.get_contacts()) == 2

    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=None) # unconfirmed contact at this AHJ
    Contact.objects.create(ParentTable='AHJ', ParentID=ahj2.AHJPK, ContactStatus=True) # Active contact at a different AHJ
    assert len(ahj1.get_contacts()) == 2

@pytest.mark.django_db
def test_ahj_get_unconfirmed_contacts(two_ahjs, three_users):
    ahj1, ahj2 = two_ahjs
    user1, user2, user3 = three_users
    assert len(ahj1.get_unconfirmed()) == 0

    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=None) 
    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=None)
    assert len(ahj1.get_unconfirmed()) == 2

    Contact.objects.create(ParentTable='AHJ', ParentID=ahj1.AHJPK, ContactStatus=True) # confirmed contact at this AHJ
    Contact.objects.create(ParentTable='AHJ', ParentID=ahj2.AHJPK, ContactStatus=None) # unconfirmed contact at a different AHJ
    assert len(ahj1.get_unconfirmed()) == 2

@pytest.mark.django_db
def test_ahj_get_comments(two_ahjs, three_users):
    ahj1, ahj2 = two_ahjs
    user1, user2, user3 = three_users
    assert len(ahj1.get_comments()) == 0

    Comment.objects.create(CommentID=1, AHJPK=ahj1.AHJPK, UserID=user1)
    Comment.objects.create(AHJPK=ahj1.AHJPK, UserID=user2, CommentText='This is a comment.') 
    assert len(ahj1.get_comments()) == 2 # See if empty and normal comment are connected to the AHJ
    Comment.objects.create(UserID=user1, CommentText='This is a comment.', ReplyingTo=1) 
    Comment.objects.create(AHJPK=ahj2.AHJPK, UserID=user2, CommentText='This is a comment.') 
    assert len(ahj1.get_comments()) == 2 # Make sure nested comment on this AHJ and comments on other AHJs don't get returned.

@pytest.mark.django_db
def test_ahj_get_confirmed_inspections(two_ahjs):
    ahj1, ahj2 = two_ahjs
    assert len(ahj1.get_inspections()) == 0

    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection1', InspectionStatus=True) 
    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection2', InspectionStatus=True)
    assert len(ahj1.get_inspections()) == 2

    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection3', InspectionStatus=None)  # unconfirmed inspection at this AHJ
    AHJInspection.objects.create(AHJPK=ahj2, AHJInspectionName='Inspection4', InspectionStatus=True)  # confirmed inspection at a different AHJ
    assert len(ahj1.get_inspections()) == 2

@pytest.mark.django_db
def test_ahj_get_unconfirmed_inspections(two_ahjs):
    ahj1, ahj2 = two_ahjs
    assert len(ahj1.get_unconfirmed_inspections()) == 0

    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection1', InspectionStatus=None) 
    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection2', InspectionStatus=None) 
    assert len(ahj1.get_unconfirmed_inspections()) == 2

    AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection3', InspectionStatus=True)  # confirmed inspection at this AHJ
    AHJInspection.objects.create(AHJPK=ahj2, AHJInspectionName='Inspection4', InspectionStatus=None)  # unconfirmed inspection at a different AHJ
    assert len(ahj1.get_unconfirmed_inspections()) == 2

@pytest.mark.django_db
def test_ahj_get_confirmed_dsm(two_ahjs, document_submission_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = document_submission_methods
    assert len(ahj1.get_document_submission_methods()) == 0

    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method1, MethodStatus=True)
    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method2, MethodStatus=True) 
    assert len(ahj1.get_document_submission_methods()) == 2

    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method3, MethodStatus=None) # unconfirmed dsm
    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj2, DocumentSubmissionMethodID=method3, MethodStatus=True) # confirmed dsm different ahj
    assert len(ahj1.get_document_submission_methods()) == 2

@pytest.mark.django_db
def test_ahj_get_unconfirmed_dsm(two_ahjs, document_submission_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = document_submission_methods
    assert len(ahj1.get_uncon_dsm()) == 0

    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method1, MethodStatus=None)
    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method2, MethodStatus=None) 
    assert len(ahj1.get_uncon_dsm()) == 2

    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method3, MethodStatus=True) # confirmed dsm
    AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj2, DocumentSubmissionMethodID=method3, MethodStatus=None) # unconfirmed dsm different ahj
    assert len(ahj1.get_uncon_dsm()) == 2

@pytest.mark.django_db
def test_ahj_get_confirmed_psm(two_ahjs, permit_issue_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = permit_issue_methods
    assert len(ahj1.get_permit_submission_methods()) == 0

    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method1, MethodStatus=True)
    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method2, MethodStatus=True)
    assert len(ahj1.get_permit_submission_methods()) == 2

    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method3, MethodStatus=None) # uncofirmed psm
    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj2, PermitIssueMethodID=method1, MethodStatus=True) # confirmed psm different ahj
    assert len(ahj1.get_permit_submission_methods()) == 2

@pytest.mark.django_db
def test_ahj_get_unconfirmed_psm(two_ahjs, permit_issue_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = permit_issue_methods
    assert len(ahj1.get_uncon_pim()) == 0

    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method1, MethodStatus=None)
    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method2, MethodStatus=None)
    assert len(ahj1.get_uncon_pim()) == 2

    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method3, MethodStatus=True) # confirmed psm
    AHJPermitIssueMethodUse.objects.create(AHJPK=ahj2, PermitIssueMethodID=method1, MethodStatus=None) # unconfirmed psm different ahj
    assert len(ahj1.get_uncon_pim()) == 2
    

@pytest.mark.django_db
def test_ahj_get_engineering_review_requirements(two_ahjs):
    ahj1, ahj2 = two_ahjs
    reviewType = EngineeringReviewType.objects.create(Value='ElectricalEngineer')
    requirementLevel = RequirementLevel.objects.create(Value='Required')
    assert len(ahj1.get_err()) == 0

    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=True)
    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=True)
    assert len(ahj1.get_err()) == 2

    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=None)
    EngineeringReviewRequirement.objects.create(AHJPK=ahj2, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=True)
    assert len(ahj1.get_err()) == 2

@pytest.mark.django_db
def test_ahj_get_unconfirmed_engineering_review_requirements(two_ahjs):
    ahj1, ahj2 = two_ahjs
    reviewType = EngineeringReviewType.objects.create(Value='ElectricalEngineer')
    requirementLevel = RequirementLevel.objects.create(Value='Required')
    assert len(ahj1.get_uncon_err())== 0

    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=None)
    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=None)
    assert len(ahj1.get_uncon_err()) == 2

    EngineeringReviewRequirement.objects.create(AHJPK=ahj1, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=True)
    EngineeringReviewRequirement.objects.create(AHJPK=ahj2, EngineeringReviewType=reviewType, RequirementLevel=requirementLevel, EngineeringReviewRequirementStatus=None)
    assert len(ahj1.get_uncon_err()) == 2

@pytest.mark.django_db
def test_ahj_get_fee_structures(two_ahjs):
    ahj1, ahj2 = two_ahjs
    feeStructure = FeeStructureType.objects.create(Value='Flat')
    assert len(ahj1.get_fee_structures()) == 0

    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test1', FeeStructureName='Some Fee', FeeStructureType=feeStructure, FeeStructureStatus=True)
    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test2', FeeStructureName='Submission Fee', FeeStructureType=feeStructure, FeeStructureStatus=True)
    assert len(ahj1.get_fee_structures()) == 2

    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test3', FeeStructureName='Another Fee', FeeStructureType=feeStructure, FeeStructureStatus=None) # unconfirmed fee same ahj
    FeeStructure.objects.create(AHJPK=ahj2, FeeStructureID='test4', FeeStructureName='And Another Fee', FeeStructureType=feeStructure, FeeStructureStatus=True) # confirmed fee different ahj
    assert len(ahj1.get_fee_structures()) == 2

@pytest.mark.django_db
def test_ahj_get_unconf_fee_structures(two_ahjs):
    ahj1, ahj2 = two_ahjs
    feeStructure = FeeStructureType.objects.create(Value='Flat')
    assert len(ahj1.get_uncon_fs()) == 0

    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test1', FeeStructureName='Some Fee', FeeStructureType=feeStructure, FeeStructureStatus=None)
    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test2', FeeStructureName='Submission Fee', FeeStructureType=feeStructure, FeeStructureStatus=None)
    assert len(ahj1.get_uncon_fs()) == 2

    FeeStructure.objects.create(AHJPK=ahj1, FeeStructureID='test3', FeeStructureName='Another Fee', FeeStructureType=feeStructure, FeeStructureStatus=True) # confirmed fee same ahj
    FeeStructure.objects.create(AHJPK=ahj2, FeeStructureID='test4', FeeStructureName='And Another Fee', FeeStructureType=feeStructure, FeeStructureStatus=None) # unconf fee different ahj
    assert len(ahj1.get_uncon_fs()) == 2

"""
    Comment Model
"""

@pytest.mark.django_db
def test_comment_get_replies(two_ahjs, three_users):
    ahj1, ahj2 = two_ahjs
    user1, user2, user3 = three_users
    comment1 = Comment.objects.create(CommentID=1, AHJPK=ahj1.AHJPK, UserID=user1, CommentText='Original Comment.')
    assert len(comment1.get_replies()) == 0
    comment2 = Comment.objects.create(CommentID=2, AHJPK=ahj1.AHJPK, UserID=user2, CommentText='This is a comment.', ReplyingTo=1)
    Comment.objects.create(CommentID=3, AHJPK=ahj1.AHJPK, UserID=user3, CommentText='This is a comment.', ReplyingTo=1)
    assert len(comment1.get_replies()) == 2
    Comment.objects.create(CommentID=4, AHJPK=ahj1.AHJPK, UserID=user2, CommentText='This is a comment.', ReplyingTo=2)
    assert len(comment1.get_replies()) == 2
    assert len(comment2.get_replies()) == 1

"""    
    Contact Model
"""
@pytest.fixture
def contact_obj():
    return  Contact.objects.create(ContactID=1)

@pytest.mark.django_db
def test_contact_create_relation_to__valid_param(ahj_inspection, contact_obj):
    response = contact_obj.create_relation_to(ahj_inspection)
    assert contact_obj.ContactStatus == None
    assert contact_obj.ParentTable == 'AHJInspection'
    assert response == contact_obj

@pytest.mark.django_db
def test_contact_create_relation_to__invalid_param(ahj_obj, contact_obj):
    with pytest.raises(ValueError):
        contact_obj.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_contact_get_relation_status_field(contact_obj):
    assert contact_obj.get_relation_status_field() == 'ContactStatus'

"""
    AHJInspection Model
"""
@pytest.fixture
def two_inspections(two_ahjs, three_users):
    ahj1, ahj2 = two_ahjs
    user1, user2, user3 = three_users
    inspection1 = AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection1', TechnicianRequired=1, InspectionStatus=True)
    inspection2 = AHJInspection.objects.create(AHJPK=ahj1, AHJInspectionName='Inspection2', TechnicianRequired=1, InspectionStatus=True)
    return inspection1, inspection2

@pytest.fixture
def ahj_inspection(ahj_obj):
    return  AHJInspection.objects.create(AHJPK=ahj_obj, AHJInspectionName='Inspection', TechnicianRequired=1, InspectionStatus=True)

@pytest.mark.django_db
def test_ahj_inspection_get_contacts(two_inspections):
    inspection1, inspection2 = two_inspections
    assert len(inspection1.get_contacts()) == 0
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=True) 
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=True)
    assert len(inspection1.get_contacts()) == 2
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=None) 
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection2.InspectionID, ContactStatus=True)
    assert len(inspection1.get_contacts()) == 2

@pytest.mark.django_db
def test_ahj_inspection_get_unconfirmed_contacts(two_inspections):
    inspection1, inspection2 = two_inspections
    assert len(inspection1.get_uncon_con()) == 0
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=None) 
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=None)
    assert len(inspection1.get_uncon_con()) == 2
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection1.InspectionID, ContactStatus=True) 
    Contact.objects.create(ParentTable='AHJInspection', ParentID=inspection2.InspectionID, ContactStatus=None)
    assert len(inspection1.get_uncon_con()) == 2

@pytest.mark.django_db
def test_ahj_inspection_create_relation_to__valid_param(ahj_obj, ahj_inspection):
    response = ahj_inspection.create_relation_to(ahj_obj)
    assert ahj_inspection.InspectionStatus == None
    assert response == ahj_inspection

@pytest.mark.django_db
def test_ahj_inspection_create_relation_to__invalid_param(ahj_obj, ahj_inspection):
    with pytest.raises(ValueError):
        ahj_inspection.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_ahj_inspection_get_relation_status_field(ahj_inspection):
    assert ahj_inspection.get_relation_status_field() == 'InspectionStatus'

""" 
    Fee Structure Model
"""
@pytest.fixture
def fee_structure(ahj_obj):
    return FeeStructure.objects.create(AHJPK=ahj_obj, FeeStructureName='name')

@pytest.mark.django_db
def test_fee_structure_create_relation_to__valid_param(ahj_obj, fee_structure):
    response = fee_structure.create_relation_to(ahj_obj)
    assert fee_structure.FeeStructureStatus == None
    assert response == fee_structure

@pytest.mark.django_db
def test_fee_structure_create_relation_to__invalid_param(ahj_obj, fee_structure):
    with pytest.raises(ValueError):
        fee_structure.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_fee_structure_get_relation_status_field(fee_structure):
    assert fee_structure.get_relation_status_field() == 'FeeStructureStatus'

"""
    EngineeringReviewRequirement Model
"""
@pytest.fixture
def engineering_review_requirement(ahj_obj):
    return EngineeringReviewRequirement.objects.create(AHJPK=ahj_obj)

@pytest.mark.django_db
def test_engineering_review_requirement_create_relation_to__valid_param(ahj_obj, engineering_review_requirement):
    response = engineering_review_requirement.create_relation_to(ahj_obj)
    assert engineering_review_requirement.EngineeringReviewRequirementStatus == None
    assert response == engineering_review_requirement

@pytest.mark.django_db
def test_engineering_review_requirement_create_relation_to__invalid_param(ahj_obj, engineering_review_requirement):
    with pytest.raises(ValueError):
        engineering_review_requirement.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_engineering_review_requirement_get_relation_status_field(engineering_review_requirement):
    assert engineering_review_requirement.get_relation_status_field() == 'EngineeringReviewRequirementStatus'


"""
    DocumentSubmissionMethod Model
"""
@pytest.fixture
def document_submission_method():
    return DocumentSubmissionMethod.objects.create(Value='Email')

@pytest.mark.django_db
def test_document_submission_method_create_relation_to__valid_param(ahj_obj, document_submission_method):
    document_submission_method.create_relation_to(ahj_obj)
    assert len(AHJDocumentSubmissionMethodUse.objects.all()) == 1 # A valid AHJDocumentSubmissionMethodUse object should be created as a result

@pytest.mark.django_db
def test_document_submission_method_create_relation_to__invalid_param(ahj_obj, document_submission_method):
    with pytest.raises(ValueError):
        document_submission_method.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_document_submission_method_get_relation_status_field(document_submission_method):
    assert document_submission_method.get_relation_status_field() == 'MethodStatus'

"""
    AHJDocumentSubmissionMethodUse Model
"""

@pytest.mark.django_db
def test_ahj_document_submission_method_use_get_value(two_ahjs, document_submission_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = document_submission_methods
    doc_method1 = AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method1, MethodStatus=1)
    assert doc_method1.get_value() == method1.Value
    doc_method2 = AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method2, MethodStatus=1)
    assert doc_method2.get_value() == method2.Value

@pytest.mark.django_db
def test_ahj_document_submission_method_use_get_relation_status_field(two_ahjs, document_submission_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = document_submission_methods
    doc_method = AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj1, DocumentSubmissionMethodID=method1, MethodStatus=1)
    assert doc_method.get_relation_status_field() == 'MethodStatus'

"""
    PermitIssueMethod Model
"""
@pytest.fixture
def permit_issue_method():
    return PermitIssueMethod.objects.create(Value='SolarApp')

@pytest.mark.django_db
def test_permit_issue_method_create_relation_to__valid_param(ahj_obj, permit_issue_method):
    permit_issue_method.create_relation_to(ahj_obj)
    assert len(AHJPermitIssueMethodUse.objects.all()) == 1 # A valid PermitIssueMethodUse object should be created as a result

@pytest.mark.django_db
def test_permit_issue_method_create_relation_to__invalid_param(ahj_obj, permit_issue_method):
    with pytest.raises(ValueError):
        permit_issue_method.create_relation_to(Contact.objects.create())

@pytest.mark.django_db
def test_permit_issue_method_get_relation_status_field(permit_issue_method):
    assert permit_issue_method.get_relation_status_field() == 'MethodStatus'

"""
    AHJPermitIssueMethodUse Model
"""
@pytest.mark.django_db
def test_permit_issue_method_use_get_value(two_ahjs, permit_issue_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = permit_issue_methods
    pim1 = AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method1, MethodStatus=1)
    assert pim1.get_value() == method1.Value
    pim2 = AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method2, MethodStatus=1)
    assert pim2.get_value() == method2.Value

@pytest.mark.django_db
def test_permit_issue_method_use_get_relation_status_field(two_ahjs, permit_issue_methods):
    ahj1, ahj2 = two_ahjs
    method1, method2, method3 = permit_issue_methods
    pim1 = AHJPermitIssueMethodUse.objects.create(AHJPK=ahj1, PermitIssueMethodID=method1, MethodStatus=1)
    assert pim1.get_relation_status_field() == 'MethodStatus'

"""
    User Model
"""
@pytest.mark.parametrize(
    'is_superuser', [
        False,
        True
    ]
)
@pytest.mark.django_db
def test_user_create_user(is_superuser):
    user_dict = {'Email': 'a@a.com', 'Username': 'test', 'password': 'fhieusdnjds34',
                 'FirstName': 'First', 'LastName': 'Last'}
    if is_superuser:
        user = get_user_model().objects.create_superuser(**user_dict)
    else:
        user = get_user_model().objects.create_user(**user_dict)
    if is_superuser:
        assert user.is_superuser is True
    assert user.Email == 'a@a.com'
    contact = Contact.objects.get(ContactID=user.ContactID.ContactID)
    assert contact.Email == 'a@a.com'
    assert contact.FirstName == 'First'
    assert contact.LastName == 'Last'
    assert contact.AddressID is not None
    assert contact.AddressID.LocationID is not None


@pytest.mark.django_db
def test_user_get_email_field_name(create_user):
    user = create_user(Email='a@a.com')
    assert user.get_email_field_name() == 'Email' 

@pytest.mark.django_db
def test_user_get_maintained_ahjs(create_user, two_ahjs):
    ahj1, ahj2 = two_ahjs
    user = create_user(Email='a@a.com')
    assert len(user.get_maintained_ahjs()) == 0
    AHJUserMaintains.objects.create(AHJPK=ahj1, UserID=user, MaintainerStatus=1)
    assert len(user.get_maintained_ahjs()) == 1
    AHJUserMaintains.objects.create(AHJPK=ahj2, UserID=user, MaintainerStatus=1)
    assert len(user.get_maintained_ahjs()) == 2

@pytest.mark.django_db
def test_user_get_API_token__token_exists(create_user):
    user = create_user()
    token = user.api_token
    assert user.get_API_token() == token

@pytest.mark.django_db
def test_user_get_API_token__token_does_not_exist(create_user):
    user = create_user()
    user.api_token.delete()
    assert user.get_API_token() is None

"""
    WebpageToken Model
"""
@pytest.mark.django_db
def test_WebpageToken_get_user(create_user):
    user = create_user(Email='a@a.com')
    token = WebpageToken.objects.create(user=user)
    assert token.get_user() == user

@pytest.mark.django_db
def test_WebpageToken_str(create_user):
    user = create_user(Email='a@a.com')
    token = WebpageToken.objects.create(user=user)
    assert str(token) == 'WebpageToken(' + token.key + ')'

"""
    APIToken Model
"""
@pytest.mark.django_db
def test_APIToken_str(create_user):
    token = create_user(Email='a@a.com').api_token
    assert str(token) == 'APIToken(' + token.key + ')'

"""
    Shapefile Models
"""
@pytest.mark.django_db
def test_state_temp__str__(mpoly_obj):
    statetemp = StateTemp.objects.create(GEOID=54, NAME='West Virginia', ALAND=62266296765, AWATER=63465327, INTPTLAT=40, INTPTLON=-40, mpoly=mpoly_obj)
    assert str(statetemp) == 'West Virginia'

@pytest.mark.django_db
def test_County_temp__str__(mpoly_obj):
    countytemp = CountyTemp.objects.create(GEOID=54, NAME='Orange', NAMELSAD='Orange County', ALAND=62266296765, AWATER=63465327, INTPTLAT=40, INTPTLON=-40, mpoly=mpoly_obj)
    assert str(countytemp) == 'Orange County'

@pytest.mark.django_db
def test_cousub_temp__str__(mpoly_obj):
    cousubtemp = CousubTemp.objects.create(GEOID=54, NAME='Munic', NAMELSAD='Municipality subdivision not defined', ALAND=62266296765, AWATER=63465327, INTPTLAT=40, INTPTLON=-40, mpoly=mpoly_obj)
    assert str(cousubtemp) == 'Municipality subdivision not defined'

@pytest.mark.django_db
def test_city_temp__str__(mpoly_obj):
    citytemp = CityTemp.objects.create(GEOID=54, NAME='Los Angeles', NAMELSAD='Los Angeles City', ALAND=62266296765, AWATER=63465327, INTPTLAT=40, INTPTLON=-40, mpoly=mpoly_obj)
    assert str(citytemp) == 'Los Angeles City'
