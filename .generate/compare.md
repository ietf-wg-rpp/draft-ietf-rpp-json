# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 0 of 94 (case only: 0)

## `identifier` (draft line 1078) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1096) -> `clientIdentifier`

## `phoneNumber` (draft line 1115) -> `phoneNumber`

## `period.read` (draft line 1129) -> `period.read`

## `period.create` (draft line 1147) -> `period.create`

## `provMetadata.read` (draft line 1173) -> `provMetadata.read`

## `domainStatus.read` (draft line 1216) -> `domainStatus.read`

## `domainStatus.create` (draft line 1264) -> `domainStatus.create`

## `hostStatus.read` (draft line 1295) -> `hostStatus.read`

## `hostStatus.create` (draft line 1328) -> `hostStatus.create`

## `contactStatus.read` (draft line 1352) -> `contactStatus.read`

## `contactStatus.create` (draft line 1387) -> `contactStatus.create`

## `organisationRoleStatus.read` (draft line 1411) -> `organisationRoleStatus.read`

## `organisationRoleStatus.create` (draft line 1433) -> `organisationRoleStatus.create`

## `organisationStatus.read` (draft line 1458) -> `organisationStatus.read`

## `organisationStatus.create` (draft line 1494) -> `organisationStatus.create`

## `userStatus.read` (draft line 1528) -> `userStatus.read`

## `userStatus.create` (draft line 1550) -> `userStatus.create`

## `dnsRecord.read` (draft line 1588) -> `dnsRecord.read`

## `dnsRecord.create` (draft line 1608) -> `dnsRecord.create`

## `dnsControls.read` (draft line 1632) -> `dnsControls.read`

## `dnsControls.create` (draft line 1658) -> `dnsControls.create`

## `dnsData.read` (draft line 1692) -> `dnsData.read`

## `dnsData.create` (draft line 1713) -> `dnsData.create`

## `authInfo.read` (draft line 1741) -> `authInfo.read`

## `authInfo.create` (draft line 1759) -> `authInfo.create`

## `disclose.read` (draft line 1783) -> `disclose.read`

## `Card` (draft line 1807) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport.read` (draft line 1911) -> `restoreReport.read`

## `restoreReport.create` (draft line 1939) -> `restoreReport.create`

## `organisationRole.read` (draft line 1973) -> `organisationRole.read`

## `organisationRole.create` (draft line 1994) -> `organisationRole.create`

## `extension.read` (draft line 2022) -> `extension.read`

## `discoveryVersion.read` (draft line 2050) -> `discoveryVersion.read`

## `discoveryEnvironment.read` (draft line 2070) -> `discoveryEnvironment.read`

## `discoveryIdnLgr.read` (draft line 2094) -> `discoveryIdnLgr.read`

## `discoveryNotice.read` (draft line 2121) -> `discoveryNotice.read`

## `processes.read` (draft line 2143) -> `processes.read`

## `baseMessage.read` (draft line 2204) -> `baseMessage.read`

## `reviewResponseMessage.read` (draft line 2224) -> `reviewResponseMessage.read`

## `transferRequestMessage.read` (draft line 2260) -> `transferRequestMessage.read`

## `transferOutcomeMessage.read` (draft line 2290) -> `transferOutcomeMessage.read`

## `expirationDeletionMessage.read` (draft line 2331) -> `expirationDeletionMessage.read`

## `autoRenewalMessage.read` (draft line 2352) -> `autoRenewalMessage.read`

## `serviceNoticeMessage.read` (draft line 2376) -> `serviceNoticeMessage.read`

## `baseProcess.read` (draft line 2405) -> `baseProcess.read`

## `createProcess.create` (draft line 2426) -> `createProcess.create`

## `createProcess.read` (draft line 2444) -> `createProcess.read`

## `createProcess.reference` (draft line 2463) -> `createProcess.reference`

## `renewProcess.create` (draft line 2484) -> `renewProcess.create`

## `renewProcess.read` (draft line 2504) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2525) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2548) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2592) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2665) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2688) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2717) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2736) -> `restoreProcess.read`

## `restoreProcess.update` (draft line 2766) -> `restoreProcess.update`

## `restoreProcess.reference` (draft line 2786) -> `restoreProcess.reference`

## `domainName.create` (draft line 2818) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2876) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2895) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2915) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2936) -> `domainName.read`

## `domainName.update` (draft line 2990) -> `domainName.update`

## `domainTransferProcess.create` (draft line 3033) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 3076) -> `domainTransferProcess.read`
- draft structure: allOf

## `domainTransferProcess.transferReject` (draft line 3141) -> `domainTransferProcess.transferReject`

## `domainTransferProcess.reference` (draft line 3162) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 3183) -> `domainName.reference`

## `contact.create` (draft line 3219) -> `contact.create`

## `contact.read` (draft line 3247) -> `contact.read`

## `contact.update` (draft line 3278) -> `contact.update`

## `contact.reference` (draft line 3305) -> `contact.reference`

## `host.create` (draft line 3333) -> `host.create`

## `host.read` (draft line 3359) -> `host.read`

## `host.update` (draft line 3388) -> `host.update`

## `host.reference` (draft line 3414) -> `host.reference`

## `organisation.create` (draft line 3444) -> `organisation.create`

## `organisation.read` (draft line 3498) -> `organisation.read`

## `organisation.update` (draft line 3555) -> `organisation.update`

## `organisation.reference` (draft line 3608) -> `organisation.reference`

## `message.create` (draft line 3635) -> `message.create`

## `message.read` (draft line 3666) -> `message.read`

## `message.query` (draft line 3700) -> `message.query`

## `message.reference` (draft line 3717) -> `message.reference`

## `user.create` (draft line 3745) -> `user.create`

## `user.read` (draft line 3769) -> `user.read`

## `user.update` (draft line 3795) -> `user.update`

## `user.reference` (draft line 3818) -> `user.reference`

## `discovery.read` (draft line 3850) -> `discovery.read`

## `profile.read` (draft line 3933) -> `profile.read`

## `profile.reference` (draft line 3978) -> `profile.reference`

## Generated definitions without a draft counterpart

(none)
