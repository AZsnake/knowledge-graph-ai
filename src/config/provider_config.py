"""
多模型 Provider 配置

支持多个 LLM Provider，统一管理 API 端点、密钥、可用模型。
新增 Provider 只需添加配置项。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os


@dataclass
class ProviderConfig:
    """单个 Provider 的配置"""
    name: str                    # 显示名称
    base_url: str                # API 端点
    env_key: str                 # 环境变量名（API Key）
    env_endpoint: str            # 环境变量名（自定义端点，可选）
    models: List[str]            # 可用模型列表
    default_model: str           # 默认模型
    description: str = ""        # 描述

    def get_api_key(self) -> Optional[str]:
        """从环境变量获取 API Key"""
        return os.getenv(self.env_key)

    def get_endpoint(self) -> str:
        """获取端点（优先使用环境变量覆盖）"""
        return os.getenv(self.env_endpoint, self.base_url)


# ── 已注册的 Provider ──────────────────────────────────────────

PROVIDERS: Dict[str, ProviderConfig] = {
    "deepseek": ProviderConfig(
        name="DeepSeek",
        base_url="https://api.deepseek.com",
        env_key="DEEPSEEK_API_KEY",
        env_endpoint="DEEPSEEK_API_ENDPOINT",
        models=["deepseek-chat", "deepseek-reasoner"],
        default_model="deepseek-chat",
        description="DeepSeek 官方 API，适合通用文本处理和深度推理",
    ),
    "sjtu_zhiyuan": ProviderConfig(
        name="致远一号 (SJTU)",
        base_url="https://models.sjtu.edu.cn/api/v1",
        env_key="SJTU_API_KEY",
        env_endpoint="SJTU_API_ENDPOINT",
        models=[
            "deepseek-chat",
            "deepseek-reasoner",
            "minimax",
            "minimax-m2.5",
            "qwen3coder",
            "qwen3vl",
        ],
        default_model="deepseek-chat",
        description="上海交大本地大模型 API (致远一号)，校园网/VPN 访问",
    ),
    # 可扩展：添加更多 Provider
    # "openai": ProviderConfig(...),
    # "zhipu": ProviderConfig(...),
    # "moonshot": ProviderConfig(...),
}


def get_provider(name: Optional[str] = None) -> ProviderConfig:
    """
    获取 Provider 配置

    优先级：
    1. 显式传入 name
    2. 环境变量 LLM_PROVIDER
    3. 默认使用 deepseek（向后兼容）
    """
    if name and name in PROVIDERS:
        return PROVIDERS[name]

    env_provider = os.getenv("LLM_PROVIDER", "").strip()
    if env_provider and env_provider in PROVIDERS:
        return PROVIDERS[env_provider]

    # 向后兼容：检查旧的环境变量
    if os.getenv("DEEPSEEK_API_KEY"):
        return PROVIDERS["deepseek"]
    if os.getenv("SJTU_API_KEY"):
        return PROVIDERS["sjtu_zhiyuan"]

    # 默认
    return PROVIDERS["deepseek"]


def get_active_model(provider_name: Optional[str] = None) -> str:
    """获取当前生效的模型名称"""
    env_model = os.getenv("LLM_MODEL", "").strip()
    if env_model:
        return env_model

    provider = get_provider(provider_name)
    return provider.default_model


def list_providers() -> List[dict]:
    """列出所有已配置的 Provider（已屏蔽敏感信息）"""
    result = []
    for key, cfg in PROVIDERS.items():
        has_key = bool(cfg.get_api_key())
        result.append({
            "id": key,
            "name": cfg.name,
            "models": cfg.models,
            "default_model": cfg.default_model,
            "configured": has_key,
            "description": cfg.description,
        })
    return result
