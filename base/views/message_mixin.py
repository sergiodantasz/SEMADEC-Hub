from django.contrib import messages


class MessageMixin:
    success_message = ''
    error_message = ''
    warning_message = ''
    msg = {
        'success': dict(),
        'error': dict(),
    }

    def is_model_populated(self, model):
        if self.success_message:
            messages.success(self.request, self.success_message)
        elif self.error_message:
            messages.error(self.request, self.error_message)
        return model.objects.exists()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(self.request, self.success_message)
        elif msg := self.msg['success'].get('form', ''):
            messages.success(self.request, msg)
        return response

    def get_queryset(self):
        response = super().get_queryset()
        if self.warning_message:
            messages.warning(self.request, self.warning_message)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        elif msg := self.msg['success'].get('form', ''):
            messages.success(self.request, msg)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.error(self.request, self.error_message)
        elif msg := self.msg['error'].get('form', ''):
            messages.error(self.request, msg)
        return response
