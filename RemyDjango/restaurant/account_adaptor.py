from allauth.account.adapter import DefaultAccountAdapter


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False

    def get_logout_redirect_url(self, request):
        path = "/accounts/login"
        return path.format()
