# SyntaxScope

A command syntax search engine for multiple shells.

## Overview

SyntaxScope is a web application that allows users to search for command syntax across multiple shells including Bash, Zsh, PowerShell, and Python. It provides a clean, modern interface for discovering and learning command syntax.

## Features

- Search for commands across multiple shells
- Filter by shell type
- Copy commands to clipboard
- Tag-based organization
- Responsive design

## Getting Started

### Prerequisites

- Node.js 18+ (recommended)
- npm or pnpm

#### Linux-specific Setup

If you're on Linux and encounter issues with pnpm not being found:

```bash
# Install pnpm globally
npm install -g pnpm

# Or use npm instead by installing cross-env
npm install --save-dev cross-env
```

**Important Note**: This project uses Next.js with SWC compiler for faster builds and support for features like `next/font`. Do not add a custom `.babelrc` file as it will conflict with SWC and break font loading.

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/syntax-scope.git
cd syntax-scope
```

2. Install dependencies
```bash
# Using npm
npm install

# Using pnpm
pnpm install
```

3. Start the development server
```bash
# Using npm
npm run dev

# Using pnpm
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Building for Production

```bash
# Normal build (with TypeScript checking)
npm run build

# Build with TypeScript checking disabled
npm run build:skip-ts
```

## TypeScript Notes

The project has been configured to work properly with TypeScript. Here are some notes:

1. TypeScript checking is enabled by default. If you need to disable it temporarily, you can use the `.env.local` file:
```
SKIP_TYPE_CHECK=true
```

2. Run the type checker separately to identify issues:
```bash
npm run type-check
```

3. The project uses `@ts-ignore` comments for some third-party libraries that don't have proper TypeScript definitions (like lucide-react and fuse.js). This is a temporary solution until proper type definitions are available.

## Dependencies

- Next.js 15
- React 19
- date-fns (v2.30.0 for compatibility with react-day-picker)
- Tailwind CSS
- shadcn/ui components
- Lucide React icons

## License

This project is licensed under the MIT License - see the LICENSE file for details.
