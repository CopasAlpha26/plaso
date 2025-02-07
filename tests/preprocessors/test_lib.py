# -*- coding: utf-8 -*-
"""Preprocessing related functions and classes for testing."""

from artifacts import reader as artifacts_reader
from artifacts import registry as artifacts_registry
from dfvfs.helpers import file_system_searcher

from plaso.preprocessors import mediator
from plaso.storage.fake import writer as fake_writer

from tests import test_lib as shared_test_lib


class ArtifactPreprocessorPluginTestCase(shared_test_lib.BaseTestCase):
  """Artifact preprocessor plugin test case."""

  @classmethod
  def setUpClass(cls):
    """Makes preparations before running any of the tests."""
    artifacts_path = shared_test_lib.GetTestFilePath(['artifacts'])
    cls._artifacts_registry = artifacts_registry.ArtifactDefinitionsRegistry()

    reader = artifacts_reader.YamlArtifactsReader()
    cls._artifacts_registry.ReadFromDirectory(reader, artifacts_path)

  def _CreateTestStorageWriter(self):
    """Creates a storage writer for testing purposes.

    Returns:
      StorageWriter: storage writer.
    """
    storage_writer = fake_writer.FakeStorageWriter()
    storage_writer.Open()
    return storage_writer

  def _RunPreprocessorPluginOnFileSystem(
      self, file_system, mount_point, storage_writer, plugin):
    """Runs a preprocessor plugin on a file system.

    Args:
      file_system (dfvfs.FileSystem): file system to be preprocessed.
      mount_point (dfvfs.PathSpec): mount point path specification that refers
          to the base location of the file system.
      storage_writer (StorageWriter): storage writer.
      plugin (ArtifactPreprocessorPlugin): preprocessor plugin.

    Return:
      PreprocessMediator: preprocess mediator.
    """
    artifact_definition = self._artifacts_registry.GetDefinitionByName(
        plugin.ARTIFACT_DEFINITION_NAME)
    self.assertIsNotNone(artifact_definition)

    test_mediator = mediator.PreprocessMediator(storage_writer)

    searcher = file_system_searcher.FileSystemSearcher(file_system, mount_point)

    plugin.Collect(test_mediator, artifact_definition, searcher, file_system)

    return test_mediator
