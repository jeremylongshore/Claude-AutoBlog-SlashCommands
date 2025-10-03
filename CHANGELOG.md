# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2025-10-03
### Added
- **Enhanced Documentation Suite**:
  - `AUDIT_SUMMARY.md` - Repository health tracking and audit trails
  - `COMMANDS.md` - Complete command reference guide
  - `CONTENT-SYSTEMS-HANDOFF.md` - Workflow documentation for content systems
  - `command-analytics.html` - Interactive usage tracking dashboard
  - `command-bible-complete.md` - Comprehensive command usage guide
  - `command-quick-ref.md` - Quick reference for all commands
  - `google-leaders-x-list.md` - Curated X thread content resources
  - `scripts/parse_x_thread_fixed.py` - Enhanced tweet parsing utility

### Improved
- **X-Gen-System Integration Across All Commands**:
  - All 11 slash commands now use X-Gen-System (previously only 5)
  - `/blog-gatsby-technical.md` - X-Gen integration added
  - `/blog-jekyll-technical.md` - X-Gen integration added
  - `/blog-nextjs-technical.md` - X-Gen integration added
  - `/blog-wordpress-technical.md` - X-Gen integration added
  - `/blog-jeremylongshore.md` - X-Gen integration added
  - `/blog-startaitools.md` - X-Gen integration added

- **Enhanced Tweet Parsing** (`scripts/post_x_thread.py`):
  - Regex-based extraction for "TWEET X/Y:" format
  - Improved content validation and error handling
  - Better support for MCP-compliant JSON payloads
  - More robust multi-tweet thread processing

- **Session Analysis Optimization**:
  - Git history fallback refined: 14 days → 24 hours for daily usage
  - Better commit analysis for recent work sessions
  - More accurate content context extraction

### Fixed
- Command execution issues with X-Gen-System parameter passing
- Tweet formatting inconsistencies in automated posting
- Character count validation in thread generation

### Documentation
- Updated all command files with consistent X-Gen-System integration patterns
- Enhanced CLAUDE.md with latest architecture details
- Improved README with comprehensive setup instructions

## [2.0.1] - 2025-09-28
### Security
- **CRITICAL**: Removed exposed API keys from documentation and command files
- Replaced all real API credentials with placeholder values
- Enhanced security documentation with proper credential handling

### Changed
- Updated all command fallback periods from 14 days to 24 hours for daily usage
- Improved session analysis focus for frequent content creation

## [2.0.0] - 2025-09-28
### Added
- **X-Gen-System Integration**: Complete overhaul of X content generation
  - Advanced character budgeting with 280-char limit, URL=23, emoji buffer calculations
  - Proven hook patterns: counter-intuitive, mini-case, list-promise, myth-bust templates
  - MCP (Master Control Protocol) integration for direct API consumption
  - 100% schema compliance validation for automated posting
  - Accessibility standards: CamelCase hashtags, alt text requirements, ASCII-only
  - A/B variant generation for engagement optimization testing
  - Graceful error handling with auto-split algorithm and content recovery
- **Updated Primary Commands**: content-nuke.md, blog-single-startai.md, blog-jeremy-x.md, blog-both-x.md, post-x.md
- **MCP-Compliant JSON Output**: All X content now generates exact schema for MCP consumption
- **Enhanced Documentation**: X-Gen-System integration details in README and CLAUDE.md

### Changed
- **File Paths Updated**: X threads now save to `/home/jeremy/projects/content-nuke/x-threads/`
- **Deployment Process**: Automated MCP posting via `python3 scripts/post_x_thread.py [filename]`
- **Content Quality**: All X content now follows proven engagement patterns and accessibility standards

### Deprecated
- **Legacy Size Templates**: Replaced with intelligent X-Gen-System processing
- **Manual Character Counting**: Now handled automatically with buffer calculations

## [1.0.1] - 2025-09-28
### Changed
- Updated end-of-day status documentation and reporting

## [1.0.0] - 2025-09-28
### Added
- Initial release with comprehensive content automation platform
- 14 specialized slash command definitions for Claude Code
- Multi-platform content blast commands (`/content-nuke`)
- Single-platform commands for StartAITools and JeremyLongshore blogs
- X (Twitter) API OAuth 1.0a and OAuth 2.0 authentication handlers
- LinkedIn content generation and posting automation
- Token refresh automation with Waygate MCP integration
- Documentation system with platform setup guides
- Session analysis engine with git history + conversation context
- Content adaptation engine for technical vs personal angles
- Intelligent link selection for cross-platform optimization
- Multi-platform deployment coordination
- SQLite database for command execution tracking
- Cross-platform analytics and performance monitoring