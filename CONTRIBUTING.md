# Contributing to Claude AutoBlog Slash Commands

Thank you for considering contributing! This project helps developers automate blog publishing across multiple platforms, and community contributions make it better for everyone.

## Ways to Contribute

### 1. Report Issues
Found a bug or problem?
- [Open an issue](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues/new)
- Include your platform (Hugo, Jekyll, Gatsby, Next.js, WordPress)
- Describe what you expected vs. what happened
- Include error messages if applicable

### 2. Request Features
Have an idea for improvement?
- [Open a feature request](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues/new)
- Describe the use case
- Explain how it would help others
- Provide examples if possible

### 3. Add Platform Support
Want to add support for another blogging platform?
- Fork the repository
- Create a new command file: `commands/blog-[platform]-technical.md`
- Follow the existing command structure
- Include customization instructions
- Update README with new platform
- Submit a pull request

### 4. Share Customizations
Have a useful variation of an existing command?
- Share your customized command
- Explain what makes it different
- Provide context on your use case
- Submit via pull request or issue

### 5. Improve Documentation
Found something unclear?
- Fix typos or clarify instructions
- Add examples or screenshots
- Improve setup guides
- Update platform-specific docs

### 6. Share Examples
Generated great posts with these commands?
- Share links to published posts
- Explain your workflow
- Showcase different use cases
- Help others see real-world results

## Pull Request Process

### Before Submitting
1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
4. **Make your changes** following the guidelines below
5. **Test your changes** with Claude Code CLI
6. **Commit with clear messages** describing what you changed and why

### Submitting
1. **Push to your fork:** `git push origin feature/your-feature-name`
2. **Open a pull request** from your fork to the main repository
3. **Describe your changes:**
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Any breaking changes?

### After Submitting
- Respond to feedback from maintainers
- Make requested changes if needed
- Be patient - reviews may take a few days

## Command File Guidelines

When adding or modifying command files:

### Structure
```markdown
Brief description of what this command does.

## Your Task

1. **Analyze ENTIRE Working Session**
   [Analysis instructions]

2. **Find Cross-Links**
   [Cross-linking instructions]

3. **Write the Blog Post**
   [Generation instructions]

4. **Show Draft for Review**
   [Review process]

5. **Publish (After Approval)**
   [Publishing steps]

## Key Principles
[Guiding principles]

## Critical Reminders
[Important notes]

## Customization Required
[What users need to change]

## Example Invocation
[How to use the command]
```

### Content Requirements
- **Clear instructions** for Claude on what to do
- **Platform-specific details** (file paths, build commands, front matter format)
- **Customization section** explaining what users need to change
- **Example invocation** showing how to use the command
- **Inline comments** explaining important decisions

### Best Practices
- Use absolute paths in examples (users replace with their paths)
- Include both successful and error scenarios
- Explain WHY things work a certain way
- Test with Claude Code before submitting
- Follow existing command structure for consistency

## Documentation Guidelines

### README Updates
- Add new platforms to the platform support table
- Update command count badges
- Add links to new command files
- Keep examples consistent
- Maintain existing formatting

### Setup Guides
- Include prerequisites (tools, versions)
- Provide step-by-step instructions
- Show example configurations
- Include troubleshooting tips
- Test on fresh installations

### Code Examples
- Use real, working examples
- Include explanatory comments
- Show both successful and error cases
- Format code consistently
- Test all commands before documenting

## Testing Your Contribution

Before submitting:

1. **Test the command with Claude Code:**
   ```bash
   cp your-command.md ~/.claude/commands/
   cd test-project/
   /your-command-name
   ```

2. **Verify the generated post:**
   - Check front matter format
   - Verify build succeeds
   - Confirm git commit/push works
   - Test deployment if applicable

3. **Test on multiple scenarios:**
   - New project (no prior posts)
   - Project with existing posts
   - Project with recent commits
   - Project with long conversation history

4. **Document any issues encountered** and how you resolved them

## Style Guidelines

### Markdown
- Use headings hierarchy (h1 → h2 → h3)
- Include code blocks with language tags
- Use bold for **emphasis** on key points
- Use lists for step-by-step instructions
- Keep line length reasonable (80-100 chars)

### Writing Style
- Write for developers (technical but clear)
- Be concise and direct
- Use active voice ("Run the command" not "The command should be run")
- Include "why" explanations, not just "what"
- Avoid jargon without explanation

### Code Style
- Use 2 spaces for indentation in YAML
- Use 4 spaces for indentation in code blocks
- Follow platform conventions (Hugo YAML, Jekyll conventions, etc.)
- Comment non-obvious decisions
- Keep examples realistic

## Questions?

Not sure about something? Have questions before contributing?

- **Open a discussion** on GitHub Discussions (if enabled)
- **Open an issue** with the "question" label
- **Check existing issues** - your question may already be answered
- **Review command files** - see how existing platforms are implemented

## Code of Conduct

### Be Respectful
- Treat all contributors with respect
- Be constructive in feedback
- Focus on the code, not the person
- Help newcomers feel welcome

### Be Collaborative
- Share knowledge generously
- Acknowledge others' contributions
- Work together to solve problems
- Celebrate successes

### Be Patient
- Maintainers are volunteers with limited time
- Reviews may take a few days
- Not all PRs will be accepted
- Rejection isn't personal - keep contributing!

## Recognition

Contributors will be recognized in:
- GitHub contributors list (automatic)
- Release notes for significant contributions
- README credits section (for major features)

## License

By contributing, you agree that your contributions will be licensed under the MIT License, the same as the rest of the project.

---

**Thank you for contributing!** Every contribution, no matter how small, makes this project better for everyone.

Questions? [Open an issue](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues/new) or reach out to [@jeremylongshore](https://github.com/jeremylongshore).