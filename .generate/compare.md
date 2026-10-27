# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 75 (case only: 0)

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

## `userStatus` (draft line 1293) -> `userStatus`
- properties only in generated: @type, label, reason
- required: draft=[] generated=['@type', 'label']

## `dnsRecord` (draft line 1317) -> `dnsRecord`

## `dnsControls` (draft line 1339) -> `dnsControls`

## `dnsData` (draft line 1371) -> `dnsData`

## `authInfo` (draft line 1397) -> `authInfo`

## `Card` (draft line 1423) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1525) -> `restoreReport`

## `organisationRole` (draft line 1557) -> `organisationRole`

## `extension` (draft line 1583) -> `extension`

## `discoveryVersion` (draft line 1609) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1627) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1649) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1674) -> `discoveryNotice`

## `processes` (draft line 1694) -> `processes`

## `baseMessage` (draft line 1743) -> `baseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `reviewResponseMessage` (draft line 1762) -> `reviewResponseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `transferRequestMessage` (draft line 1786) -> `transferRequestMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `transferOutcomeMessage` (draft line 1808) -> `transferOutcomeMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `expirationDeletionMessage` (draft line 1841) -> `expirationDeletionMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `autoRenewalMessage` (draft line 1861) -> `autoRenewalMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `serviceNoticeMessage` (draft line 1884) -> `serviceNoticeMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `maintenanceMessage` (draft line 1906) -> NO COUNTERPART

## `createProcess.create` (draft line 1941) -> `createProcess.create`

## `createProcess.read` (draft line 1959) -> `createProcess.read`
- properties only in draft: period
- properties only in generated: processId

## `renewProcess.create` (draft line 1980) -> `renewProcess.create`

## `renewProcess.read` (draft line 2000) -> `renewProcess.read`

## `transferProcess.create` (draft line 2025) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2069) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2142) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2173) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2192) -> `restoreProcess.read`

## `domainName.create` (draft line 2233) -> `domainName.create`
- `processes.properties.createProcess.items.$ref`: draft="<domainCreateProcess.create>" generated="domainCreateProcess.create"

## `domainName.read` (draft line 2290) -> `domainName.read`

## `domainName.update` (draft line 2344) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2388) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2404) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2447) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2510) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2524) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2538) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2557) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2573) -> `domainName.reference`

## `contact.create` (draft line 2609) -> `contact.create`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.read` (draft line 2638) -> `contact.read`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.update` (draft line 2669) -> `contact.update`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `transferProcess.create.contact` (draft line 2697) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2713) -> `contact.reference`

## `host.create` (draft line 2741) -> `host.create`

## `host.read` (draft line 2768) -> `host.read`

## `host.reference` (draft line 2801) -> `host.reference`

## `organisation.create` (draft line 2831) -> `organisation.create`

## `organisation.read` (draft line 2886) -> `organisation.read`

## `organisation.update` (draft line 2943) -> `organisation.update`

## `organisation.reference` (draft line 2997) -> `organisation.reference`

## `message.create` (draft line 3024) -> `message.create`

## `message.read` (draft line 3045) -> `message.read`

## `message.query` (draft line 3069) -> `message.query`

## `message.reference` (draft line 3086) -> `message.reference`

## `user.create` (draft line 3111) -> `user.create`

## `user.read` (draft line 3135) -> `user.read`

## `user.update` (draft line 3161) -> `user.update`

## `user.reference` (draft line 3184) -> `user.reference`

## `discovery.read` (draft line 3216) -> `discovery.read`

## `profile.read` (draft line 3299) -> `profile.read`

## `profile.reference` (draft line 3344) -> `profile.reference`

## Generated definitions without a draft counterpart

`disclose`, `baseProcess`, `restoreProcess.report`, `domainCreateProcess.create`, `domainCreateProcess.read`, `host.update`
