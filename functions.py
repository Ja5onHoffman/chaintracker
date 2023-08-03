import os
from database import db
from datetime import datetime
from pint import UnitRegistry

ureg = UnitRegistry()

# Update expired refresh token
def update_token(user, client):
    if user.refresh_token_expiration:
        if not user.refresh_token_expiration or user.refresh_token_expiration < datetime.now():
            refresh_response = client.refresh_access_token(client_id=os.getenv('CLIENT_ID'), 
                                                            client_secret=os.getenv('CLIENT_SECRET'), 
                                                            refresh_token=user.refresh_token)
            user.access_token = refresh_response['access_token']
            user.refresh_token = refresh_response['refresh_token']
            user.refresh_token_expiration = datetime.fromtimestamp(refresh_response['expires_at'])
            client.access_token = refresh_response['access_token']
            db.session.commit()

def update_miles(user, client):
    bikes = user.bikes
    for bike in bikes:
        strava_bike = client.get_gear(bike.id)
        bike.miles_current = round(strava_bike.distance.to(ureg.mile).magnitude, 1)
        print('miles updated')
        db.session.commit()
