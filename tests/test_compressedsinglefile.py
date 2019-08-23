# -*- coding: utf-8 -*-
"""Tests for the `CompressedSinglefileData` class."""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import tempfile
from aiida.manage.fixtures import PluginTestCase
from aiida_compressedsinglefile import CompressedSinglefileData


def test_reload_singlefile_data(imp, aiida_profile):
    """Test writing and reloading a `CompressedSinglefileData` instance."""
    content_original = 'some text ABCDE'

    with tempfile.NamedTemporaryFile(mode='w+') as handle:
        filepath = handle.name
        basename = os.path.basename(filepath)
        handle.write(content_original)
        handle.flush()
        node = CompressedSinglefileData(filepath=filepath)

    uuid = node.uuid

    with node.open() as handle:
        content_written = handle.read().decode('UTF-8')

    assert content_written == content_original
    assert node.get_content() == content_original

    node.store()

    with node.open() as handle:
        content_stored = handle.read().decode('UTF-8')

    assert content_stored == content_original
    assert node.get_content() == content_original

    node_loaded = load_node(uuid)
    assert isinstance(node_loaded, CompressedSinglefileData)

    with node.open() as handle:
        content_loaded = handle.read().decode('UTF-8')

    assert content_loaded == content_original
    assert node.get_content() == content_original

    with node_loaded.open() as handle:
        assert handle.read().decode('UTF-8') == content_original

    assert node_loaded.get_content() == content_original
