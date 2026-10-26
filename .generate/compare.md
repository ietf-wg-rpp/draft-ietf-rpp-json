# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 70 (case only: 0)

## `identifier` (draft line 1000) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1018) -> `clientIdentifier`

## `phoneNumber` (draft line 1037) -> `phoneNumber`

## `period` (draft line 1049) -> `period`

## `provMetadata` (draft line 1073) -> `provMetadata`

## `status` (draft line 1102) -> NO COUNTERPART

## `dnsRecord` (draft line 1139) -> `dnsRecord`

## `dnsControls` (draft line 1161) -> `dnsControls`

## `dnsData` (draft line 1193) -> `dnsData`

## `authInfo` (draft line 1219) -> `authInfo`

## `Card` (draft line 1245) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1347) -> `restoreReport`

## `organisationRole` (draft line 1377) -> `organisationRole`
- `status.items.$ref`: draft="<organisationRoleStatus>" generated="organisationRoleStatus"

## `extension` (draft line 1403) -> `extension`

## `discoveryVersion` (draft line 1429) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1447) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1469) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1494) -> `discoveryNotice`

## `processes` (draft line 1514) -> `processes`
- `createProcess.items.oneOf`: draft=["<domainCreateProcess.read>", "createProcess.read"] generated=["createProcess.read", "domainCreateProcess.read"]

## `baseMessage` (draft line 1573) -> `baseMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `reviewResponseMessage` (draft line 1603) -> `reviewResponseMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `transferRequestMessage` (draft line 1638) -> `transferRequestMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `transferOutcomeMessage` (draft line 1671) -> `transferOutcomeMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `expirationDeletionMessage` (draft line 1715) -> `expirationDeletionMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `autoRenewalMessage` (draft line 1746) -> `autoRenewalMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `serviceNoticeMessage` (draft line 1780) -> `serviceNoticeMessage`
- `process.oneOf`: draft=["<baseProcess>", "<domainCreateProcess.read>", "createProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"] generated=["baseProcess", "createProcess.read", "domainCreateProcess.read", "domainTransferProcess.read", "renewProcess.read", "restoreProcess.read", "transferProcess.read"]

## `maintenanceMessage` (draft line 1813) -> NO COUNTERPART

## `createProcess.create` (draft line 1848) -> `createProcess.create`

## `createProcess.read` (draft line 1866) -> `createProcess.read`

## `renewProcess.create` (draft line 1887) -> `renewProcess.create`

## `renewProcess.read` (draft line 1907) -> `renewProcess.read`

## `transferProcess.create` (draft line 1932) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 1976) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2049) -> `transferProcess.transferReject`

## `restoreProcess.create` (draft line 2080) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2099) -> `restoreProcess.read`

## `domainName.create` (draft line 2140) -> `domainName.create`
- `status.items.$ref`: draft="<domainStatus>" generated="domainStatus"
- `processes.properties.createProcess.items.$ref`: draft="<domainCreateProcess.create>" generated="domainCreateProcess.create"

## `domainName.read` (draft line 2197) -> `domainName.read`
- `status.items.$ref`: draft="<domainStatus>" generated="domainStatus"

## `domainName.update` (draft line 2251) -> `domainName.update`
- `status.items.$ref`: draft="<domainStatus>" generated="domainStatus"

## `renewProcess.create.domain` (draft line 2295) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2311) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2354) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2417) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2431) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2445) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2464) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainName.reference` (draft line 2480) -> `domainName.reference`

## `contact.create` (draft line 2516) -> `contact.create`
- `status.items.$ref`: draft="<contactStatus>" generated="contactStatus"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.read` (draft line 2550) -> `contact.read`
- `status.items.$ref`: draft="<contactStatus>" generated="contactStatus"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `contact.update` (draft line 2586) -> `contact.update`
- `status.items.$ref`: draft="<contactStatus>" generated="contactStatus"
- `disclose.$ref`: draft="<disclose>" generated="disclose"

## `transferProcess.create.contact` (draft line 2619) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 2635) -> `contact.reference`

## `host.create` (draft line 2663) -> `host.create`
- `status.items.$ref`: draft="<hostStatus>" generated="hostStatus"

## `host.read` (draft line 2690) -> `host.read`
- `status.items.$ref`: draft="<hostStatus>" generated="hostStatus"

## `host.reference` (draft line 2723) -> `host.reference`

## `organisation.create` (draft line 2753) -> `organisation.create`
- `status.items.$ref`: draft="<organisationStatus>" generated="organisationStatus"

## `organisation.read` (draft line 2808) -> `organisation.read`
- `status.items.$ref`: draft="<organisationStatus>" generated="organisationStatus"

## `organisation.update` (draft line 2865) -> `organisation.update`
- `status.items.$ref`: draft="<organisationStatus>" generated="organisationStatus"

## `organisation.reference` (draft line 2919) -> `organisation.reference`

## `message.create` (draft line 2946) -> `message.create`

## `message.read` (draft line 2978) -> `message.read`

## `message.query` (draft line 3013) -> `message.query`

## `message.reference` (draft line 3030) -> `message.reference`

## `user.create` (draft line 3057) -> `user.create`

## `user.read` (draft line 3081) -> `user.read`

## `user.update` (draft line 3107) -> `user.update`

## `user.reference` (draft line 3130) -> `user.reference`

## `discovery.read` (draft line 3162) -> `discovery.read`

## `profile.read` (draft line 3245) -> `profile.read`

## `profile.reference` (draft line 3290) -> `profile.reference`

## Generated definitions without a draft counterpart

`domainStatus`, `hostStatus`, `contactStatus`, `organisationRoleStatus`, `organisationStatus`, `disclose`, `baseProcess`, `restoreProcess.report`, `domainCreateProcess.create`, `domainCreateProcess.read`, `host.update`
