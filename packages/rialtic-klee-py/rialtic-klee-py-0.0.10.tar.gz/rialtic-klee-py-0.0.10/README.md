# Rialtic Klee Overview

This library should serve to replace our loose scripts `build_test_cases.python`, `test_engine.python`, `smoke_test.python` in almost all cases.

_You are still able to write an interim scripts using library calls, 
when new engines create yet unaddressed requirements. 
However, this should be kept to a minimum._

## The Command Line Utility
This library provides a command line utility in order to conduct local tests (with automatic building), and remote (smoke) tests.
- `klee build [<optional_test_cases>]`
- `klee test [<optional_test_cases>]`
- `klee smoke [<optional_test_cases>]`

note: could we perhaps reconcile the diverged logic of SPEs/MPEs?

## The Library API

### File: `klee.build`

##### Command: `klee build [<optional_test_cases>]`
With the following arguments,
- `-p <plan-type>`, default: `'default'`
- `-c <claims-dir>`, default: `'test_claims'`
- `-o <output-dir>`, default: `test_cases`

It will output `InsightEngineTestCase` objects to `<output_dir>/json_cases`, 
and `HistoryClaim` arrays to `<output_dir>/history`.

### File: `klee.plans`

##### Class Interface
```python
class <LegacyTestPlan|MPETestPlan>(EngineTestPlan):
  def __init__(self, claims_dir = 'test_claims', output_dir = '', history_dir = ''):
    ...
  def build_all_cases(self) -> Dict[str, InsightEngineTestCase]:
    ...
  def build_test_case(self, node: Union[str, KleeTestClaim]) -> InsightEngineTestCase:
    ...
  def build_node_labels(self, node_labels: List[str]) -> Dict[str, InsightEngineTestCase]:
    ...
```

### File: `klee.test`

##### Command: `klee test [<optional_test_cases>]`
With the following arguments,
- `-p <plan_type>`, default: `'default'`
- `-c <claims_dir>`, default: `'test_claims'`
- `-o <output-dir>`, default: `test_cases`
- `--pytest="..."`, default: `'-vvv'`

##### Class Interface
```python
class LocalTest(PyTestUtility):
    def __init__(self, args: Iterable[str] = tuple()):
        ...        
    def invoke_cases(self, test_cases: Dict[str, InsightEngineTestCase]):
        ...
```

##### Command: `klee smoke [<optional_test_cases>]`
With the following arguments,
- `-p <plan_type>`, default: `'default'`
- `-c <claims_dir>`, default: `'test_claims'`
- `-o <output-dir>`, default: `'test_cases'`
- `--pytest="..."`, default: `'-vvv'`

##### Class Interface
```python
class SmokeTest(PyTestUtility):
    def __init__(self, args: Iterable[str] = tuple()):
        ...        
    def invoke_cases(self, test_cases: Dict[str, InsightEngineTestCase]):
        ...
```

# Library Structure

## Supported Test Plan Formats

### File: `klee.plans.*`
Exposes
```python
class MPETestPlan(EngineTestPlan):
    pass

class LegacyTestPlan(EngineTestPlan):
    pass

class EngineTestPlan(TestCaseBuilder):
    def claim_line(self, claim: KleeTestClaim) -> int:
        ...
    def get_history(self, claim: KleeTestClaim) -> List[HistoryClaim]:
        ...
    def get_defense(self, case: InsightEngineTestCase) -> str:
        ...
    def validate_case(self, case: InsightEngineTestCase) -> bool:
        ...
```

## Supported Test Claims Formats

### File: `klee.claims`
Exposes
```python
class ClaimsDirectory:
    ...

class KleeTestClaim:
    ...

```

[Test Claim/Tab Naming Conventions](http://community.rialtic.io/docs/spec/test_claims/)

## Supported Insight/Defenses Formats

### File: `klee.insights`
Exposes
```python
class InsightDict(dict):
    ...
class InsightText:
    ...

def load_insights() -> InsightDict:
    ...
def read_engine_result() -> InsightDict:
    ...
def read_local_files() -> InsightDict:
    ...
```

Flow:
- `result.EngineResult.insight_<type|text|defense>` > `<insights_and_defenses|insights|defense>.csv` > `<insights|defense>.json` > `test_plan.csv + test_dataset.csv ???`

## Library File Utils

### File: `klee.files`
Exposes
```python
class KleeFile:
    ...

class Inspection:
    ...

def save_json(data, target):
   ...

def read_claim(target) -> Claim:
    ...

def read_json(target) -> Dict[Any, Any]:
    ...

def read_str(target) -> str:
    ...

def read_csv(target, normalize = False, **kwargs):
    ...

def fhir_to_json(obj: domainresource.DomainResource) -> Dict:
    ...
```

### File: `klee.internal`
Exposes
```python
class Structure:    
    root_dir: str
    claim_dir: str
    output_dir: str

    internal: str
    reports: str
    logs:str

    history: str
    binary: str

    search: str
    timestamp: int
    json_enabled: bool
```

## Mass Testing
We could potentially create a [Github Action](https://docs.github.com/en/actions) to test (by a yet to be decided trigger) against a range of engine repos.

## Versioning
As the design of this library evolves over time, engines will be written depending on certain assumptions made by this test suite. To address these,  we will be using semantic versioning (https://semver.org/).
If features/tests are removed, it should be considered a **major** breaking change.
If features/tests are added, it should be considered a **minor** api change.
If there is a bug introduced, a bugfix **patch** should be released.

In the format of `v<MAJOR>.<MINOR>.<PATCH>`, which can be used with Pipenv's compatibility operator to accept all non breaking changes as `rialtic-klee-python ~= <MAJOR>.<MINOR>`.

## Repository Branches
Branches:
- `development` serves as our development/specification discussion head
- `v<MAJOR>.<MINOR>` should be used for retroactive fixes

Tags:
- `v<MAJOR>.<MINOR>.<PATCH>` for each release

<hr>

![ships in the dark](ships_in_the_dark.jpg)
