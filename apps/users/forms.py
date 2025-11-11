"""
User registration and profile forms
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    نموذج تسجيل مستخدم جديد
    User registration form with email and name fields
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': 'البريد الإلكتروني',
            'dir': 'ltr',
        }),
        label='البريد الإلكتروني'
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': 'الاسم الأول',
        }),
        label='الاسم الأول'
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': 'اسم العائلة',
        }),
        label='اسم العائلة'
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': '+966xxxxxxxxx أو 05xxxxxxxx',
            'dir': 'ltr',
        }),
        label='رقم الجوال (اختياري)'
    )
    
    password1 = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': 'كلمة المرور',
            'dir': 'ltr',
        })
    )
    
    password2 = forms.CharField(
        label='تأكيد كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all',
            'placeholder': 'تأكيد كلمة المرور',
            'dir': 'ltr',
        })
    )
    
    accept_terms = forms.BooleanField(
        required=True,
        label='أوافق على الشروط والأحكام',
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary',
        }),
        error_messages={
            'required': 'يجب الموافقة على الشروط والأحكام للمتابعة'
        }
    )
    
    newsletter_subscribed = forms.BooleanField(
        required=False,
        label='أرغب في الاشتراك في النشرة البريدية',
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary',
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
    
    def clean_email(self):
        """
        Validate that the email is unique
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('هذا البريد الإلكتروني مستخدم بالفعل. يرجى استخدام بريد آخر أو تسجيل الدخول.')
        return email.lower()
    
    def clean_phone_number(self):
        """
        Validate phone number format (International numbers accepted)
        """
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove spaces and dashes for validation
            phone_cleaned = phone.replace(' ', '').replace('-', '')
            
            # Check if starts with + (international format)
            if phone_cleaned.startswith('+'):
                # Remove + for further validation
                phone_digits = phone_cleaned[1:]
                
                # Validate it contains only digits after +
                if not phone_digits.isdigit():
                    raise ValidationError('رقم الجوال غير صحيح. استخدم الصيغة: +966xxxxxxxxx')
                
                # Check reasonable length (7-15 digits for international numbers)
                if len(phone_digits) < 7 or len(phone_digits) > 15:
                    raise ValidationError('رقم الجوال غير صحيح. يجب أن يحتوي على 7-15 رقماً')
                
                return phone_cleaned
            
            # If no +, check local Saudi format
            else:
                phone_digits = phone_cleaned.replace('+', '')
                
                # Validate contains only digits
                if not phone_digits.isdigit():
                    raise ValidationError('رقم الجوال يجب أن يحتوي على أرقام فقط')
                
                # Accept Saudi local format (05xxxxxxxx) or international (9665xxxxxxxx)
                # Or any other format with 7-15 digits
                if len(phone_digits) < 7 or len(phone_digits) > 15:
                    raise ValidationError('رقم الجوال غير صحيح')
                
                return phone_cleaned
        
        return phone
    
    def save(self, commit=True):
        """
        Save user with email as username
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        user.phone_number = self.cleaned_data.get('phone_number', '')  # phone_number is in User model
        
        if commit:
            user.save()
            
            # Create user profile (phone_number is NOT in Profile model)
            from apps.users.models import Profile
            Profile.objects.create(
                user=user,
                newsletter_subscribed=self.cleaned_data.get('newsletter_subscribed', False)
            )
        
        return user
