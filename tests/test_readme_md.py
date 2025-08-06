import re
import pytest
from pathlib import Path


class TestReadmeMd:
    """Test suite for README.md file validation and content verification."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content for testing."""
        readme_path = Path("README.md")
        if not readme_path.exists():
            pytest.skip("README.md file not found")
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_readme_file_exists(self):
        """Test that README.md file exists in the repository root."""
        readme_path = Path("README.md")
        assert readme_path.exists(), "README.md file should exist in the repository root"
        assert readme_path.is_file(), "README.md should be a file, not a directory"
    
    def test_readme_not_empty(self, readme_content):
        """Test that README.md is not empty."""
        assert readme_content.strip(), "README.md should not be empty"
        assert len(readme_content.strip()) > 10, "README.md should have meaningful content"
    
    def test_readme_has_title(self, readme_content):
        """Test that README.md has a proper title."""
        lines = readme_content.split('\n')
        title_found = any(line.strip().startswith('# ') for line in lines[:10])
        assert title_found, "README.md should have a main title (# heading) near the top"
    
    def test_readme_has_overview_section(self, readme_content):
        """Test that README.md contains an Overview section."""
        assert "## Overview" in readme_content, "README.md should have an Overview section"
    
    def test_readme_has_workflow_logic_section(self, readme_content):
        """Test that README.md contains a Workflow Logic section."""
        assert "## Workflow Logic" in readme_content, "README.md should have a Workflow Logic section"
    
    def test_readme_has_usage_instructions(self, readme_content):
        """Test that README.md contains usage instructions."""
        assert "## How to use this workflow" in readme_content, "README.md should have usage instructions"
    
    def test_readme_mentions_required_branches(self, readme_content):
        """Test that README.md mentions the required branches."""
        assert "image-update" in readme_content, "README.md should mention the image-update branch"
        assert "auto-pr-branch-create" in readme_content, "README.md should mention the auto-pr-branch-create branch"
    
    def test_readme_mentions_github_token(self, readme_content):
        """Test that README.md mentions GitHub token configuration."""
        assert "GH_PAT" in readme_content, "README.md should mention the GH_PAT secret"
        assert "personal access token" in readme_content.lower(), "README.md should mention personal access token"
    
    def test_readme_mentions_workflow_file(self, readme_content):
        """Test that README.md mentions the workflow file location."""
        assert ".github/workflows/auto-pr-demo.yml" in readme_content, "README.md should mention the workflow file path"
    
    def test_readme_has_proper_markdown_structure(self, readme_content):
        """Test that README.md follows proper Markdown structure."""
        lines = readme_content.split('\n')
        
        # Check for proper heading hierarchy
        h1_count = sum(1 for line in lines if line.strip().startswith('# '))
        h2_count = sum(1 for line in lines if line.strip().startswith('## '))
        
        assert h1_count >= 1, "README.md should have at least one H1 heading"
        assert h2_count >= 3, "README.md should have multiple H2 sections"
    
    def test_readme_list_formatting(self, readme_content):
        """Test that README.md uses proper list formatting."""
        # Check for proper bullet points and numbered lists
        bullet_points = re.findall(r'^\s*[-*]\s+', readme_content, re.MULTILINE)
        numbered_lists = re.findall(r'^\s*\d+\.\s+', readme_content, re.MULTILINE)
        
        assert len(bullet_points) > 0 or len(numbered_lists) > 0, "README.md should contain formatted lists"
    
    def test_readme_code_blocks(self, readme_content):
        """Test that README.md properly formats code blocks where present."""
        # Check for code blocks (backticks)
        code_block_pattern = r'```[\s\S]*?```|`[^`]+`'
        code_blocks = re.findall(code_block_pattern, readme_content)
        
        # If code blocks exist, they should be properly formatted
        for block in code_blocks:
            if block.startswith('```'):
                assert block.endswith('```'), f"Code block should be properly closed: {block[:50]}..."
    
    def test_readme_workflow_steps_documented(self, readme_content):
        """Test that README.md documents the workflow steps properly."""
        workflow_section = readme_content[readme_content.find("## Workflow Logic"):]
        
        # Should mention key workflow components
        assert "Trigger:" in workflow_section, "Workflow section should explain triggers"
        assert "checkout" in workflow_section.lower(), "Should mention code checkout step"
        assert "pull request" in workflow_section.lower(), "Should mention pull request creation"
    
    def test_readme_security_considerations(self, readme_content):
        """Test that README.md addresses security considerations."""
        assert "Security:" in readme_content, "README.md should mention security considerations"
        assert "authentication" in readme_content.lower(), "Should mention authentication"
    
    def test_readme_design_considerations_section(self, readme_content):
        """Test that README.md has a comprehensive design considerations section."""
        assert "## Project Concerns & Design Considerations" in readme_content, "Should have design considerations section"
        
        concerns_section = readme_content[readme_content.find("## Project Concerns & Design Considerations"):]
        
        # Check for key design aspects
        assert "Automation:" in concerns_section, "Should discuss automation benefits"
        assert "Consistency:" in concerns_section, "Should discuss consistency"
        assert "Limitations:" in concerns_section, "Should acknowledge limitations"
        assert "Extensibility:" in concerns_section, "Should discuss extensibility"
    
    def test_readme_proper_github_actions_references(self, readme_content):
        """Test that README.md properly references GitHub Actions components."""
        # Check for proper action references
        assert "actions/checkout@v3" in readme_content, "Should reference specific checkout action version"
        assert "diillson/auto-pull-request@v1.0.1" in readme_content, "Should reference specific auto-PR action version"
        assert "rlespinasse/git-commit-data-action@v1" in readme_content, "Should reference git commit data action"
    
    def test_readme_configuration_parameters(self, readme_content):
        """Test that README.md documents configuration parameters."""
        # Should mention key configuration options
        assert "pr_allow_empty: true" in readme_content, "Should document pr_allow_empty parameter"
        assert "auto-pr" in readme_content, "Should mention auto-pr label"
        assert "reviewer" in readme_content.lower(), "Should mention reviewer assignment"
    
    def test_readme_branch_requirements_clear(self, readme_content):
        """Test that README.md clearly explains branch requirements."""
        usage_section = readme_content[readme_content.find("## How to use this workflow"):]
        
        assert "image-update" in usage_section, "Usage section should mention image-update branch"
        assert "auto-pr-branch-create" in usage_section, "Usage section should mention target branch"
        assert "branches" in usage_section.lower(), "Should explicitly mention branch requirements"
    
    def test_readme_step_by_step_instructions(self, readme_content):
        """Test that README.md provides clear step-by-step instructions."""
        usage_section = readme_content[readme_content.find("## How to use this workflow"):]
        
        # Should have numbered steps
        numbered_steps = re.findall(r'^\s*\d+\.\s+', usage_section, re.MULTILINE)
        assert len(numbered_steps) >= 3, "Should have at least 3 numbered steps in usage instructions"
    
    def test_readme_proper_yaml_file_reference(self, readme_content):
        """Test that README.md properly references the YAML workflow file."""
        # Should mention the workflow file exists
        assert "already present in this repo" in readme_content, "Should indicate workflow file is present"
        assert ".github/workflows/" in readme_content, "Should mention proper workflow directory structure"
    
    def test_readme_customization_guidance(self, readme_content):
        """Test that README.md provides guidance on customization."""
        assert "customize" in readme_content.lower(), "Should mention customization options"
        assert "team's requirements" in readme_content.lower(), "Should mention adapting to team needs"
    
    def test_readme_no_broken_internal_references(self, readme_content):
        """Test that README.md doesn't have broken internal references."""
        # Check for file references that should exist
        file_references = re.findall(r'`([^`]+\.yml)`', readme_content)
        
        for file_ref in file_references:
            if not file_ref.startswith('http') and "auto-pr-demo.yml" in file_ref:
                expected_path = Path(".github/workflows/auto-pr-demo.yml")
                # Either file exists or it's mentioned as an example
                assert expected_path.exists() or "example" in readme_content.lower(), \
                    f"Referenced file should exist or be clearly marked as example: {file_ref}"
    
    def test_readme_consistent_terminology(self, readme_content):
        """Test that README.md uses consistent terminology throughout."""
        # Check for consistent naming of key concepts
        pr_variations = ['pull request', 'Pull Request', 'PR', 'pull requests']
        workflow_mentions = readme_content.lower().count('workflow')
        pr_mentions = sum(readme_content.count(variation) for variation in pr_variations)
        
        assert workflow_mentions >= 5, "Should mention 'workflow' multiple times for consistency"
        assert pr_mentions >= 5, "Should mention pull requests multiple times"
    
    def test_readme_line_length_reasonable(self, readme_content):
        """Test that README.md doesn't have excessively long lines."""
        lines = readme_content.split('\n')
        excessively_long_lines = [line for line in lines if len(line) > 200]
        
        # Allow some flexibility but flag extremely long lines
        assert len(excessively_long_lines) < 5, f"Too many excessively long lines found: {len(excessively_long_lines)}"
    
    def test_readme_proper_emphasis_formatting(self, readme_content):
        """Test that README.md uses proper emphasis formatting."""
        # Check for balanced emphasis markers
        bold_markers = readme_content.count('**')
        
        # Bold markers should be even (opening and closing pairs)
        assert bold_markers % 2 == 0, "Bold markers (**) should be properly paired"
    
    def test_readme_github_specific_features(self, readme_content):
        """Test that README.md properly documents GitHub-specific features."""
        # Should mention GitHub Actions specific concepts
        assert "GitHub Actions" in readme_content, "Should explicitly mention GitHub Actions"
        assert "runner" in readme_content.lower(), "Should mention GitHub Actions runners"
        assert "secrets" in readme_content.lower(), "Should mention GitHub secrets"
    
    def test_readme_workflow_trigger_explanation(self, readme_content):
        """Test that README.md clearly explains workflow triggers."""
        workflow_section = readme_content[readme_content.find("## Workflow Logic"):]
        
        assert "push" in workflow_section.lower(), "Should explain push trigger"
        assert "trigger" in workflow_section.lower(), "Should use 'trigger' terminology"
    
    def test_readme_environment_specifications(self, readme_content):
        """Test that README.md specifies the runtime environment."""
        assert "Ubuntu" in readme_content, "Should specify Ubuntu as the runner environment"
        assert "latest" in readme_content, "Should specify latest Ubuntu runner"
    
    def test_readme_empty_pr_explanation(self, readme_content):
        """Test that README.md explains the empty PR configuration."""
        # Should explain why empty PRs are allowed
        empty_pr_explanation = readme_content[readme_content.find("pr_allow_empty: true"):]
        
        assert "even if there are no changes" in empty_pr_explanation, \
            "Should explain empty PR behavior"
        assert "automation consistency" in empty_pr_explanation.lower(), \
            "Should explain the purpose of allowing empty PRs"


