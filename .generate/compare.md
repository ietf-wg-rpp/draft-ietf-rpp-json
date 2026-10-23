# Comparison: generated schemas vs. draft-ietf-rpp-json

- DUPLICATE draft $defs name `transferProcess.reject.domain` (block at line 2362); the later one wins

## `identifier` (draft line 1000) -> `identifier`

## `clientIdentifier` (draft line 1018) -> `clientIdentifier`

## `phoneNumber` (draft line 1037) -> NO COUNTERPART

## `period` (draft line 1052) -> `period`
- `value.maximum`: draft=99 generated=null [prose constraint]
- `value.minimum`: draft=1 generated=null [prose constraint]
- `unit.enum`: draft=["y", "m"] generated=null [prose constraint]

## `provMetadata` (draft line 1083) -> `provMetadata`
- `repositoryId.$ref`: draft=null generated="identifier"
- `repositoryId.type`: draft="string" generated=null

## `status` (draft line 1112) -> NO COUNTERPART

## `dnsRecord` (draft line 1149) -> `dnsRecord`
- `rdata.additionalProperties`: draft=null generated=true
- `rdata.unevaluatedProperties`: draft=true generated=null

## `dnsControls` (draft line 1171) -> `dnsControls`
- `ttl.additionalProperties.minimum`: draft=1 generated=null [prose constraint]
- `ttl.propertyNames.pattern`: draft="^[a-z]+$" generated=null [prose constraint]
- `maxSigLifetime.additionalProperties.minimum`: draft=1 generated=null [prose constraint]
- `maxSigLifetime.propertyNames.pattern`: draft="^[a-z]+$" generated=null [prose constraint]

## `dnsData` (draft line 1207) -> `dnsData`

## `authInfo` (draft line 1233) -> `authInfo`

## `Card` (draft line 1259) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1361) -> `restoreReport`
- required: draft=['@type', 'statements'] generated=['@type']
- `statements.maxItems`: draft=2 generated=null [prose constraint]
- `statements.minItems`: draft=1 generated=null

## `organisationRole` (draft line 1393) -> `organisationRole`
- `status.items.$ref`: draft=null generated="organisationRoleStatus"
- `status.items.enum`: draft=["ok", "linked", "clientLinkProhibited", "serverLinkProhibited"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null

## `extension` (draft line 1422) -> `extension`

## `discoveryVersion` (draft line 1448) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1466) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1488) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1513) -> `discoveryNotice`

## `processes` (draft line 1533) -> `processes`
- `createProcess.items.$ref`: draft="createProcess.read" generated=null
- `createProcess.items.oneOf`: draft=null generated=["createProcess.read", "domainCreateProcess.read"]
- `transferProcess.items.$ref`: draft="transferProcess.read" generated=null
- `transferProcess.items.oneOf`: draft=null generated=["domainTransferProcess.read", "transferProcess.read"]

## `baseMessage` (draft line 1584) -> `baseMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null

## `reviewResponseMessage` (draft line 1613) -> `reviewResponseMessage`
- `@type.readOnly`: draft=true generated=null
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null
- `message.readOnly`: draft=true generated=null

## `transferRequestMessage` (draft line 1647) -> `transferRequestMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null
- `status.const`: draft="pending" generated=null [prose constraint]

## `transferOutcomeMessage` (draft line 1679) -> `transferOutcomeMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null
- `trStatus.enum`: draft=["clientApproved", "clientCancelled", "clientRejected", "serverApproved", "serverCancelled"] generated=null [prose constraint]

## `expirationDeletionMessage` (draft line 1717) -> `expirationDeletionMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null

## `autoRenewalMessage` (draft line 1747) -> `autoRenewalMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null

## `serviceNoticeMessage` (draft line 1780) -> `serviceNoticeMessage`
- `process.oneOf`: draft=null generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]
- `process.properties.@type.type`: draft="string" generated=null
- `process.properties.processId.type`: draft="string" generated=null
- `process.required`: draft=["@type", "processId"] generated=null
- `process.type`: draft="object" generated=null

## `maintenanceMessage` (draft line 1812) -> NO COUNTERPART

## `createProcess.create` (draft line 1847) -> `createProcess.create`
- properties only in draft: period

