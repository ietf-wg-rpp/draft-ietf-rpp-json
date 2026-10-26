# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 6 of 74 (case only: 0)

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
- required: draft=['@type', 'statements'] generated=['@type']
- `statements.maxItems`: draft=2 generated=null [prose constraint]
- `statements.minItems`: draft=1 generated=null

## `organisationRole` (draft line 1546) -> `organisationRole`

## `extension` (draft line 1572) -> `extension`

## `discoveryVersion` (draft line 1598) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1616) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1638) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1663) -> `discoveryNotice`

## `processes` (draft line 1683) -> `processes`

## `baseMessage` (draft line 1732) -> `baseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `reviewResponseMessage` (draft line 1754) -> `reviewResponseMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `transferRequestMessage` (draft line 1781) -> `transferRequestMessage`
- `process.$ref`: draft="transferProcess.read" generated="baseProcess"

## `transferOutcomeMessage` (draft line 1806) -> `transferOutcomeMessage`
- `process.$ref`: draft="transferProcess.read" generated="baseProcess"

## `expirationDeletionMessage` (draft line 1842) -> `expirationDeletionMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `autoRenewalMessage` (draft line 1865) -> `autoRenewalMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `serviceNoticeMessage` (draft line 1891) -> `serviceNoticeMessage`
- `process.$ref`: draft="<baseProcess>" generated="baseProcess"

## `maintenanceMessage` (draft line 1916) -> NO COUNTERPART

## `createProcess.create` (draft line 1951) -> `createProcess.create`
- properties only in draft: period

## `createProcess.read` (draft line 1970) -> `createProcess.read`
- properties only in draft: period
- properties only in generated: processId

## `renewProcess.create` (draft line 1991) -> `renewProcess.create`

## `renewProcess.read` (draft line 2011) -> `renewProcess.read`

## `transferProcess.create` (draft line 2036) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2080) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2153) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2184) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2203) -> `restoreProcess.read`

## `domainName.create` (draft line 2244) -> `domainName.create`
- `processes.properties.createProcess.items.$ref`: draft="<domainCreateProcess.create>" generated="domainCreateProcess.create"

## `domainName.read` (draft line 2301) -> `domainName.read`

## `domainName.update` (draft line 2355) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2399) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2415) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2458) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2521) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2535) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2549) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2568) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2584) -> `domainName.reference`

## `contact.create` (draft line 2620) -> `contact.create`
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.read` (draft line 2649) -> `contact.read`
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.update` (draft line 2680) -> `contact.update`
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `transferProcess.create.contact` (draft line 2708) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2724) -> `contact.reference`

## `host.create` (draft line 2752) -> `host.create`

## `host.read` (draft line 2779) -> `host.read`

## `host.reference` (draft line 2812) -> `host.reference`

## `organisation.create` (draft line 2842) -> `organisation.create`

## `organisation.read` (draft line 2897) -> `organisation.read`

## `organisation.update` (draft line 2954) -> `organisation.update`

## `organisation.reference` (draft line 3008) -> `organisation.reference`

## `message.create` (draft line 3035) -> `message.create`
- `data.$ref`: draft=null generated="baseMessage"
- `data.oneOf`: draft=["<maintenanceMessage>", "autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"] generated=null

## `message.read` (draft line 3068) -> `message.read`
- `data.$ref`: draft=null generated="baseMessage"
- `data.oneOf`: draft=["<maintenanceMessage>", "autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"] generated=null

## `message.query` (draft line 3104) -> `message.query`

## `message.reference` (draft line 3121) -> `message.reference`

## `userObject.create` (draft line 3148) -> `user.create`
- KEY MISMATCH (name): draft `userObject.create`, Rule 27 key `user.create`
- properties only in draft: organisationId
- properties only in generated: id
- required: draft=['@type', 'details', 'organisationId'] generated=['@type', 'details', 'id', 'status']
- `details.$ref`: draft="<contactObject.reference>" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"
- `description.const`: draft="user" generated=null [prose constraint]

## `userObject.read` (draft line 3178) -> `user.read`
- KEY MISMATCH (name): draft `userObject.read`, Rule 27 key `user.read`
- properties only in draft: userId
- properties only in generated: id, processes
- required: draft=['@type', 'details', 'status', 'userId'] generated=['@type', 'details', 'id', 'organisationId', 'status']
- `organisationId.$ref`: draft="<organisationObject.reference>" generated="organisation.reference"
- `organisationId.readOnly`: draft=null generated=true
- `details.$ref`: draft="<contactObject.reference>" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"
- `description.const`: draft="user" generated=null [prose constraint]

## `userObject.update` (draft line 3209) -> `user.update`
- KEY MISMATCH (name): draft `userObject.update`, Rule 27 key `user.update`
- properties only in generated: description
- required: draft=['@type'] generated=['@type', 'details', 'status']
- `details.$ref`: draft="<contactObject.reference>" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"

## `user.reference` (draft line 3237) -> `user.reference`

## `discovery.read` (draft line 3269) -> `discovery.read`

## `profile.read` (draft line 3352) -> `profile.read`

## `profile.reference` (draft line 3397) -> `profile.reference`

## Generated definitions without a draft counterpart

`disclose`, `baseProcess`, `restoreProcess.report`, `domainCreateProcess.create`, `domainCreateProcess.read`, `host.update`
