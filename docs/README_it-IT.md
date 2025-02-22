# Chat Bedrock Claude (Nova)

![](https://img.shields.io/github/v/release/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/license/aws-samples/bedrock-claude-chat?style=flat-square)
![](https://img.shields.io/github/actions/workflow/status/aws-samples/bedrock-claude-chat/cdk.yml?style=flat-square)
[![](https://img.shields.io/badge/roadmap-view-blue)](https://github.com/aws-samples/bedrock-claude-chat/issues?q=is%3Aissue%20state%3Aopen%20label%3Aroadmap)

[English](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/README.md) | [日本語](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ja-JP.md) | [한국어](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ko-KR.md) | [中文](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_zh-CN.md) | [Français](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_fr-FR.md) | [Deutsch](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_de-DE.md) | [Español](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_es-ES.md) | [Italian](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_it-IT.md) | [Norsk](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_nb-NO.md) | [ไทย](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_th-TH.md) | [Bahasa Indonesia](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_id-ID.md) | [Bahasa Melayu](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_ms-MY.md) | [Tiếng Việt](https://github.com/aws-samples/bedrock-claude-chat/blob/v2/docs/README_vi-VN.md)

> [!Warning]  
> **Rilasciata la versione V2. Per aggiornare, si prega di rivedere attentamente la [guida alla migrazione](./migration/V1_TO_V2_it-IT.md).** Senza alcuna attenzione, **I BOT DELLA VERSIONE V1 DIVENTERANNO INUTILIZZABILI.**

Un chatbot multilingua che utilizza modelli LLM forniti da [Amazon Bedrock](https://aws.amazon.com/bedrock/) per l'intelligenza artificiale generativa.

### Guarda Panoramica e Installazione su YouTube

[![Panoramica](https://img.youtube.com/vi/PDTGrHlaLCQ/hq1.jpg)](https://www.youtube.com/watch?v=PDTGrHlaLCQ)

### Conversazione di Base

![](./imgs/demo.gif)

### Personalizzazione del Bot

Aggiungi le tue istruzioni e fornisci conoscenze esterne tramite URL o file (noto come [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)). Il bot può essere condiviso tra gli utenti dell'applicazione. Il bot personalizzato può anche essere pubblicato come API autonoma (Vedi [dettagli](./PUBLISH_API_it-IT.md)).

![](./imgs/bot_creation.png)
![](./imgs/bot_chat.png)
![](./imgs/bot_api_publish_screenshot3.png)

> [!Important]
> Per ragioni di governance, solo gli utenti autorizzati possono creare bot personalizzati. Per consentire la creazione di bot personalizzati, l'utente deve essere un membro del gruppo chiamato `CreatingBotAllowed`, che può essere configurato tramite la console di gestione > Pool di utenti Amazon Cognito o aws cli. Si noti che l'ID del pool di utenti può essere consultato accedendo a CloudFormation > BedrockChatStack > Output > `AuthUserPoolIdxxxx`.

### Dashboard dell'Amministratore

<details>
<summary>Dashboard dell'Amministratore</summary>

Analizza l'utilizzo per ogni utente / bot nella dashboard dell'amministratore. [dettagli](./ADMINISTRATOR_it-IT.md)

![](./imgs/admin_bot_analytics.png)

</details>

### Agente basato su LLM

<details>
<summary>Agente basato su LLM</summary>

Utilizzando la [funzionalità Agente](./AGENT_it-IT.md), il tuo chatbot può gestire automaticamente attività più complesse. Ad esempio, per rispondere a una domanda di un utente, l'Agente può recuperare le informazioni necessarie da strumenti esterni o suddividere l'attività in più passaggi per l'elaborazione.

![](./imgs/agent1.png)
![](./imgs/agent2.png)

</details>

## 🚀 Distribuzione Super-Facile

- Nella regione us-east-1, aprire [Accesso al Modello Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) > `Gestisci accesso al modello` > Selezionare tutte le opzioni di `Anthropic / Claude 3`, tutte le opzioni di `Amazon / Nova`, `Amazon / Titan Text Embeddings V2` e `Cohere / Embed Multilingual`, quindi fare clic su `Salva modifiche`.

<details>
<summary>Screenshot</summary>

![](./imgs/model_screenshot.png)

</details>

- Aprire [CloudShell](https://console.aws.amazon.com/cloudshell/home) nella regione in cui si desidera eseguire la distribuzione
- Eseguire la distribuzione tramite i seguenti comandi. Se si desidera specificare la versione da distribuire o applicare criteri di sicurezza, specificare i parametri appropriati da [Parametri Facoltativi](#parametri-facoltativi).

```sh
git clone https://github.com/aws-samples/bedrock-claude-chat.git
cd bedrock-claude-chat
chmod +x bin.sh
./bin.sh
```

- Verrà chiesto se si tratta di un nuovo utente o se si sta utilizzando la versione 2. Se non si è un utente che continua dalla versione 0, inserire `y`.

### Parametri Facoltativi

È possibile specificare i seguenti parametri durante la distribuzione per migliorare la sicurezza e la personalizzazione:

- **--disable-self-register**: Disabilita la registrazione automatica (predefinito: abilitata). Se questo flag è impostato, sarà necessario creare tutti gli utenti su Cognito e non sarà consentita la registrazione autonoma degli account.
- **--enable-lambda-snapstart**: Abilita [Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) (predefinito: disabilitato). Se questo flag è impostato, migliora i tempi di avvio a freddo per le funzioni Lambda, fornendo tempi di risposta più rapidi per una migliore esperienza utente.
- **--ipv4-ranges**: Elenco separato da virgole di intervalli IPv4 consentiti. (predefinito: consente tutti gli indirizzi ipv4)
- **--ipv6-ranges**: Elenco separato da virgole di intervalli IPv6 consentiti. (predefinito: consente tutti gli indirizzi ipv6)
- **--disable-ipv6**: Disabilita le connessioni su IPv6. (predefinito: abilitato)
- **--allowed-signup-email-domains**: Elenco separato da virgole di domini di posta elettronica consentiti per la registrazione. (predefinito: nessuna restrizione di dominio)
- **--bedrock-region**: Definisce la regione in cui Bedrock è disponibile. (predefinito: us-east-1)
- **--repo-url**: L'URL del repository personalizzato di Bedrock Claude Chat da distribuire, se biforcato o con un controllo del codice sorgente personalizzato. (predefinito: https://github.com/aws-samples/bedrock-claude-chat.git)
- **--version**: La versione di Bedrock Claude Chat da distribuire. (predefinito: ultima versione in sviluppo)
- **--cdk-json-override**: È possibile sovrascrivere qualsiasi valore di contesto CDK durante la distribuzione utilizzando il blocco JSON di override. Questo consente di modificare la configurazione senza modificare direttamente il file cdk.json.

Esempio di utilizzo:

```bash
./bin.sh --cdk-json-override '{
  "context": {
    "selfSignUpEnabled": false,
    "enableLambdaSnapStart": true,
    "allowedIpV4AddressRanges": ["192.168.1.0/24"],
    "allowedSignUpEmailDomains": ["example.com"]
  }
}'
```

Il JSON di override deve seguire la stessa struttura di cdk.json. È possibile sovrascrivere qualsiasi valore di contesto tra cui:

- `selfSignUpEnabled`
- `enableLambdaSnapStart`
- `allowedIpV4AddressRanges`
- `allowedIpV6AddressRanges`
- `allowedSignUpEmailDomains`
- `bedrockRegion`
- `enableRagReplicas`
- `enableBedrockCrossRegionInference`
- E altri valori di contesto definiti in cdk.json

> [!Nota]
> I valori di override verranno uniti alla configurazione cdk.json esistente durante il tempo di distribuzione in AWS code build. I valori specificati nell'override avranno la precedenza sui valori in cdk.json.

#### Esempio di comando con parametri:

```sh
./bin.sh --disable-self-register --ipv4-ranges "192.0.2.0/25,192.0.2.128/25" --ipv6-ranges "2001:db8:1:2::/64,2001:db8:1:3::/64" --allowed-signup-email-domains "example.com,anotherexample.com" --bedrock-region "us-west-2" --version "v1.2.6"
```

- Dopo circa 35 minuti, si otterrà l'output seguente, a cui è possibile accedere dal proprio browser

```
URL Frontend: https://xxxxxxxxx.cloudfront.net
```

![](./imgs/signin.png)

Verrà visualizzata la schermata di registrazione come mostrato sopra, dove è possibile registrare la propria email e accedere.

> [!Importante]
> Senza impostare il parametro facoltativo, questo metodo di distribuzione consente a chiunque conosca l'URL di registrarsi. Per l'uso in produzione, è fortemente consigliato aggiungere restrizioni degli indirizzi IP e disabilitare la registrazione automatica per mitigare i rischi di sicurezza (è possibile definire allowed-signup-email-domains per limitare gli utenti in modo che solo gli indirizzi email del dominio della propria azienda possano registrarsi). Utilizzare sia ipv4-ranges che ipv6-ranges per le restrizioni degli indirizzi IP e disabilitare la registrazione automatica utilizzando disable-self-register durante l'esecuzione di ./bin.

> [!SUGGERIMENTO]
> Se l'`URL Frontend` non appare o Bedrock Claude Chat non funziona correttamente, potrebbe esserci un problema con l'ultima versione. In questo caso, aggiungere `--version "v1.2.6"` ai parametri e riprovare la distribuzione.

## Architettura

Un'architettura basata su servizi gestiti AWS, che elimina la necessità di gestire l'infrastruttura. Utilizzando Amazon Bedrock, non è necessario comunicare con API esterne ad AWS. Questo consente di distribuire applicazioni scalabili, affidabili e sicure.

- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/): Database NoSQL per l'archiviazione della cronologia delle conversazioni
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/) + [AWS Lambda](https://aws.amazon.com/lambda/): Endpoint API backend ([AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter), [FastAPI](https://fastapi.tiangolo.com/))
- [Amazon CloudFront](https://aws.amazon.com/cloudfront/) + [S3](https://aws.amazon.com/s3/): Distribuzione dell'applicazione frontend ([React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/))
- [AWS WAF](https://aws.amazon.com/waf/): Restrizione degli indirizzi IP
- [Amazon Cognito](https://aws.amazon.com/cognito/): Autenticazione utente
- [Amazon Bedrock](https://aws.amazon.com/bedrock/): Servizio gestito per utilizzare modelli foundational tramite API
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/): Fornisce un'interfaccia gestita per la Generazione Aumentata dal Recupero ([RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)), offrendo servizi per l'embedding e l'analisi dei documenti
- [Amazon EventBridge Pipes](https://aws.amazon.com/eventbridge/pipes/): Ricezione di eventi dal flusso DynamoDB e avvio di Step Functions per l'embedding di conoscenze esterne
- [AWS Step Functions](https://aws.amazon.com/step-functions/): Orchestrazione della pipeline di acquisizione per l'embedding di conoscenze esterne in Bedrock Knowledge Bases
- [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/features/serverless/): Funge da database backend per Bedrock Knowledge Bases, fornendo funzionalità di ricerca full-text e ricerca vettoriale, consentendo il recupero accurato di informazioni rilevanti
- [Amazon Athena](https://aws.amazon.com/athena/): Servizio di query per analizzare bucket S3

![](./imgs/arch.png)

## Distribuzione tramite CDK

La distribuzione Super-facile utilizza [AWS CodeBuild](https://aws.amazon.com/codebuild/) per eseguire la distribuzione tramite CDK internamente. Questa sezione descrive la procedura per la distribuzione diretta con CDK.

- Assicurati di avere UNIX, Docker e un ambiente di runtime Node.js. In caso contrario, puoi utilizzare [Cloud9](https://github.com/aws-samples/cloud9-setup-for-prototyping)

> [!Importante]
> Se lo spazio di archiviazione nell'ambiente locale è insufficiente durante la distribuzione, il bootstrap di CDK potrebbe generare un errore. Se si sta eseguendo su Cloud9 ecc., si consiglia di espandere la dimensione del volume dell'istanza prima della distribuzione.

- Clonare questo repository

```
git clone https://github.com/aws-samples/bedrock-claude-chat
```

- Installare i pacchetti npm

```
cd bedrock-claude-chat
cd cdk
npm ci
```

- Se necessario, modificare le seguenti voci in [cdk.json](./cdk/cdk.json)

  - `bedrockRegion`: Regione in cui Bedrock è disponibile. **NOTA: Bedrock NON supporta ancora tutte le regioni.**
  - `allowedIpV4AddressRanges`, `allowedIpV6AddressRanges`: Intervallo di indirizzi IP consentiti.
  - `enableLambdaSnapStart`: Per impostazione predefinita è true. Impostare su false se si distribuisce in una [regione che non supporta Lambda SnapStart per funzioni Python](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions).

- Prima di distribuire CDK, è necessario eseguire il bootstrap una volta per la regione in cui si sta distribuendo.

```
npx cdk bootstrap
```

- Distribuire questo progetto di esempio

```
npx cdk deploy --require-approval never --all
```

- Otterrai un output simile al seguente. L'URL dell'app web verrà visualizzato in `BedrockChatStack.FrontendURL`, quindi accedervi tramite browser.

```sh
 ✅  BedrockChatStack

✨  Deployment time: 78.57s

Outputs:
BedrockChatStack.AuthUserPoolClientIdXXXXX = xxxxxxx
BedrockChatStack.AuthUserPoolIdXXXXXX = ap-northeast-1_XXXX
BedrockChatStack.BackendApiBackendApiUrlXXXXX = https://xxxxx.execute-api.ap-northeast-1.amazonaws.com
BedrockChatStack.FrontendURL = https://xxxxx.cloudfront.net
```

## Altri

### Configurare il supporto per i modelli Mistral

Aggiorna `enableMistral` a `true` in [cdk.json](./cdk/cdk.json), e esegui `npx cdk deploy`.

```json
...
  "enableMistral": true,
```

> [!Importante]
> Questo progetto si concentra sui modelli Anthropic Claude, i modelli Mistral sono supportati in modo limitato. Ad esempio, gli esempi di prompt sono basati sui modelli Claude. Questa è un'opzione solo per Mistral, una volta abilitati i modelli Mistral, potrai utilizzare solo i modelli Mistral per tutte le funzionalità di chat, NON sia Claude che Mistral.

### Configurare la generazione di testo predefinita

Gli utenti possono regolare i [parametri di generazione del testo](https://docs.anthropic.com/claude/reference/complete_post) dalla schermata di creazione del bot personalizzato. Se il bot non viene utilizzato, verranno utilizzati i parametri predefiniti impostati in [config.py](./backend/app/config.py).

```py
DEFAULT_GENERATION_CONFIG = {
    "max_tokens": 2000,
    "top_k": 250,
    "top_p": 0.999,
    "temperature": 0.6,
    "stop_sequences": ["Human: ", "Assistant: "],
}
```

### Rimuovere le risorse

Se utilizzi cli e CDK, esegui `npx cdk destroy`. Altrimenti, accedi a [CloudFormation](https://console.aws.amazon.com/cloudformation/home) e poi elimina manualmente `BedrockChatStack` e `FrontendWafStack`. Nota che `FrontendWafStack` si trova nella regione `us-east-1`.

### Impostazioni Lingua

Questa risorsa rileva automaticamente la lingua utilizzando [i18next-browser-languageDetector](https://github.com/i18next/i18next-browser-languageDetector). Puoi cambiare lingua dal menu dell'applicazione. In alternativa, puoi utilizzare la Stringa di Query per impostare la lingua come mostrato di seguito.

> `https://example.com?lng=ja`

### Disabilitare la registrazione autonoma

Questo esempio ha la registrazione autonoma abilitata per impostazione predefinita. Per disabilitare la registrazione autonoma, apri [cdk.json](./cdk/cdk.json) e imposta `selfSignUpEnabled` su `false`. Se configuri un [provider di identità esterno](#external-identity-provider), il valore verrà ignorato e disabilitato automaticamente.

### Limitare i Domini per gli Indirizzi Email di Registrazione

Per impostazione predefinita, questo esempio non limita i domini per gli indirizzi email di registrazione. Per consentire la registrazione solo da domini specifici, apri `cdk.json` e specifica i domini come elenco in `allowedSignUpEmailDomains`.

```ts
"allowedSignUpEmailDomains": ["example.com"],
```

### Provider di Identità Esterno

Questo esempio supporta provider di identità esterno. Attualmente supportiamo [Google](./idp/SET_UP_GOOGLE_it-IT.md) e [provider OIDC personalizzato](./idp/SET_UP_CUSTOM_OIDC_it-IT.md).

### Aggiungere nuovi utenti ai gruppi automaticamente

Questo esempio ha i seguenti gruppi per dare autorizzazioni agli utenti:

- [`Admin`](./ADMINISTRATOR_it-IT.md)
- [`CreatingBotAllowed`](#bot-personalization)
- [`PublishAllowed`](./PUBLISH_API_it-IT.md)

Se vuoi che i nuovi utenti si uniscano automaticamente ai gruppi, puoi specificarli in [cdk.json](./cdk/cdk.json).

```json
"autoJoinUserGroups": ["CreatingBotAllowed"],
```

Per impostazione predefinita, i nuovi utenti verranno aggiunti al gruppo `CreatingBotAllowed`.

### Configurare Repliche RAG

`enableRagReplicas` è un'opzione in [cdk.json](./cdk/cdk.json) che controlla le impostazioni delle repliche per il database RAG, specificamente le Knowledge Bases che utilizzano Amazon OpenSearch Serverless.

- **Predefinito**: true
- **true**: Migliora la disponibilità abilitando repliche aggiuntive, adatto per ambienti di produzione ma aumentando i costi.
- **false**: Riduce i costi utilizzando meno repliche, adatto per sviluppo e test.

Questa è un'impostazione a livello di account/regione che interessa l'intera applicazione piuttosto che singoli bot.

> [!Nota]
> A giugno 2024, Amazon OpenSearch Serverless supporta 0,5 OCU, abbassando i costi di ingresso per carichi di lavoro su piccola scala. Le distribuzioni di produzione possono iniziare con 2 OCU, mentre i carichi di lavoro di sviluppo/test possono utilizzare 1 OCU. OpenSearch Serverless si scala automaticamente in base alle richieste di lavoro. Per maggiori dettagli, visita [annuncio](https://aws.amazon.com/jp/about-aws/whats-new/2024/06/amazon-opensearch-serverless-entry-cost-half-collection-types/).

### Inferenza tra regioni

L'[inferenza tra regioni](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) consente ad Amazon Bedrock di instradare dinamicamente le richieste di inferenza del modello tra più regioni AWS, migliorando la velocità effettiva e la resilienza durante i periodi di picco della domanda. Per configurare, modifica `cdk.json`.

```json
"enableBedrockCrossRegionInference": true
```

### Lambda SnapStart

[Lambda SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html) migliora i tempi di avvio a freddo per le funzioni Lambda, fornendo tempi di risposta più veloci per una migliore esperienza utente. D'altra parte, per le funzioni Python, c'è un [addebito in base alle dimensioni della cache](https://aws.amazon.com/lambda/pricing/#SnapStart_Pricing) e [non disponibile in alcune regioni](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html#snapstart-supported-regions) attualmente. Per disabilitare SnapStart, modifica `cdk.json`.

```json
"enableLambdaSnapStart": false
```

### Configurare Dominio Personalizzato

Puoi configurare un dominio personalizzato per la distribuzione CloudFront impostando i seguenti parametri in [cdk.json](./cdk/cdk.json):

```json
{
  "alternateDomainName": "chat.example.com",
  "hostedZoneId": "Z0123456789ABCDEF"
}
```

- `alternateDomainName`: Il nome di dominio personalizzato per la tua applicazione di chat (es. chat.example.com)
- `hostedZoneId`: L'ID della zona ospitata Route 53 in cui verranno create i record DNS

Quando questi parametri vengono forniti, la distribuzione eseguirà automaticamente:

- Creare un certificato ACM con convalida DNS nella regione us-east-1
- Creare i record DNS necessari nella tua zona Route 53
- Configurare CloudFront per utilizzare il tuo dominio personalizzato

> [!Nota]
> Il dominio deve essere gestito da Route 53 nel tuo account AWS. L'ID della zona ospitata può essere trovato nella console Route 53.

### Sviluppo Locale

Vedi [SVILUPPO LOCALE](./LOCAL_DEVELOPMENT_it-IT.md).

### Contributo

Grazie per aver considerato di contribuire a questo repository! Accogliamo con favore correzioni di bug, traduzioni linguistiche (i18n), miglioramenti delle funzionalità, [strumenti agente](./docs/AGENT.md#how-to-develop-your-own-tools) e altri miglioramenti.

Per i miglioramenti delle funzionalità e altri miglioramenti, **prima di creare una Pull Request, apprezzeremmo molto che tu crei un Issue di Richiesta Funzionalità per discutere l'approccio e i dettagli dell'implementazione. Per correzioni di bug e traduzioni linguistiche (i18n), procedi direttamente con la creazione di una Pull Request.**

Dai un'occhiata anche alle seguenti linee guida prima di contribuire:

- [Sviluppo Locale](./LOCAL_DEVELOPMENT_it-IT.md)
- [CONTRIBUIRE](./CONTRIBUTING_it-IT.md)

## Contatti

- [Takehiro Suzuki](https://github.com/statefb)
- [Yusuke Wada](https://github.com/wadabee)
- [Yukinobu Mine](https://github.com/Yukinobu-Mine)

## 🏆 Contributori Significativi

- [k70suK3-k06a7ash1](https://github.com/k70suK3-k06a7ash1)
- [fsatsuki](https://github.com/fsatsuki)

## Contributori

[![contributori di bedrock claude chat](https://contrib.rocks/image?repo=aws-samples/bedrock-claude-chat&max=1000)](https://github.com/aws-samples/bedrock-claude-chat/graphs/contributors)

## Licenza

Questa libreria è licenziata sotto la Licenza MIT-0. Consulta [il file LICENSE](./LICENSE).