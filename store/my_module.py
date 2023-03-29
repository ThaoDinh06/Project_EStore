# Hàm dùng chung
def check_session(request, session_name):
    return session_name in request.session  # True / False
