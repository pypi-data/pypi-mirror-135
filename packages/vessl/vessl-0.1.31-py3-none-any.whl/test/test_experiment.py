from test.conftest import USE_MOCK

import pytest

import vessl
from vessl.util.exception import InvalidExperimentError


@pytest.mark.skipif(USE_MOCK, reason="Does not run if mocking is used.")
class TestExperiment:
    @pytest.mark.order(index=1)
    def test_create_experiment(self):
        # Use pytest.experiment instead of self.experiment because self gets reset
        # after each test
        pytest.experiment = vessl.create_experiment(
            cluster_name="aws-uw2-dev",  # TODO: change when CI server is relocated
            start_command="echo 'Hello world!'",
            kernel_resource_spec_name="v1.cpu-0.mem-1",
            kernel_image_url="vessl/kernels:py36.full-cpu",
            message="test message",
            termination_protection=False,
            env_vars=["VAR=value"],
        )
        assert pytest.experiment.is_distributed == False

    @pytest.mark.order(index=2)
    def test_create_distributed_experiment(self):
        pytest.distributed_experiment = vessl.create_experiment(
            cluster_name="aws-uw2-dev",  # TODO: change when CI server is relocated
            start_command="echo 'Hello world!'",
            kernel_resource_spec_name="v1.cpu-0.mem-1",
            kernel_image_url="vessl/kernels:py36.full-cpu",
            message="test message",
            termination_protection=False,
            env_vars=["VAR=value"],
            worker_count=2,
            framework_type="pytorch",
        )
        assert pytest.distributed_experiment.is_distributed == True

    @pytest.mark.order(index=3)
    def test_create_local_experiment(self):
        pytest.local_experiment = vessl.experiment.create_local_experiment()

    def test_read_experiment(self):
        experiment = vessl.read_experiment(pytest.experiment.name)
        assert experiment.is_distributed == False

    def test_read_distributed_experiment(self):
        distributed_experiment = vessl.read_experiment(
            pytest.distributed_experiment.name
        )
        assert distributed_experiment.is_distributed == True

    def test_read_experiment_by_id(self):
        vessl.read_experiment_by_id(pytest.experiment.id)

    def test_list_experiments(self):
        vessl.list_experiments()

    def test_list_experiment_logs(self):
        vessl.list_experiment_logs(pytest.experiment.name)
        vessl.list_experiment_logs(pytest.distributed_experiment.name)

    def test_list_experiment_output_files(self):
        vessl.list_experiment_output_files(pytest.experiment.name)
        vessl.list_experiment_output_files(pytest.distributed_experiment.name)
        # vessl.list_experiment_logs(pytest.local_experiment.name)

    def test_download_experiment_output_files(self):
        vessl.download_experiment_output_files(pytest.experiment.name)
        vessl.download_experiment_output_files(pytest.distributed_experiment.name)
        vessl.download_experiment_output_files(pytest.local_experiment.name)

    def test_upload_experiment_output_files(self):
        with pytest.raises(InvalidExperimentError):
            # Cannot upload to managed experiment
            vessl.upload_experiment_output_files(pytest.experiment.name, "test/fixture")
        vessl.upload_experiment_output_files(
            pytest.local_experiment.name, "test/fixture"
        )
