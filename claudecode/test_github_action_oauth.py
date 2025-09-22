#!/usr/bin/env python3
"""
Unit tests for GitHub Action OAuth token support.
"""

import os
from unittest.mock import Mock, patch

from claudecode.github_action_audit import initialize_findings_filter


class TestGitHubActionOAuth:
    """Test GitHub Action OAuth token functionality."""

    @patch('claudecode.github_action_audit.FindingsFilter')
    def test_oauth_token_passed_to_findings_filter(self, mock_filter):
        """Test that OAuth token is passed to FindingsFilter when available."""
        mock_filter.return_value = Mock()

        with patch.dict(os.environ, {
            'ENABLE_CLAUDE_FILTERING': 'true',
            'CLAUDE_CODE_OAUTH_TOKEN': 'test-oauth-token'
        }):
            initialize_findings_filter()

        call_args = mock_filter.call_args[1]
        assert call_args['oauth_token'] == 'test-oauth-token'
        assert call_args['use_claude_filtering'] is True

