# Claude AutoBlog Slash Commands

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Claude Code](https://img.shields.io/badge/Claude_Code-v1.0.123+-blue.svg)](https://docs.claude.com/en/docs/claude-code)
[![Platform Support](https://img.shields.io/badge/Platforms-5-orange.svg)](#platform-support)
[![Active](https://img.shields.io/badge/Status-Production_Ready-success.svg)](#status)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-green.svg)](#contributing)

Automated blog publishing workflow for Claude Code. Analyze your development work, generate contextual blog posts, and deploy to production - all with a single slash command.

**Supports:** Hugo • Jekyll • Gatsby • Next.js • WordPress

## What This Does

Transform your development sessions into published blog posts automatically:

1. **Run a command** - `/blog-startaitools` or `/blog-jeremylongshore`
2. **Claude analyzes** - Git history + conversation context + project files
3. **Generates draft** - Complete blog post with cross-links and SEO
4. **You review** - Approve or edit the draft
5. **Auto-publishes** - Creates file, builds site, commits, pushes, deploys

**Zero friction. Complete automation. Professional results.**

## Platform Support

Choose the command that matches your blog platform:

| Platform | Command Template | Features |
|----------|-----------------|----------|
| **Hugo** | `blog-hugo-technical.md` | Static site, YAML/TOML front matter, fast builds |
| **Jekyll** | `blog-jekyll-technical.md` | GitHub Pages compatible, Ruby-based, simple setup |
| **Gatsby** | `blog-gatsby-technical.md` | React-based, GraphQL queries, modern stack |
| **Next.js** | `blog-nextjs-technical.md` | App/Pages Router, MDX support, Vercel deployment |
| **WordPress** | `blog-wordpress-technical.md` | WP-CLI or REST API, largest CMS, plugin ecosystem |

### Example Commands (Hugo - Original)

**`/blog-startaitools`** - Technical blog for developer audiences
View file: [`commands/blog-startaitools.md`](commands/blog-startaitools.md)

**`/blog-jeremylongshore`** - Portfolio blog for professional audiences
View file: [`commands/blog-jeremylongshore.md`](commands/blog-jeremylongshore.md)

### Platform-Specific Commands

**Jekyll:** [`commands/blog-jekyll-technical.md`](commands/blog-jekyll-technical.md)
**Gatsby:** [`commands/blog-gatsby-technical.md`](commands/blog-gatsby-technical.md)
**Next.js:** [`commands/blog-nextjs-technical.md`](commands/blog-nextjs-technical.md)
**WordPress:** [`commands/blog-wordpress-technical.md`](commands/blog-wordpress-technical.md)

## Quick Start

### One-Command Install (Copy & Paste)

**Got Claude Code? Install in 30 seconds:**

```bash
cd /tmp && git clone https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands.git && cp Claude-AutoBlog-SlashCommands/commands/*.md ~/.claude/commands/ && echo "✅ Installed! Choose a command to customize:" && ls -1 ~/.claude/commands/blog-*.md
```

This installs all platform commands. Pick one that matches your blog platform and customize it.

### Manual Install

```bash
# Clone this repository
cd ~/projects
git clone https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands.git

# Copy ALL platform commands (choose what you need)
cp Claude-AutoBlog-SlashCommands/commands/*.md ~/.claude/commands/

# OR copy only your platform's command
cp Claude-AutoBlog-SlashCommands/commands/blog-hugo-technical.md ~/.claude/commands/blog-myblog.md
# (Rename to match your use case: blog-myblog, blog-technical, blog-portfolio, etc.)
```

### 2. Customize for Your Blog

Each command file includes a **"Customization Required"** section. Edit your copied command:

**Universal Changes:**
- Update blog content directory paths
- Adjust build commands for your setup
- Modify front matter format
- Customize tone and structure

**Platform-Specific:**
- **Hugo:** Content path, theme config, build flags
- **Jekyll:** `_posts/` location, bundle exec, categories
- **Gatsby:** Content directory, GraphQL schema, slug format
- **Next.js:** App/Pages Router, MDX config, routing style
- **WordPress:** WP-CLI or REST API, authentication, taxonomy IDs

Each command file has inline documentation for required customizations.

### 3. Use In Any Project

```bash
cd ~/projects/my-awesome-project
# ... do your development work ...
/blog-startaitools
# Review draft, approve, and it auto-publishes!
```

## Key Features

✅ **Context-Aware Analysis**
- Git commits since last blog post
- Complete conversation history from working session
- Project files, TODOs, and documentation
- Captures the journey, not just the destination

✅ **Smart Content Generation**
- Technical depth appropriate for audience
- Shows troubleshooting and iterative refinements
- Includes code examples and architecture decisions
- Cross-links to 2-3 related existing posts

✅ **Full Pipeline Automation**
- Creates markdown file in blog directory
- Runs Hugo build to verify no errors
- Git commits with proper message format
- Pushes to trigger Netlify/GitHub deployment

✅ **Quality Control**
- Shows complete draft for review
- You approve before publishing
- Edit capability for refinements
- Maintains professional standards

## Real-World Examples

These commands document themselves:

**Technical Post (startaitools):**
[Building Custom Claude Code Slash Commands](https://startaitools.com/posts/building-custom-claude-code-slash-commands-complete-journey/)
- 330 lines of technical content
- Complete implementation journey
- Troubleshooting steps included
- Educational for developers

**Portfolio Post (jeremylongshore):**
[Automating Developer Workflows](https://jeremylongshore.com/posts/automating-developer-workflows-custom-ai-commands/)
- 136 lines of professional narrative
- Problem-solving capabilities showcased
- Career-focused presentation
- Resume-building content

## Requirements

**Universal:**
- Claude Code CLI (v1.0.123+)
- Git repository with remote
- Your blog's deployment pipeline configured

**Platform-Specific:**
- **Hugo:** Hugo v0.100+ installed
- **Jekyll:** Ruby, Bundler, Jekyll gem
- **Gatsby:** Node.js, npm/yarn, Gatsby CLI
- **Next.js:** Node.js, npm/yarn/pnpm
- **WordPress:** WP-CLI or REST API access with authentication

## Command Files

### Hugo Commands (Original)
- [`commands/blog-startaitools.md`](commands/blog-startaitools.md) - Technical blog for startaitools.com
- [`commands/blog-jeremylongshore.md`](commands/blog-jeremylongshore.md) - Portfolio blog for jeremylongshore.com

### Platform Templates
- [`commands/blog-jekyll-technical.md`](commands/blog-jekyll-technical.md) - Jekyll static site generator
- [`commands/blog-gatsby-technical.md`](commands/blog-gatsby-technical.md) - Gatsby React-based framework
- [`commands/blog-nextjs-technical.md`](commands/blog-nextjs-technical.md) - Next.js with App/Pages Router
- [`commands/blog-wordpress-technical.md`](commands/blog-wordpress-technical.md) - WordPress CMS via CLI/API

All command files include detailed customization instructions.

## How It Works

### The Analysis Phase

Commands review multiple context sources:

```
Current Working Session
├── Git History (commits since last post)
├── Conversation Context (problems, solutions, iterations)
├── Project Files (code, docs, TODOs)
└── Existing Posts (for cross-linking)
```

### The Generation Phase

Creates blog post with:
- **Title**: Clear, specific to what was built
- **Journey**: What you tried, what failed, how you solved it
- **Technical Details**: Implementation, architecture, decisions
- **Lessons Learned**: Insights from the process
- **Cross-Links**: 2-3 related existing posts
- **SEO**: Proper tags, descriptions, formatting

### The Publishing Phase

After your approval:
1. Creates content file in platform-specific location
2. Runs build command to verify (Hugo, Jekyll, Gatsby, Next.js) or publishes directly (WordPress)
3. Verifies build succeeds (stops if errors)
4. Git commit: `feat: add blog post - [title]`
5. Git push to trigger deployment (or WordPress REST API publish)
6. Confirms deployment initiated

**Platform-Specific Publishing:**
- **Hugo:** `hugo --gc --minify --cleanDestinationDir`
- **Jekyll:** `bundle exec jekyll build`
- **Gatsby:** `gatsby build` or `npm run build`
- **Next.js:** `npm run build` then deploy to Vercel/Netlify
- **WordPress:** WP-CLI `wp post create` or REST API `POST /wp/v2/posts`

## Why This Matters

**Before:**
- Finish project → forget what you did → reconstruct context → write post → manual deployment
- Documentation becomes a chore you avoid
- Valuable insights never get shared

**After:**
- Finish project → run command → review draft → approve → live in 2 minutes
- Documentation is natural byproduct of work
- Consistent, high-quality content

## Philosophy

### Show the Journey

These commands don't just document final solutions - they capture:
- Problems you faced
- Solutions you tried that didn't work
- Troubleshooting steps
- Iterative refinements
- What you learned

**Readers learn more from seeing the process than just the result.**

### Different Audiences, Different Narratives

Same work can be presented differently:
- **Technical blog**: Deep implementation details for developers
- **Portfolio blog**: Problem-solving capabilities for employers

Same analysis, different presentation.

### Automation + Judgment

Automation handles mechanics:
- Context gathering
- Content generation
- Build and deployment

Human judgment maintains quality:
- Review draft before publishing
- Edit if needed
- Approve only when ready

## Contributing

Found these commands useful? Ways to contribute:

1. **Share your customizations** - PR your adapted commands for different platforms
2. **Report issues** - [Open an issue](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues/new) for bugs or problems
3. **Suggest features** - [Request features](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues/new) for improvements
4. **Add examples** - Show generated posts and use cases
5. **Improve documentation** - Help make setup guides clearer
6. **Star the repo** - Help others discover these commands

**PRs Welcome!** All contributions are appreciated. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file

## Author

**Jeremy Longshore** / Intent Solutions Inc

- Technical Blog: [startaitools.com](https://startaitools.com)
- Portfolio: [jeremylongshore.com](https://jeremylongshore.com)
- GitHub: [@jeremylongshore](https://github.com/jeremylongshore)

## Related Resources

**Claude Code:**
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Blog Post: Building These Commands](https://startaitools.com/posts/building-custom-claude-code-slash-commands-complete-journey/)

**Platform Documentation:**
- [Hugo](https://gohugo.io/documentation/) - Fast static site generator
- [Jekyll](https://jekyllrb.com/docs/) - GitHub Pages default
- [Gatsby](https://www.gatsbyjs.com/docs/) - React-based framework
- [Next.js](https://nextjs.org/docs) - React production framework
- [WordPress](https://developer.wordpress.org/) - REST API and WP-CLI

---

**Status:** Production-ready, actively maintained
**Last Updated:** September 27, 2025

*These commands are used daily to maintain two active blog sites with 50+ technical posts combined.*