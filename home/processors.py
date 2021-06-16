def groups_processor(request):
    return { 'grp' : str(request.user.groups.values_list('name', flat=True).first())}
