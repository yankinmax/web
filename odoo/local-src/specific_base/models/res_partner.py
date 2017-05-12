# -*- coding: utf-8 -*-
# Author: Damien Crier
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import uuid

from datetime import datetime, timedelta

from odoo import models, fields, api, _


DUPLICATE_FIELDS_KEY = ['company_type', 'company_id',
                        'mobile', 'email']


class ResPartnerTitle(models.Model):
    _inherit = 'res.partner.title'

    active = fields.Boolean(default=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_product_pricelist = fields.Many2one(
        compute='_compute_product_pricelist'
    )

    @api.multi
    @api.depends('country_id')
    def _compute_product_pricelist(self):
        for p in self:
            if not isinstance(p.id, models.NewId):  # if not onchange
                p.property_product_pricelist = (
                    self.env['product.pricelist']._get_partner_pricelist(p.id)
                )
            else:
                p.property_product_pricelist = self.env['ir.property'].get(
                    'property_product_pricelist',
                    self._name
                )

    country_id = fields.Many2one(
        default=lambda self: self.env.user.company_id.partner_id.country_id
    )

    @api.model
    def _get_partner_provenance_selection(self):
        """
        -- Faire un choix --
        Internet (site Dépil Tech, article, moteur de recherche,
                  réseaux sociaux, forum de discussion,
                  bannière publicitaire...)
        Presse écrite (publicité ou article)
        Affiches / Panneaux publicitaire
        Cinéma / télévision
        Radio
        Communication Emailing
        Communication Prospectus (Flyers, publipostage en boite au lettre…)
        Téléprospection (contact téléphonique)
        SMS
        Evénement (stand sur salon, porte ouverte, foire…)
        Partenariat
         -> CE
         -> Salle de sport
         -> Ecole/étudiants
         -> Autre : préciser
        Parrainage / Amis
        En passant devant le centre / Vitrine
        Autres : préciser
        """
        return [
            ('internet', _('Internet (website, blog post, search engine,'
                           'social networks, forum, banner')),
            ('newspapers', _('Newspapers (post or advertisement')),
            ('poster', _('Poster advertising, Signboard')),
            ('tele', _('Cinema, television')),
            ('radio', _('Radio')),
            ('emailing', _('Emailing communication')),
            ('flyers',
             _('Prospectus communication (flyers, mail in letterbox')),
            ('telemarketing', _('Telemarketing (phone contact)')),
            ('sms', _('SMS')),
            ('event', _('Event (stand in salon, open doors, fair, ...)')),
            ('sponsor_ce', _('Sponsorship / Works Council')),
            ('sponsor_sport', _('Sponsorship / Fitness Center')),
            ('sponsor_school', _('Sponsorship / School')),
            ('sponsor_other', _('Sponsorship / Other (precise)')),
            ('sponsor_friend', _('Sponsorship / Friend')),
            ('passing', _('Passing by the center / Showcase')),
            ('other', _('Other (precise)')),
        ]

    @api.model
    def _get_socio_pro_categ_selection(self):
        """ Agriculteurs **Farmer**
            Artisan ** Artisan**
            Commerçant et assimilés ** Storekeeper and equivalent**
            Chefs d’entreprise de 10 salariés ou plus **Head of a company > 10
                                                        employees**
            Professions libérales **Liberal professions**
            Cadres de la fonction publique **Executive public service**
            Professeurs, Chercheurs **Teachers, Researchers**
            Professions de l’information, des arts et des spectacles
                **Information professions, arts and entertainment**
            Cadres d’entreprise privée **Executive private companies**
            Médecins, Médecins spécialistes **Doctors, Specialized Doctors**
            Professeurs des écoles, instituteurs et assimilés
                **School teachers, teachers and assimilated**
            Autres professions de la santé et du travail social
                **Other Health Professions and Social Work**
            Clergé, Autres professions religieuses
                **Clergy, other religious professions**
            Autres professions de la fonction publique
                **Other professions Public Service**
            Autres professions d'entreprise privée
                **Other private business professions**
            Techniciens **technicians**
            Contremaîtres, agents de maîtrise **Foremen, supervisors**
            Employés et agents de la fonction publique
                **Employees and agents of the Public Service**
            Policiers et militaires **Police and military**
            Employés d’entreprise privée **Employees of private enterprise**
            Personnels des services directs aux particuliers
                **Of personal services workers**
            Esthéticiens et autres professions de la beauté
                **Aestheticians and other beauty professionals**
            Ouvriers **Workers**
            Retraités **Retirees**
            Chômeurs **Unemployed**
            Militaires du contingent **Conscripts**
            Étudiants, élèves **Student, pupils**
            """
        return [
            ('farmer', _('Farmer')),
            ('artisan', _('Artisan')),
            ('storekeeper', _('Storekeeper and equivalent')),
            ('boss', _('Head of a company more than 10 employees')),
            ('liberal', _('Liberal professions')),
            ('public_executive', _('Executive public service')),
            ('researcher', _('Teachers, Researchers')),
            ('art_entertainment',
             _('Information professions, arts and entertainment')),
            ('private_executive', _('Executive private companies')),
            ('doctor', _('Doctors, Specialized Doctors')),
            ('teacher', _('School teachers, teachers and assimilated')),
            ('health_social', _('Other Health Professions and Social Work')),
            ('religious', _('Clergy, other religious professions')),
            ('other_public', _('Other professions Public Service')),
            ('other_private', _('Other private business professions')),
            ('technician', _('Technicians')),
            ('supervisor', _('Foremen, supervisors')),
            ('public_employee',
             _('Employees and agents of the Public Service')),
            ('police', _('Police and military')),
            ('private_employee', _('Employees of private enterprise')),
            ('personnal_worker', _('Personal services workers')),
            ('beauty', _('Aestheticians and other beauty professionals')),
            ('worker', _('Workers')),
            ('retiree', _('Retirees')),
            ('unemployed', _('Unemployed')),
            ('conscript', _('Conscripts')),
            ('student', _('Student, pupils')),
        ]

    @api.model
    def _get_family_situation_selection(self):
        return [('single', _('Single')),
                ('couple', _('Couple')),
                ('divorced', _('Divorced')),
                ('widower', _('Widower')),
                ]

    @api.model
    def _get_why_no_buy_selection(self):
        """
            Intraitable
            Pas de budget
            Déssaccord du conjoint
            Ce n'est pas le bon moment
            Autre
        """
        return [
            ('intractable', _('Intractable')),
            ('no_budget', _('No budget')),
            ('conjoint', _('Conjoint disagreement')),
            ('no_time', _('Not the good time')),
            ('other', _('Other')),
        ]

    @api.model
    def _get_maximum_budget_selection(self):
        l = [(x, x) for x in range(50, 550, 50)]
        l.extend([(x, x) for x in range(600, 1600, 100)])
        l.extend([
            ('more_1500', _('More than 1500')),
        ])
        return l

    @api.model
    def create(self, values):
        new_values = values.copy()
        if not new_values.get('company_type'):
            new_values['company_type'] = (
                'company'
                if new_values.get('is_company')
                else 'person'
            )
        return super(ResPartner, self).create(new_values)

    @api.depends('is_company')
    def _compute_company_type(self):
        # Do nothing
        pass

    company_type = fields.Selection(
        selection_add=[('agency_customer', 'Agency customer')],
        default=lambda self: self._default_company_type(),
        compute=False
    )

    @api.model
    def _default_company_type(self):
        return (
            'agency_customer'
            if self.env.user.has_group('scenario.grp_centers')
            else 'person'
        )

    company_type_visible = fields.Boolean(
        default=lambda self: not self.env.user.has_group(
            'scenario.grp_centers'
        ),
        compute='_compute_company_type_visible',
        store=False,
    )

    @api.multi
    def _compute_company_type_visible(self):
        for item in self:
            item.company_type_visible = not self.env.user.has_group(
                'scenario.grp_centers'
            )

    phototherapist_id = fields.Many2one(
        comodel_name='res.company.phototherapist',
        string='Phototherapist')
    birthday = fields.Date()
    provenance = fields.Selection(
        selection='_get_partner_provenance_selection',
        string='How do you know us ?')
    provenance_other = fields.Char()
    info_meeting_date = fields.Date()
    flash_test_date = fields.Date()
    flash_test_zone = fields.Char()
    flash_test_setting = fields.Char()
    flash_done = fields.Selection(
        selection=[('y', 'Yes'), ('n', 'No')],
        string='Flash test done',
        required=True,
        default='n',
        )
    socio_professional_category = fields.Selection(
        selection='_get_socio_pro_categ_selection',
        string='Socio-Professional Category'
        )
    family_situation = fields.Selection(
        selection='_get_family_situation_selection'
        )
    children_nb = fields.Integer(string='# Children')  # or Selection ???
    why_no_buy = fields.Selection(
        selection='_get_why_no_buy_selection'
        )
    maximum_budget = fields.Selection(
        selection='_get_maximum_budget_selection'
        )
    beauty_institute_attented = fields.Selection(
        selection=[('y', 'Yes'), ('n', 'No')],
        )
    comment1 = fields.Text(string='Anecdote/Vacations')
    comment2 = fields.Text(string='Cosmetic habits / Brand used')
    comment3 = fields.Text(string='Other')

    coffret_date_remise = fields.Date(
        string='Delivery date of the box',
        help='Delivery date of the gift box to the customer',
    )

    @api.multi
    def take_me_to_diagnostic_survey(self):
        self.ensure_one()
        survey_response_obj = self.env['survey.user_input']
        diagnostic_survey = self.env.ref(
            'specific_base_scen.diagnostic_survey')
        # if there's already a survey started (state=skip), relaunch this one
        if self.survey_inputs:
            for sur in self.survey_inputs:
                if sur.survey_id == diagnostic_survey and sur.state != 'done':
                    url = '%s/%s' % (diagnostic_survey.public_url, sur.token)
                    return {
                        'type': 'ir.actions.act_url',
                        'name': "Resume Survey",
                        'target': 'self',
                        'url': url,
                    }
        else:
            # else create a new one

            # generate invitation link for this partner
            # (do not send email to customer)
            token = uuid.uuid4().__str__()
            # create response with token
            now = datetime.now()
            survey_response_obj.create({
                'survey_id': diagnostic_survey.id,
                'deadline': fields.Datetime.to_string(now + timedelta(days=1)),
                'date_create': fields.Datetime.to_string(now),
                'type': 'link',
                'state': 'new',
                'token': token,
                'partner_id': self.id,
                'email': self.email}
                )
            # get link to the survey
            url = '%s/%s' % (diagnostic_survey.public_url, token)

            # open survey
            return {
                'type': 'ir.actions.act_url',
                'name': "Start Survey",
                'target': 'self',
                # 'target': 'new',
                'url': url,
            }

    _sql_constraints = [
        ('customer_unique',
         'unique(%s)' % ','.join(DUPLICATE_FIELDS_KEY),
         'It seems that there already a customer existing with same '
         'phone and email adress. Please use the search function to find it.'
         )
    ]
