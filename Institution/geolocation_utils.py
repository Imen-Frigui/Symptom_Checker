# geolocation_utils.py
from geopy.distance import great_circle
from .models import HealthCareInstitution

def find_nearest_institutions(user_location, max_distance=10):
    """Find institutions within a certain distance from the user location."""
    nearest_institutions = []
    for institution in HealthCareInstitution.objects.all():
        institution_location = (institution.latitude, institution.longitude)
        distance = great_circle(user_location, institution_location).kilometers
        
        if distance <= max_distance:
            nearest_institutions.append({
                'institution': institution,
                'distance': distance
            })
    
    # Sort institutions by distance
    nearest_institutions.sort(key=lambda x: x['distance'])
    return nearest_institutions
