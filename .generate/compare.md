# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 80 (case only: 0)

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

## `baseMessage` (draft line 1774) -> `baseMessage`

## `reviewResponseMessage` (draft line 1792) -> `reviewResponseMessage`

## `transferRequestMessage` (draft line 1816) -> `transferRequestMessage`

## `transferOutcomeMessage` (draft line 1838) -> `transferOutcomeMessage`

## `expirationDeletionMessage` (draft line 1871) -> `expirationDeletionMessage`

## `autoRenewalMessage` (draft line 1890) -> `autoRenewalMessage`

## `serviceNoticeMessage` (draft line 1912) -> `serviceNoticeMessage`

## `baseProcess` (draft line 1939) -> `baseProcess`

## `createProcess.create` (draft line 1960) -> `createProcess.create`

## `createProcess.read` (draft line 1978) -> `createProcess.read`

## `renewProcess.create` (draft line 1999) -> `renewProcess.create`

## `renewProcess.read` (draft line 2019) -> `renewProcess.read`

## `transferProcess.create` (draft line 2044) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2088) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2161) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2192) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2211) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2241) -> NO COUNTERPART

## `domainName.create` (draft line 2274) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2333) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2352) -> `domainCreateProcess.read`

## `domainName.read` (draft line 2374) -> `domainName.read`

## `domainName.update` (draft line 2428) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2472) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2488) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2531) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2594) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2608) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2622) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2641) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2657) -> `domainName.reference`

## `contact.create` (draft line 2693) -> `contact.create`

## `contact.read` (draft line 2722) -> `contact.read`

## `contact.update` (draft line 2753) -> `contact.update`

## `transferProcess.create.contact` (draft line 2781) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2797) -> `contact.reference`

## `host.create` (draft line 2825) -> `host.create`

## `host.read` (draft line 2852) -> `host.read`

## `host.update` (draft line 2881) -> `host.update`

## `host.reference` (draft line 2908) -> `host.reference`

## `organisation.create` (draft line 2938) -> `organisation.create`

## `organisation.read` (draft line 2993) -> `organisation.read`

## `organisation.update` (draft line 3050) -> `organisation.update`

## `organisation.reference` (draft line 3104) -> `organisation.reference`

## `message.create` (draft line 3131) -> `message.create`

## `message.read` (draft line 3152) -> `message.read`

## `message.query` (draft line 3176) -> `message.query`

## `message.reference` (draft line 3193) -> `message.reference`

## `user.create` (draft line 3221) -> `user.create`

## `user.read` (draft line 3245) -> `user.read`

## `user.update` (draft line 3271) -> `user.update`

## `user.reference` (draft line 3294) -> `user.reference`

## `discovery.read` (draft line 3326) -> `discovery.read`

## `profile.read` (draft line 3409) -> `profile.read`

## `profile.reference` (draft line 3454) -> `profile.reference`

## Generated definitions without a draft counterpart

`restoreProcess.update`
