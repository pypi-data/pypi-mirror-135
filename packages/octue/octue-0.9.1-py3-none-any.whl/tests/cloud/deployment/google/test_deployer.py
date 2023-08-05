import copy
import os
import tempfile
from unittest.mock import Mock, patch

import yaml

from octue.cloud.deployment.google.deployer import DEFAULT_DOCKERFILE_URL, CloudRunDeployer
from octue.exceptions import DeploymentError
from tests.base import BaseTestCase


octue_configuration = {
    "name": "test-service",
    "repository_name": "test-repository",
    "repository_owner": "octue",
    "project_name": "test-project",
    "region": "europe-west2",
    "branch_pattern": "my-branch",
}


GET_SUBSCRIPTIONS_METHOD_PATH = "octue.cloud.deployment.google.deployer.Topic.get_subscriptions"

SERVICE_ID = "octue.services.0df08f9f-30ad-4db3-8029-ea584b4290b7"

EXPECTED_IMAGE_NAME = (
    f"eu.gcr.io/{octue_configuration['project_name']}/octue/{octue_configuration['repository_name']}/"
    f"{octue_configuration['name']}"
)

EXPECTED_CLOUD_BUILD_CONFIGURATION = {
    "steps": [
        {
            "id": "Get default Octue Dockerfile",
            "name": "alpine:latest",
            "args": ["wget", DEFAULT_DOCKERFILE_URL],
        },
        {
            "id": "Build image",
            "name": "gcr.io/cloud-builders/docker",
            "args": [
                "build",
                "-t",
                EXPECTED_IMAGE_NAME,
                ".",
                "-f",
                "Dockerfile",
            ],
        },
        {
            "id": "Push image",
            "name": "gcr.io/cloud-builders/docker",
            "args": ["push", EXPECTED_IMAGE_NAME],
        },
        {
            "id": "Deploy image to Google Cloud Run",
            "name": "gcr.io/google.com/cloudsdktool/cloud-sdk:slim",
            "entrypoint": "gcloud",
            "args": [
                "run",
                "services",
                "update",
                "test-service",
                "--platform=managed",
                f"--image={EXPECTED_IMAGE_NAME}",
                f"--region={octue_configuration['region']}",
                "--memory=128Mi",
                "--cpu=1",
                f"--set-env-vars=SERVICE_ID={SERVICE_ID},SERVICE_NAME={octue_configuration['name']}",
                "--timeout=3600",
                "--concurrency=10",
                "--min-instances=0",
                "--max-instances=10",
                "--ingress=internal",
            ],
        },
    ],
    "images": [EXPECTED_IMAGE_NAME],
}

EXPECTED_BUILD_TRIGGER_CREATION_COMMAND = [
    "gcloud",
    "beta",
    "builds",
    "triggers",
    "create",
    "github",
    f"--name={octue_configuration['name']}",
    f"--repo-name={octue_configuration['repository_name']}",
    f"--repo-owner={octue_configuration['repository_owner']}",
    f"--description=Build the {octue_configuration['name']!r} service and deploy it to Cloud Run.",
    f"--branch-pattern={octue_configuration['branch_pattern']}",
]


