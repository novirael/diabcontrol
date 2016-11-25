
def is_doctor(request):
    return dict(
        is_doctor=request.user.groups.filter(name='Doctor').exists()
    )
