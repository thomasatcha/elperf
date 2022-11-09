# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import ValidationError
from math import *
from datetime import *
import datetime
import dateutil


class hrContactInherit(models.Model):
    _inherit = 'hr.contract'

    absence = fields.Float(
	    string='Absences',
	    default=0,
	)
    adjustement = fields.Float(
	    string='Ajustement de salaire net',
	    default=0,
	)
    appel_urgence = fields.Float(
	    string="Appel d'urgence",
	    default=0,
	)
    astreinte = fields.Float(
	    string='Astreinte',
	    default=0,
	)
    conge_sans_solde = fields.Float(
	    string='Nbr de jrs de congé sans solde',
	    default=0,
	)
    indemnite_transport = fields.Float(
	    string='Indemnité de transport',
	    default=0,
	)
    prime_caisse = fields.Float(
	    string='Prime de caisse',
	    default=0,
	)
    prime_garde = fields.Float(
	     string='Prime de garde',
	     default=0,
	)
    prime_panier = fields.Float(
	    string='Prime de panier',
	    default=0,
	)
    prime_risque = fields.Float(
	    string='Prime de rique',
	)
    prime_salisure = fields.Float(
		string="Prime de salissure"
	)
    prime_speciale = fields.Float(
	    string='Prime spéciale',
	)
    prime_specialite = fields.Float(
	    string='Prime de spécialité',
	)
    prime_responsabilite = fields.Float(
	    string='Prime de responsabilté',
	)
    rapel_salaire_imp = fields.Float(
	    string='Rappel de salaire imposable',
	)
    remboursement_pret = fields.Float(
	    string='Remboursement de prêt',
	)
    sursalaire = fields.Float(
	    string='Sursalaire',
	)
    regularisation_salaire_net = fields.Float(
		string="Régularisation salaire net",
	)
    trop_percu = fields.Float(
	    string='Trop perçu sur prime',
	)
    type_paiement = fields.Selection([
        ('espece','Espèce'),
        ('virement','Virement'),
        ('cheque','Chèque banciare'),
	], string="Type de paiement", default="virement")


class hrPersoneACharge(models.Model):
    _name = 'hr.personne.acharge'
    _description = 'Personne à charge'

    name = fields.Char(
        string='Nom et prénom(s)',
        required=True,
    )
    date_naissance = fields.Date(string="Date de naissance")
    age = fields.Integer(
        string='Age',
        store=True,
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Personne à charge',
    )

    @api.onchange('date_naissance')
    def _calculer_age(self):
        for rec in self:
            if type(rec.date_naissance) != bool:
                today_year = datetime.today().year
                birth_year = rec.date_naissance.year
                age = today_year - birth_year
                rec.age = age


class hrEmployeInherit(models.Model):
    _inherit = 'hr.employee'

    persone_acharge_ids = fields.One2many(
        'hr.personne.acharge',
        'employee_id',
        string='Personnes à charge',
    )
    numero_cnss = fields.Char(
        string="Numéro de CNSS",
    )
    matricule = fields.Char(
        string='Numéro matricule',
    )
    payslip_ids = fields.One2many(
        'hr.payslip',
        'employee_id',
        string='Field Label',
    )
    heure_travail = fields.Float(
        string="Nombre d'heure de travail",
    )
    count_bancaire = fields.Char(
        string="Numéro de compte"
    )
    banque = fields.Char(
        string="Banque"
    )
    indice = fields.Float(
        string="Indice"
    )
    valeur_indice = fields.Float(
        string="Valeur indice"
    )

    @api.onchange('persone_acharge_ids')
    def onchange_persone_acharge_ids(self):
        for rec in self:
            rec.children = len(rec.persone_acharge_ids)


class RubriqueLine(models.Model):
    _name = 'rubrique.lier'
    _description = 'Description'

    nom = fields.Char(
        string='Rubrique',
    )
    montant = fields.Char(
        string='Montant',
    )


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'
    anciennete = fields.Float(string="Ancienneté")

    @api.onchange('contract_id')
    def calcule_anciennete(self):
        for rec in self:
            date_debut = rec.contract_id.date_start
            date_fin = rec.date_to
            if date_debut and date_fin:
                datef = date_debut.strftime('%Y,%m,%d')
                dated = date_fin.strftime('%Y,%m,%d')
                n1 = datef.split(',')
                n2 = dated.split(',')
                d0 = datetime.date(int(n1[0]),int(n1[1]),int(n1[2]))
                d1 = datetime.date(int(n2[0]),int(n2[1]),int(n2[2]))
                deltat = d1 - d0
                annee = (deltat.days) / 365
                mois = ((deltat.days) - int(annee) * 365)/30
                rec.anciennete = deltat.days
