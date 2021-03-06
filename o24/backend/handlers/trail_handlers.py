import o24.backend.handlers.trail_failed_handlers as failed_handlers
import o24.backend.handlers.trail_carryout_handlers as carryout_handlers
import o24.backend.handlers.trail_block_handlers as block_handlers

import os
from o24.globals import *


FAILED_HANDLERS = {
    TRAIL_UNKNOWN_ERROR: failed_handlers.system_error
}

CARRYOUT_HANDLERS = {
    LINKEDIN_SEARCH_ACTION: carryout_handlers.linkedin_search_action,
    LINKEDIN_PARSE_PROFILE_ACTION: carryout_handlers.linkedin_parse_profile_action,
    LINKEDIN_POST_PARSING_ACTION: carryout_handlers.linkedin_post_parsing_action,
    EMAIL_CHECK_BOUNCED_ACTION: carryout_handlers.email_check_bounced_action,
    CARRYOUT_DEFAULT_HANDLER: carryout_handlers.default_handler
}

BLOCK_HANDLERS = {
    BLOCK_HAPPENED : block_handlers.block_happend,
    NEED_USER_ACTION_RESOLVED : block_handlers.block_resolved,
    BLOCK_DEFAULT_HANDLER : block_handlers.block_default
}