import coreWebVitals from "eslint-config-next/core-web-vitals";
import typescript from "eslint-config-next/typescript";
import prettier from "eslint-config-prettier";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const eslintConfig = [
  ...coreWebVitals,
  ...typescript,
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    ignores: [
      "eslint.config.js",
      "eslint.config.mjs",
      "node_modules/",
      ".next/",
      "dist/",
      "build/",
      "prettier.config.js",
      "postcss.config.cjs",
      "next.config.js",
      "tailwind.config.js",
      "*.config.js",
      "*.config.mjs",
      "src/components/ui/",
    ],
    languageOptions: {
      parser: (await import("@typescript-eslint/parser")).default,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        ecmaVersion: "latest",
        sourceType: "module",
        tsconfigRootDir: __dirname,
        project: "./tsconfig.json",
      },
    },
    rules: {
      // TypeScript 관련
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          destructuredArrayIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/explicit-function-return-type": "warn",
      "@typescript-eslint/no-explicit-any": "warn",

      // React 관련
      "react/prop-types": "off",
      "react/jsx-uses-react": "off",
      "react/react-in-jsx-scope": "off",
      "react/self-closing-comp": "warn",
      "react/jsx-boolean-value": ["warn", "never"],

      // React Hooks 관련
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      "linebreak-style": "off",

      // 일반적인 규칙
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "prefer-const": "error",
      "no-var": "error",

      // Next.js 관련
      "@next/next/no-html-link-for-pages": "error",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
  prettier,
];

export default eslintConfig;
