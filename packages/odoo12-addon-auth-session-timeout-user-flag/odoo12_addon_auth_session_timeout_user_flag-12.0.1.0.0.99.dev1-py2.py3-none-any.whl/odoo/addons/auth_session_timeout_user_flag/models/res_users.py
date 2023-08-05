from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    allow_session_termination = fields.Boolean(
        string="Allow session expiration",
        default=True
    )

    @api.model_cr_context
    def _auth_timeout_check(self):
        """
        Only check sessions from users that allow it with the flag "allow_session_termination".
        Without this, API calls to a module with 'auth_session_timeout'
        installed would raise an SessionExpiredException
        """
        if self.allow_session_termination:
            return super()._auth_timeout_check()

