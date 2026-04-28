# config/__init__.py
"""
配置层 - 统一配置管理、Prompt模板、Provider配置
"""

from .prompts import (
    # Generation prompts
    GENERATOR_NODE_SYSTEM_PROMPT,
    GENERATOR_NODE_USER_TEMPLATE,
    GENERATOR_RELATION_SYSTEM_PROMPT,
    GENERATOR_RELATION_USER_TEMPLATE,

    # Evaluation prompts
    CHECKER_NODE_SYSTEM_PROMPT,
    CHECKER_NODE_USER_TEMPLATE,
    CHECKER_RELATION_SYSTEM_PROMPT,
    CHECKER_RELATION_USER_TEMPLATE,
)

from .provider_config import (
    ProviderConfig,
    PROVIDERS,
    get_provider,
    get_active_model,
    list_providers,
)

__all__ = [
    # Generation
    'GENERATOR_NODE_SYSTEM_PROMPT',
    'GENERATOR_NODE_USER_TEMPLATE',
    'GENERATOR_RELATION_SYSTEM_PROMPT',
    'GENERATOR_RELATION_USER_TEMPLATE',

    # Evaluation
    'CHECKER_NODE_SYSTEM_PROMPT',
    'CHECKER_NODE_USER_TEMPLATE',
    'CHECKER_RELATION_SYSTEM_PROMPT',
    'CHECKER_RELATION_USER_TEMPLATE',

    # Provider
    'ProviderConfig',
    'PROVIDERS',
    'get_provider',
    'get_active_model',
    'list_providers',
]