class TestCloudRunDeployer(BaseTestCase):
    def _create_octue_configuration_file(self, directory_path):
        """Create an `octue.yaml` configuration file in the given directory.

        :param str directory_path:
        :return str: the path of the `octue.yaml` file
        """
        octue_configuration_path = os.path.join(directory_path, "octue.yaml")

        with open(octue_configuration_path, "w") as f:
            yaml.dump(octue_configuration, f)

        return octue_configuration_path

    def test_generate_cloud_build_configuration(self):
        """Test that a correct Google Cloud Build configuration is generated from the given `octue.yaml` file."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            octue_configuration_path = self._create_octue_configuration_file(temporary_directory)
            deployer = CloudRunDeployer(octue_configuration_path, service_id=SERVICE_ID)
            deployer._generate_cloud_build_configuration()

        # Remove the commit hash from the image name as it will change for each commit made.
        generated_config = deployer.cloud_build_configuration
        generated_config["steps"][1]["args"][2] = generated_config["steps"][1]["args"][2].split(":")[0]
        generated_config["steps"][2]["args"][1] = generated_config["steps"][2]["args"][1].split(":")[0]
        generated_config["steps"][3]["args"][5] = generated_config["steps"][3]["args"][5].split(":")[0]
        generated_config["images"][0] = generated_config["images"][0].split(":")[0]

        self.assertEqual(generated_config, EXPECTED_CLOUD_BUILD_CONFIGURATION)

    def test_generate_cloud_build_configuration_with_custom_dockerfile(self):
        """Test that a correct Google Cloud Build configuration is generated from the given `octue.yaml` file when a
        dockerfile path is given.
        """
        try:
            octue_configuration["dockerfile_path"] = "path/to/Dockerfile"

            with tempfile.TemporaryDirectory() as temporary_directory:
                octue_configuration_path = self._create_octue_configuration_file(temporary_directory)
                deployer = CloudRunDeployer(octue_configuration_path, service_id=SERVICE_ID)
                deployer._generate_cloud_build_configuration()

            # Remove the commit hash from the image name as it will change for each commit made.
            generated_config = deployer.cloud_build_configuration
            generated_config["steps"][0]["args"][2] = generated_config["steps"][0]["args"][2].split(":")[0]
            generated_config["steps"][1]["args"][1] = generated_config["steps"][1]["args"][1].split(":")[0]
            generated_config["steps"][2]["args"][5] = generated_config["steps"][2]["args"][5].split(":")[0]
            generated_config["images"][0] = generated_config["images"][0].split(":")[0]

            # Expect the extra "Get default Octue Dockerfile" step to be absent and the given Dockerfile path to be
            # provided in the first step.
            expected_cloud_build_configuration = copy.deepcopy(EXPECTED_CLOUD_BUILD_CONFIGURATION)
            expected_cloud_build_configuration["steps"] = expected_cloud_build_configuration["steps"][1:]
            expected_cloud_build_configuration["steps"][0]["args"][5] = octue_configuration["dockerfile_path"]

            self.assertEqual(generated_config, expected_cloud_build_configuration)

        finally:
            del octue_configuration["dockerfile_path"]

    def test_deploy(self):
        """Test that the build trigger creation, build and deployment, and Eventarc run trigger creation are requested
        correctly.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            octue_configuration_path = self._create_octue_configuration_file(temporary_directory)
            deployer = CloudRunDeployer(octue_configuration_path, service_id=SERVICE_ID)

            with patch("subprocess.run", return_value=Mock(returncode=0)) as mock_run:
                with patch("octue.cloud.deployment.google.deployer.Topic.create"):
                    with patch(GET_SUBSCRIPTIONS_METHOD_PATH, return_value=["test-service"]):
                        with patch("octue.cloud.deployment.google.deployer.Subscription"):
                            deployer.deploy()

            # Remove the "random" path used for the build configuration in the `--inline-config` argument of the
            # command.
            build_trigger_command_without_inline_config_path = copy.deepcopy(mock_run.call_args_list[0].args)[0]
            build_trigger_command_without_inline_config_path.pop(9)

            # Test the build trigger creation request.
            self.assertEqual(build_trigger_command_without_inline_config_path, EXPECTED_BUILD_TRIGGER_CREATION_COMMAND)

            # Test the build request.
            self.assertEqual(mock_run.call_args_list[1].args[0][:4], ["gcloud", "builds", "submit", "."])

            # Test setting the Cloud Run service to accept unauthenticated requests.
            self.assertEqual(
                mock_run.call_args_list[2].args[0],
                [
                    "gcloud",
                    "run",
                    "services",
                    "add-iam-policy-binding",
                    octue_configuration["name"],
                    f'--region={octue_configuration["region"]}',
                    "--member=allUsers",
                    "--role=roles/run.invoker",
                ],
            )

            # Test the Eventarc run trigger creation request.
            self.assertEqual(
                mock_run.call_args_list[3].args[0],
                [
                    "gcloud",
                    "beta",
                    "eventarc",
                    "triggers",
                    "create",
                    f'{octue_configuration["name"]}-trigger',
                    "--matching-criteria=type=google.cloud.pubsub.topic.v1.messagePublished",
                    f"--destination-run-service={octue_configuration['name']}",
                    f"--location={octue_configuration['region']}",
                    f"--transport-topic={SERVICE_ID}",
                ],
            )

    def test_create_build_trigger_with_update(self):
        """Test that creating a build trigger for a service when one already exists and the deployer is in `update`
        mode results in the existing trigger being deleted and recreated.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            octue_configuration_path = self._create_octue_configuration_file(temporary_directory)
            deployer = CloudRunDeployer(octue_configuration_path)
            deployer._generate_cloud_build_configuration()

            with tempfile.NamedTemporaryFile(delete=False) as temporary_file:
                with open(temporary_file.name, "w") as f:
                    yaml.dump(deployer.cloud_build_configuration, f)

                with patch(
                    "octue.cloud.deployment.google.deployer.CloudRunDeployer._run_command",
                    side_effect=[DeploymentError("already exists"), None, None],
                ) as mock_run_command:
                    with patch("builtins.print") as mock_print:
                        deployer._create_build_trigger(temporary_file.name, update=True)

        self.assertEqual(mock_print.call_args[0][0], "recreated.")

        # Remove the "random" path used for the build configuration in the "--inline-config" argument of the
        # command.
        build_trigger_command_without_inline_config_path = copy.deepcopy(mock_run_command.call_args_list[0].args)[0]
        build_trigger_command_without_inline_config_path.pop(9)

        # Test the build trigger creation request.
        self.assertEqual(build_trigger_command_without_inline_config_path, EXPECTED_BUILD_TRIGGER_CREATION_COMMAND)

        # Test that trigger deletion is requested.
        self.assertEqual(
            mock_run_command.call_args_list[1].args[0],
            ["gcloud", "beta", "builds", "triggers", "delete", octue_configuration["name"]],
        )

        # Test the build trigger creation request is retried.
        retried_build_trigger_command_without_inline_config_path = copy.deepcopy(
            mock_run_command.call_args_list[2].args
        )[0]

        retried_build_trigger_command_without_inline_config_path.pop(9)

        self.assertEqual(
            retried_build_trigger_command_without_inline_config_path,
            EXPECTED_BUILD_TRIGGER_CREATION_COMMAND,
        )

    def test_create_eventarc_run_trigger_with_update(self):
        """Test that creating an Eventarc run trigger for a service when one already exists and the deployer is in
        `update` mode results in the Eventarc subscription update being skipped and an "already exists" message being
        printed.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            octue_configuration_path = self._create_octue_configuration_file(temporary_directory)
            deployer = CloudRunDeployer(octue_configuration_path)

            with patch("octue.cloud.deployment.google.deployer.Topic.create"):
                with patch(
                    "octue.cloud.deployment.google.deployer.CloudRunDeployer._run_command",
                    side_effect=DeploymentError("already exists"),
                ):
                    with patch(GET_SUBSCRIPTIONS_METHOD_PATH) as mock_get_subscriptions:
                        with patch("builtins.print") as mock_print:
                            deployer._create_eventarc_run_trigger(update=True)

        mock_get_subscriptions.assert_not_called()
        self.assertEqual(mock_print.call_args[0][0], "already exists.")
