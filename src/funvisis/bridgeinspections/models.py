# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from funvisis.users.models import FVISUser
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

    # 3. General data and set location
    bridge_distributor_highway_name = models.CharField(
		max_length=50, 
		verbose_name=u'3.1 Nombre del Puente, Distribuidor o Autopista')
    road_function = models.CharField(
        max_length=20, verbose_name= u'3.2 Función vial',
        choices=(
            (u'puente', u'Puente'),
            (u'elevado', u'Tramo elevado'),
            (u'distribuidor', u'Distribuidor'),),)
    state = models.CharField(
		max_length=25, verbose_name=u'3.3 Estado',  blank=True)
    city = models.CharField(
		max_length=25, verbose_name=u'3.4 Ciudad',  blank=True)
    municipality = models.CharField(
        max_length=100, verbose_name=u'3.5 Municipio')
    parish = models.CharField(
		max_length=100, verbose_name=u'3.6 Parroquia')
    urbanization = models.CharField(
        max_length=100, verbose_name=u'3.7 Urb, Sector, Barrio')
    
    # 4. Ramp or independent bridge identification and location
    name_or_direction_identification = models.CharField(
        max_length=50, 
		verbose_name=u'4.1 Nombre o identificación de sentidos')
    name_of_road_on_bridge = models.CharField(
		max_length=40,
		verbose_name=u'4.2.1 Nombre de vía sobre el puente',
        blank=True)
    road_type = models.CharField(
		max_length = 40,
        blank=True,
        verbose_name=u'4.2.2 Tipo',
		choices=(
			(u'autopista', u'Autopista'),
			(u'calle_o_avenida', u'Calle o Avenida'),),)
    under_bridge_element_name = models.CharField(
		max_length=50, 
        blank=True,
		verbose_name=u'4.3.1 Nombres de vías, ríos u otros elementos bajo el puente')
    under_bridge_element_type = models.CharField(
		max_length=30,
        blank=True, 
		verbose_name=u'4.3.2 Tipos de elementos bajo el puente',
		choices=(
			(u'autopista', u'Autopista'),
			(u'calle_o_avenida', u'Calle o Avenida'),
			(u'rio', u'Río'),
			(u'edificacion', u'Edificación'),
			(u'instalacion_importante', u'Instalación importante'),
			(u'otros', u'Otros'),),)
    access_to_important_facility = models.BooleanField(
            blank=False,
			verbose_name=u'4.4.1 ¿El puente da acceso a inst. importante?',
			choices=(
			    (True, 'Sí'),
			    (False, 'No'),),)
    name_of_important_facility = models.CharField(
		max_length=100,
        blank=True,
		verbose_name=u'4.4.2 Nombre de la inst. importante')
    coord_pins = models.FloatField(
        verbose_name=u'4.5.1 Coord. P.I. N-S', null=True, blank=True)
    coord_pieo = models.FloatField(
        verbose_name=u'4.5.2 Coord. P.I. E-O', null=True, blank=True)
    coord_pfns = models.FloatField(
        verbose_name=u'4.6.1 Coord. P.F. N-S', null=True, blank=True)
    coord_pfeo = models.FloatField(
        verbose_name=u'4.6.2 Coord. P.F. E-O', null=True, blank=True)

   	# 5. Bridge age
    year = models.IntegerField(
        verbose_name=u'5.1 Año', null=True, blank=True)
    source = models.CharField(
		max_length=50, verbose_name=u'5.2 Fuente')
    year_range = models.CharField(
        max_length=20, 
        verbose_name = u'5.3 Rango del año de construcción',
        choices=(
            ('<1968', 'Antes de 1968'),
            ('[1968, 1985]', 'Entre 1968 y 1985'),
            ('[1986, 1998]', 'Entre 1986 y 1998'),
            ('>1998', 'Después de 1998'),))

    # 6. Ground conditions
    location = models.CharField(
        max_length=40, verbose_name=u'6.1 Ubicación',
        choices=(
            ('planicie_o_ladera_inferior', u'En Planicie o la mitad superior de una ladera'),
            ('ladera_superior_o_cima', u'En la mitad superior de una ladera o en la cima de una ladera'),),)

    maximum_ground_slope = models.CharField(
        max_length=10, verbose_name=u'6.2 Pendiente máxima de la ladera',
        choices=(
            ('<20', 'Menor a 20°(36%))'),
            ('>20', 'Mayor a 20°(36%))'),),
        )
    soil_weakness = models.CharField(
		max_length=20, 
		verbose_name=u'6.3 Susceptibilidad de licuación del suelo',
        choices=(
			('baja', 'Baja'),
			('moderada', 'Moderada'),
			('alta', 'Alta'),
			('desconocida', 'No se conoce'),),)

    # 7. Geometric and Structural Characteristics
    bridge_length = models.FloatField(
        verbose_name=u'7.1 Longitud del puente')
    bridge_width = models.FloatField(
        verbose_name=u'7.2 Ancho del puente')
    segment_number = models.FloatField(
        verbose_name=u'7.3 Número de tramos')
    maximum_distance_between_columns = models.FloatField(
        verbose_name=u'7.4 Luz máxima')
    maximum_column_height = models.FloatField(
        verbose_name=u'7.5 Altura máxima de pilas')
    joint_number_on_road = models.FloatField(
        verbose_name=u'7.6 Número de juntas en la losa del tablero')
    L_relation_between_close_segments = models.CharField(
        max_length=4,
        verbose_name=u'7.7 Relación L en tramos adyacentes',
        choices=(
            ('<2', '<2.0'),
            ('>2', '>2.0'),),)
    H_relation_between_close_columns = models.CharField(
        max_length=4,
        verbose_name=u'7.8 Relación H en pilas adyacentes',
        choices=(
            ('<2', '<2.0'),
            ('>2', '>2.0'),),)
    straight_bridge = models.BooleanField(
        verbose_name=u'7.9 Alineamiento del puente',
        blank=False,
        choices=(
		    (True, 'Recto'),
		    (False, 'Curvo'),),)
    subtended_angle = models.IntegerField(
        verbose_name=u'7.10 Ángulo Subtendido',)
    bridge_deviation = models.IntegerField(
        verbose_name=u'7.11 Esviaje del puente',)
    structure_continuity = models.CharField(
        max_length=40,
        verbose_name=u'7.12 Continuidad de la estructura',
        choices=(
            ('apoyados', 'Tableros simplemente apoyados'),
            ('continuos', u'Tableros contínuos'),
            ('totalmente_continuo', 'Estructura totalmente contínua'),),)
    superstructure_type = models.CharField(
        max_length=40,
        verbose_name=u'7.13 Tipo de superestructura',
        choices=(
            (u'MACIZ', u'Losa maciza de concreto (MACIZ)'),
            (u'VCON', u'Losa sobre viga de concreto (VCON)'),
            (u'VPRE', u'Losa sobre vigas prefabricadas de concreto (VPRE)'),
            (u'VCAJC', u'Losa sobre viga cajón de concreto (VCAJC)'),
            (u'ACA', u'Arco de concreto (ACA)'),
            (u'PMET', u'Losa sobre perfiles metálicos (PMET)'),
            (u'VARM', u'Losa sobre vigas de acero armadas (VARM)'),
            (u'VCAJM', u'Losa sobre viga cajón metálica (VCAJM)'),
            (u'AMI', u'Armadura metálica con arriostramiento inferior (AMI)'),
            (u'AMS', u'Armadura metálica con arriostramiento superior (AMS)'),
            (u'AAC', u'Arco de acero (ACC)'),
            (u'COLG', u'Puente colgante (COLG)'),
            (u'ATIR', u'Puente atirantado (ATIR)'),
            (u'MAMP', u'Puente de mamposteria (MAMP)'),
            (u'MAD', u'Puente de madera (MAD)'),
            (u'OTRO', u'Otro'),),)
    superstructural_type_other = models.CharField(
        max_length=40,
        verbose_name=u'OTRO - Otro, indique', 
        null=True, 
        blank=True)
    column_material_type = models.CharField(
        max_length=40,
        verbose_name=u'7.14.1 Tipo de pilas. Material',
        choices=(
            (u'concreto', u'Concreto'),
            (u'acero', u'Acero'),
            (u'otro', u'Otro'),),)
    column_material_type_other = models.CharField(
        max_length=100,
        verbose_name=u'Otro. Indique',
        null=True, blank=True)
    column_geometry_type = models.CharField(
        max_length=40,
        verbose_name=u'7.14.2 Tipo de pilas. Geometría',
        choices=(
            (u'monocolumnas', u'Pilas monocolumnas'),
            (u'multicolumnas', u'Pilas multicolumnas'),
            (u'muros', u'Pilas de muros'),
            (u'estribos', u'Solo estribos'),
            (u'otro', u'Otro'),),)
    column_geometry_type_other = models.CharField(
        max_length=100,
        verbose_name=u'Otro. Indique',
        null=True, blank=True)
    is_any_column_a_pergola = models.BooleanField(
        verbose_name=u'7.14.3 ¿Alguna de las pilas es de tipo pérgola?',
        blank=False,
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    does_columns_had_side_capitals_tops = models.CharField(
        max_length=40,
        blank=False,
        verbose_name=u'7.15 ¿Las pilas tienen topes laterales en el capitel?',
        choices=(
            ('si', 'Sí'),
            ('no', 'No'),
            ('algunas', 'Sólo algunas') ,),)
    does_board_has_individuals_beams = models.BooleanField(
        verbose_name=u'7.16 ¿El tablero posee vigas individuales y esta soportado por columnas o pedestales individuales sin capitel?',
        blank=False,
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    does_board_has_two_or_tree_beams = models.BooleanField(
        verbose_name=u'7.17 ¿El tablero posee 2 ó 3 vigas individuales y la viga exterior esta cerca del borde lateral del apoyo?',
        choices=(
		    (True, 'Sí'),
		    (False, 'No'),),)
    superstructure_number_of_discontinuities = models.IntegerField(
        verbose_name=u'7.18 Nro. de discontinuidades en la superestructura',)
    typical_joint_length = models.FloatField(
        verbose_name=u'7.19 Longitud de apoyo típica en las juntas',)
    does_bridge_horizontally_linked_to_others_structures = models.BooleanField(
        verbose_name=u'7.20.1 ¿La estructura del puente esta vinculada horizontalmente a otras estructuras?',
            choices=(
		    (True, 'Sí'),
		    (False, 'No'),))
    horizontally_linked_structures_names = models.CharField (
        max_length=100,
        verbose_name=u'7.20.2 Nombre de estructuras vinculadas horizontalmente:',
        blank=True,)
    does_bridge_vertically_linked_to_others_structures = models.BooleanField(
        verbose_name=u'7.21.1 ¿La estructura del puente esta vinculada verticalmente a otras estructuras?',
        blank=False,
            choices=(
		    (True, 'Sí'),
		    (False, 'No'),))
    verticallyy_linked_structures_names = models.CharField (
        max_length=100,
        verbose_name=u'7.21.2 Nombre de estructuras vinculadas verticalmente:',
        blank=True,)

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

