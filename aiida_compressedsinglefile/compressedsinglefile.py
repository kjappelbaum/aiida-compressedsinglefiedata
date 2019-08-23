"""CompressedSinglefileData for AiiDA"""
from __future__ import absolute_import
import os
from pathlib import Path
import zipfile
import tempfile
import io
from aiida.common import exceptions
from aiida.orm import Data

__all__ = ('CompressedSinglefileData',)


class CompressedSinglefileData(Data):
    """Data class that can be used to store a single file compressed in its repository.
    It is not intended to be used with filelike
    """

    DEFAULT_FILENAME = 'file.zip'

    def __init__(self, filepath, **kwargs):
        """Construct a new instance and set the contents to that of the file.
        :param filepath: an absolute filepath
        """
        # pylint: disable=redefined-builtin
        super(CompressedSinglefileData, self).__init__(**kwargs)
        if filepath is not None:
            self.set_file(filepath)
        self._oldkey = Path(filepath).name

    @property
    def filename(self):
        """Return the name of the file stored.
        :return: the filename under which the file is stored in the repository
        """
        return self.get_attribute('filename')

    def open(self, key=None):  # pylint: disable=arguments-differ
        """Return an open file handle to the content of this data node.
        :param key: optional key within the repository, by default is the `filename` set in the attributes
        :return: a file handle
        """

        if key is None:
            key = self.filename

        self._folder = self._repository._get_base_folder()  # pylint:disable=protected-access, attribute-defined-outside-init
        archive = zipfile.ZipFile(os.path.join(self._folder.abspath, key), 'r')
        handle = archive.read(self._oldkey)
        return io.BytesIO(handle)

    def get_content(self):
        """Return the content of the single file stored for this data node.
        :return: the content of the file as a string
        """
        with self.open() as handle:  # pylint:disable=no-value-for-parameter
            return handle.read().decode('UTF-8')

    def _compress(self, file, key):
        """compresses a file and changes the key to *.zip extension"""

        self._oldkey = key
        key = ''.join([Path(self._oldkey).stem, '.zip'])
        self._tempfile = tempfile.NamedTemporaryFile(mode='w')  # pylint:disable=attribute-defined-outside-init
        with zipfile.ZipFile(self._tempfile.name, 'w') as zip_file:
            zip_file.write(file, self._oldkey)
        return key

    def set_file(self, filepath):
        """Store the content of the file in the node's repository, deleting any other existing objects.
        :param filepath: an absolute filepath
        """
        # pylint: disable=redefined-builtin

        try:
            key = Path(filepath).name
        except AttributeError:
            key = self.DEFAULT_FILENAME

        if not os.path.isabs(filepath):
            raise ValueError('path `{}` is not absolute'.format(filepath))

        if not os.path.isfile(filepath):
            raise ValueError('path `{}` does not correspond to an existing file'.format(filepath))

        key = self._compress(filepath, key)
        existing_object_names = self.list_object_names()

        try:
            # Remove the 'key' from the list of currently existing objects such that it is not deleted after storing
            existing_object_names.remove(key)
        except ValueError:
            pass
        self._folder = self._repository._get_base_folder()  # pylint:disable=protected-access
        self._folder.insert_path(self._tempfile.name, key)  # pylint:disable=protected-access

        # Delete any other existing objects (minus the current `key` which was already removed from the list)
        for existing_key in existing_object_names:
            self.delete_object(existing_key)

        self.set_attribute('filename', key)

    def _validate(self):
        """Ensure that there is one object stored in the repository, whose key matches value set for `filename` attr."""
        super(CompressedSinglefileData, self)._validate()

        try:
            filename = self.filename
        except AttributeError:
            raise exceptions.ValidationError('the `filename` attribute is not set.')

        objects = self.list_object_names()

        if [filename] != objects:
            raise exceptions.ValidationError(
                'respository files {} do not match the `filename` attribute {}.'.format(objects, filename)
            )
