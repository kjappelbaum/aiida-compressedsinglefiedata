# -*- coding: utf-8 -*-
"""Tests for the `CompressedSinglefileData` class."""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import tempfile

from aiida.orm import load_node
from aiida.manage.fixtures import PluginTestCase
from aiida_compressedsinglefile import CompressedSinglefileData


class TestCompressedSinglefileData(PluginTestCase):
    """Tests for the `CompressedSinglefileData` class."""

    def test_reload_singlefile_data(self):
        """Test writing and reloading a `CompressedSinglefileData` instance."""
        content_original = 'some text ABCDE'

        with tempfile.NamedTemporaryFile(mode='w+') as handle:
            filepath = handle.name
            basename = os.path.basename(filepath)
            handle.write(content_original)
            handle.flush()
            node = CompressedSinglefileData(file=filepath)

        uuid = node.uuid

        with node.open() as handle:
            content_written = handle.read()

        # self.assertEqual(node.list_object_names(), [basename])
        self.assertEqual(content_written, content_original)

        node.store()

        with node.open() as handle:
            content_stored = handle.read()

        self.assertEqual(content_stored, content_original)
        self.assertEqual(node.list_object_names(), [basename])

        node_loaded = load_node(uuid)
        self.assertTrue(isinstance(node_loaded, CompressedSinglefileData))

        with node.open() as handle:
            content_loaded = handle.read()

        self.assertEqual(content_loaded, content_original)

        with node_loaded.open() as handle:
            self.assertEqual(handle.read(), content_original)
