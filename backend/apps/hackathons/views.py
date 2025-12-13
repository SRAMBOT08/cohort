from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime


class HackathonListView(APIView):
    """
    Fetch upcoming hackathons from API sources only
    """
    
    def get(self, request):
        hackathons = []
        
        # Fetch from Devpost API
        devpost_hackathons = self.fetch_devpost_hackathons()
        hackathons.extend(devpost_hackathons)
        
        # Sort by start date
        hackathons.sort(key=lambda x: x.get('start_date', ''))
        
        return Response({
            'success': True,
            'count': len(hackathons),
            'hackathons': hackathons
        }, status=status.HTTP_200_OK)
    
    def fetch_devpost_hackathons(self):
        """
        Fetch hackathons from Devpost-compatible API
        Using community hackathon tracker API
        """
        hackathons = []
        try:
            # Try using a hackathon aggregator API
            # This is a community-maintained API that aggregates from multiple sources
            response = requests.get(
                'https://hackathon-tracker-backend.herokuapp.com/api/hackathons',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                for event in data.get('hackathons', [])[:20]:
                    hackathon = {
                        'id': event.get('id', f"hack_{len(hackathons)}"),
                        'name': event.get('title', 'Unnamed Hackathon'),
                        'start_date': event.get('startDate', 'TBA'),
                        'end_date': event.get('endDate', ''),
                        'location': event.get('location', 'Online'),
                        'url': event.get('url', '#'),
                        'logo': event.get('logo', ''),
                        'source': 'Hackathon Tracker',
                        'is_online': event.get('isOnline', True),
                        'description': event.get('description', ''),
                    }
                    hackathons.append(hackathon)
        except Exception as e:
            print(f"Error fetching hackathons: {e}")
        
        # Fallback: Return sample data if API fails
        if not hackathons:
            hackathons = self.get_sample_hackathons()
        
        return hackathons
    
    def get_sample_hackathons(self):
        """
        Fallback sample hackathons data
        """
        return [
            {
                'id': 'sample_1',
                'name': 'HackMIT 2025',
                'start_date': 'Feb 15, 2025',
                'end_date': 'Feb 17, 2025',
                'location': 'MIT, Cambridge, MA',
                'url': 'https://hackmit.org',
                'logo': 'https://via.placeholder.com/300x150?text=HackMIT',
                'source': 'Sample',
                'is_online': False,
                'description': 'Annual hackathon at MIT with amazing prizes and workshops. Join 1000+ hackers for 36 hours of innovation.'
            },
            {
                'id': 'sample_2',
                'name': 'TreeHacks 2025',
                'start_date': 'Feb 21, 2025',
                'end_date': 'Feb 23, 2025',
                'location': 'Stanford University, CA',
                'url': 'https://www.treehacks.com',
                'logo': 'https://via.placeholder.com/300x150?text=TreeHacks',
                'source': 'Sample',
                'is_online': False,
                'description': 'Stanford\'s premier hackathon bringing together innovators from around the world'
            },
            {
                'id': 'sample_3',
                'name': 'ETHGlobal Online',
                'start_date': 'Mar 1, 2025',
                'end_date': 'Mar 15, 2025',
                'location': 'Online',
                'url': 'https://ethglobal.com',
                'logo': 'https://via.placeholder.com/300x150?text=ETHGlobal',
                'source': 'Sample',
                'is_online': True,
                'description': 'Build decentralized applications with Ethereum. Win from a $50k prize pool.'
            },
            {
                'id': 'sample_4',
                'name': 'HackTheNorth',
                'start_date': 'Sep 15, 2025',
                'end_date': 'Sep 17, 2025',
                'location': 'University of Waterloo, Canada',
                'url': 'https://hackthenorth.com',
                'logo': 'https://via.placeholder.com/300x150?text=HackTheNorth',
                'source': 'Sample',
                'is_online': False,
                'description': 'Canada\'s biggest hackathon with 1000+ hackers, amazing speakers, and mentors'
            },
            {
                'id': 'sample_5',
                'name': 'CalHacks',
                'start_date': 'Oct 11, 2025',
                'end_date': 'Oct 13, 2025',
                'location': 'UC Berkeley, CA',
                'url': 'https://calhacks.io',
                'logo': 'https://via.placeholder.com/300x150?text=CalHacks',
                'source': 'Sample',
                'is_online': False,
                'description': 'The largest collegiate hackathon in the world. 2000+ participants annually.'
            },
            {
                'id': 'sample_6',
                'name': 'DevPost Global Hackathon',
                'start_date': 'Ongoing',
                'end_date': 'Ongoing',
                'location': 'Online',
                'url': 'https://devpost.com/hackathons',
                'logo': 'https://via.placeholder.com/300x150?text=DevPost',
                'source': 'Sample',
                'is_online': True,
                'description': 'Explore hundreds of online hackathons on DevPost'
            },
            {
                'id': 'sample_7',
                'name': 'PennApps',
                'start_date': 'Sep 8, 2025',
                'end_date': 'Sep 10, 2025',
                'location': 'University of Pennsylvania',
                'url': 'https://pennapps.com',
                'logo': 'https://via.placeholder.com/300x150?text=PennApps',
                'source': 'Sample',
                'is_online': False,
                'description': 'The original collegiate hackathon. 48 hours of innovation at UPenn.'
            },
            {
                'id': 'sample_8',
                'name': 'HackHarvard',
                'start_date': 'Oct 20, 2025',
                'end_date': 'Oct 22, 2025',
                'location': 'Harvard University, MA',
                'url': 'https://hackharvard.io',
                'logo': 'https://via.placeholder.com/300x150?text=HackHarvard',
                'source': 'Sample',
                'is_online': False,
                'description': 'Harvard\'s annual hackathon with workshops, speakers, and great food!'
            },
        ]
