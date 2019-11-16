# awslambda
Basic set of classes for creating AWS lambda function


## Creating / using base lambda methods

Environment variables

```bash
PARAM1 = 'param1'
PARAM2 = 10
```

```python
from awslambda import LambdaBaseEnv


class LambdaBaseEnvImpl(LambdaBaseEnv):
    
    def __init__(self):
        super().__init__(
            {
                'PARAM1': str,
                'PARAM2': int
            }
        )

    def handle(self, event, context) -> dict:
        event.update({
            'param1': self.get_parameter('PARAM1', 'param1'),
            'param2': self.get_parameter('PARAM2', 10),
        })
        
        return event


lambda_handler = LambdaBaseEnvImpl().get_handler()

lambda_handler({'test': 'test'})

# returns {'test': 'test', 'param1': 'param1', 'param2': 10}
```
