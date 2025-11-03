"""Tests for configuration module"""

import os
from pathlib import Path

from applyr.config import PersonalConfig, get_config, get_css_variables


class TestPersonalConfigSingleton:
    """Tests for PersonalConfig singleton pattern"""

    def test_singleton_pattern(self, temp_dir: Path):
        """Test that PersonalConfig is a singleton"""
        # Change to temp directory to avoid conflicts
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config1 = PersonalConfig()
            config2 = PersonalConfig()

            assert config1 is config2
        finally:
            os.chdir(original_cwd)


class TestLoadConfig:
    """Tests for _load_config method"""

    def test_load_config_from_file(self, temp_dir: Path):
        """Test loading config from config.yaml"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
personal_info:
  name: Test User
  email: test@example.com
  phone: 555-1234
  location: Test City, ST
""")

            config = PersonalConfig()
            value = config.get("personal_info.name")

            assert value == "Test User"
        finally:
            os.chdir(original_cwd)

    def test_load_config_from_template(self, temp_dir: Path):
        """Test loading config from template file"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            template_file = temp_dir / "config.template.yaml"
            template_file.write_text("""
personal_info:
  name: "{{YOUR_NAME}}"
  email: "{{YOUR_EMAIL}}"
""")

            config = PersonalConfig()
            # Template values should return placeholders
            value = config.get("personal_info.name")

            assert "{{" in value or value == "{{YOUR_NAME}}"
        finally:
            os.chdir(original_cwd)

    def test_load_config_no_files(self, temp_dir: Path):
        """Test loading config when no files exist"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config = PersonalConfig()
            value = config.get("personal_info.name", "Default Value")

            assert value == "Default Value"
        finally:
            os.chdir(original_cwd)


class TestGet:
    """Tests for get method"""

    def test_get_simple_key(self, temp_dir: Path):
        """Test getting simple configuration key"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
personal_info:
  name: Test User
""")

            config = PersonalConfig()
            value = config.get("personal_info.name")

            assert value == "Test User"
        finally:
            os.chdir(original_cwd)

    def test_get_nested_key(self, temp_dir: Path):
        """Test getting nested configuration key"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
branding:
  svg_text: "data:image/svg+xml;base64,..."
  footer_text: "example.com"
""")

            config = PersonalConfig()
            value = config.get("branding.footer_text")

            assert value == "example.com"
        finally:
            os.chdir(original_cwd)

    def test_get_with_default(self, temp_dir: Path):
        """Test getting key with default value"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config = PersonalConfig()
            value = config.get("nonexistent.key", "Default Value")

            assert value == "Default Value"
        finally:
            os.chdir(original_cwd)

    def test_get_with_placeholder(self, temp_dir: Path):
        """Test getting key returns placeholder when not found"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config = PersonalConfig()
            value = config.get("personal_info.name")

            assert "{{" in value or "YOUR" in value
        finally:
            os.chdir(original_cwd)

    def test_get_environment_variable_priority(self, temp_dir: Path, monkeypatch):
        """Test that environment variables take priority"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
personal_info:
  name: Config File Name
""")

            monkeypatch.setenv("APPLYR_PERSONAL_INFO_NAME", "Env Var Name")

            config = PersonalConfig()
            value = config.get("personal_info.name")

            assert value == "Env Var Name"
        finally:
            os.chdir(original_cwd)
            monkeypatch.delenv("APPLYR_PERSONAL_INFO_NAME", raising=False)


class TestGetPersonalInfo:
    """Tests for get_personal_info method"""

    def test_get_personal_info(self, temp_dir: Path):
        """Test getting all personal info"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
personal_info:
  name: Test User
  email: test@example.com
  phone: 555-1234
  website: example.com
  github: testuser
  linkedin: linkedin.com/in/testuser
  location: Test City, ST
""")

            config = PersonalConfig()
            personal_info = config.get_personal_info()

            assert personal_info["name"] == "Test User"
            assert personal_info["email"] == "test@example.com"
            assert personal_info["phone"] == "555-1234"
            assert personal_info["website"] == "example.com"
            assert personal_info["github"] == "testuser"
            assert personal_info["linkedin"] == "linkedin.com/in/testuser"
            assert personal_info["location"] == "Test City, ST"
        finally:
            os.chdir(original_cwd)


class TestGetBranding:
    """Tests for get_branding method"""

    def test_get_branding(self, temp_dir: Path):
        """Test getting all branding info"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
branding:
  svg_text: "data:image/svg+xml;base64,..."
  footer_text: "example.com"
""")

            config = PersonalConfig()
            branding = config.get_branding()

            assert branding["svg_text"] == "data:image/svg+xml;base64,..."
            assert branding["footer_text"] == "example.com"
        finally:
            os.chdir(original_cwd)


class TestGetConfigFunction:
    """Tests for get_config function"""

    def test_get_config_returns_instance(self):
        """Test that get_config returns PersonalConfig instance"""
        config = get_config()

        assert isinstance(config, PersonalConfig)


class TestGetCSSVariables:
    """Tests for get_css_variables function"""

    def test_get_css_variables(self, temp_dir: Path):
        """Test CSS variables generation"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
branding:
  svg_text: "data:image/svg+xml;base64,..."
  footer_text: "example.com"
""")

            css_vars = get_css_variables()

            assert ":root" in css_vars
            assert "--footer-text" in css_vars
            assert "--brand-svg-url" in css_vars
            assert "example.com" in css_vars
        finally:
            os.chdir(original_cwd)

    def test_get_css_variables_with_website_fallback(self, temp_dir: Path):
        """Test CSS variables use website as footer fallback"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            PersonalConfig._instance = None
            PersonalConfig._config_data = None

            config_file = temp_dir / "config.yaml"
            config_file.write_text("""
personal_info:
  website: "fallback.com"
""")

            css_vars = get_css_variables()

            assert "fallback.com" in css_vars
        finally:
            os.chdir(original_cwd)
