# Copyright 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

import werkzeug
import odoo.http as http
from odoo.http import request

from odoo import _

from odoo.osv.expression import OR
from odoo.addons.project_portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def portal_my_tasks_prepare_task_search_domain(self, search_in, search):
        domain = super(CustomerPortal, self)\
            .portal_my_tasks_prepare_task_search_domain(search_in, search)

        if search and search_in:
            if search_in in ('content', 'all'):
                domain = OR([domain, [('key', 'ilike', search)]])
        return domain

    def portal_my_tasks_prepare_searchbar(self):
        searchbar = super(CustomerPortal, self)\
            .portal_my_tasks_prepare_searchbar()

        searchbar['sorting'].update({
            'key': {'label': _('Key'), 'order': 'key'},
        })

        return searchbar

    def get_task_url(self, key):
        env = request.env()

        Task = env['project.task']
        tasks = Task.search([('key', '=ilike', key)])

        url = "/my/task/%s"
        return url % (tasks and tasks.id or -1)

    def get_project_url(self, key):
        env = request.env()

        Project = env['project.project']
        projects = Project.search([('key', '=ilike', key)])
        if not projects.exists():
            return False

        url = "/my/project/%s"
        return url % (projects and projects.id or -1)

    @http.route(['/my/browse/<string:key>'], type='http', auth="user", website=True)
    def open_human_url(self, key, **kwargs):
        redirect_url = self.get_project_url(key)
        if not redirect_url:
            redirect_url = self.get_task_url(key)
        return werkzeug.utils.redirect(redirect_url or '', 301)
