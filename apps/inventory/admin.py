# Import all admin classes from the admins package
# This file is required for Django to discover admin registrations
# Note: InventoryItem is managed as inline in Product admin

from apps.inventory.admins import *  # noqa
