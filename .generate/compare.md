# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 74 (case only: 0)

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

## `dnsRecord` (draft line 1306) -> `dnsRecord`

## `dnsControls` (draft line 1328) -> `dnsControls`

## `dnsData` (draft line 1360) -> `dnsData`

## `authInfo` (draft line 1386) -> `authInfo`

## `Card` (draft line 1412) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1514) -> `restoreReport`

## `organisationRole` (draft line 1546) -> `organisationRole`

## `extension` (draft line 1572) -> `extension`

## `discoveryVersion` (draft line 1598) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1616) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1638) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1663) -> `discoveryNotice`

## `processes` (draft line 1683) -> `processes`

## `baseMessage` (draft line 1732) -> `baseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `reviewResponseMessage` (draft line 1751) -> `reviewResponseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `transferRequestMessage` (draft line 1775) -> `transferRequestMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `transferOutcomeMessage` (draft line 1797) -> `transferOutcomeMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `expirationDeletionMessage` (draft line 1830) -> `expirationDeletionMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `autoRenewalMessage` (draft line 1850) -> `autoRenewalMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `serviceNoticeMessage` (draft line 1873) -> `serviceNoticeMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `maintenanceMessage` (draft line 1895) -> NO COUNTERPART

## `createProcess.create` (draft line 1930) -> `createProcess.create`

## `createProcess.read` (draft line 1948) -> `createProcess.read`
- properties only in draft: period
- properties only in generated: processId

## `renewProcess.create` (draft line 1969) -> `renewProcess.create`

## `renewProcess.read` (draft line 1989) -> `renewProcess.read`

## `transferProcess.create` (draft line 2014) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2058) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2131) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2162) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2181) -> `restoreProcess.read`

## `domainName.create` (draft line 2222) -> `domainName.create`
- `processes.properties.createProcess.items.$ref`: draft="<domainCreateProcess.create>" generated="domainCreateProcess.create"

## `domainName.read` (draft line 2279) -> `domainName.read`

## `domainName.update` (draft line 2333) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2377) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2393) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2436) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2499) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2513) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2527) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2546) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2562) -> `domainName.reference`

## `contact.create` (draft line 2598) -> `contact.create`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.read` (draft line 2627) -> `contact.read`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.update` (draft line 2658) -> `contact.update`
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `transferProcess.create.contact` (draft line 2686) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2702) -> `contact.reference`

## `host.create` (draft line 2730) -> `host.create`

## `host.read` (draft line 2757) -> `host.read`

## `host.reference` (draft line 2790) -> `host.reference`

## `organisation.create` (draft line 2820) -> `organisation.create`

## `organisation.read` (draft line 2875) -> `organisation.read`

## `organisation.update` (draft line 2932) -> `organisation.update`

## `organisation.reference` (draft line 2986) -> `organisation.reference`

## `message.create` (draft line 3013) -> `message.create`

## `message.read` (draft line 3034) -> `message.read`

## `message.query` (draft line 3058) -> `message.query`

## `message.reference` (draft line 3075) -> `message.reference`

## `user.create` (draft line 3102) -> `user.create`
- `status.$ref`: draft=null generated="userStatus"
- `status.type`: draft="string" generated=null

## `user.read` (draft line 3126) -> `user.read`
- properties only in draft: organisationId, userId
- properties only in generated: id, organisation, processes
- required: draft=['@type', 'details', 'id', 'organisationId', 'status'] generated=['@type', 'details', 'id', 'organisation', 'status']
- `details.$ref`: draft="<contactObject.reference>" generated="Card"
- `status.$ref`: draft=null generated="userStatus"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated=null
- `description.const`: draft="user" generated=null [prose constraint]

## `user.update` (draft line 3157) -> `user.update`
- properties only in generated: description
- required: draft=['@type'] generated=['@type', 'details', 'status']
- `details.$ref`: draft="<contactObject.reference>" generated="Card"
- `status.$ref`: draft=null generated="userStatus"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated=null

## `user.reference` (draft line 3185) -> `user.reference`

## `discovery.read` (draft line 3217) -> `discovery.read`

## `profile.read` (draft line 3300) -> `profile.read`

## `profile.reference` (draft line 3345) -> `profile.reference`

## Generated definitions without a draft counterpart

`userStatus`, `disclose`, `baseProcess`, `restoreProcess.report`, `domainCreateProcess.create`, `domainCreateProcess.read`, `host.update`
