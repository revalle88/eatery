def groupfinder(user_id, request):
    user_role = ''
    if user_id:
        request.cur.execute("select role from users where id = %s ",
                            (user_id,))
        user_role = request.cur.fetchone()[0]
        return [user_role]


# helpers
# request method to get user role
def get_user_role(request):
    user_id = request.authenticated_userid
    if user_id is not None:
        request.cur.execute("select role from users where id = %s ",
                            (user_id,))
        user_role = request.cur.fetchone()[0]
        return user_role


# request method to get user name
def get_user_name(request):
    user_id = request.authenticated_userid
    if user_id is not None:
        request.cur.execute("select username from users where id = %s ",
                            (user_id,))
        user_name = request.cur.fetchone()[0]
        return user_name
