from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from .authentication import WebpageTokenAuth
from .models import User, Comment, Edit
from .utils import CommentSerializer, EditSerializer


@api_view(['GET'])
def form_validator(request):
    """
    API call to validate the form information when a new user signs up
    """
    Username = request.GET.get('Username', None)
    Email = request.GET.get('Email', None)
    usernameExists = User.objects.filter(Username=Username).exists()
    emailExists = User.objects.filter(Email=Email).exists()
    return Response({"UsernameExists": usernameExists, "EmailExists": emailExists}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_comments(request):
    """
    Endpoint to get all the comments made by a specific user.
    """
    try:
        comments = Comment.objects.filter(UserID=request.query_params.get('UserID'))
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def comment_submit(request):
    """
    Endpoint to submit a new user comment.
    """
    comment_text = request.data.get('CommentText', None)
    if comment_text is None:
        return Response('Missing comment text', status=status.HTTP_400_BAD_REQUEST)
    AHJPK = request.data.get('AHJPK', None)
    ReplyingTo = request.data.get('ReplyingTo', None)
    comment = Comment.objects.create(UserID=User.objects.get(Email=request.user),
                                     AHJPK=AHJPK,
                                     CommentText=comment_text, ReplyingTo=ReplyingTo)
    # send the serialized comment back to the front-end
    return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_edits(request):
    """
    Endpoint returning all edits made a user specified by UserID.
    """
    try:
        edits = Edit.objects.filter(ChangedBy=request.query_params.get('UserID'))
        return Response(EditSerializer(edits, many=True).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_support_email(request):
    """
    Endpoint to send mail to SunSpec's support email address.
    """
    try:
        email = request.data.get('Email')
        subject = request.data.get('Subject')
        message = request.data.get('Message')
        full_message = f'Sender: {email}\nMessage: {message}'
        send_mail(subject, full_message, settings.EMAIL_HOST_USER, [settings.SUNSPEC_SUPPORT_EMAIL], fail_silently=False)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
