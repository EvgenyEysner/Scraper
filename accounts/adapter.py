from allauth.account.adapter import DefaultAccountAdapter


# функция переопределения редиректов allauth
class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = '/profile'
        return path

    def get_logout_redirect_url(self, request):
        path = '/'
        return path

    def get_signup_redirect_url(self, request):
        path = '/profile'
        return path