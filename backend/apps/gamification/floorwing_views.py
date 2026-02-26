"""
Floor Wing views for gamification management
Floor wings can create/manage seasons and episodes
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime

from .models import Season, Episode
from .serializers import SeasonSerializer, EpisodeSerializer


def is_floor_wing(user):
    """Check if user is a floor wing"""
    try:
        return user.profile.role == 'FLOOR_WING'
    except:
        return False


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_seasons(request):
    """
    GET: List all seasons
    POST: Create a new season
    """
    if not is_floor_wing(request.user):
        return Response(
            {'error': 'Only floor wings can manage seasons'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        seasons = Season.objects.all().order_by('-season_number')
        serializer = SeasonSerializer(seasons, many=True)
        return Response({'seasons': serializer.data})
    
    elif request.method == 'POST':
        name = request.data.get('name')
        season_number = request.data.get('season_number')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        is_active = request.data.get('is_active', False)
        
        if not all([name, season_number, start_date, end_date]):
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse date strings to date objects
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if season number already exists
        if Season.objects.filter(season_number=season_number).exists():
            return Response(
                {'error': 'Season number already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If setting as active, deactivate other seasons
        if is_active:
            Season.objects.all().update(is_active=False)
        
        season = Season.objects.create(
            name=name,
            season_number=season_number,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active
        )
        
        serializer = SeasonSerializer(season)
        return Response({
            'message': 'Season created successfully',
            'season': serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_season_detail(request, season_id):
    """
    PUT: Update a season
    DELETE: Delete a season
    """
    if not is_floor_wing(request.user):
        return Response(
            {'error': 'Only floor wings can manage seasons'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    season = get_object_or_404(Season, id=season_id)
    
    if request.method == 'PUT':
        # Update season fields
        season.name = request.data.get('name', season.name)
        
        # Parse date strings if provided
        start_date = request.data.get('start_date', season.start_date)
        end_date = request.data.get('end_date', season.end_date)
        
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        season.start_date = start_date
        season.end_date = end_date
        
        is_active = request.data.get('is_active', season.is_active)
        if is_active and not season.is_active:
            # Deactivate other seasons
            Season.objects.exclude(id=season_id).update(is_active=False)
        
        season.is_active = is_active
        season.save()
        
        serializer = SeasonSerializer(season)
        return Response({
            'message': 'Season updated successfully',
            'season': serializer.data
        })
    
    elif request.method == 'DELETE':
        season.delete()
        return Response({
            'message': 'Season deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_episodes(request, season_id):
    """
    GET: List episodes for a season
    POST: Create a new episode
    """
    if not is_floor_wing(request.user):
        return Response(
            {'error': 'Only floor wings can manage episodes'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    season = get_object_or_404(Season, id=season_id)
    
    if request.method == 'GET':
        episodes = Episode.objects.filter(season=season).order_by('episode_number')
        serializer = EpisodeSerializer(episodes, many=True)
        return Response({'episodes': serializer.data})
    
    elif request.method == 'POST':
        episode_number = request.data.get('episode_number')
        name = request.data.get('name')
        description = request.data.get('description', '')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not all([episode_number, name, start_date, end_date]):
            return Response(
                {'error': 'All required fields must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse date strings to date objects
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if episode already exists
        if Episode.objects.filter(season=season, episode_number=episode_number).exists():
            return Response(
                {'error': f'Episode {episode_number} already exists for this season'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        episode = Episode.objects.create(
            season=season,
            episode_number=episode_number,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        
        serializer = EpisodeSerializer(episode)
        return Response({
            'message': 'Episode created successfully',
            'episode': serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_episode_detail(request, episode_id):
    """
    PUT: Update an episode
    DELETE: Delete an episode
    """
    if not is_floor_wing(request.user):
        return Response(
            {'error': 'Only floor wings can manage episodes'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    episode = get_object_or_404(Episode, id=episode_id)
    
    if request.method == 'PUT':
        episode.name = request.data.get('name', episode.name)
        episode.description = request.data.get('description', episode.description)
        episode.start_date = request.data.get('start_date', episode.start_date)
        episode.end_date = request.data.get('end_date', episode.end_date)
        episode.save()
        
        serializer = EpisodeSerializer(episode)
        return Response({
            'message': 'Episode updated successfully',
            'episode': serializer.data
        })
    
    elif request.method == 'DELETE':
        episode.delete()
        return Response({
            'message': 'Episode deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
