# Copyright 2021-Coopdevs Treball SCCL (<https://coopdevs.org>)
# - Gerard Funosas i Planas - <gerard.funosas@somconnexio.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Auth Session Timeout with User flag",
    "version": "12.0.1.0.0",
    "depends": ["auth_session_timeout"],
    "author": "Coopdevs Treball SCCL",
    "category": "User types",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Terminate user's session after timeout only if they allow so with a user flag
    """,
    "data": ['views/res_users_views.xml', 'data/res_users.xml'],
    "installable": True,
}

