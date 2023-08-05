# django-simple-ip-restrict

This middleware allows you to mark Django URL namespaces as unavailable to all
requests except those coming from a whitelisted IP subnet.


## Instructions

Add to the list of MIDDLEWARE:

    "django_simple_ip_restrict.middleware.ip_filter",

Then you can set the following keys on settings.py:

  - IP_PROTECTED_NAMESPACES: list of namespaces to block (default: ["admin"])
  - IP_NETWORKS_WHITELIST: list of subnets to allow, in CIDR notation
