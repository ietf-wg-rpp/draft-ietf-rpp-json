# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 0 of 104 (case only: 0)

## `identifier` (draft line 1121) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1139) -> `clientIdentifier`

## `phoneNumber` (draft line 1158) -> `phoneNumber`

## `period.read` (draft line 1172) -> `period.read`

## `period.create` (draft line 1190) -> `period.create`

## `provMetadata.read` (draft line 1216) -> `provMetadata.read`

## `domainStatus.read` (draft line 1259) -> `domainStatus.read`

## `domainStatus.create` (draft line 1307) -> `domainStatus.create`

## `hostStatus.read` (draft line 1338) -> `hostStatus.read`

## `hostStatus.create` (draft line 1371) -> `hostStatus.create`

## `contactStatus.read` (draft line 1395) -> `contactStatus.read`

## `contactStatus.create` (draft line 1430) -> `contactStatus.create`

## `organisationRoleStatus.read` (draft line 1454) -> `organisationRoleStatus.read`

## `organisationRoleStatus.create` (draft line 1476) -> `organisationRoleStatus.create`

## `organisationStatus.read` (draft line 1501) -> `organisationStatus.read`

## `organisationStatus.create` (draft line 1537) -> `organisationStatus.create`

## `userStatus.read` (draft line 1571) -> `userStatus.read`

## `userStatus.create` (draft line 1593) -> `userStatus.create`

## `dnsRecord.read` (draft line 1631) -> `dnsRecord.read`

## `dnsRecord.create` (draft line 1651) -> `dnsRecord.create`

## `dnsControls.read` (draft line 1675) -> `dnsControls.read`

## `dnsControls.create` (draft line 1701) -> `dnsControls.create`

## `dnsData.read` (draft line 1735) -> `dnsData.read`

## `dnsData.create` (draft line 1756) -> `dnsData.create`

## `authInfo.read` (draft line 1784) -> `authInfo.read`

## `authInfo.create` (draft line 1802) -> `authInfo.create`

## `disclose.read` (draft line 1826) -> `disclose.read`

## `Card` (draft line 1850) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport.read` (draft line 1954) -> `restoreReport.read`

## `restoreReport.create` (draft line 1982) -> `restoreReport.create`

## `organisationRole.read` (draft line 2016) -> `organisationRole.read`

## `organisationRole.create` (draft line 2037) -> `organisationRole.create`

## `extension.read` (draft line 2065) -> `extension.read`

## `discoveryVersion.read` (draft line 2093) -> `discoveryVersion.read`

## `discoveryEnvironment.read` (draft line 2113) -> `discoveryEnvironment.read`

## `discoveryIdnLgr.read` (draft line 2137) -> `discoveryIdnLgr.read`

## `discoveryNotice.read` (draft line 2164) -> `discoveryNotice.read`

## `processes.read` (draft line 2186) -> `processes.read`

## `baseMessage.read` (draft line 2237) -> `baseMessage.read`

## `reviewResponseMessage.read` (draft line 2257) -> `reviewResponseMessage.read`

## `transferRequestMessage.read` (draft line 2283) -> `transferRequestMessage.read`

## `transferOutcomeMessage.read` (draft line 2307) -> `transferOutcomeMessage.read`

## `expirationDeletionMessage.read` (draft line 2342) -> `expirationDeletionMessage.read`

## `autoRenewalMessage.read` (draft line 2363) -> `autoRenewalMessage.read`

## `serviceNoticeMessage.read` (draft line 2387) -> `serviceNoticeMessage.read`

## `core.baseMessage.read` (draft line 2410) -> `core.baseMessage.read`

## `any.baseMessage.read` (draft line 2429) -> `any.baseMessage.read`
- draft structure: $ref alias -> core.baseMessage.read

## `baseProcess.read` (draft line 2452) -> `baseProcess.read`

## `createProcess.create` (draft line 2473) -> `createProcess.create`

## `createProcess.read` (draft line 2491) -> `createProcess.read`

## `createProcess.reference` (draft line 2510) -> `createProcess.reference`

## `renewProcess.create` (draft line 2531) -> `renewProcess.create`

## `renewProcess.read` (draft line 2551) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2572) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2595) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2639) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2712) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2735) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2764) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2783) -> `restoreProcess.read`

## `restoreProcess.update` (draft line 2813) -> `restoreProcess.update`

## `restoreProcess.reference` (draft line 2832) -> `restoreProcess.reference`

## `core.baseProcess.read` (draft line 2855) -> `core.baseProcess.read`

## `any.baseProcess.read` (draft line 2874) -> `any.baseProcess.read`
- draft structure: $ref alias -> core.baseProcess.read

## `core.createProcess.reference` (draft line 2887) -> `core.createProcess.reference`

## `any.createProcess.reference` (draft line 2902) -> `any.createProcess.reference`
- draft structure: $ref alias -> core.createProcess.reference

## `core.transferProcess.read` (draft line 2915) -> `core.transferProcess.read`

## `any.transferProcess.read` (draft line 2930) -> `any.transferProcess.read`
- draft structure: $ref alias -> core.transferProcess.read

## `core.transferProcess.reference` (draft line 2943) -> `core.transferProcess.reference`

## `any.transferProcess.reference` (draft line 2958) -> `any.transferProcess.reference`
- draft structure: $ref alias -> core.transferProcess.reference

## `domainName.create` (draft line 2984) -> `domainName.create`

## `domainCreateProcess.create` (draft line 3042) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 3061) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 3081) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 3102) -> `domainName.read`

## `domainName.update` (draft line 3156) -> `domainName.update`

## `domainTransferProcess.create` (draft line 3199) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 3242) -> `domainTransferProcess.read`
- draft structure: allOf

## `domainTransferProcess.transferReject` (draft line 3307) -> `domainTransferProcess.transferReject`

## `domainTransferProcess.reference` (draft line 3328) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 3349) -> `domainName.reference`

## `contact.create` (draft line 3385) -> `contact.create`

## `contact.read` (draft line 3413) -> `contact.read`

## `contact.update` (draft line 3444) -> `contact.update`

## `contact.reference` (draft line 3471) -> `contact.reference`

## `host.create` (draft line 3499) -> `host.create`

## `host.read` (draft line 3525) -> `host.read`

## `host.update` (draft line 3554) -> `host.update`

## `host.reference` (draft line 3580) -> `host.reference`

## `organisation.create` (draft line 3610) -> `organisation.create`

## `organisation.read` (draft line 3664) -> `organisation.read`

## `organisation.update` (draft line 3721) -> `organisation.update`

## `organisation.reference` (draft line 3774) -> `organisation.reference`

## `message.create` (draft line 3799) -> `message.create`

## `message.read` (draft line 3820) -> `message.read`

## `message.query` (draft line 3844) -> `message.query`

## `message.reference` (draft line 3861) -> `message.reference`

## `user.create` (draft line 3889) -> `user.create`

## `user.read` (draft line 3913) -> `user.read`

## `user.update` (draft line 3939) -> `user.update`

## `user.reference` (draft line 3962) -> `user.reference`

## `discovery.read` (draft line 3994) -> `discovery.read`

## `profile.read` (draft line 4077) -> `profile.read`

## `profile.reference` (draft line 4122) -> `profile.reference`

## Generated definitions without a draft counterpart

(none)
