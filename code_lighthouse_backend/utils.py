def retrieve_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.replace('Bearer ', '')

    return token