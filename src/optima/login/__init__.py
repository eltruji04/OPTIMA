# OPTIMA/login/__init__.py

"""
Initialization module for the login package.

This module serves as the entry point for the login package. It imports and exports
the `login_bp` Blueprint, which handles authentication-related routes and functionality.
"""

# Import the authentication Blueprint
from .auth_blueprint import login_bp


# Export the Blueprint for use in other modules
__all__ = ["login_bp"]