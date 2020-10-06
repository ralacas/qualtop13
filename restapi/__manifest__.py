# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Odoo REST API',
    'version': '1.0',
    'summary': """The Odoo RESTful API that accesses Odoo using standard HTTP GET, PUT, POST, and DELETE methods and a simple JSON input and output format
    
    The Odoo REST API can be used for a variety of purposes such as:
================================================================

* Calling Methods to check access rights, list records, count records, read records, listing record fields, create, update and delete records
* Workflow Manipulations
* Report Printing and
* Inspection and Introspection

via endpoints.

Check out our http://odoo-restapi.readthedocs.io online docs for a quick reference guide to use the odoo REST API.
    
    restapi
restful api
restfulapi
 HTTP GET, PUT, POST, and DELETE methods
JSON input and output format
JSON input & output format
OAuth1 and OAuth2
OAuth1 & OAuth2
OAuth1 OAuth2
endpoints
Calling Methods
Check Access Rights
List Records
count Records
Inspection and Introspection
Inspection Introspection
Activate Developer Mode
configuration
Workflow Manipulations
ir.model
ir.model.fields
Report Printing
Print Single Report
Print List Reports
connection
odoo server
OAuth applications
Consumer Key and Secret
Consumer Key & Secret
Request Headers
Credential Request
    """,
    'category': 'Tools',
    'description': """
The Odoo API is a RESTful web service and uses both the OAuth1 and OAuth2 protocols to authenticate 3rd party applications.

The Odoo REST API can be used for a variety of purposes such as:
================================================================

* Calling Methods to check access rights, list records, count records, read records, listing record fields, create, update and delete records
* Workflow Manipulations
* Report Printing and
* Inspection and Introspection

via endpoints.

Check out our http://odoo-restapi.readthedocs.io online docs for a quick reference guide to use the odoo REST API.
    """,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'https://www.synconics.com',
    'depends': ['base', 'web', 'base_automation'],
    'external_dependencies': {
            'python': ['oauthlib']},
    'data': [
        'views/auth_view.xml',
        'views/restapi_cron.xml',
        'security/ir.model.access.csv',
        'data/auth_data.xml',
    ],
    'demo': [],
    'css': [],
    'qweb': [],
    'js': [],
    'test': [],
    'images': [
        'static/description/main_screen.jpg',
    ],
    'price': 120,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
