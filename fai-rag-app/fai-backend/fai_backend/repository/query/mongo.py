from dataclasses import dataclass

from fai_backend.repository.query import AttributeAssignment, AttributeComparison, LogicalExpression, QueryComponent


class QueryAdapter:
    def to_mongo_query(self):
        raise NotImplementedError('Must implement to_mongo_query')


@dataclass
class AttributeAssignmentAdapter(QueryAdapter):
    component: AttributeAssignment

    def to_mongo_query(self):
        # MongoDB uses $set for updates; for a find query, simple equality is assumed
        return {self.component.path: self.component.value}


@dataclass
class AttributeComparisonAdapter(QueryAdapter):
    component: AttributeComparison

    def to_mongo_query(self):
        # MongoDB specific operator map
        operator_map = {
            '<': '$lt',
            '<=': '$lte',
            '==': '$eq',
            '!=': '$ne',
            '>': '$gt',
            '>=': '$gte'
        }
        mongo_operator = operator_map[self.component.operator]
        return {self.component.path: {mongo_operator: self.component.value}}


@dataclass
class LogicalExpressionAdapter(QueryAdapter):
    component: LogicalExpression

    def to_mongo_query(self):
        logical_operator_map = {
            'AND': '$and',
            'OR': '$or'
        }
        return {
            logical_operator_map[self.component.operator]: [adapt_query_component(sub_component).to_mongo_query() for
                                                            sub_component in self.component.components]}


def adapt_query_component(component: QueryComponent) -> QueryAdapter:
    if isinstance(component, AttributeAssignment):
        return AttributeAssignmentAdapter(component)
    elif isinstance(component, AttributeComparison):
        return AttributeComparisonAdapter(component)
    elif isinstance(component, LogicalExpression):
        return LogicalExpressionAdapter(component)
    else:
        raise ValueError('Unsupported query component type')