## `createProcess.read` (draft line 1866) -> `createProcess.read`
- properties only in draft: period
- properties only in generated: processId

## `renewProcess.create` (draft line 1887) -> `renewProcess.create`
- `expiryDate.writeOnly`: draft=null generated=true
- `renewalPeriod.writeOnly`: draft=null generated=true

## `renewProcess.read` (draft line 1907) -> `renewProcess.read`
- properties only in generated: processId, renewalPeriod

## `transferProcess.create` (draft line 1930) -> `transferProcess.create`
- draft structure: oneOf
- required: draft=['@type', 'transferDir'] generated=['@type']
- `transferDir.const`: draft="push" generated=null [prose constraint]
- `transferDir.writeOnly`: draft=null generated=true
- `gainingClientId.writeOnly`: draft=null generated=true

## `transferProcess.read` (draft line 1973) -> `transferProcess.read`
- properties only in generated: processId
- required: draft=['@type', 'actClientId', 'actionDate', 'reqClientId', 'requestDate', 'trStatus', 'transferDir'] generated=['@type', 'actClientId', 'actionDate', 'reqClientId', 'requestDate', 'trStatus']
- `trStatus.enum`: draft=["pending", "clientApproved", "clientCancelled", "clientRejected", "serverApproved", "serverCancelled"] generated=null [prose constraint]
- `transferDir.enum`: draft=["pull", "push"] generated=null [prose constraint]

## `transferProcess.reject` (draft line 2024) -> `transferProcess.reject`

## `restoreProcess.create` (draft line 2055) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2074) -> `restoreProcess.read`
- properties only in generated: processId
- `restoreStatus.enum`: draft=["pendingRestore", "restored", "rgpPendingDelete"] generated=null [prose constraint]

## `domainObject.create` (draft line 2114) -> `domainName.create`
- properties only in generated: status
- required: draft=['@type', 'name'] generated=['@type', 'name', 'status']
- `name.format`: draft=null generated="hostname"
- `processes.properties.createProcess.items.$ref`: draft="createProcess.create" generated="domainCreateProcess.create"
- `processes.properties.createProcess.maxItems`: draft=1 generated=null [prose constraint]

## `domainObject.read` (draft line 2167) -> `domainName.read`
- required: draft=['@type', 'name', 'provMetadata'] generated=['@type', 'name', 'provMetadata', 'status']
- `name.format`: draft=null generated="hostname"
- `provMetadata.readOnly`: draft=null generated=true
- `status.items.$ref`: draft="<status>" generated="domainStatus"
- `status.minItems`: draft=null generated=1
- `status.readOnly`: draft=true generated=null

## `domainObject.update` (draft line 2221) -> `domainName.update`
- properties only in generated: status
- required: draft=['@type'] generated=['@type', 'status']

## `renewProcess.create.domain` (draft line 2260) -> `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create
- `expiryDate.writeOnly`: draft=null generated=true
- `renewalPeriod.writeOnly`: draft=null generated=true

## `transferProcess.create.domain` (draft line 2276) -> `domainTransferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf
- draft structure: oneOf
- required: draft=['@type', 'transferDir'] generated=['@type']
- `@type.const`: draft="transferProcess" generated="domainTransferProcess" [@type value]
- `transferDir.const`: draft="push" generated=null [prose constraint]
- `transferDir.writeOnly`: draft=null generated=true
- `gainingClientId.writeOnly`: draft=null generated=true
- `transferPeriod.writeOnly`: draft=null generated=true

## `transferProcess.read.domain` (draft line 2297) -> `domainTransferProcess.read`
- draft structure: $ref alias -> transferProcess.read
- draft structure: allOf
- properties only in generated: processId, transferPeriod
- required: draft=['@type', 'actClientId', 'actionDate', 'reqClientId', 'requestDate', 'trStatus', 'transferDir'] generated=['@type', 'actClientId', 'actionDate', 'reqClientId', 'requestDate', 'trStatus']
- `@type.const`: draft="transferProcess" generated="domainTransferProcess" [@type value]
- `trStatus.enum`: draft=["pending", "clientApproved", "clientCancelled", "clientRejected", "serverApproved", "serverCancelled"] generated=null [prose constraint]
- `transferDir.enum`: draft=["pull", "push"] generated=null [prose constraint]

