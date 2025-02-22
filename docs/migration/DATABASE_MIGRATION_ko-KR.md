# 데이터베이스 마이그레이션 가이드

본 가이드는 Aurora 클러스터 교체를 포함하는 Bedrock Claude Chat의 업데이트를 수행할 때 데이터를 마이그레이션하는 단계를 설명합니다. 다음 절차는 다운타임과 데이터 손실을 최소화하면서 원활한 전환을 보장합니다.

## 개요

마이그레이션 프로세스에는 모든 봇을 스캔하고 각 봇에 대한 임베딩 ECS 작업을 시작하는 작업이 포함됩니다. 이 접근 방식은 임베딩을 다시 계산해야 하므로 시간이 오래 걸리고 ECS 작업 실행 및 Bedrock Cohere 사용 요금으로 인해 추가 비용이 발생할 수 있습니다. 이러한 비용과 시간 요구 사항을 피하고 싶다면 이 가이드의 뒷부분에 제공된 [대체 마이그레이션 옵션](#alternative-migration-options)을 참조하세요.

## 마이그레이션 단계

- [npx cdk deploy](../README.md#deploy-using-cdk)로 Aurora 대체 후, [migrate.py](./migrate.py) 스크립트를 열고 다음 변수를 적절한 값으로 업데이트하세요. 값은 `CloudFormation` > `BedrockChatStack` > `출력` 탭에서 참조할 수 있습니다.

```py
# AWS Management Console에서 CloudFormation 스택을 열고 출력 탭에서 값을 복사하세요.
# 키: DatabaseConversationTableNameXXXX
TABLE_NAME = "BedrockChatStack-DatabaseConversationTableXXXXX"
# 키: EmbeddingClusterNameXXX
CLUSTER_NAME = "BedrockChatStack-EmbeddingClusterXXXXX"
# 키: EmbeddingTaskDefinitionNameXXX
TASK_DEFINITION_NAME = "BedrockChatStackEmbeddingTaskDefinitionXXXXX"
CONTAINER_NAME = "Container"  # 변경할 필요 없음
# 키: PrivateSubnetId0
SUBNET_ID = "subnet-xxxxx"
# 키: EmbeddingTaskSecurityGroupIdXXX
SECURITY_GROUP_ID = "sg-xxxx"  # BedrockChatStack-EmbeddingTaskSecurityGroupXXXXX
```

- 마이그레이션 프로세스를 시작하려면 `migrate.py` 스크립트를 실행하세요. 이 스크립트는 모든 봇을 스캔하고, 임베딩 ECS 작업을 시작하며, 새 Aurora 클러스터에 데이터를 생성합니다. 다음 사항에 유의하세요:
  - 스크립트에는 `boto3`가 필요합니다.
  - 환경에는 DynamoDB 테이블에 액세스하고 ECS 작업을 호출할 수 있는 IAM 권한이 필요합니다.

## 대체 마이그레이션 옵션

시간과 비용 측면에서 위의 방법을 선호하지 않는 경우, 다음과 같은 대체 접근 방식을 고려해 보세요:

### 스냅샷 복원 및 DMS 마이그레이션

먼저 현재 Aurora 클러스터에 접근하기 위한 비밀번호를 확인하세요. 그런 다음 `npx cdk deploy`를 실행하여 클러스터를 대체합니다. 그 후, 원본 데이터베이스의 스냅샷을 복원하여 임시 데이터베이스를 생성합니다.
[AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)를 사용하여 임시 데이터베이스에서 새 Aurora 클러스터로 데이터를 마이그레이션합니다.

참고: 2024년 5월 29일 현재, DMS는 pgvector 확장을 기본적으로 지원하지 않습니다. 그러나 이 제한을 해결하기 위한 다음 옵션을 탐색할 수 있습니다:

[DMS 동종 마이그레이션](https://docs.aws.amazon.com/dms/latest/userguide/dm-migrating-data.html)을 사용하여 네이티브 논리적 복제를 활용합니다. 이 경우 소스와 대상 데이터베이스 모두 PostgreSQL이어야 합니다. DMS는 이를 위해 네이티브 논리적 복제를 활용할 수 있습니다.

프로젝트의 특정 요구 사항과 제약 조건을 고려하여 가장 적합한 마이그레이션 접근 방식을 선택하세요.