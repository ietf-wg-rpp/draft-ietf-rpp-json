# Comparison: generated schemas vs. draft-ietf-rpp-json

Draft keys that differ from the Rule 27 key: 3 of 91 (case only: 0)

## `identifier` (draft line 1012) -> `identifier`
- `maxLength`: draft=89 generated=null [prose constraint]
- `pattern`: draft="^(\\w|_){1,8}-\\w{1,}$" generated=null [prose constraint]

## `clientIdentifier` (draft line 1030) -> `clientIdentifier`

## `phoneNumber` (draft line 1049) -> `phoneNumber`

## `period` (draft line 1061) -> `period`

## `provMetadata` (draft line 1085) -> `provMetadata`

## `domainStatus` (draft line 1126) -> `domainStatus`

## `domainStatus.request` (draft line 1173) -> `domainStatus.request`

## `hostStatus` (draft line 1201) -> `hostStatus`

## `hostStatus.request` (draft line 1233) -> `hostStatus.request`

## `contactStatus` (draft line 1251) -> `contactStatus`

## `contactStatus.request` (draft line 1285) -> `contactStatus.request`

## `organisationRoleStatus` (draft line 1306) -> `organisationRoleStatus`

## `organisationStatus` (draft line 1332) -> `organisationStatus`

## `organisationStatus.request` (draft line 1367) -> `organisationStatus.request`

## `userStatus` (draft line 1398) -> `userStatus`

## `userStatus.request` (draft line 1416) -> `userStatus.request`

## `dnsRecord` (draft line 1452) -> `dnsRecord`

## `dnsControls` (draft line 1474) -> `dnsControls`

## `dnsData` (draft line 1506) -> `dnsData`

## `authInfo` (draft line 1532) -> `authInfo`

## `disclose` (draft line 1554) -> `disclose`

## `Card` (draft line 1578) -> `Card`
- properties only in draft: @type, version, kind, language, name, organizations, addresses, phones, emails, links, localizations
- required: draft=['@type', 'version'] generated=[]

## `restoreReport` (draft line 1680) -> `restoreReport`

## `organisationRole` (draft line 1712) -> `organisationRole`

## `extension` (draft line 1738) -> `extension`

## `discoveryVersion` (draft line 1764) -> `discoveryVersion`

## `discoveryEnvironment` (draft line 1782) -> `discoveryEnvironment`

## `discoveryIdnLgr` (draft line 1804) -> `discoveryIdnLgr`

## `discoveryNotice` (draft line 1829) -> `discoveryNotice`

## `processes` (draft line 1849) -> `processes`

## `baseMessage` (draft line 1908) -> `baseMessage`

## `reviewResponseMessage` (draft line 1926) -> `reviewResponseMessage`

## `transferRequestMessage` (draft line 1961) -> `transferRequestMessage`

## `transferOutcomeMessage` (draft line 1989) -> `transferOutcomeMessage`

## `expirationDeletionMessage` (draft line 2028) -> `expirationDeletionMessage`

## `autoRenewalMessage` (draft line 2047) -> `autoRenewalMessage`

## `serviceNoticeMessage` (draft line 2069) -> `serviceNoticeMessage`

## `baseProcess` (draft line 2096) -> `baseProcess`

## `createProcess.create` (draft line 2117) -> `createProcess.create`

## `createProcess.read` (draft line 2135) -> `createProcess.read`

## `createProcess.reference` (draft line 2154) -> `createProcess.reference`

## `renewProcess.create` (draft line 2175) -> `renewProcess.create`

## `renewProcess.read` (draft line 2195) -> `renewProcess.read`

## `renewProcess.reference` (draft line 2216) -> `renewProcess.reference`

## `transferProcess.create` (draft line 2239) -> `transferProcess.create`
- draft structure: allOf

## `transferProcess.read` (draft line 2283) -> `transferProcess.read`
- draft structure: allOf

## `transferProcess.transferReject` (draft line 2356) -> `transferProcess.transferReject`

