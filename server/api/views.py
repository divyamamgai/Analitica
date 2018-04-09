import django.db.utils as db_utils
import django.db.models as db_models
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone

from analitica import models


@api_view(['POST'])
def auth_register(request):
    """
    API endpoint that registers a user if not already existing.
    """
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    if email is None:
        return Response({'detail': 'email field is required'},
                        status=status.HTTP_400_BAD_REQUEST)
    if password is None:
        return Response({'detail': 'password field is required'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = models.User.objects.create_user(email=email, password=password)
        user.save()
        return Response(user.serialize, status=status.HTTP_201_CREATED)
    except db_utils.IntegrityError:
        return Response({'detail': 'email already taken'},
                        status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def auth_login(request):
    """
    API endpoint that logs in the user if the email and password combination
    is correct.
    """
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    if email is None:
        return Response({'detail': 'email field is required'},
                        status=status.HTTP_400_BAD_REQUEST)
    if password is None:
        return Response({'detail': 'password field is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            user_serialized = user.serialize
            user_serialized.update({
                'token': token.key
            })
            return Response(user_serialized, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'detail': 'You are not authorized to access this page.'},
                status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(data={
            'detail': 'Email and password combination is incorrect.'},
            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def track(request):
    """
    API endpoint that tracks the visits done to third party sites of the
    admins.
    """
    tracking_id = request.data.get('tracking_id', None)
    session_data = request.data.get('session', None)
    visit_data = request.data.get('visit', None)
    if tracking_id is None or session_data is None or visit_data is None:
        return Response({'detail': 'Invalid data is provided.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = models.User.objects.get(tracking_id=tracking_id)
    except models.User.DoesNotExist:
        return Response({'detail': 'Tracking ID not found.'},
                        status=status.HTTP_404_NOT_FOUND)
    try:
        try:
            session = models.Session.objects.get(session_id=session_data
                                                 .get('id'))
        except models.Session.DoesNotExist:
            session = models.Session(session_id=session_data.get('id'),
                                     browser=session_data
                                     .get('browser').get('name'),
                                     browser_version=session_data
                                     .get('browser').get('version'),
                                     user=user)
            session.save()
        visit = models.Visit(url=visit_data.get('url'),
                             ip=visit_data.get('ip'),
                             country=visit_data.get('country'),
                             screen_resolution=visit_data
                             .get('screen_resolution'),
                             session=session)
        visit.save(force_insert=True)
        return Response({
            'session': session.serialize,
            'visit': visit.serialize
        }, status=status.HTTP_200_OK)
    except db_utils.IntegrityError as error:
        print(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def auth_logout(request):
    """
    API endpoint that logs out the user if session exists.
    """
    token, created = Token.objects.get_or_create(user=request.user)
    # Delete existing token so that user cannot authenticate APIs.
    token.delete()
    Token.objects.create(user=request.user)
    return Response(request.user.serialize, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def analytics_consolidated(request):
    """
    API endpoint that gives consolidated analytics information.
    """
    three_days_ago = timezone.now().date() - timedelta(days=3)
    total_visits = len(models.Visit.objects
                       .filter(created_at__gte=three_days_ago)
                       .all())
    total_browsers = len(models.Session.objects
                         .filter(created_at__gte=three_days_ago)
                         .values('browser', 'browser_version')
                         .distinct())
    total_countries = len(models.Visit.objects
                          .filter(created_at__gte=three_days_ago)
                          .values('country')
                          .distinct())
    total_screen_resolutions = len(models.Visit.objects
                                   .filter(created_at__gte=three_days_ago)
                                   .values('screen_resolution')
                                   .distinct())
    return Response({
        'visits': total_visits,
        'browsers': total_browsers,
        'countries': total_countries,
        'screen_resolutions': total_screen_resolutions
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def analytics_top_pages(request):
    """
    API endpoint that gives analytics information about the top pages.
    """
    three_days_ago = timezone.now().date() - timedelta(days=3)
    pages = models.Visit.objects \
                .filter(created_at__gte=three_days_ago) \
                .values('url') \
                .annotate(total=db_models.Count('url')) \
                .order_by('-total')[:10]
    return Response({'pages': pages}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def analytics_top_countries(request):
    """
    API endpoint that gives analytics information about the top countries.
    """
    three_days_ago = timezone.now().date() - timedelta(days=3)
    countries = models.Visit.objects \
                    .filter(created_at__gte=three_days_ago) \
                    .values('country') \
                    .annotate(total=db_models.Count('country')) \
                    .order_by('-total')[:10]
    return Response({'countries': countries}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def analytics_top_browsers(request):
    """
    API endpoint that gives analytics information about the top browsers.
    """
    three_days_ago = timezone.now().date() - timedelta(days=3)
    browsers = models.Visit.objects \
                   .filter(created_at__gte=three_days_ago) \
                   .annotate(name=db_models.F('session__browser'),
                             version=db_models.F(
                                 'session__browser_version')) \
                   .values('name', 'version') \
                   .annotate(total=db_models.Count('url')) \
                   .order_by('-total')[:10]
    return Response({'browsers': browsers}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def analytics_top_screen_resolutions(request):
    """
    API endpoint that gives analytics information about the top screen
    resolutions.
    """
    three_days_ago = timezone.now().date() - timedelta(days=3)
    screen_resolutions = models.Visit.objects \
                             .filter(created_at__gte=three_days_ago) \
                             .annotate(value=db_models
                                       .F('screen_resolution')) \
                             .values('value') \
                             .annotate(total=db_models
                                       .Count('value')) \
                             .order_by('-total')[:10]
    return Response({'screen_resolutions': screen_resolutions},
                    status=status.HTTP_200_OK)
