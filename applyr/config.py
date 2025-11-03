"""Configuration module for personal information and branding"""

import os
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


class PersonalConfig:
    """Loads and provides access to personal information configuration"""

    _instance: Optional["PersonalConfig"] = None
    _config_data: Optional[dict[str, Any]] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> None:
        """Load configuration from config.yaml, fallback to template"""
        config_path = Path("config.yaml")
        template_path = Path("config.template.yaml")

        if config_path.exists():
            try:
                if yaml:
                    with open(config_path) as f:
                        self._config_data = yaml.safe_load(f) or {}
                else:
                    print("Warning: PyYAML not installed. Install with: poetry add pyyaml")
                    self._config_data = {}
            except Exception as e:
                print(f"Warning: Could not load config.yaml: {e}")
                self._config_data = {}
        elif template_path.exists():
            try:
                if yaml:
                    with open(template_path) as f:
                        self._config_data = yaml.safe_load(f) or {}
                else:
                    self._config_data = {}
            except Exception as e:
                print(f"Warning: Could not load config.template.yaml: {e}")
                self._config_data = {}
        else:
            self._config_data = {}

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Get configuration value with fallback to environment variable, config file, then placeholder

        Args:
            key: Configuration key (e.g., 'personal_info.name', 'branding.footer_text')
            default: Fallback value if nothing else found

        Returns:
            Configuration value or placeholder
        """
        # Try environment variable first (for CI/CD compatibility)
        env_key = f"APPLYR_{key.upper().replace('.', '_')}"
        env_value = os.getenv(env_key)
        if env_value:
            return env_value

        # Try config file
        if self._config_data:
            # Support nested keys like 'personal_info.name'
            parts = key.split(".")
            value = self._config_data
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    value = None
                    break

            if value and isinstance(value, str) and not value.startswith("{{"):
                return value

        # Return provided default or placeholder
        return default or f"{{{{YOUR_{key.upper().replace('.', '_')}}}}}"

    def get_personal_info(self) -> dict[str, str]:
        """Get all personal info as a dictionary"""
        return {
            "name": self.get("personal_info.name"),
            "email": self.get("personal_info.email"),
            "phone": self.get("personal_info.phone"),
            "website": self.get("personal_info.website"),
            "github": self.get("personal_info.github"),
            "linkedin": self.get("personal_info.linkedin"),
            "location": self.get("personal_info.location"),
        }

    def get_branding(self) -> dict[str, str]:
        """Get all branding info as a dictionary"""
        return {
            "svg_text": self.get("branding.svg_text"),
            "footer_text": self.get("branding.footer_text"),
        }


def get_config() -> PersonalConfig:
    """Get the global PersonalConfig instance"""
    return PersonalConfig()


def get_css_variables() -> str:
    """
    Generate CSS custom properties (variables) from config for injection into HTML

    Returns:
        CSS string with :root variables for branding and personal info
    """
    config = get_config()
    footer_text = config.get("branding.footer_text", config.get("personal_info.website", "{{YOUR_WEBSITE}}"))
    svg_text = config.get("branding.svg_text", "{{YOUR_BRAND_TEXT}}")

    return f"""
    :root {{
        --footer-text: "{footer_text}";
        --brand-svg-url: url("{svg_text}");
    }}
    """
