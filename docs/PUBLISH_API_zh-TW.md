# API 發佈

## 概觀

此範例包含發佈 API 的功能。雖然聊天介面可以方便進行初步驗證，但實際實作取決於特定使用案例和為終端使用者設計的使用者體驗（UX）。在某些情況下，聊天使用者介面可能是首選，而在其他情況下，獨立 API 可能更為合適。在初步驗證之後，此範例提供根據專案需求發佈自訂機器人的能力。通過設定配額、流量限制、來源等設定，可以發佈端點並提供 API 金鑰，為不同的整合選項提供靈活性。

## 安全性

僅使用 API 金鑰並不建議，詳情請參見：[AWS API Gateway 開發人員指南](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)。因此，此範例透過 AWS WAF 實作了簡單的 IP 位址限制。基於成本考量，WAF 規則通常會套用於整個應用程式，假設需要限制的來源可能在所有已發行的 API 中大致相同。**請遵循您組織的安全性政策進行實際實作。**另請參閱[架構](#architecture)章節。

## 如何發佈自訂機器人 API

### 先決條件

出於治理原因，只有有限的使用者能夠發佈機器人。在發佈之前，使用者必須是名為 `PublishAllowed` 的群組成員，該群組可以透過管理主控台 > Amazon Cognito 使用者池或 AWS CLI 設定。請注意，使用者池 ID 可以透過存取 CloudFormation > BedrockChatStack > 輸出 > `AuthUserPoolIdxxxx` 來參考。

![](./imgs/group_membership_publish_allowed.png)

### API 發佈設定

以 `PublishedAllowed` 使用者登入並建立機器人後，選擇 `API 發佈設定`。請注意，只有共享機器人可以發佈。
![](./imgs/bot_api_publish_screenshot.png)

在下面的畫面中，我們可以設定有關節流的多個參數。詳細資訊，請參閱：[節流 API 請求以提高輸送量](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)。
![](./imgs/bot_api_publish_screenshot2.png)

部署後，將出現以下畫面，您可以在此取得端點 URL 和 API 金鑰。我們還可以新增和刪除 API 金鑰。

![](./imgs/bot_api_publish_screenshot3.png)

## 架構

API 按照以下圖表發佈：

![](./imgs/published_arch.png)

WAF 用於 IP 地址限制。可以通過在 `cdk.json` 中設置參數 `publishedApiAllowedIpV4AddressRanges` 和 `publishedApiAllowedIpV6AddressRanges` 來配置地址。

當用戶點擊發佈機器人時，[AWS CodeBuild](https://aws.amazon.com/codebuild/) 會啟動 CDK 部署任務，以佈建 API 堆疊（另請參見：[CDK 定義](../cdk/lib/api-publishment-stack.ts)），該堆疊包含 API Gateway、Lambda 和 SQS。SQS 用於解耦用戶請求和 LLM 操作，因為生成輸出可能超過 30 秒，這是 API Gateway 配額的限制。要獲取輸出，需要異步訪問 API。更多詳細信息，請參見 [API 規範](#api-specification)。

客戶端需要在請求標頭中設置 `x-api-key`。

## API 規格

請查看[此處](https://aws-samples.github.io/bedrock-claude-chat)。