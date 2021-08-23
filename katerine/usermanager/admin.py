from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class SemacUserAdminPanel(UserAdmin):

    search_fields = ('email',)
    list_filter = ('email', 'is_staff', 'is_superuser', 'is_active')
    ordering = ('-email',)
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')

    readonly_fields = ('email',)

    fieldsets = (
        ('Login Data', {'fields': ('email', 'password')}),
        ('Django Data', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )


class UserPersonalDataAdminPanel(admin.ModelAdmin):

    search_fields = ('cpf', 'user_email__email', 'full_name')
    ordering = ('-full_name',)
    list_display = ('cpf', 'full_name', 'user_email')

    readonly_fields = ('cpf', 'user_email')

    fieldsets = (
        ('Related User', {'fields': ('user_email',)}),
        ('Personal Data', {'fields': ('full_name', 'cpf', 'dob')}),
        ('Location', {'fields': ('state', 'city', 'address')}),
        ('Contact', {'fields': ('contact_number',)})
    )


class UserUnespDataAdminPanel(admin.ModelAdmin):

    search_fields = ('ra', 'user_cpf__cpf', 'course_name')
    ordering = ('-ra',)
    list_display = ('ra', 'course_name', 'user_cpf')

    readonly_fields = ('ra', 'user_cpf')

    fieldsets = (
        ('Data', {'fields': ('ra', 'user_cpf', 'course_name')}),
    )


class SubscriptionAdminPanel(admin.ModelAdmin):

    search_fields = ('id', 'user_cpf__cpf', 'user_cpf__full_name', 'type')
    list_filter = ('type', 'is_payed')
    ordering = ('-id',)
    list_display = ('id', 'user_cpf', 'type', 'is_payed')

    fieldsets = (
        ('Subscription Data', {'fields': ('type', 'is_payed')}),
        ('User Data', {'fields': ('user_cpf',)})
    )


class LecturerAdminPanel(admin.ModelAdmin):

    search_fields = ('id', 'full_name', 'email')
    ordering = ('-id',)
    list_display = ('id', 'full_name', 'email')

    fieldsets = (
        ('Data', {'fields': ('full_name', 'email')}),
    )


class LectureAdminPanel(admin.ModelAdmin):

    search_fields = ('id', 'title', 'lecturer_id__id', 'lecturer_id__full_name', 'date_and_time')
    ordering = ('-id',)
    list_display = ('id', 'title', 'lecturer_id', 'date_and_time')

    fieldsets = (
        ('Lecture Data', {'fields': ('title', 'date_and_time')}),
        ('Lecturer Data', {'fields': ('lecturer_id',)})
    )


class PersonOnLectureAdminPanel(admin.ModelAdmin):

    search_fields = ('id', 'lecture_id__id', 'lecture_id__title', 'lecture_id__date_and_time', 'user_cpf__cpf',
                     'user_cpf__full_name')
    ordering = ('-id',)
    list_display = ('id', 'lecture_id', 'user_cpf')

    fieldsets = (
        ('Lecture with person data', {'fields': ('lecture_id', 'user_cpf')}),
    )

'''
class VacDosesAdminPanel(admin.ModelAdmin):
    search_fields = ('id', 'date_and_time', 'vac_batch', 'room')
    list_filter = ('was_person_vaccinated', 'was_medical_staff_vaccinated', 'was_employee_vaccinated')
    ordering = ('-id',)
    list_display = ('id', 'date_and_time', 'room', 'was_person_vaccinated', 'was_medical_staff_vaccinated',
                    'was_employee_vaccinated', 'vac_batch')

    readonly_fields = ['id']

    fieldsets = (
        ('Control Data', {'fields': ('id', 'date_and_time', 'next_dose', 'due_alert')}),
        ('Where was applied', {'fields': ['room']}),
        ('Who applied', {'fields': ['medical_staff']}),
        ('Who got applied', {'fields': ('was_person_vaccinated', 'was_medical_staff_vaccinated',
                                        'was_employee_vaccinated', 'vaccinated_person',
                                        'vaccinated_medical_staff', 'vaccinated_employee')}),
        ('Type and batch', {'fields': ('vac_type', 'vac_batch')}),
        ('Doses', {'fields': ['doses']}),
    )
'''


admin.site.register(models.SemacUser, SemacUserAdminPanel)
admin.site.register(models.UserPersonalData, UserPersonalDataAdminPanel)
admin.site.register(models.UserUnespData, UserUnespDataAdminPanel)
admin.site.register(models.Subscription, SubscriptionAdminPanel)
admin.site.register(models.Lecturer, LecturerAdminPanel)
admin.site.register(models.Lecture, LectureAdminPanel)
admin.site.register(models.PersonOnLecture, PersonOnLectureAdminPanel)
