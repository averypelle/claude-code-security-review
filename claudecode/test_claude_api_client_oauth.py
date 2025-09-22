#!/usr/bin/env python3
"""
Unit tests for ClaudeAPIClient OAuth token support.
"""

import os
import pytest
from unittest.mock import Mock, patch

from claudecode.claude_api_client import ClaudeAPIClient


class TestClaudeAPIClientOAuth:
    """Test ClaudeAPIClient OAuth token functionality."""

    @patch('claudecode.claude_api_client.Anthropic')
    def test_oauth_token_priority_over_api_key(self, mock_anthropic):
        """Test that OAuth token takes priority over API key when both provided."""
        mock_anthropic.return_value = Mock()

        client = ClaudeAPIClient(
            oauth_token='test-oauth-token',
            api_key='test-api-key'
        )

        mock_anthropic.assert_called_once_with(auth_token='test-oauth-token')

    @patch('claudecode.claude_api_client.Anthropic')
    def test_oauth_env_priority_over_api_key_env(self, mock_anthropic):
        """Test that OAuth token env var takes priority over API key env var."""
        mock_anthropic.return_value = Mock()

        with patch.dict(os.environ, {
            'CLAUDE_CODE_OAUTH_TOKEN': 'env-oauth-token',
            'ANTHROPIC_API_KEY': 'env-api-key'
        }):
            client = ClaudeAPIClient()

        mock_anthropic.assert_called_once_with(auth_token='env-oauth-token')

    @patch('claudecode.claude_api_client.Anthropic')
    def test_backward_compatibility_api_key_only(self, mock_anthropic):
        """Test that existing API key functionality still works unchanged."""
        mock_anthropic.return_value = Mock()

        client = ClaudeAPIClient(api_key='existing-api-key')

        mock_anthropic.assert_called_once_with(api_key='existing-api-key')
        assert client.api_key == 'existing-api-key'
        assert client.oauth_token is None