## `transferProcess.delete.domain` (draft line 2320) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read
- draft structure: $ref alias -> transferProcess.read.domain
- draft structure: allOf

## `transferProcess.approve.domain` (draft line 2334) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read
- draft structure: $ref alias -> transferProcess.read.domain
- draft structure: allOf

## `transferProcess.reject.domain` (draft line 2362) -> `domainTransferProcess.reject`
- draft structure: $ref alias -> transferProcess.read
- draft structure: $ref alias -> transferProcess.read.domain
- draft structure: allOf
- properties only in draft: trStatus, transferDir, gainingClientId, reqClientId, requestDate, actClientId, actionDate, expiryDate
- properties only in generated: reason
- required: draft=['@type', 'actClientId', 'actionDate', 'reqClientId', 'requestDate', 'trStatus', 'transferDir'] generated=['@type']
- `@type.const`: draft="transferProcess" generated="domainTransferProcess" [@type value]
- `@type.readOnly`: draft=true generated=null

## `domainObject.reference` (draft line 2378) -> `domainName.reference`
- `@type.readOnly`: draft=true generated=null
- `name.format`: draft=null generated="hostname"
- `name.readOnly`: draft=true generated=null

## `contactObject.create` (draft line 2414) -> `contact.create`
- draft structure: unevaluatedProperties: false
- properties only in generated: status, disclose
- required: draft=['@type', 'contactInfo', 'id'] generated=['@type', 'contactInfo', 'id', 'status']
- `id.$ref`: draft=null generated="identifier"
- `id.type`: draft="string" generated=null
- `id.writeOnly`: draft=null generated=true
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"

## `contactObject.read` (draft line 2438) -> `contact.read`
- draft structure: unevaluatedProperties: false
- properties only in generated: disclose, processes
- required: draft=['@type', 'contactInfo', 'id', 'provMetadata'] generated=['@type', 'contactInfo', 'id', 'provMetadata', 'status']
- `id.$ref`: draft=null generated="identifier"
- `id.type`: draft="string" generated=null
- `provMetadata.readOnly`: draft=null generated=true
- `status.items.$ref`: draft="<status>" generated="contactStatus"
- `status.minItems`: draft=null generated=1
- `status.readOnly`: draft=true generated=null
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"

## `contactObject.update` (draft line 2468) -> `contact.update`
- draft structure: unevaluatedProperties: false
- properties only in draft: processes
- properties only in generated: status, disclose
- required: draft=['@type', 'contactInfo'] generated=['@type', 'contactInfo', 'status']
- `contactInfo.$ref`: draft="Card" generated=null
- `contactInfo.items.$ref`: draft=null generated="Card"
- `contactInfo.maxItems`: draft=null generated=2
- `contactInfo.minItems`: draft=null generated=1
- `contactInfo.type`: draft=null generated="array"

## `transferProcess.create.contact` (draft line 2492) -> `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: oneOf
- required: draft=['@type', 'transferDir'] generated=['@type']
- `transferDir.const`: draft="push" generated=null [prose constraint]
- `transferDir.writeOnly`: draft=null generated=true
- `gainingClientId.writeOnly`: draft=null generated=true

## `contactObject.reference` (draft line 2508) -> `contact.reference`
- `@type.readOnly`: draft=true generated=null
- `id.$ref`: draft=null generated="identifier"
- `id.readOnly`: draft=true generated=null
- `id.type`: draft="string" generated=null

## `hostObject.create` (draft line 2536) -> `host.create`
- properties only in generated: status
- required: draft=['@type', 'hostName'] generated=['@type', 'hostName', 'status']

## `hostObject.read` (draft line 2558) -> `host.read`
- required: draft=['@type', 'hostName', 'provMetadata'] generated=['@type', 'hostName', 'provMetadata', 'status']
- `provMetadata.readOnly`: draft=null generated=true
- `status.items.$ref`: draft="<status>" generated="hostStatus"
- `status.minItems`: draft=null generated=1
- `status.readOnly`: draft=true generated=null

## `hostObject.reference` (draft line 2591) -> `host.reference`
- `@type.readOnly`: draft=true generated=null
- `hostName.readOnly`: draft=true generated=null

