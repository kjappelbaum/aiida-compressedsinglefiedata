# -*- coding: utf-8 -*-
"""Tests for the `CompressedSinglefileData` class."""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import tempfile
from aiida_compressedsinglefile import CompressedSinglefileData


def test_reload_singlefile_data(imp, aiida_profile):  # pylint:disable =unused-argument
    """Test writing and reloading a `CompressedSinglefileData` instance."""
    content_original = 'some text ABCDE'
    # load_node = imp
    with tempfile.NamedTemporaryFile(mode='w+') as handle:
        filepath = handle.name
        handle.write(content_original)
        handle.flush()
        node = CompressedSinglefileData(filepath=filepath)

    with node.open() as handle:
        content_written = handle.read().decode('UTF-8')

    assert content_written == content_original
    assert node.get_content() == content_original

    node.store()

    with node.open() as handle:
        content_stored = handle.read().decode('UTF-8')

    assert content_stored == content_original
    assert node.get_content() == content_original

    with node.open() as handle:
        content_loaded = handle.read().decode('UTF-8')

    assert content_loaded == content_original
    assert node.get_content() == content_original
