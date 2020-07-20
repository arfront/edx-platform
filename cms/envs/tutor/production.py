# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

DEFAULT_FROM_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
SERVER_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
TECH_SUPPORT_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
CONTACT_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
BUGS_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
UNIVERSITY_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
PRESS_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
BULK_EMAIL_DEFAULT_FROM_EMAIL = "no-reply@" + ENV_TOKENS["LMS_BASE"]
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]
API_ACCESS_FROM_EMAIL = ENV_TOKENS["CONTACT_EMAIL"]

# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/"
for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Disable django/drf deprecation warnings
import logging
import warnings
from django.utils.deprecation import RemovedInDjango30Warning, RemovedInDjango31Warning
from rest_framework import RemovedInDRF310Warning, RemovedInDRF311Warning
warnings.simplefilter('ignore', RemovedInDjango30Warning)
warnings.simplefilter('ignore', RemovedInDjango31Warning)
warnings.simplefilter('ignore', RemovedInDRF310Warning)
warnings.simplefilter('ignore', RemovedInDRF311Warning)

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "DoCYo6A99fYVfcjMgIzNV6wl"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "LqS1PWIxbPmmNGFw3tYoRlz_DcUP6PYBMwFLLggo676rTy1lZRziBToLfzHivm_VzK7rDLegYeZPAE9HlYlhCHbVONL2mPdc4JcBuCDqqW6OgOU6ZZkPFltPeZl_5WzYp2tmUXnJFW1T0NNUXco-3cWj6CaHgh6Uni64LAps0k2Ofpj3tuv4xB4jlEGwvKOnOq6eb2F0EkS9dgYHfl_o9A7aWeNfsAqCzeHEYHR_vbqCYsOj3VHC_F1q3FWcVeI3UoTzdHM_mn2nSURaVLT8621Y69JrLFL5hACesKeFDWXhr54uef8JnE3YHprjBb3WevHxLdtEy7BfykbypRFm6Q",
        "n": "818bcgMNphQ40uYmwCft6Xa4Ph_uWaflCSF1suJF2E8kU55ijeFZYnlN3zGd_h3IL6Ae5AUeJQGZEP5bbVCMbKFAOY-LVe_qefB0kFAdZaLV5CIanVAFXmeDcp0w7IU20jGp_PcdbMDKzC7xMgSj02AKY-XdOOV343Pdct8M_NNdT5_btxAqFH9ZlGZe0prI3uS32eRkHwwRrsBhTR82znQuudPRqQJ10Dbgd3aGlvHkywWb7HSO0Xn1xb_crcDdiitj_QSVjt6BIyYuj9jwtXk_Ic0WvjA8ZPyN2BNonUHfMP02yNQoUPlXGrSjFHgTqM_wzzLCW3PPzdDo5j1Raw",
        "p": "9mZzK9dZMYvfP84wfwYjLci7oN6ffw_IM1F6SLB5fd8Qo5bJsC2QDj5d_53ICIXDQ7lkNDnzxxPicDMq3aFaC_y56T-vKZI7KcEDjqLL9Tx_oJUkoIJ0OdNfzNlfd2foy5QZt_2HKoOJP5Sh73t1VN0rzmu4a9nOHGe9l4D9ySk",
        "q": "_NpzJjCdXjbl6bozSTG0IYPgXeDJK7UCl7eaqxBnvGvFHv-pxCXFExIgP6EYZnDD_dly4croOtJCsz34KyIoXatl9uo9ZrvZxjgBEJfHYJ3j9QDyd3YiWRvGVo7TS3LRyJGXAyg_54dl9CclknR64PBMcObTmurU_GbTIOM21HM",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "818bcgMNphQ40uYmwCft6Xa4Ph_uWaflCSF1suJF2E8kU55ijeFZYnlN3zGd_h3IL6Ae5AUeJQGZEP5bbVCMbKFAOY-LVe_qefB0kFAdZaLV5CIanVAFXmeDcp0w7IU20jGp_PcdbMDKzC7xMgSj02AKY-XdOOV343Pdct8M_NNdT5_btxAqFH9ZlGZe0prI3uS32eRkHwwRrsBhTR82znQuudPRqQJ10Dbgd3aGlvHkywWb7HSO0Xn1xb_crcDdiitj_QSVjt6BIyYuj9jwtXk_Ic0WvjA8ZPyN2BNonUHfMP02yNQoUPlXGrSjFHgTqM_wzzLCW3PPzdDo5j1Raw",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "DoCYo6A99fYVfcjMgIzNV6wl"
    }
]


######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"My Open edX - Studio"
MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_LOGOUT_URL = LMS_ROOT_URL + '/logout'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]

