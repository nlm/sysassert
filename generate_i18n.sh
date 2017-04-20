#!/bin/sh
find sysassert -name "*.py" | xgettext -f - -d sysassert
echo "update sysassert.po and run 'msgfmt sysassert.po'"
