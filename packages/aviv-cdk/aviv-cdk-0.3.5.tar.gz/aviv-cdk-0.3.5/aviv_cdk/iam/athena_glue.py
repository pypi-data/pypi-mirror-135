from aws_cdk import (
    aws_iam
)

def ReadPolicyDocument(account_id: str, database: str='*') -> aws_iam.PolicyDocument:
    athena = aws_iam.PolicyStatement(
        actions=[
            "athena:GetDatabase",
            "athena:GetDataCatalog",
            "athena:GetQueryExecution",
            "athena:GetQueryResults",
            "athena:GetTableMetadata",
            "athena:ListDatabases",
            "athena:ListQueryExecutions",
            "athena:ListTableMetadata",
            "athena:StartQueryExecution",
            "athena:StopQueryExecution",
        ],
        resources=[
            f"arn:aws:athena:*:{account_id}:datacatalog/{database}",
            f"arn:aws:athena:*:{account_id}:workgroup/primary"
        ],
        effect=aws_iam.Effect.ALLOW
    )
    glue = aws_iam.PolicyStatement(
        actions=[
            "glue:CreateTable",
            "glue:DeleteTable",
            "glue:GetDatabase*",
            "glue:GetPartitions",
            "glue:GetTable*"
        ],
        resources=[
            f"arn:aws:glue:*:{account_id}:database/{database}",
            f"arn:aws:glue:*:{account_id}:catalog"
        ],
        effect=aws_iam.Effect.ALLOW
    )
    return aws_iam.PolicyDocument(
        statements=[
            athena,
            glue,
            aws_iam.PolicyStatement(
                actions=[
                    "glue:*"
                ],
                resources=[
                    f"arn:aws:glue:*:{account_id}:table/*"
                ],
                effect=aws_iam.Effect.ALLOW
            )
        ]
    )
