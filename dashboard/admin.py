"""
dashboard/admin.py
──────────────────
Registers a read-only DashboardAdmin panel so you can inspect
the aggregated stats directly from the Django admin without
navigating to each CRM app.
"""

from django.contrib   import admin
from django.db.models import Count, Sum, Q
from django.utils.html import format_html


class DashboardAdminSite(admin.AdminSite):
    """
    Optional: swap in a custom admin site with a stats header.
    Most teams just use the default admin site (see below).
    """
    site_header = 'CRM Admin'
    site_title  = 'CRM'
    index_title = 'Dashboard'


