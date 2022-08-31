class ConditionContext(object):
    def __init__(self, variables):
        self.variables = variables

    def get_variable_value(self, var_name):
        attr_lst = var_name.split(".")
        cur = self.variables
        for attr in attr_lst:
            if hasattr(cur, attr):
                cur = getattr(cur, attr)
            elif isinstance(cur, dict) and cur.get(attr) is not None:
                cur = cur.get(attr)
            else:
                return None

        return cur
