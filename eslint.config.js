import path from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const compat = new FlatCompat({
  baseDirectory: __dirname,
  resolvePluginsRelativeTo: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "plugin:@typescript-eslint/recommended", "plugin:react/recommended", "plugin:prettier/recommended"),

  {
    ignores: ["eslint.config.js", "eslint.config.mjs", "node_modules/", ".next/", "dist/", "prettier.config.js"],
    languageOptions: {
      parser: (await import("@typescript-eslint/parser")).default,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        ecmaVersion: 2021,
        sourceType: "module",
        tsconfigRootDir: __dirname,
        project: "./tsconfig.json",
      },
    },

    plugins: {
      "@typescript-eslint": (await import("@typescript-eslint/eslint-plugin")).default,
      react: (await import("eslint-plugin-react")).default,
      prettier: (await import("eslint-plugin-prettier")).default,
    },

    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "react/prop-types": "off",
      "react/jsx-uses-react": "off",
      "react/react-in-jsx-scope": "off",
      "prettier/prettier": "error",
      "@typescript-eslint/explicit-function-return-type": "warn",
      "linebreak-style": ["error", "windows"],
    },

    settings: {
      react: {
        version: "detect",
      },
    },
  },
];

export default eslintConfig;
