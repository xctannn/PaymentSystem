from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "account/login.html"
    
    def get_success_url(self):
        if self.request.user.groups.filter(name='Employee').exists():
            return reverse_lazy('invoice-home') 
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))