from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from mickroservices.models import QuestionModel
from mickroservices.forms import QuestionForm
from mickroservices.utils import send_message


class QuestionView(FormView):
    """ """    
    template_name = 'faq.html'      
    success_url = reverse_lazy('faqview')
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        ctx = super(QuestionView, self).get_context_data(**kwargs)
        ctx['questions_ok'] = QuestionModel.objects.filter(status=QuestionModel.ST_OK)[:5]
        ctx['breadcrumb'] = [{'title':'FAQ'}]
        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        ctx = self.get_context_data(**kwargs)
        if form.is_valid():
            print('is_valid')
            self.form_valid(form)
            ctx.update(self.form_valid_send_message(
                       form,
                       'Обращение в техподдержку',
                       settings.DEFAULT_SUPORT_EMAIL,
                       self.get_context_data(**kwargs)))
            ctx['status'] = 'Ваше вопрос принят на рассмотрение!'
            ctx.pop('errors')
        else:
            ctx['errors'] = f'Ошибка заполнения полей: {form.errors}'            

        return TemplateResponse(request, self.template_name, ctx)
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.name = self.request.user
        form.save()

    def form_valid_send_message(self, form, subject, to_email, ctx):
        if form.is_valid():
            error = send_message(template='emails/email_question.html',
                                 subject=subject,
                                 ctx={},
                                 to_email=to_email,
                                 request=self.request)
            if not error:

                ctx['status'] = 'email_send'
            else:
                ctx['errors'] = 'Ошибка отправления письма'
        else:
            ctx['errors'] = 'Что-то пошло не так: одно из полей было заполнено некорректно. Повторите попытку отправки формы.'
        return ctx

