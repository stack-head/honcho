import textwrap
from ..helpers import TestCase

from honcho.procfile import Procfile

FIXTURES = [
    [
        # Simple
        """
        web: command
        """,
        {'web': 'command'}
    ],
    [
        # Simple 2
        """
        foo: python foo.py
        bar: python bar.py
        """,
        {'foo': 'python foo.py', 'bar': 'python bar.py'}
    ],
    [
        # No newline at EOF
        """
        web: command""",
        {'web': 'command'}
    ],
    [
        # Comments
        """
        #commented: command
        """,
        {}
    ],
    [
        # Invalid characters
        """
        -foo: command
        """,
        {}
    ],
    [
        # Shell metacharacters
        """
        web: sh -c "echo $FOOBAR" >/dev/null 2>&1
        """,
        {'web': 'sh -c "echo $FOOBAR" >/dev/null 2>&1'}
    ],
]


class TestProcfiles(TestCase):

    def test_procfiles(self):
        for content, commands in FIXTURES:
            content = textwrap.dedent(content)
            procfile = Procfile(content)
            self.assertEqual(procfile.commands, commands)

    def test_procfile_ordered(self):
        content = textwrap.dedent("""
        one: onecommand
        two: twocommand
        three: twocommand
        four: fourcommand
        """)

        procfile = Procfile(content)

        order = [k for k in procfile.commands]
        self.assertEqual(['one', 'two', 'three', 'four'], order)