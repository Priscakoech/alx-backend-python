#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)
        
    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, 'org', new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/testorg/repos'}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, 'https://api.github.com/orgs/testorg/repos')
            
        @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        test_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_repos

        with patch.object(GithubOrgClient, '_public_repos_url', return_value="https://api.github.com/orgs/testorg/repos"):
            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
         
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("testorg")
        self.assertEqual(client.has_license(repo, license_key), expected)
        
    @parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


