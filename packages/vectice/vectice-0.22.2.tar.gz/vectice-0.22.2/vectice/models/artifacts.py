from typing import Optional

from .code_version_artifact import CodeVersionArtifact
from .dataset_version_artifact import DatasetVersionArtifact
from .model_version_artifact import ModelVersionArtifact
from .api_token import ApiToken


class Artifacts:
    """
    Factory class for Artifacts
    """

    @classmethod
    def create_dataset_version(
        cls,
        description: Optional[str] = None,
    ) -> DatasetVersionArtifact:
        """
        Create an artifact for a dataset

        :param description: The description of the dataset version
        :return: A DatasetVersionArtifact
        """
        return DatasetVersionArtifact.create(description)

    @classmethod
    def create_model_version(
        cls,
        description: Optional[str] = None,
    ) -> ModelVersionArtifact:
        """
        Create an artifact for a model

        :param description: The description of the model version
        :return: A ModelVersionArtifact
        """
        return ModelVersionArtifact.create(description)

    @classmethod
    def create_code_version(cls, path: str = ".") -> Optional[CodeVersionArtifact]:
        """
        Create a code artifact based on the git information relative to the given local path.

        :param path: The path to look for the git repository
        :return: A CodeVersion or None if a git repository was not found locally
        """
        return CodeVersionArtifact.create(path)

    @classmethod
    def create_code_version_with_github_uri(
        cls, uri: str, script_relative_path: Optional[str] = None, login_or_token=None, password=None, jwt=None
    ) -> Optional[CodeVersionArtifact]:
        """
        Create a code artifact based on the github information relative to the given URI and relative path.

        Note: The URI given can include the branch you are working on. otherwise, the default repository branch will be used.

        sample :
            https://github.com/my-organization/my-repository (no branch given so using default branch)
            https://github.com/my-organization/my-repository/tree/my-current-branch (branch given is my-current-branch)

        To access private repositories, you need to authenticate with your credentials.
        see https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/about-authentication-to-github

        :param uri: The uri of the repository with a specific branch if needed.
        :param script_relative_path:  The file that is executed
        :param login_or_token: A real login or personal access token
        :param password: The password
        :param jwt: The Oauth2 access token
        :return: A CodeVersion or None if the github repository was not found or is not accessible
        """
        return CodeVersionArtifact.create_from_github_uri(uri, script_relative_path, login_or_token, password, jwt)

    @classmethod
    def create_code_version_with_gitlab_uri(
        cls, uri: str, script_relative_path: str, private_token: Optional[str] = None, oauth_token: Optional[str] = None
    ) -> Optional[CodeVersionArtifact]:
        """
        Create an artifact that contains a version of a code

        :param uri: The uri of the repository with a specific branch if needed.
        :param script_relative_path:  The file that is executed
        :param private_token: A real login or a personal access token
        :param oauth_token: The OAuth2 access token
        :return: A CodeVersion or None if the GitHub repository was not found or is not accessible
        """
        return CodeVersionArtifact.create_from_gitlab_uri(uri, script_relative_path, private_token, oauth_token)

    @classmethod
    def create_code_version_with_bitbucket_uri(
        cls,
        uri: str,
        script_relative_path: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[CodeVersionArtifact]:
        """
        Create a code artifact based on the Bitbucket information relative to the given URI and relative path.

        Note: The URI given can include the branch you are working on. otherwise, the default repository branch will be used.

        sample :
            https://bitbucket.org/workspace/project/ (no branch given so using default branch)
            https://bitbucket.org/workspace/project/src/branch (branch given is my-current-branch)

        To access private repositories, you need to authenticate with your credentials.
        see Bitbucket Cloud: https://atlassian-python-api.readthedocs.io/index.html

        :param uri: The uri of the repository with a specific branch if needed.
        :param script_relative_path:  The file that is executed
        :param username: Bitbucket email
        :param password: Bitbucket password
        :return: A CodeVersion or None if the Bitbucket repository was not found or is not accessible
        """
        return CodeVersionArtifact.create_from_bitbucket_uri(uri, script_relative_path, username, password)

    @classmethod
    def parse_api_token(cls, token_file: str) -> ApiToken:
        """
        Parses the the API Token json file and sets the os environmental variable for the "VECTICE_API_TOKEN"
        for the user.

        :param token_file: The filepath to the json file containing the "VECTICE_API_TOKEN", found on the Vectice App
        :return: ApiToken or None if the json file can not be parsed or found
        """
        return ApiToken.parse_api_token_json(token_file)
