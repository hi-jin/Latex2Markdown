from __future__ import annotations
from description.ast import Description
from description.parser import parse
from typing import Tuple
import json


class Statement:
    def __init__(self, name: str, legend: Description, input: Description, output: Description, tests: Tuple[Test], tutorial: Description | None):
        self.name = name
        self.legend = legend
        self.input = input
        self.output = output
        self.tests = tests
        self.tutorial = tutorial

    @staticmethod
    def from_dict(d: dict) -> Statement:
        return Statement(
            d['name'],
            parse(d['legend']),
            parse(d['input']),
            parse(d['output']),
            tuple(Test.from_dict(test) for test in d['sampleTests']),
            parse(d['tutorial']) if d['tutorial'] else None
        )

    def __repr__(self) -> str:
        return json.dumps({
            'name': self.name,
            'legend': repr(self.legend),
            'input': repr(self.input),
            'output': repr(self.output),
            'sampleTests': tuple(test.to_dict() for test in self.tests),
            'tutorial': repr(self.tutorial)
        }, indent=4, ensure_ascii=False)


class Test:
    def __init__(self, input: str, output: str):
        self.input = input
        self.output = output

    @staticmethod
    def from_dict(d: dict) -> Test:
        return Test(d['input'].replace('\r\n', '\n'), d['output'].replace('\r\n', '\n'))

    def to_dict(self) -> dict:
        return {
            'input': self.input,
            'output': self.output
        }

    def __repr__(self) -> str:
        return json.dumps({
            'input': self.input,
            'output': self.output
        }, indent=4)

    def __iter__(self):
        return iter((self.input, self.output))
