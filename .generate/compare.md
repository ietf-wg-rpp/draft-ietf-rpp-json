# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 0 of 94 (case only: 0)

## `identifier` (draft line 1069) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1087) -> `clientIdentifier`

## `phoneNumber` (draft line 1106) -> `phoneNumber`

## `period.read` (draft line 1120) -> `period.read`

## `period.create` (draft line 1138) -> `period.create`

## `provMetadata.read` (draft line 1164) -> `provMetadata.read`

## `domainStatus.read` (draft line 1207) -> `domainStatus.read`

## `domainStatus.create` (draft line 1255) -> `domainStatus.create`

## `hostStatus.read` (draft line 1286) -> `hostStatus.read`

## `hostStatus.create` (draft line 1319) -> `hostStatus.create`

## `contactStatus.read` (draft line 1343) -> `contactStatus.read`

## `contactStatus.create` (draft line 1378) -> `contactStatus.create`

## `organisationRoleStatus.read` (draft line 1402) -> `organisationRoleStatus.read`

## `organisationRoleStatus.create` (draft line 1424) -> `organisationRoleStatus.create`

## `organisationStatus.read` (draft line 1449) -> `organisationStatus.read`

## `organisationStatus.create` (draft line 1485) -> `organisationStatus.create`

## `userStatus.read` (draft line 1519) -> `userStatus.read`

## `userStatus.create` (draft line 1541) -> `userStatus.create`

## `dnsRecord.read` (draft line 1579) -> `dnsRecord.read`

## `dnsRecord.create` (draft line 1599) -> `dnsRecord.create`

## `dnsControls.read` (draft line 1623) -> `dnsControls.read`

## `dnsControls.create` (draft line 1649) -> `dnsControls.create`

## `dnsData.read` (draft line 1683) -> `dnsData.read`

## `dnsData.create` (draft line 1704) -> `dnsData.create`

## `authInfo.read` (draft line 1732) -> `authInfo.read`

## `authInfo.create` (draft line 1750) -> `authInfo.create`

## `disclose.read` (draft line 1774) -> `disclose.read`

## `Card` (draft line 1798) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport.read` (draft line 1902) -> `restoreReport.read`

## `restoreReport.create` (draft line 1930) -> `restoreReport.create`

## `organisationRole.read` (draft line 1964) -> `organisationRole.read`

## `organisationRole.create` (draft line 1985) -> `organisationRole.create`

## `extension.read` (draft line 2013) -> `extension.read`

## `discoveryVersion.read` (draft line 2041) -> `discoveryVersion.read`

## `discoveryEnvironment.read` (draft line 2061) -> `discoveryEnvironment.read`

## `discoveryIdnLgr.read` (draft line 2085) -> `discoveryIdnLgr.read`

## `discoveryNotice.read` (draft line 2112) -> `discoveryNotice.read`

## `processes.read` (draft line 2134) -> `processes.read`

## `baseMessage.read` (draft line 2195) -> `baseMessage.read`

## `reviewResponseMessage.read` (draft line 2215) -> `reviewResponseMessage.read`

## `transferRequestMessage.read` (draft line 2252) -> `transferRequestMessage.read`

## `transferOutcomeMessage.read` (draft line 2282) -> `transferOutcomeMessage.read`

## `expirationDeletionMessage.read` (draft line 2323) -> `expirationDeletionMessage.read`

## `autoRenewalMessage.read` (draft line 2344) -> `autoRenewalMessage.read`

## `serviceNoticeMessage.read` (draft line 2368) -> `serviceNoticeMessage.read`

## `baseProcess.read` (draft line 2397) -> `baseProcess.read`

## `createProcess.create` (draft line 2418) -> `createProcess.create`

## `createProcess.read` (draft line 2436) -> `createProcess.read`

## `createProcess.reference` (draft line 2455) -> `createProcess.reference`

## `renewProcess.create` (draft line 2476) -> `renewProcess.create`

## `renewProcess.read` (draft line 2496) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2517) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2540) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2584) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2657) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2680) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2709) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2728) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2758) -> NO COUNTERPART

## `restoreProcess.reference` (draft line 2778) -> `restoreProcess.reference`

## `domainName.create` (draft line 2810) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2868) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2887) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2907) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2928) -> `domainName.read`

## `domainName.update` (draft line 2982) -> `domainName.update`

## `domainTransferProcess.create` (draft line 3025) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 3068) -> `domainTransferProcess.read`
- draft structure: allOf

## `domainTransferProcess.transferReject` (draft line 3133) -> `domainTransferProcess.transferReject`

## `domainTransferProcess.reference` (draft line 3154) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 3175) -> `domainName.reference`

## `contact.create` (draft line 3211) -> `contact.create`

## `contact.read` (draft line 3239) -> `contact.read`

## `contact.update` (draft line 3270) -> `contact.update`

## `contact.reference` (draft line 3297) -> `contact.reference`

## `host.create` (draft line 3325) -> `host.create`

## `host.read` (draft line 3351) -> `host.read`

## `host.update` (draft line 3380) -> `host.update`

## `host.reference` (draft line 3406) -> `host.reference`

## `organisation.create` (draft line 3436) -> `organisation.create`

## `organisation.read` (draft line 3490) -> `organisation.read`

## `organisation.update` (draft line 3547) -> `organisation.update`

## `organisation.reference` (draft line 3600) -> `organisation.reference`

## `message.create` (draft line 3627) -> `message.create`

## `message.read` (draft line 3659) -> `message.read`

## `message.query` (draft line 3694) -> `message.query`

## `message.reference` (draft line 3711) -> `message.reference`

## `user.create` (draft line 3739) -> `user.create`

## `user.read` (draft line 3763) -> `user.read`

## `user.update` (draft line 3789) -> `user.update`

## `user.reference` (draft line 3812) -> `user.reference`

## `discovery.read` (draft line 3844) -> `discovery.read`

## `profile.read` (draft line 3927) -> `profile.read`

## `profile.reference` (draft line 3972) -> `profile.reference`

## Generated definitions without a draft counterpart

`restoreProcess.update`
