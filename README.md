# Claude AutoBlog Slash Commands

Automated blog publishing workflow for Claude Code. Analyze your development work, generate contextual blog posts, and deploy to production Hugo sites - all with a single slash command.

## What This Does

Transform your development sessions into published blog posts automatically:

1. **Run a command** - `/blog-startaitools` or `/blog-jeremylongshore`
2. **Claude analyzes** - Git history + conversation context + project files
3. **Generates draft** - Complete blog post with cross-links and SEO
4. **You review** - Approve or edit the draft
5. **Auto-publishes** - Creates file, builds site, commits, pushes, deploys

**Zero friction. Complete automation. Professional results.**

## Commands Included

### `/blog-startaitools`
**Technical blog posts for developer audiences**
- Deep technical content with implementation details
- Captures complete problem-solving journey
- Includes troubleshooting and iterations
- Cross-links to related posts automatically
- Hugo static site deployment

View the command file: [`commands/blog-startaitools.md`](commands/blog-startaitools.md)

### `/blog-jeremylongshore`
**Portfolio blog posts for professional audiences**
- Career-focused narrative
- Demonstrates problem-solving capabilities
- Professional tone for employers/clients
- Highlights skills and growth
- Hugo static site deployment

View the command file: [`commands/blog-jeremylongshore.md`](commands/blog-jeremylongshore.md)

## Quick Start

### 1. Install Commands

```bash
# Clone this repository
cd ~/projects
git clone https://github.com/jeremylongshore/claude-AutoBlog-SlashCommands.git

# Copy commands to your Claude commands directory
cp claude-AutoBlog-SlashCommands/commands/*.md ~/.claude/commands/
```

### 2. Customize for Your Blog

Edit the command files in `commands/` to point to your blog:
- Update blog post directory paths (search for `/home/jeremy/`)
- Adjust Hugo build commands
- Modify front matter format (YAML/TOML)
- Customize tone and structure

See the command files for inline comments on what to change.

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

- Claude Code CLI (v1.0.123+)
- Hugo static site generator
- Git repository with remote
- Netlify or similar auto-deploy setup

## Command Files

- [`commands/blog-startaitools.md`](commands/blog-startaitools.md) - Technical blog command with inline documentation
- [`commands/blog-jeremylongshore.md`](commands/blog-jeremylongshore.md) - Portfolio blog command with inline documentation

Both command files include detailed instructions on what they do and how to customize them.

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
1. Creates `.md` file in blog `content/posts/`
2. Runs `hugo --gc --minify --cleanDestinationDir`
3. Verifies build succeeds (stops if errors)
4. Commits: `feat: add blog post - [title]`
5. Pushes to origin (triggers deployment)
6. Confirms deployment initiated

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

1. **Share your customizations** - PR your adapted commands
2. **Report issues** - Let us know what doesn't work
3. **Suggest features** - Ideas for improvements
4. **Add examples** - Show what you've generated

## License

MIT License - see [LICENSE](LICENSE) file

## Author

**Jeremy Longshore** / Intent Solutions Inc

- Technical Blog: [startaitools.com](https://startaitools.com)
- Portfolio: [jeremylongshore.com](https://jeremylongshore.com)
- GitHub: [@jeremylongshore](https://github.com/jeremylongshore)

## Related Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Hugo Documentation](https://gohugo.io/documentation/)
- [Blog Post: Building These Commands](https://startaitools.com/posts/building-custom-claude-code-slash-commands-complete-journey/) - Complete implementation guide

---

**Status:** Production-ready, actively maintained
**Last Updated:** September 27, 2025

*These commands are used daily to maintain two active blog sites with 50+ technical posts combined.*