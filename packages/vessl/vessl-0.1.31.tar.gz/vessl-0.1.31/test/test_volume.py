from test.conftest import USE_MOCK
from test.util import random_string

import pytest

import vessl


@pytest.mark.skipif(USE_MOCK, reason="Does not run if mocking is used.")
class TestVolume:
    file_name = random_string()

    @pytest.mark.order(index=1)
    def test_create_volume_file(self):
        volume_id = vessl.vessl_api.project.volume_id
        vessl.create_volume_file(volume_id, False, self.file_name)

    def test_read_volume_file(self):
        volume_id = vessl.vessl_api.project.volume_id
        vessl.read_volume_file(volume_id, self.file_name)

    def test_list_volume_files(self):
        volume_id = vessl.vessl_api.project.volume_id
        vessl.list_volume_files(volume_id)

    @pytest.mark.order(index=-1)
    def test_delete_volume_file(self):
        volume_id = vessl.vessl_api.project.volume_id
        vessl.delete_volume_file(volume_id, path=self.file_name)
