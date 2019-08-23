# CompressedSinglefileData

[![Build Status](https://travis-ci.org/kjappelbaum/aiida-compressedsinglefiedata.svg?branch=master)](https://travis-ci.org/kjappelbaum/aiida-compressedsinglefiedata)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ae9aec36e3e448e5be30c9942a729bd8)](https://www.codacy.com/app/kjappelbaum/aiida-compressedsinglefiedata?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kjappelbaum/aiida-compressedsinglefiedata&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/kjappelbaum/aiida-compressedsinglefiedata/badge.svg?branch=master)](https://coveralls.io/github/kjappelbaum/aiida-compressedsinglefiedata?branch=master)

In development!

Somehow not really worth a plugin but can be useful in some cases.
Provides `CompressedSinglefileData` nodes which work like `SingleFileData`
except that they only take files (and not filelikes) and save the files
`zip` compressed.

This can be useful for larger simulation output files (like MD trajectories).
