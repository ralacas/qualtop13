# -*- encoding: utf-8 -*-
###########################################################################
# Desarrollado por German Ponce
############################################################################
#    Coded by: german_442 email: (german.ponce@argil.mx)
##############################################################################


{
    'name': 'Segmentación por Etiquetas Especiales',
    'version': '1',
    "author" : "German Ponce Dominguez",
    "category" : "EDI",
    "summary": "Modulo para manejo de etiquetas de Analisis por Periodos.",
    'description': """

    
    Addenda Chrysler PPY
    """,
    "website" : "http://argil.mx",
    "license" : "AGPL-3",
    "depends" : ["account","l10n_mx_edi","analytic"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
                "views/wizard_segmentation.xml",
                "views/extra_fits_view.xml",
                "security/ir.model.access.csv",
              ],
    "installable" : True,
    "active" : False,
}
