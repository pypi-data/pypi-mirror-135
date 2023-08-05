# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relational_stream']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.5,<7.0.0']

entry_points = \
{'console_scripts': ['amt = apple_music_tools.main:app']}

setup_kwargs = {
    'name': 'relational-stream',
    'version': '0.4.0',
    'description': 'A Python library for relational stream analysis.',
    'long_description': '# Python Relational Stream Analysis\nA Python (3.9+) library for relational stream analysis. Define sequences ("flows") of events, each of which may depend on a previous event in the flow, and collect all such flows from a stream. This is particularly useful for analyzing network captures, as after identifying a certain flow of events (e.g. a series of network requests used to authenticate a user), this library can be used to easily filter out all such flows from a larger capture. This is highly resilient to extraneous requests occurring in the middle of long-running flows, so it can easily be used to target individual applications within complete network captures from system-wide MITM attacks.\n\n## Example\n\nIt can be a bit hard to wrap your head around what this library does just from a written description, so let\'s take a look at a code example. The following shows a class which can be used to analyze a stream of strings, filtering out sequences with a predefined format. However, the included classes are fully generic, so a similar `Flow` could easily be created for a stream of HTTP requests.\n\n```python\nimport re\nfrom typing import Optional\n\nfrom relational_stream import Flow, RelationalStream\n\nclass SomeStringFlow(Flow[str]):\n    """\n    Simple flow example to identify a sequence of strings using regex. This flow will match a series\n    of the events in the form::\n\n        "start A"\n        "A -> B or C"\n        "B" OR "C"\n    """\n\n    first_char: Optional[str] = None\n    second_char_options: Optional[set[str]] = None\n    second_char_choice: Optional[str] = None\n\n    EVENT_REGEXES = [\n        r"start (\\w)",\n        r"(\\w) -> (\\w) or (\\w)",\n        r"(\\w)",\n    ]\n\n    def is_next_event(self, event: str) -> bool:\n        if len(self.events) == 0:\n            match = re.match(self.EVENT_REGEXES[0], event)\n            if match is None:\n                return False\n            self.first_char = match[1]\n            return True\n\n        elif len(self.events) == 1:\n            match = re.match(self.EVENT_REGEXES[1], event)\n            if match is None or match[1] != self.first_char:\n                return False\n            self.second_char_options = {match[2], match[3]}\n            return True\n\n        else:  # len(self.events) == 2\n            assert self.second_char_options is not None\n            match = re.match(self.EVENT_REGEXES[2], event)\n            if match is None or match[1] not in self.second_char_options:\n                return False\n            self.second_char_choice = match[1]\n            return True\n\n    def is_complete(self) -> bool:\n        return len(self.events) == 3\n\n\nstream = RelationalStream([SomeStringFlow])\n\nstream.ingest("start A")\nstream.ingest("B")\nstream.ingest("A -> B or C")\nstream.ingest("A -> D or E")\nstream.ingest("B")\n\n# len(stream.incomplete_flows(SomeStringFlow)) == 0\n# len(stream.completed_flows(SomeStringFlow)) == 1\n# stream.completed_flows(SomeStringFlow)[0].first_char == "A"\n# stream.completed_flows(SomeStringFlow)[0].second_char_options == {"B", "C"}\n# stream.completed_flows(SomeStringFlow)[0].second_char_choice == "B"\n```\n\nAs you can see, the addition of extraneous data in the middle of the stream has no effect on the completed flows. A need for this resilience when developing tools to analyze network captures was the primary motivation for developing this library.\n\n\n## Installation\n\n```\npip3 install relational-stream\n```\n',
    'author': 'Stephan Lensky',
    'author_email': 'stephanl.public@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephanlensky/python-relational-stream-analysis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