## `organisationObject.create` (draft line 2621) -> `organisation.create`
- properties only in generated: status, users
- required: draft=['@type', 'id', 'roles'] generated=['@type', 'id', 'roles', 'status']
- `id.writeOnly`: draft=null generated=true

## `organisationObject.read` (draft line 2660) -> `organisation.read`
- draft structure: $ref alias -> organisationObject.create
- draft structure: allOf
- properties only in generated: processes
- `@type.readOnly`: draft=null generated=true
- `id.readOnly`: draft=null generated=true
- `status.items.$ref`: draft="<status>" generated="organisationStatus"
- `status.minItems`: draft=null generated=1
- `status.readOnly`: draft=true generated=null

## `organisationObject.update` (draft line 2700) -> `organisation.update`
- required: draft=['@type'] generated=['@type', 'roles', 'status']
- `roles.minProperties`: draft=null generated=1
- `status.items.$ref`: draft="<status>" generated="organisationStatus"
- `status.minItems`: draft=null generated=1
- `status.readOnly`: draft=true generated=null

## `organisationObject.reference` (draft line 2753) -> `organisation.reference`
- `@type.readOnly`: draft=true generated=null
- `id.readOnly`: draft=true generated=null

## `messageObject.create` (draft line 2780) -> `message.create`
- `data.oneOf`: draft=["<maintenanceMessage>", "autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"] generated=["autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"]

## `messageObject.read` (draft line 2813) -> `message.read`
- `status.enum`: draft=["queued", "delivered", "removed"] generated=null [prose constraint]
- `data.oneOf`: draft=["<maintenanceMessage>", "autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"] generated=["autoRenewalMessage", "baseMessage", "expirationDeletionMessage", "reviewResponseMessage", "serviceNoticeMessage", "transferOutcomeMessage", "transferRequestMessage"]

## `messageObject.query` (draft line 2849) -> NO COUNTERPART

## `messageObject.reference` (draft line 2866) -> `message.reference`
- `@type.readOnly`: draft=true generated=null

## `userObject.create` (draft line 2893) -> `user.create`
- properties only in draft: organisationId
- properties only in generated: id
- required: draft=['@type', 'details', 'organisationId'] generated=['@type', 'details', 'id', 'status']
- `details.$ref`: draft="contact.reference" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"
- `description.const`: draft="user" generated=null [prose constraint]

## `userObject.read` (draft line 2923) -> `user.read`
- properties only in draft: userId
- properties only in generated: id, processes
- required: draft=['@type', 'details', 'status', 'userId'] generated=['@type', 'details', 'id', 'organisationId', 'status']
- `organisationId.readOnly`: draft=null generated=true
- `details.$ref`: draft="contact.reference" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"
- `description.const`: draft="user" generated=null [prose constraint]

## `userObject.update` (draft line 2954) -> `user.update`
- properties only in generated: description
- required: draft=['@type'] generated=['@type', 'details', 'status']
- `details.$ref`: draft="contact.reference" generated="Card"
- `status.items.enum`: draft=["active", "suspended", "deactivated", "pending"] generated=null [prose constraint]
- `status.items.type`: draft="string" generated=null
- `status.type`: draft="array" generated="string"

## `userObject.reference` (draft line 2982) -> `user.reference`
- `@type.readOnly`: draft=true generated=null
- `id.readOnly`: draft=true generated=null

## `discoveryObject.read` (draft line 3014) -> `discovery.read`
- `links.items.properties.object.format`: draft="uri" generated=null
- `links.items.properties.object.pattern`: draft="^https://" generated=null [prose constraint]

## `profileObject.read` (draft line 3097) -> `profile.read`
- `baseProfile.readOnly`: draft=null generated=true

## `profileObject.reference` (draft line 3134) -> `profile.reference`
- `@type.readOnly`: draft=true generated=null

## Generated definitions without a draft counterpart

`domainStatus`, `hostStatus`, `contactStatus`, `organisationRoleStatus`, `organisationStatus`, `disclose`, `baseProcess`, `restoreProcess.report`, `domainCreateProcess.create`, `domainCreateProcess.read`, `host.update`, `message.query`
