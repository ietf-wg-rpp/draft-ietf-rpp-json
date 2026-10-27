# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 99 (case only: 0)

## `identifier` (draft line 1068) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1086) -> `clientIdentifier`

## `phoneNumber` (draft line 1105) -> `phoneNumber`

## `period.read` (draft line 1119) -> `period.read`

## `period.create` (draft line 1137) -> `period.create`

## `provMetadata.read` (draft line 1163) -> `provMetadata.read`

## `domainStatus.read` (draft line 1206) -> `domainStatus.read`

## `domainStatus.create` (draft line 1254) -> `domainStatus.create`

## `hostStatus.read` (draft line 1285) -> `hostStatus.read`

## `hostStatus.create` (draft line 1318) -> `hostStatus.create`

## `contactStatus.read` (draft line 1342) -> `contactStatus.read`

## `contactStatus.create` (draft line 1377) -> `contactStatus.create`

## `organisationRoleStatus.read` (draft line 1401) -> `organisationRoleStatus.read`

## `organisationRoleStatus.create` (draft line 1423) -> `organisationRoleStatus.create`

## `organisationStatus.read` (draft line 1448) -> `organisationStatus.read`

## `organisationStatus.create` (draft line 1484) -> `organisationStatus.create`

## `userStatus.read` (draft line 1518) -> `userStatus.read`

## `userStatus.create` (draft line 1540) -> `userStatus.create`

## `dnsRecord.read` (draft line 1578) -> `dnsRecord.read`

## `dnsRecord.create` (draft line 1598) -> `dnsRecord.create`

## `dnsControls.read` (draft line 1622) -> `dnsControls.read`

## `dnsControls.create` (draft line 1648) -> `dnsControls.create`

## `dnsData.read` (draft line 1682) -> `dnsData.read`

## `dnsData.create` (draft line 1703) -> `dnsData.create`

## `authInfo.read` (draft line 1731) -> `authInfo.read`

## `authInfo.create` (draft line 1749) -> `authInfo.create`

## `disclose.read` (draft line 1773) -> `disclose.read`

## `Card` (draft line 1797) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport.read` (draft line 1901) -> `restoreReport.read`

## `restoreReport.create` (draft line 1929) -> `restoreReport.create`

## `organisationRole.read` (draft line 1963) -> `organisationRole.read`

## `organisationRole.create` (draft line 1984) -> `organisationRole.create`

## `extension.read` (draft line 2012) -> `extension.read`

## `discoveryVersion.read` (draft line 2040) -> `discoveryVersion.read`

## `discoveryEnvironment.read` (draft line 2060) -> `discoveryEnvironment.read`

## `discoveryIdnLgr.read` (draft line 2084) -> `discoveryIdnLgr.read`

## `discoveryNotice.read` (draft line 2111) -> `discoveryNotice.read`

## `processes.read` (draft line 2133) -> `processes.read`

## `baseMessage.read` (draft line 2194) -> `baseMessage.read`

## `reviewResponseMessage.read` (draft line 2214) -> `reviewResponseMessage.read`

## `transferRequestMessage.read` (draft line 2251) -> `transferRequestMessage.read`

## `transferOutcomeMessage.read` (draft line 2281) -> `transferOutcomeMessage.read`

## `expirationDeletionMessage.read` (draft line 2322) -> `expirationDeletionMessage.read`

## `autoRenewalMessage.read` (draft line 2343) -> `autoRenewalMessage.read`

## `serviceNoticeMessage.read` (draft line 2367) -> `serviceNoticeMessage.read`

## `baseProcess.read` (draft line 2396) -> `baseProcess.read`

## `createProcess.create` (draft line 2417) -> `createProcess.create`

## `createProcess.read` (draft line 2435) -> `createProcess.read`

## `createProcess.reference` (draft line 2454) -> `createProcess.reference`

## `renewProcess.create` (draft line 2475) -> `renewProcess.create`

## `renewProcess.read` (draft line 2495) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2516) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2539) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2583) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2656) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2679) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2708) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2727) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2757) -> NO COUNTERPART

## `restoreProcess.reference` (draft line 2777) -> `restoreProcess.reference`

## `domainName.create` (draft line 2809) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2867) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2886) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2906) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2927) -> `domainName.read`

## `domainName.update` (draft line 2981) -> `domainName.update`

## `renewProcess.create.domain` (draft line 3024) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 3040) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 3083) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 3146) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 3160) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 3174) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 3193) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainTransferProcess.reference` (draft line 3207) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 3228) -> `domainName.reference`

## `contact.create` (draft line 3264) -> `contact.create`

## `contact.read` (draft line 3292) -> `contact.read`

## `contact.update` (draft line 3323) -> `contact.update`

## `transferProcess.create.contact` (draft line 3350) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 3366) -> `contact.reference`

## `host.create` (draft line 3394) -> `host.create`

## `host.read` (draft line 3420) -> `host.read`

## `host.update` (draft line 3449) -> `host.update`

## `host.reference` (draft line 3475) -> `host.reference`

## `organisation.create` (draft line 3505) -> `organisation.create`

## `organisation.read` (draft line 3559) -> `organisation.read`

## `organisation.update` (draft line 3616) -> `organisation.update`

## `organisation.reference` (draft line 3669) -> `organisation.reference`

## `message.create` (draft line 3696) -> `message.create`

## `message.read` (draft line 3728) -> `message.read`

## `message.query` (draft line 3763) -> `message.query`

## `message.reference` (draft line 3780) -> `message.reference`

## `user.create` (draft line 3808) -> `user.create`

## `user.read` (draft line 3832) -> `user.read`

## `user.update` (draft line 3858) -> `user.update`

## `user.reference` (draft line 3881) -> `user.reference`

## `discovery.read` (draft line 3913) -> `discovery.read`

## `profile.read` (draft line 3996) -> `profile.read`

## `profile.reference` (draft line 4041) -> `profile.reference`

## Generated definitions without a draft counterpart

`restoreProcess.update`
