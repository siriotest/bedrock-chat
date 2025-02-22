# Sett opp ekstern identitetsleverandør for Google

## Trinn 1: Opprett en Google OAuth 2.0-klient

1. Gå til Google Developer Console.
2. Opprett et nytt prosjekt eller velg et eksisterende.
3. Naviger til "Credentials", klikk deretter på "Create Credentials" og velg "OAuth client ID".
4. Konfigurer samtykkeskjermen hvis du blir bedt om det.
5. For applikasjonstype, velg "Web application".
6. La omstillingsadressen (redirect URI) stå tom foreløpig for å sette den senere. [Se Trinn 5](#step-5-update-google-oauth-client-with-cognito-redirect-uris)
7. Når den er opprettet, noter ned klient-ID og klienthemmelighet.

For detaljer, besøk [Googles offisielle dokument](https://support.google.com/cloud/answer/6158849?hl=en)

## Trinn 2: Lagre Google OAuth-legitimasjon i AWS Secrets Manager

1. Gå til AWS Management Console.
2. Naviger til Secrets Manager og velg "Store a new secret".
3. Velg "Other type of secrets".
4. Legg inn Google OAuth clientId og clientSecret som nøkkel-verdi-par.

   1. Nøkkel: clientId, Verdi: <YOUR_GOOGLE_CLIENT_ID>
   2. Nøkkel: clientSecret, Verdi: <YOUR_GOOGLE_CLIENT_SECRET>

5. Følg veiledningen for å navngi og beskrive hemmeligheten. Merk deg hemmelighetsnavnet, da du vil trenge det i din CDK-kode. For eksempel googleOAuthCredentials. (Brukes i Trinn 3 variabelnavn <YOUR_SECRET_NAME>)
6. Gjennomgå og lagre hemmeligheten.

### Merk

Nøkkelnavnene må eksakt samsvare med strengene 'clientId' og 'clientSecret'.

## Trinn 3: Oppdater cdk.json

I din cdk.json-fil, legg til ID-leverandøren og SecretName i cdk.json-filen.

som følger:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "google",
        "secretName": "<DIN_HEMMELIGE_NAVN>"
      }
    ],
    "userPoolDomainPrefix": "<UNIKT_DOMENE_PREFIKS_FOR_DIN_BRUKERGRUPPE>"
  }
}
```

### Oppmerksomhet

#### Unike navn

UserPoolDomainPrefix må være globalt unikt på tvers av alle Amazon Cognito-brukere. Hvis du velger et prefiks som allerede er i bruk av en annen AWS-konto, vil opprettelsen av brukergruppens domene mislykkes. Det er god praksis å inkludere identifikatorer, prosjektnavn eller miljønavn i prefikset for å sikre at det er unikt.

## Trinn 4: Distribuer CDK-stakken

Distribuer CDK-stakken til AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Trinn 5: Oppdater Google OAuth-klient med Cognito-omdirigerings-URI-er

Etter å ha distribuert stacken vil AuthApprovedRedirectURI vises i CloudFormation-resultatene. Gå tilbake til Google Developer Console og oppdater OAuth-klienten med de riktige omdirigerings-URI-ene.