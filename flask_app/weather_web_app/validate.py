
def validate_user_data(**kwargs):
    for param, val in kwargs.items():
        if param == 'username':
            if not val:
                return 'Username required.'
        if param == 'password':
            if not val:
                return 'Password required.' 
        if param == 'email':
            if val.find('@') == -1:
                return 'Invalid email address.'
