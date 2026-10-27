# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 81 (case only: 0)

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

## `disclose` (draft line 1426) -> `disclose`

## `Card` (draft line 1450) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1552) -> `restoreReport`

## `organisationRole` (draft line 1584) -> `organisationRole`

## `extension` (draft line 1610) -> `extension`

## `discoveryVersion` (draft line 1636) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1654) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1676) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1701) -> `discoveryNotice`

## `processes` (draft line 1721) -> `processes`

## `baseMessage` (draft line 1770) -> `baseMessage`

## `reviewResponseMessage` (draft line 1789) -> `reviewResponseMessage`

## `transferRequestMessage` (draft line 1813) -> `transferRequestMessage`

## `transferOutcomeMessage` (draft line 1835) -> `transferOutcomeMessage`

## `expirationDeletionMessage` (draft line 1868) -> `expirationDeletionMessage`

## `autoRenewalMessage` (draft line 1888) -> `autoRenewalMessage`

## `serviceNoticeMessage` (draft line 1911) -> `serviceNoticeMessage`

## `maintenanceMessage` (draft line 1933) -> NO COUNTERPART

## `baseProcess` (draft line 1964) -> `baseProcess`
- properties only in generated: processId

## `createProcess.create` (draft line 1984) -> `createProcess.create`

## `createProcess.read` (draft line 2002) -> `createProcess.read`

## `renewProcess.create` (draft line 2023) -> `renewProcess.create`

## `renewProcess.read` (draft line 2043) -> `renewProcess.read`

## `transferProcess.create` (draft line 2068) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2112) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2185) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2216) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2235) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2262) -> `restoreProcess.report`
- properties only in generated: restoreReport
- required: draft=['@type'] generated=['@type', 'restoreReport']

## `domainName.create` (draft line 2294) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2351) -> `domainCreateProcess.create`
- properties only in generated: period

## `domainCreateProcess.read` (draft line 2369) -> `domainCreateProcess.read`
- properties only in generated: processId, period

## `domainName.read` (draft line 2389) -> `domainName.read`

## `domainName.update` (draft line 2443) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2487) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2503) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2546) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2609) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2623) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2637) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2656) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2672) -> `domainName.reference`

## `contact.create` (draft line 2708) -> `contact.create`

## `contact.read` (draft line 2737) -> `contact.read`

## `contact.update` (draft line 2768) -> `contact.update`

## `transferProcess.create.contact` (draft line 2796) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2812) -> `contact.reference`

## `host.create` (draft line 2840) -> `host.create`

## `host.read` (draft line 2867) -> `host.read`

## `host.update` (draft line 2896) -> `host.update`
- properties only in generated: hostName, status, dns
- required: draft=['@type'] generated=['@type', 'hostName', 'status']

## `host.reference` (draft line 2916) -> `host.reference`

## `organisation.create` (draft line 2946) -> `organisation.create`

## `organisation.read` (draft line 3001) -> `organisation.read`

## `organisation.update` (draft line 3058) -> `organisation.update`

## `organisation.reference` (draft line 3112) -> `organisation.reference`

## `message.create` (draft line 3139) -> `message.create`

## `message.read` (draft line 3160) -> `message.read`

## `message.query` (draft line 3184) -> `message.query`

## `message.reference` (draft line 3201) -> `message.reference`

## `user.create` (draft line 3229) -> `user.create`

## `user.read` (draft line 3253) -> `user.read`

## `user.update` (draft line 3279) -> `user.update`

## `user.reference` (draft line 3302) -> `user.reference`

## `discovery.read` (draft line 3334) -> `discovery.read`

## `profile.read` (draft line 3417) -> `profile.read`

## `profile.reference` (draft line 3462) -> `profile.reference`

## Generated definitions without a draft counterpart

(none)
