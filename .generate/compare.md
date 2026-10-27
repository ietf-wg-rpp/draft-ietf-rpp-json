# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 86 (case only: 0)

## `identifier` (draft line 1000) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1018) -> `clientIdentifier`

## `phoneNumber` (draft line 1037) -> `phoneNumber`

## `period` (draft line 1049) -> `period`

## `provMetadata` (draft line 1073) -> `provMetadata`

## `domainStatus` (draft line 1114) -> `domainStatus`

## `hostStatus` (draft line 1161) -> `hostStatus`

## `contactStatus` (draft line 1193) -> `contactStatus`

## `organisationRoleStatus` (draft line 1227) -> `organisationRoleStatus`

## `organisationStatus` (draft line 1253) -> `organisationStatus`

## `userStatus` (draft line 1292) -> `userStatus`

## `dnsRecord` (draft line 1328) -> `dnsRecord`

## `dnsControls` (draft line 1350) -> `dnsControls`

## `dnsData` (draft line 1382) -> `dnsData`

## `authInfo` (draft line 1408) -> `authInfo`

## `disclose` (draft line 1430) -> `disclose`

## `Card` (draft line 1454) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1556) -> `restoreReport`

## `organisationRole` (draft line 1588) -> `organisationRole`

## `extension` (draft line 1614) -> `extension`

## `discoveryVersion` (draft line 1640) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1658) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1680) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1705) -> `discoveryNotice`

## `processes` (draft line 1725) -> `processes`
- `transferProcess.items.oneOf`: draft=["domainTransferProcess.read", "transferProcess.read"] generated=["domainTransferProcess.reference", "transferProcess.reference"]
- `renewProcess.items.$ref`: draft="renewProcess.read" generated="renewProcess.reference"
- `restoreProcess.items.$ref`: draft="restoreProcess.read" generated="restoreProcess.reference"
- `createProcess.items.oneOf`: draft=["createProcess.read", "domainCreateProcess.read"] generated=["createProcess.reference", "domainCreateProcess.reference"]

## `baseMessage` (draft line 1784) -> `baseMessage`

## `reviewResponseMessage` (draft line 1802) -> `reviewResponseMessage`

## `transferRequestMessage` (draft line 1837) -> `transferRequestMessage`

## `transferOutcomeMessage` (draft line 1865) -> `transferOutcomeMessage`

## `expirationDeletionMessage` (draft line 1904) -> `expirationDeletionMessage`

## `autoRenewalMessage` (draft line 1923) -> `autoRenewalMessage`

## `serviceNoticeMessage` (draft line 1945) -> `serviceNoticeMessage`

## `baseProcess` (draft line 1972) -> `baseProcess`

## `createProcess.create` (draft line 1993) -> `createProcess.create`

## `createProcess.read` (draft line 2011) -> `createProcess.read`

## `createProcess.reference` (draft line 2030) -> `createProcess.reference`

## `renewProcess.create` (draft line 2051) -> `renewProcess.create`

## `renewProcess.read` (draft line 2071) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2092) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2115) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2159) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2232) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2255) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2284) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2303) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2333) -> NO COUNTERPART

## `restoreProcess.reference` (draft line 2353) -> `restoreProcess.reference`

## `domainName.create` (draft line 2385) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2444) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2463) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2483) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2504) -> `domainName.read`

## `domainName.update` (draft line 2558) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2602) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2618) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2661) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2724) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2738) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2752) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2771) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainTransferProcess.reference` (draft line 2785) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 2806) -> `domainName.reference`

## `contact.create` (draft line 2842) -> `contact.create`

## `contact.read` (draft line 2871) -> `contact.read`

## `contact.update` (draft line 2902) -> `contact.update`

## `transferProcess.create.contact` (draft line 2930) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2946) -> `contact.reference`

## `host.create` (draft line 2974) -> `host.create`

## `host.read` (draft line 3001) -> `host.read`

## `host.update` (draft line 3030) -> `host.update`

## `host.reference` (draft line 3057) -> `host.reference`

## `organisation.create` (draft line 3087) -> `organisation.create`

## `organisation.read` (draft line 3142) -> `organisation.read`

## `organisation.update` (draft line 3199) -> `organisation.update`

## `organisation.reference` (draft line 3253) -> `organisation.reference`

## `message.create` (draft line 3280) -> `message.create`

## `message.read` (draft line 3312) -> `message.read`

## `message.query` (draft line 3347) -> `message.query`

## `message.reference` (draft line 3364) -> `message.reference`

## `user.create` (draft line 3392) -> `user.create`

## `user.read` (draft line 3416) -> `user.read`

## `user.update` (draft line 3442) -> `user.update`

## `user.reference` (draft line 3465) -> `user.reference`

## `discovery.read` (draft line 3497) -> `discovery.read`

## `profile.read` (draft line 3580) -> `profile.read`

## `profile.reference` (draft line 3625) -> `profile.reference`

## Generated definitions without a draft counterpart

`restoreProcess.update`
