import os
import six
import zipfile
from io import BytesIO
import shutil
import tempfile
from pathlib import Path
from aiida.common import exceptions
from aiida.orm.data import Data

__all__ = ('CompressedSinglefileData', )


class CompressedSinglefileData(Data):
    """Data class that can be used to store a single file compressed in its repository.
    For reading, it creates a temporary file
    """

    DEFAULT_FILENAME = 'file.txt'

    def __init__(self, file, **kwargs):
        """Construct a new instance and set the contents to that of the file.
        :param file: an absolute filepath or filelike object whose contents to copy
        """
        # pylint: disable=redefined-builtin
        super(CompressedSinglefileData, self).__init__(**kwargs)
        if file is not None:
            self.set_file(file)
        self._oldkey = DEFAULT_FILENAME

    @property
    def filename(self):
        """Return the name of the file stored.
        :return: the filename under which the file is stored in the repository
        """
        return self.get_attribute('filename')

    def open(self, key=None, mode='r'):
        """Return an open file handle to the content of this data node.
        :param key: optional key within the repository, by default is the `filename` set in the attributes
        :param mode: the mode with which to open the file handle (default: read mode)
        :return: a file handle
        """

        if key is None:
            key = self.filename
        archive = zipfile.ZipFile(key, 'r')
        return archive

    def get_content(self):
        """Return the content of the single file stored for this data node.
        :return: the content of the file as a string
        """
        with self.open() as handle:
            return handle.read()

    def _compress(self, file, key):
        with zipfile.ZipFile(file, 'w') as zip_file:
            zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED)
        self._oldkey = key
        key = "".join([Path(self._oldkey).stem, '.zip'])
        return key

    def set_file(self, file):
        """Store the content of the file in the node's repository, deleting any other existing objects.
        :param file: an absolute filepath or filelike object whose contents to copy
            Hint: Pass io.StringIO("my string") to construct the file directly from a string.
        """
        # pylint: disable=redefined-builtin

        try:
            key = os.path.basename(file.name)
        except AttributeError:
            key = self.DEFAULT_FILENAME

        if not os.path.isabs(file):
            raise ValueError('path `{}` is not absolute'.format(file))

        if not os.path.isfile(file):
            raise ValueError(
                'path `{}` does not correspond to an existing file'.format(
                    file))

        key = self._compress(file, key)

        existing_object_names = self.list_object_names()

        try:
            # Remove the 'key' from the list of currently existing objects such that it is not deleted after storing
            existing_object_names.remove(key)
        except ValueError:
            pass

        self.put_object_from_file(file, key)

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
            raise exceptions.ValidationError(
                'the `filename` attribute is not set.')

        objects = self.list_object_names()

        if [filename] != objects:
            raise exceptions.ValidationError(
                'respository files {} do not match the `filename` attribute {}.'
                .format(objects, filename))
