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

## `restoreProcess.update` (draft line 2757) -> `restoreProcess.update`

## `restoreProcess.reference` (draft line 2777) -> `restoreProcess.reference`

## `domainName.create` (draft line 2809) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2867) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2886) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2906) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2927) -> `domainName.read`

## `domainName.update` (draft line 2981) -> `domainName.update`

## `domainTransferProcess.create` (draft line 3024) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 3067) -> `domainTransferProcess.read`
- draft structure: allOf

## `domainTransferProcess.transferReject` (draft line 3132) -> `domainTransferProcess.transferReject`

## `domainTransferProcess.reference` (draft line 3153) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 3174) -> `domainName.reference`

## `contact.create` (draft line 3210) -> `contact.create`

## `contact.read` (draft line 3238) -> `contact.read`

## `contact.update` (draft line 3269) -> `contact.update`

## `contact.reference` (draft line 3296) -> `contact.reference`

## `host.create` (draft line 3324) -> `host.create`

## `host.read` (draft line 3350) -> `host.read`

## `host.update` (draft line 3379) -> `host.update`

## `host.reference` (draft line 3405) -> `host.reference`

## `organisation.create` (draft line 3435) -> `organisation.create`

## `organisation.read` (draft line 3489) -> `organisation.read`

## `organisation.update` (draft line 3546) -> `organisation.update`

## `organisation.reference` (draft line 3599) -> `organisation.reference`

## `message.create` (draft line 3626) -> `message.create`

## `message.read` (draft line 3657) -> `message.read`

## `message.query` (draft line 3691) -> `message.query`

## `message.reference` (draft line 3708) -> `message.reference`

## `user.create` (draft line 3736) -> `user.create`

## `user.read` (draft line 3760) -> `user.read`

## `user.update` (draft line 3786) -> `user.update`

## `user.reference` (draft line 3809) -> `user.reference`

## `discovery.read` (draft line 3841) -> `discovery.read`

## `profile.read` (draft line 3924) -> `profile.read`

## `profile.reference` (draft line 3969) -> `profile.reference`

## Generated definitions without a draft counterpart

(none)
