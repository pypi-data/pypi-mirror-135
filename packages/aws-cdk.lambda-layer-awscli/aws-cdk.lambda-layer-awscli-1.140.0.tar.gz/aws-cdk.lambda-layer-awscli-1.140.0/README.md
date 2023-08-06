# AWS Lambda Layer with AWS CLI

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module exports a single class called `AwsCliLayer` which is a `lambda.Layer` that bundles the AWS CLI.

Usage:

```python
# AwsCliLayer bundles the AWS CLI in a lambda layer
from aws_cdk.lambda_layer_awscli import AwsCliLayer

# fn: lambda.Function

fn.add_layers(AwsCliLayer(self, "AwsCliLayer"))
```

The CLI will be installed under `/opt/awscli/aws`.
