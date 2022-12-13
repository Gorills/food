from accounts.models import UserProfile

def userprofile(request):

    try:
        id = request.session['user_profile_id']
        return {'userprofile': UserProfile.objects.get(id=id)}
    except:
        return {'userprofile': []}