## `transferProcess.reference` (draft line 2379) -> `transferProcess.reference`

## `restoreProcess.create` (draft line 2408) -> `restoreProcess.create`

## `restoreProcess.read` (draft line 2427) -> `restoreProcess.read`

## `restoreProcess.report` (draft line 2457) -> NO COUNTERPART

## `restoreProcess.reference` (draft line 2477) -> `restoreProcess.reference`

## `domainName.create` (draft line 2509) -> `domainName.create`

## `domainCreateProcess.create` (draft line 2567) -> `domainCreateProcess.create`

## `domainCreateProcess.read` (draft line 2586) -> `domainCreateProcess.read`

## `domainCreateProcess.reference` (draft line 2606) -> `domainCreateProcess.reference`

## `domainName.read` (draft line 2627) -> `domainName.read`

## `domainName.update` (draft line 2681) -> `domainName.update`

## `renewProcess.create.domain` (draft line 2724) -> `renewProcess.create`
- KEY MISMATCH (name): draft `renewProcess.create.domain`, Rule 27 key `renewProcess.create`
- draft structure: $ref alias -> renewProcess.create

## `domainTransferProcess.create` (draft line 2740) -> `domainTransferProcess.create`
- draft structure: allOf

## `domainTransferProcess.read` (draft line 2783) -> `domainTransferProcess.read`
- draft structure: allOf

## `transferProcess.delete.domain` (draft line 2846) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `transferProcess.approve.domain` (draft line 2860) -> NO COUNTERPART
- draft structure: $ref alias -> transferProcess.read.domain

## `domainTransferProcess.transferReject` (draft line 2874) -> `domainTransferProcess.transferReject`

## `transferProcess.reject.domain` (draft line 2893) -> `domainTransferProcess.transferReject`
- KEY MISMATCH (name): draft `transferProcess.reject.domain`, Rule 27 key `domainTransferProcess.transferReject`
- draft structure: $ref alias -> transferProcess.read.domain
- properties only in generated: @type, reason
- required: draft=[] generated=['@type']

## `domainTransferProcess.reference` (draft line 2907) -> `domainTransferProcess.reference`

## `domainName.reference` (draft line 2928) -> `domainName.reference`

## `contact.create` (draft line 2964) -> `contact.create`

## `contact.read` (draft line 2992) -> `contact.read`

## `contact.update` (draft line 3023) -> `contact.update`

## `transferProcess.create.contact` (draft line 3050) -> `transferProcess.create`
- KEY MISMATCH (name): draft `transferProcess.create.contact`, Rule 27 key `transferProcess.create`
- draft structure: $ref alias -> transferProcess.create
- draft structure: allOf

## `contact.reference` (draft line 3066) -> `contact.reference`

## `host.create` (draft line 3094) -> `host.create`

## `host.read` (draft line 3120) -> `host.read`

## `host.update` (draft line 3149) -> `host.update`

## `host.reference` (draft line 3175) -> `host.reference`

## `organisation.create` (draft line 3205) -> `organisation.create`

## `organisation.read` (draft line 3259) -> `organisation.read`

## `organisation.update` (draft line 3316) -> `organisation.update`

## `organisation.reference` (draft line 3369) -> `organisation.reference`

## `message.create` (draft line 3396) -> `message.create`

## `message.read` (draft line 3428) -> `message.read`

## `message.query` (draft line 3463) -> `message.query`

## `message.reference` (draft line 3480) -> `message.reference`

## `user.create` (draft line 3508) -> `user.create`

## `user.read` (draft line 3532) -> `user.read`

## `user.update` (draft line 3558) -> `user.update`

## `user.reference` (draft line 3581) -> `user.reference`

## `discovery.read` (draft line 3613) -> `discovery.read`

## `profile.read` (draft line 3696) -> `profile.read`

## `profile.reference` (draft line 3741) -> `profile.reference`

## Generated definitions without a draft counterpart

`restoreProcess.update`
