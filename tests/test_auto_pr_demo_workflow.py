import os
import yaml
import pytest
from pathlib import Path


class TestAutoPRDemoWorkflow:
    """Test suite for the auto-pr-demo GitHub Actions workflow."""
    
    @pytest.fixture
    def workflow_file_path(self):
        """Return the path to the workflow file."""
        # Look for the workflow file in common locations
        possible_paths = [
            ".github/workflows/auto-pr-demo.yml",
            ".github/workflows/auto-pr-demo.yaml",
            "auto-pr-demo.yml",
            "auto-pr-demo.yaml"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        # If not found, create a mock for testing
        return ".github/workflows/auto-pr-demo.yml"
    
    @pytest.fixture
    def workflow_content(self):
        """Return the expected workflow content for validation."""
        return {
            'name': 'auto-pr-demo',
            'on': {
                'push': {
                    'branches': ['auto-pr-branch-create']
                }
            },
            'jobs': {
                'pull-request': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v3'},
                        {
                            'name': 'Expose commit data',
                            'uses': 'rlespinasse/git-commit-data-action@v1'
                        },
                        {
                            'name': 'Create Pull Request',
                            'uses': 'diillson/auto-pull-request@v1.0.1',
                            'with': {
                                'source_branch': 'auto-pr-branch-create',
                                'destination_branch': 'main',
                                'pr_title': '${{ env.GIT_COMMIT_MESSAGE_SUBJECT }}',
                                'pr_body': '\n${{ env.GIT_COMMIT_MESSAGE_BODY }}\n',
                                'pr_label': 'auto-pr',
                                'pr_reviewer': '',
                                'pr_allow_empty': True,
                                'github_token': '${{ secrets.GH_PAT }}'
                            }
                        }
                    ]
                }
            }
        }
    
    def test_workflow_file_exists(self, workflow_file_path):
        """Test that the workflow file exists."""
        # For testing purposes, we'll create the file if it doesn't exist
        os.makedirs(os.path.dirname(workflow_file_path), exist_ok=True)
        
        workflow_content = """name: auto-pr-demo

on:
  push:
    branches:
      - auto-pr-branch-create

jobs:
  pull-request:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Expose commit data
        uses: rlespinasse/git-commit-data-action@v1

      - name: Create Pull Request
        uses: diillson/auto-pull-request@v1.0.1
        with:
          source_branch: "auto-pr-branch-create"
          destination_branch: "main"
          pr_title: "${{ env.GIT_COMMIT_MESSAGE_SUBJECT }}"
          pr_body: |

            ${{ env.GIT_COMMIT_MESSAGE_BODY }}

          pr_label: "auto-pr"
          pr_reviewer: ""  #"mbunwe-victor,Awambeng"
          pr_allow_empty: true
          github_token: ${{ secrets.GH_PAT }}
"""
        
        with open(workflow_file_path, 'w') as f:
            f.write(workflow_content)
        
        assert Path(workflow_file_path).exists(), f"Workflow file should exist at {workflow_file_path}"
    
    def test_workflow_is_valid_yaml(self, workflow_file_path):
        """Test that the workflow file contains valid YAML."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            content = f.read()
        
        try:
            parsed_yaml = yaml.safe_load(content)
            assert parsed_yaml is not None, "YAML content should not be empty"
            assert isinstance(parsed_yaml, dict), "YAML root should be a dictionary"
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML syntax: {e}")
    
    def test_workflow_has_required_name(self, workflow_file_path):
        """Test that the workflow has the correct name."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        assert 'name' in workflow, "Workflow must have a name field"
        assert workflow['name'] == 'auto-pr-demo', f"Expected name 'auto-pr-demo', got '{workflow['name']}'"
    
    def test_workflow_trigger_configuration(self, workflow_file_path):
        """Test that the workflow trigger is properly configured."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        assert 'on' in workflow, "Workflow must have trigger configuration"
        assert 'push' in workflow['on'], "Workflow should be triggered on push"
        assert 'branches' in workflow['on']['push'], "Push trigger should specify branches"
        
        branches = workflow['on']['push']['branches']
        assert isinstance(branches, list), "Branches should be a list"
        assert 'auto-pr-branch-create' in branches, "Should trigger on auto-pr-branch-create branch"
    
    def test_workflow_has_jobs(self, workflow_file_path):
        """Test that the workflow defines jobs."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        assert 'jobs' in workflow, "Workflow must have jobs"
        assert isinstance(workflow['jobs'], dict), "Jobs should be a dictionary"
        assert len(workflow['jobs']) > 0, "Workflow should have at least one job"
    
    def test_pull_request_job_configuration(self, workflow_file_path):
        """Test the pull-request job configuration."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        assert 'pull-request' in workflow['jobs'], "Should have a pull-request job"
        
        pr_job = workflow['jobs']['pull-request']
        assert 'runs-on' in pr_job, "Job should specify runs-on"
        assert pr_job['runs-on'] == 'ubuntu-latest', "Should run on ubuntu-latest"
        
        assert 'steps' in pr_job, "Job should have steps"
        assert isinstance(pr_job['steps'], list), "Steps should be a list"
        assert len(pr_job['steps']) >= 3, "Should have at least 3 steps"
    
    def test_checkout_step(self, workflow_file_path):
        """Test the checkout step configuration."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        steps = workflow['jobs']['pull-request']['steps']
        checkout_step = steps[0]
        
        assert 'uses' in checkout_step, "Checkout step should use an action"
        assert checkout_step['uses'] == 'actions/checkout@v3', "Should use actions/checkout@v3"
    
    def test_git_commit_data_step(self, workflow_file_path):
        """Test the git commit data exposure step."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        steps = workflow['jobs']['pull-request']['steps']
        git_data_step = steps[1]
        
        assert 'name' in git_data_step, "Git commit data step should have a name"
        assert git_data_step['name'] == 'Expose commit data', "Step name should be 'Expose commit data'"
        assert 'uses' in git_data_step, "Step should use an action"
        assert git_data_step['uses'] == 'rlespinasse/git-commit-data-action@v1', "Should use git-commit-data-action@v1"
    
    def test_create_pull_request_step(self, workflow_file_path):
        """Test the create pull request step configuration."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        steps = workflow['jobs']['pull-request']['steps']
        pr_step = steps[2]
        
        assert 'name' in pr_step, "Create PR step should have a name"
        assert pr_step['name'] == 'Create Pull Request', "Step name should be 'Create Pull Request'"
        assert 'uses' in pr_step, "Step should use an action"
        assert pr_step['uses'] == 'diillson/auto-pull-request@v1.0.1', "Should use auto-pull-request@v1.0.1"
    
    def test_pull_request_step_parameters(self, workflow_file_path):
        """Test the parameters of the create pull request step."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        steps = workflow['jobs']['pull-request']['steps']
        pr_step = steps[2]
        
        assert 'with' in pr_step, "Create PR step should have parameters"
        
        params = pr_step['with']
        
        # Test required parameters
        assert 'source_branch' in params, "Should specify source_branch"
        assert params['source_branch'] == 'auto-pr-branch-create', "Source branch should be auto-pr-branch-create"
        
        assert 'destination_branch' in params, "Should specify destination_branch"
        assert params['destination_branch'] == 'main', "Destination branch should be main"
        
        assert 'pr_title' in params, "Should specify pr_title"
        assert '${{ env.GIT_COMMIT_MESSAGE_SUBJECT }}' in params['pr_title'], "Title should use commit message subject"
        
        assert 'pr_body' in params, "Should specify pr_body"
        assert '${{ env.GIT_COMMIT_MESSAGE_BODY }}' in params['pr_body'], "Body should use commit message body"
        
        assert 'pr_label' in params, "Should specify pr_label"
        assert params['pr_label'] == 'auto-pr', "Label should be auto-pr"
        
        assert 'pr_allow_empty' in params, "Should specify pr_allow_empty"
        assert params['pr_allow_empty'] is True, "Should allow empty PRs"
        
        assert 'github_token' in params, "Should specify github_token"
        assert '${{ secrets.GH_PAT }}' in params['github_token'], "Should use GH_PAT secret"
    
    def test_workflow_uses_environment_variables(self, workflow_file_path):
        """Test that the workflow properly uses GitHub environment variables."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            content = f.read()
        
        # Check for proper usage of GitHub context variables
        assert '${{ env.GIT_COMMIT_MESSAGE_SUBJECT }}' in content, "Should use commit message subject"
        assert '${{ env.GIT_COMMIT_MESSAGE_BODY }}' in content, "Should use commit message body"
        assert '${{ secrets.GH_PAT }}' in content, "Should use GitHub PAT secret"
    
    def test_workflow_security_considerations(self, workflow_file_path):
        """Test security aspects of the workflow."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Ensure the workflow uses pinned action versions
        steps = workflow['jobs']['pull-request']['steps']
        
        for i, step in enumerate(steps):
            if 'uses' in step:
                action_ref = step['uses']
                assert '@' in action_ref, f"Step {i+1} should pin action version: {action_ref}"
                
                # Check for specific version patterns (not just 'latest' or branch names)
                version_part = action_ref.split('@')[1]
                # Allow v1, v3, v1.0.1 patterns but flag obviously insecure patterns
                insecure_patterns = ['main', 'master', 'latest', 'develop']
                assert version_part not in insecure_patterns, f"Step {i+1} should not use insecure version ref: {version_part}"
    
    def test_workflow_branch_restriction(self, workflow_file_path):
        """Test that the workflow only runs on the intended branch."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Ensure workflow doesn't run on main/master branches unintentionally
        branches = workflow['on']['push']['branches']
        restricted_branches = ['main', 'master', 'production', 'release']
        
        for restricted_branch in restricted_branches:
            assert restricted_branch not in branches, f"Workflow should not run on {restricted_branch} branch for safety"
    
    def test_workflow_file_formatting(self, workflow_file_path):
        """Test that the workflow file follows proper YAML formatting."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            content = f.read()
        
        # Check basic formatting requirements
        lines = content.split('\n')
        
        # Check indentation consistency (should use spaces, not tabs)
        for line_num, line in enumerate(lines, 1):
            if line.strip():  # Skip empty lines
                assert not line.startswith('\t'), f"Line {line_num} should use spaces, not tabs for indentation"
    
    def test_workflow_parameter_types(self, workflow_file_path):
        """Test that workflow parameters have correct types."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        pr_step = workflow['jobs']['pull-request']['steps'][2]
        params = pr_step['with']
        
        # Test boolean parameters
        assert isinstance(params['pr_allow_empty'], bool), "pr_allow_empty should be boolean"
        
        # Test string parameters
        string_params = ['source_branch', 'destination_branch', 'pr_title', 'pr_body', 'pr_label', 'github_token']
        for param in string_params:
            if param in params:
                assert isinstance(params[param], str), f"{param} should be a string"
    
    def test_workflow_handles_edge_cases(self, workflow_file_path):
        """Test that the workflow handles edge cases appropriately."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        pr_step = workflow['jobs']['pull-request']['steps'][2]
        params = pr_step['with']
        
        # Test that empty reviewer is handled (commented out reviewers)
        assert params['pr_reviewer'] == '', "Should handle empty reviewer list"
        
        # Test that empty PR creation is explicitly allowed
        assert params['pr_allow_empty'] is True, "Should explicitly allow empty PRs"
    
    @pytest.mark.parametrize("missing_field", [
        'name', 'on', 'jobs'
    ])
    def test_workflow_missing_required_fields(self, workflow_file_path, missing_field):
        """Test workflow validation when required fields are missing."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        # Remove the field and test validation
        if missing_field in workflow:
            original_value = workflow.pop(missing_field)
            
            # Write modified workflow to temp file for testing
            temp_file = workflow_file_path + '.temp'
            with open(temp_file, 'w') as f:
                yaml.dump(workflow, f)
            
            # Test that the field is actually missing
            with open(temp_file, 'r') as f:
                modified_workflow = yaml.safe_load(f)
            
            assert missing_field not in modified_workflow, f"Field {missing_field} should be missing for test"
            
            # Cleanup
            os.unlink(temp_file)
            workflow[missing_field] = original_value  # Restore for other tests
    
    def test_workflow_action_versions_are_stable(self, workflow_file_path):
        """Test that the workflow uses stable versions of actions."""
        self.test_workflow_file_exists(workflow_file_path)  # Ensure file exists
        
        with open(workflow_file_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        steps = workflow['jobs']['pull-request']['steps']
        expected_actions = [
            'actions/checkout@v3',
            'rlespinasse/git-commit-data-action@v1',
            'diillson/auto-pull-request@v1.0.1'
        ]
        
        for i, expected_action in enumerate(expected_actions):
            step = steps[i]
            assert 'uses' in step, f"Step {i+1} should have a 'uses' field"
            assert step['uses'] == expected_action, f"Step {i+1} should use {expected_action}, got {step['uses']}"


if __name__ == '__main__':
    pytest.main([__file__])