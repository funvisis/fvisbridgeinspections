# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from funvisis.users.models import FVISUser
from funvisis.geo.bridges.models import Bridge
from photologue.models import Gallery


from fvislib.utils.djangorelated \
    import get_path_to_app_repo_ as get_path_to_app_repo

import os
import datetime
import time

class BridgeInspection(models.Model):

    # 1. General
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    init_time = models.DateTimeField('1.1 Hora inicio')
    end_time = models.DateTimeField(u'1.2 Hora culminación')
    code = models.CharField(u'1.3 Código', max_length=20, blank=True)

    # 2. Participants
    inspector = models.ForeignKey(
        FVISUser, related_name=u'bridge_inspector',
        verbose_name=u'2.1 Inspector')
    reviewer = models.ForeignKey(
        FVISUser,
        related_name=u'bridge_reviewer',
        verbose_name=u'2.2 Revisor',
        limit_choices_to={'user__groups__name': u'revisores'})
    supervisor = models.ForeignKey(
        FVISUser, related_name=u'bridge_supervisor',
        verbose_name=u'2.3 Supervisor',
                limit_choices_to={'user__groups__name': u'supervisores'})

    # 4. Bridge
    bridge = models.ForeignKey(
        Bridge, related_name=u'bridge',
        verbose_name=u'Puente')

    # 8. Damage Observed and Mantainment state of the bridge
    observations = models.TextField(
        verbose_name=u'8. Daños Observados y Estado General de Mantenimiento del Puente',
        )

    # 9. Additional Observations
    additional_observations = models.TextField(
        verbose_name=u'9. Observaciones Adicionales',
        blank=True,)

    # 10 Document Backup
    document_backup = models.FileField(
        verbose_name=u'10. Respaldo escaneado',
        upload_to=get_path_to_app_repo(
            project_name=settings.SETTINGS_MODULE.split('.')[0],
            app_name=__name__.split('.')[-2],
            model_name='Bridge'),
        null=True,
        blank=True)

    # 11 Gallery
    gallery = models.ForeignKey(
        Gallery, related_name=u'bridge_gallery',
        verbose_name=u'11 Galería de fotos')
    
    
    class Meta:
        verbose_name = u"Puente"
        verbose_name_plural = u"Puentes"

