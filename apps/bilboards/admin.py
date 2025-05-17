from django.contrib import admin
from django import forms
from .models import Location, Region, District, Billboard

# Send telegram message
import requests
from django.conf import settings
from django.contrib import messages

# Unfold
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


# User admin
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# Forma validatsiyasi
class BillboardAdminForm(forms.ModelForm):
    class Meta:
        model = Billboard
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        client = cleaned_data.get('client')
        price = cleaned_data.get('price')
        expiry_date = cleaned_data.get('expiry_date')
        total_amount = cleaned_data.get('total_amount')

        if status == 'occupied':
            errors = {}

            if not client:
                errors['client'] = "Если статус 'Занят', поле 'Клиент' обязательно."

            if price is None:
                errors['price'] = "Если статус 'Занят', поле 'Цена' обязательно."

            if expiry_date is None:
                errors['expiry_date'] = "Если статус 'Занят', поле 'Дата окончания аренды' обязательно."

            if total_amount is None:
                errors['total_amount'] = "Если статус 'Занят', поле 'Общая сумма' обязательно."

            if errors:
                raise forms.ValidationError(errors)

        return cleaned_data


# Admin interfeysi
@admin.register(Billboard)
class BillboardAdmin(ModelAdmin):
    form = BillboardAdminForm
    list_display = ('address', 'billboard_number', 'status', 'location', 'region', 'district', 'client', 'price', 'expiry_date')
    list_filter = ('status', 'location', 'region', 'district')
    search_fields = ('billboard_number', 'client', 'address')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        telegram_token = settings.TELEGRAM_BOT_TOKEN
        telegram_chat_id = settings.TELEGRAM_CHAT_ID

        if change:
            action = "♻️ Billboard yangilandi"
        else:
            action = "🆕 Yangi Billboard qo‘shildi"

        message = (
            f"*{action}!*\n\n"
            f"📍 *Manzil:* {obj.address}\n"
            f"🔢 *Raqami:* {obj.billboard_number}\n"
            f"📌 *Status:* {obj.get_status_display()}\n"
            f"👤 *Mijoz:* {obj.client or '—'}\n"
            f"💰 *Narx:* {obj.price or '—'}\n"
            f"📅 *Muddati:* {obj.expiry_date or '—'}\n"
            f"🌍 *Hudud:* {obj.region} / {obj.district}"
        )

        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.message_user(request, "✅ Telegramga xabar muvaffaqiyatli yuborildi.", messages.SUCCESS)
        except requests.exceptions.RequestException as e:
            self.message_user(
                request,
                f"❌ Telegramga xabar yuborishda xatolik: {e}",
                messages.ERROR
        )



@admin.register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location',)
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)
