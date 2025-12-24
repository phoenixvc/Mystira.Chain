# Contracts Package Migration Guide

**Last Updated:** 2025-12-24
**Status:** Phase 1 Complete - Migration Period Active

This guide covers migrating from the legacy contracts packages to the unified `@mystira/contracts` and `Mystira.Contracts` packages.

## Overview

We are consolidating scattered API contracts into unified packages:

| Old Package | New Package | Status |
|-------------|-------------|--------|
| `@mystira/app-contracts` | `@mystira/contracts/app` | Deprecated |
| `@mystira/story-generator-contracts` | `@mystira/contracts/story-generator` | Deprecated |
| `Mystira.App.Contracts` | `Mystira.Contracts.App` | Deprecated |
| `Mystira.StoryGenerator.Contracts` | `Mystira.Contracts.StoryGenerator` | Deprecated |

See [ADR-0020: Package Consolidation Strategy](../adr/0020-package-consolidation-strategy.md) for rationale.

## Benefits of Migration

- **Single Source of Truth:** All API types in one package per ecosystem
- **Simplified Dependencies:** Add one package instead of multiple
- **Consistent Versioning:** All contracts share the same version
- **Better Discoverability:** All types in one searchable package
- **Tree-Shaking Support:** Only import what you need via subpath exports

## Migration Steps

### TypeScript/NPM

#### Step 1: Install the New Package

```bash
# With npm
npm install @mystira/contracts

# With pnpm
pnpm add @mystira/contracts

# With yarn
yarn add @mystira/contracts
```

#### Step 2: Update Imports

**Before:**

```typescript
import { StoryRequest, StoryResponse } from '@mystira/app-contracts';
import { GeneratorConfig, GeneratorResult } from '@mystira/story-generator-contracts';
```

**After (Option 1 - Subpath imports):**

```typescript
import { StoryRequest, StoryResponse } from '@mystira/contracts/app';
import { GeneratorConfig, GeneratorResult } from '@mystira/contracts/story-generator';
```

**After (Option 2 - Namespace imports):**

```typescript
import { App, StoryGenerator } from '@mystira/contracts';

// Use as:
const request: App.StoryRequest = { ... };
const config: StoryGenerator.GeneratorConfig = { ... };
```

#### Step 3: Remove Old Packages

```bash
# With npm
npm uninstall @mystira/app-contracts @mystira/story-generator-contracts

# With pnpm
pnpm remove @mystira/app-contracts @mystira/story-generator-contracts

# With yarn
yarn remove @mystira/app-contracts @mystira/story-generator-contracts
```

### C#/.NET/NuGet

#### Step 1: Install the New Package

```bash
# Via CLI
dotnet add package Mystira.Contracts
```

Or in your `.csproj`:

```xml
<PackageReference Include="Mystira.Contracts" Version="0.1.0" />
```

#### Step 2: Update Using Statements

**Before:**

```csharp
using Mystira.App.Contracts;
using Mystira.StoryGenerator.Contracts;
```

**After:**

```csharp
using Mystira.Contracts.App;
using Mystira.Contracts.StoryGenerator;
```

#### Step 3: Remove Old Packages

```bash
dotnet remove package Mystira.App.Contracts
dotnet remove package Mystira.StoryGenerator.Contracts
```

## Automated Migration

> **Note:** Automated migration tooling is planned but not yet available. Please use the manual migration steps above for now.
>
> Track progress: [GitHub Issue #TBD](https://github.com/phoenixvc/Mystira.workspace/issues)

When available, the tooling will:

- **TypeScript:** `npx @mystira/contracts-codemod` - Replace imports automatically
- **C#:** Roslyn analyzer to update using statements

## Type Mapping Reference

### App Contracts

| Old Type | New Type |
|----------|----------|
| `StoryRequest` | `App.StoryRequest` or import from `/app` |
| `StoryResponse` | `App.StoryResponse` or import from `/app` |
| `ApiRequest` | `App.ApiRequest` or import from `/app` |
| `ApiResponse<T>` | `App.ApiResponse<T>` or import from `/app` |
| `ApiError` | `App.ApiError` or import from `/app` |

### Story Generator Contracts

| Old Type | New Type |
|----------|----------|
| `GeneratorConfig` | `StoryGenerator.GeneratorConfig` or import from `/story-generator` |
| `GeneratorRequest` | `StoryGenerator.GeneratorRequest` or import from `/story-generator` |
| `GeneratorResult` | `StoryGenerator.GeneratorResult` or import from `/story-generator` |
| `GeneratorContext` | `StoryGenerator.GeneratorContext` or import from `/story-generator` |
| `GeneratorMetadata` | `StoryGenerator.GeneratorMetadata` or import from `/story-generator` |

## Deprecation Timeline

| Phase | Date | Action |
|-------|------|--------|
| Phase 1 | 2025-12-24 | New packages published, migration period begins |
| Phase 2 | +2 versions | Deprecation warnings added to old packages |
| Phase 3 | +4 versions | Old packages archived, no new versions |

### Deprecation Warnings

Starting in the next version, the old packages will emit console warnings:

```
DEPRECATED: @mystira/app-contracts is deprecated.
Please migrate to @mystira/contracts/app.
See: https://github.com/phoenixvc/Mystira.workspace/blob/main/docs/guides/contracts-migration.md
```

## FAQ

### Can I use both packages during migration?

Yes, both packages can coexist. The types are compatible, so you can migrate incrementally.

### Will the old packages receive updates?

Yes, during the migration period. After Phase 3, only critical security fixes will be backported.

### Are there breaking changes in the new package?

The types are identical. The only changes are:

- Import paths
- Namespace organization
- Package name

### How do I report issues with migration?

Open an issue at: https://github.com/phoenixvc/Mystira.workspace/issues

Use the label: `contracts-migration`

## Related Documentation

- [Package Releases Guide](./package-releases.md)
- [ADR-0020: Package Consolidation Strategy](../adr/0020-package-consolidation-strategy.md)
- [Package Inventory](./package-inventory.md)
- [Publishing Flow](./publishing-flow.md)
