# Copyright 2004-2010 Tiny SPRL
# Copyright 2018 ACSONE SA/NV
# Copyright 2020 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Belgium VAT Reports",
    "author": "ACSONE SA/NV, "
    "Coop IT Easy SCRLfs, "
    "Odoo SA, "
    "Odoo Community Association (OCA)",
    "website": "http://acsone.eu",
    "category": "Reporting",
    "version": "12.0.1.0.2",
    "license": "AGPL-3",
    "depends": ["l10n_be", "account"],
    "data": [
        "wizard/l10n_be_partner_vat_listing.xml",
        "wizard/l10n_be_vat_intra_view.xml",
        "views/report_vatintraprint.xml",
        "views/report_vatpartnerlisting.xml",
        "l10n_be_reports.xml",
    ],
    "installable": True,
}
