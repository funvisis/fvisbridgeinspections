# -*- coding: utf-8 -*-

from ..models import BridgeInspection

from django.contrib import admin

from funvisis.utils.decorators import conditional_fieldsets

@conditional_fieldsets
class BridgeInspectionAdmin(admin.ModelAdmin):
    fieldsets_base = (
        (
            u'1. Datos Generales',
            {
                'fields': (
                    'init_time',
                    'end_time',
                    'code')}),
        (
            u'2. Datos de los participantes',
            {
                'fields': (
                    # 'inspector',
                    'reviewer',
                    'supervisor')}),
        (
            u'Datos del edificio',
            {
                'fields': (
                    'bridge',)}),
       (
            u'8. Daños observados y estado de mantenimiento del puente', {
                'fields': (
                    'observations',)}),
        (
            u'9. Observaciones adicionales',
            {
                'fields':
                    ('additional_observations',)}),
        (
            u'10. Respaldo digital',
            {
                'fields': (
                    'document_backup',)}),
        (
            u'11. Imágenes de la estructura',
            {
                'fields': (
                    'gallery',)}),)
    

    fieldsets_super = ( )

    conditioned_fieldsets = [
        (
            lambda request: True,
            fieldsets_base),

        (
            lambda request: \
                request.user.is_superuser or \
                request.user.groups.filter(name="supervisores") or \
                request.user.groups.filter(name="revisores"),
            fieldsets_super),

        ]



    date_hierarchy = 'init_time'

    list_display = (
        'inspector',
        'init_time',
        )

    # list_filter = (
    #      'inspector',
    #     'city',)

    search_fields = [
        '^inspector__user__username',
        '^inspector__user__first_name',
        '^inspector__user__last_name',
        ]

    def save_model(self, request, obj, form, change): # The logged
                                                      # user is going
                                                      # to be the
                                                      # inspector
        if not change: # Only adding sets the inspector
            obj.inspector = request.user.fvisuser
        obj.save()

    def queryset(self, request):

        if request.user.groups.filter(name='supervisores') or \
                request.user.is_superuser:
            return BridgeInspection.objects.all()

        return BridgeInspection.objects.filter(inspector=request.user.fvisuser)


    class Media:
        js = ('js/admin/custom.js', ) 
