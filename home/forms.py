from django import forms
from home.models import Subscriber, ContactMessage

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']

    def clean_email(self):
        if Subscriber.objects.filter(email=self.cleaned_data.get("email")).count() > 0:
            raise forms.ValidationError('You are already subscribed.')
        return self.cleaned_data.get("email")

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['group','name', 'email','cell','subscribe','message']
