from dataclasses import dataclass
from typing import Literal, Union

Path = str


@dataclass
class AttributeAssignment:
    path: Path
    value: any


@dataclass
class AttributeComparison:
    path: Path
    operator: Literal['<'] | Literal['<='] | Literal['=='] | Literal['!='] | Literal['>'] | Literal['>=']
    value: any


@dataclass
class LogicalExpression:
    operator: Literal['AND'] | Literal['OR'] = 'AND'
    components: list['QueryComponent'] = None


QueryComponent = Union[AttributeAssignment, AttributeComparison, LogicalExpression]  # noqa: UP007

if __name__ == '__main__':

    def evaluate_query(component: QueryComponent):
        if isinstance(component, LogicalExpression):
            print(f'Evaluate {component.operator} of:')
            for sub_component in component.components:
                evaluate_query(sub_component)  # Recursively handle sub-components
        elif isinstance(component, AttributeAssignment):
            print(f'Set {component.path} to {component.value}')
        elif isinstance(component, AttributeComparison):
            print(f'Compare {component.path} {component.operator} with {component.value}')
        else:
            raise ValueError('Unsupported query component')


    print('Evaluating query component:')
    print('--------------------------')
    evaluate_query(LogicalExpression('AND', [
        AttributeComparison('age', '>=', 20),
        AttributeComparison('age', '<=', 30)
    ]))