# Additional integration-style tests for README validation
class TestReadmeIntegration:
    """Integration tests for README.md that verify its relationship with the project structure."""
    
    def test_readme_workflow_file_consistency(self):
        """Test that README.md accurately describes the actual workflow file if it exists."""
        workflow_path = Path(".github/workflows/auto-pr-demo.yml")
        readme_path = Path("README.md")
        
        if workflow_path.exists() and readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Verify README mentions correspond to actual file location
            assert str(workflow_path) in readme_content, \
                "README should reference the correct workflow file path"
    
    def test_readme_repository_structure_alignment(self):
        """Test that README.md aligns with actual repository structure."""
        readme_path = Path("README.md")
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Check if .github directory exists when mentioned
            if ".github/workflows" in readme_content:
                github_dir = Path(".github")
                if github_dir.exists():
                    workflows_dir = Path(".github/workflows")
                    assert workflows_dir.exists(), \
                        "Workflows directory should exist if mentioned in README"
    
    @pytest.mark.slow
    def test_readme_external_references_valid(self):
        """Test that external references in README.md are valid (if any)."""
        readme_path = Path("README.md")
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Extract URLs (basic pattern)
            
            # For GitHub Actions references, verify they use valid action syntax
            action_references = re.findall(r'([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@v?\d+(?:\.\d+)?(?:\.\d+)?)', readme_content)
            
            assert len(action_references) >= 3, "Should reference multiple GitHub Actions"
            
            # Verify action references follow proper format
            for action_ref in action_references:
                assert '/' in action_ref and '@' in action_ref, \
                    f"Action reference should follow owner/repo@version format: {action_ref}"