# Sett opp ekstern identitetsleverandør

## Trinn 1: Opprett en OIDC-klient

Følg prosedyrene for den aktuelle OIDC-leverandøren, og noter verdiene for OIDC-klient-ID og hemmelighet. Utsteder-URL er også nødvendig i de påfølgende trinnene. Hvis en omdirigerings-URI kreves under oppsettet, kan du angi en midlertidig verdi som vil bli erstattet etter at distribusjonen er fullført.

## Trinn 2: Lagre Legitimasjon i AWS Secrets Manager

1. Gå til AWS Management Console.
2. Naviger til Secrets Manager og velg "Store a new secret".
3. Velg "Other type of secrets".
4. Legg inn klient-ID og klient-hemmelighet som nøkkel-verdi-par.

   - Nøkkel: `clientId`, Verdi: <YOUR_GOOGLE_CLIENT_ID>
   - Nøkkel: `clientSecret`, Verdi: <YOUR_GOOGLE_CLIENT_SECRET>
   - Nøkkel: `issuerUrl`, Verdi: <ISSUER_URL_OF_THE_PROVIDER>

5. Følg instruksjonene for å navngi og beskrive hemmeligheten. Merk deg hemmelighetens navn, da du vil trenge dette i din CDK-kode (Brukt i Trinn 3 variabelnavn <YOUR_SECRET_NAME>).
6. Gjennomgå og lagre hemmeligheten.

### Merk

Nøkkelnavnene må nøyaktig samsvare med strengene `clientId`, `clientSecret` og `issuerUrl`.

## Trinn 3: Oppdater cdk.json

I cdk.json-filen legger du til ID-leverandøren og hemmelighetsnavnet i cdk.json-filen.

som følger:

```json
{
  "context": {
    // ...
    "identityProviders": [
      {
        "service": "oidc", // Ikke endre
        "serviceName": "<DIN_TJENESTENAVN>", // Sett en verdi du liker
        "secretName": "<DITT_HEMMELIGHETSNAVN>"
      }
    ],
    "userPoolDomainPrefix": "<UNIKT_DOMENEPREFIX_FOR_DIN_BRUKERGRUPPE>"
  }
}
```

### Merk

#### Unikthet

`userPoolDomainPrefix` må være globalt unikt på tvers av alle Amazon Cognito-brukere. Hvis du velger et prefiks som allerede er i bruk av en annen AWS-konto, vil opprettelsen av brukergruppens domene mislykkes. Det er god praksis å inkludere identifikatorer, prosjektnavn eller miljønavn i prefikset for å sikre unikthet.

## Trinn 4: Distribuer CDK-stakken din

Distribuer CDK-stakken din til AWS:

```sh
npx cdk deploy --require-approval never --all
```

## Trinn 5: Oppdater OIDC-klient med Cognito Redirect URI-er

Etter at stabelen er distribuert, vil `AuthApprovedRedirectURI` vises i CloudFormation-resultatene. Gå tilbake til OIDC-konfigurasjonen din og oppdater med de riktige redirect URI-ene.