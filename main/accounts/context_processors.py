from accounts.models import UserProfile, LoyaltyCardSettings

def userprofile(request):

    try:
        id = request.session['user_profile_id']
        return {'userprofile': UserProfile.objects.get(id=id)}
    except:
        return {'userprofile': []}
    


def card_loyalty_settings(request):

    try:
        return {'card_loyalty_settings': LoyaltyCardSettings.objects.get()}
    except:
        return {'card_loyalty_settings': None}
    