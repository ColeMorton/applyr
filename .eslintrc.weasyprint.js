module.exports = {
  env: {
    browser: false,
    node: false
  },
  extends: [],
  plugins: ["@html-eslint"],
  parser: "@html-eslint/parser",
  parserOptions: {
    sourceType: "module"
  },
  rules: {
    "@html-eslint/require-doctype": "off",
    "@html-eslint/require-lang": "off",
    "@html-eslint/require-meta-charset": "off",
    "@html-eslint/require-meta-viewport": "off",
    "@html-eslint/require-title": "off",
    "@html-eslint/no-duplicate-id": "error",
    "@html-eslint/no-duplicate-attrs": "error",
    "@html-eslint/require-img-alt": "warn",
    "@html-eslint/no-obsolete-tags": "error",
    "@html-eslint/no-inline-styles": "off",
    "@html-eslint/require-closing-tags": "error",
    "@html-eslint/no-script-style-type": "off",
    "@html-eslint/no-target-blank": "off",
    "@html-eslint/require-meta-description": "off",
    "@html-eslint/no-abstract-roles": "off",
    "@html-eslint/no-accesskey-attrs": "off",
    "@html-eslint/no-aria-hidden-body": "off",
    "@html-eslint/require-frame-title": "off",

    "@html-eslint/indent": ["error", 2],
    "@html-eslint/element-newline": ["warn", {
        skip: ["pre", "code", "span", "a", "strong", "em"],
        inline: ["$inline"]
    }],
    "@html-eslint/no-extra-spacing-attrs": "warn",
    "@html-eslint/no-extra-spacing-text": "off",
    "@html-eslint/no-multiple-empty-lines": ["error", {max: 2}],
    "@html-eslint/no-trailing-spaces": "error"
  },
  overrides: [
    {
      files: ["*.html"],
      rules: {
        "@html-eslint/no-inline-styles": "off",
        "@html-eslint/element-newline": "off"
      }
    }
  ],
  settings: {
    "html-eslint": {
      "weasyprint-optimized": true,
      "ignore-patterns": [
        "data:image/svg+xml",
        "background-image:",
        "page-break-",
        "brand-text",
        "font-face"
      ]
    }
  }
};
