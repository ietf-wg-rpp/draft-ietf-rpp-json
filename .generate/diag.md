# Generator diagnostics

## rule-gap: No rule in draft-ietf-rpp-json covers this; generator choice applied

- Restriction 'range' has no JSON rule (Rule 22 covers enumerations only); mapped to the matching JSON Schema keyword
  (period.value, dnsControls.ttl, dnsControls.maxSigLifetime)
- Create-only element in a component object: components have a single schema, Rule 6 (writeOnly in requests, excluded from update) cannot be applied; no annotation
  (domainStatus.label, domainStatus.reason, hostStatus.label, hostStatus.reason, contactStatus.label, contactStatus.reason, organisationRoleStatus.label, organisationRoleStatus.reason, organisationStatus.label, organisationStatus.reason, userStatus.label, userStatus.reason, authInfo.method, authInfo.authdata, reviewResponseMessage.message)
- Primitive type 'Object' is not listed in Primitive Type Mappings; unevaluatedProperties: true applied (composable; Rule 24 names additionalProperties: true)
  (dnsRecord.rdata)
- Dictionary[Type] primitive has no mapping in Primitive Type Mappings (mapped to object with additionalProperties)
  (dnsControls.ttl, dnsControls.maxSigLifetime)
- Restriction 'key_pattern' has no JSON rule (Rule 22 covers enumerations only); mapped to the matching JSON Schema keyword
  (dnsControls.ttl, dnsControls.maxSigLifetime)
- Cardinality '1-2' is not covered by Rules 1-4; mapped to an array with minItems/maxItems
  (restoreReport.statements)
- Polymorphism (an object extending the referenced base object may be used in its place) has no JSON rule; only the base object is referenced
  (processes.transferProcess -> transferProcess (not: domainTransferProcess), processes.createProcess -> createProcess (not: domainCreateProcess), baseMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), reviewResponseMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), transferRequestMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), transferOutcomeMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), expirationDeletionMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), autoRenewalMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), serviceNoticeMessage.process -> baseProcess (not: transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess), message.data -> baseMessage (not: reviewResponseMessage, transferRequestMessage, transferOutcomeMessage, expirationDeletionMessage, autoRenewalMessage, serviceNoticeMessage))
- Direct Access (sub-resource addressing) has no JSON rule; the inline representation is generated unchanged
  (processes.transferProcess, processes.renewProcess, processes.restoreProcess, processes.createProcess, domainName.processes, contact.processes, host.processes, organisation.users, organisation.processes, user.processes)
- Aggregation with cardinality 1 or 0-1: Rule 8 only covers 0+ and 1+
  (baseMessage.process, reviewResponseMessage.process, transferRequestMessage.process, transferOutcomeMessage.process, expirationDeletionMessage.process, autoRenewalMessage.process, serviceNoticeMessage.process, domainName.registrant, organisation.parent, user.organisation, profile.baseProfile)
- Cross-element conditions have no JSON rule; if/then applied
  (transferProcess.create, transferProcess.read, domainTransferProcess.create, domainTransferProcess.read)
- Annotation of create-only elements in read responses is not defined (Rule 6 covers requests only); readOnly applied following the draft schemas
  (transferProcess.transferDir, transferProcess.gainingClientId, renewProcess.expiryDate, renewProcess.renewalPeriod, domainCreateProcess.period, domainTransferProcess.transferDir, domainTransferProcess.gainingClientId, domainTransferProcess.transferPeriod, domainName.name, domainName.uName, domainName.lgr, contact.id, organisation.id, message.data, user.id)
- Primitive type 'Fully Qualified Domain Name' is not listed in Primitive Type Mappings
  (domainName.name, host.hostName)
- Visibility 'onDemand' has no JSON rule; the element is never required in read views (output only on request)
  (domainName.authInfo, contact.authInfo)
- Operation parameters have no JSON representation rule; not included in any schema
  (domainName.read.hostsFilter, message.query.type)
- DictionaryComposition with cardinality 1+: Rules 10/12 do not define how cardinality maps to a JSON object; minProperties 1 applied
  (organisation.roles)
- An Output Object with cardinality '0+' has no JSON rule; array of read representations applied following the draft
  (message)
- LabelledAggregation of a primitive type: Rule 9/11 only cover associations with objects
  (discovery.links)
- Restriction 'min_length' has no JSON rule (Rule 22 covers enumerations only); mapped to the matching JSON Schema keyword
  (clientIdentifier)
- Restriction 'max_length' has no JSON rule (Rule 22 covers enumerations only); mapped to the matching JSON Schema keyword
  (clientIdentifier)
- Restriction 'pattern' has no JSON rule (Rule 22 covers enumerations only); mapped to the matching JSON Schema keyword
  (clientIdentifier, phoneNumber)
- Common Data Types have no Identifier, so Rule 27 does not name their $defs key; the draft's key is used
  (clientIdentifier, identifier, phoneNumber)
- The Processes Object is shared by all Data Objects; no rule excludes processes a Data Object does not support
  (contact: renewProcess, restoreProcess, createProcess, host: renewProcess, createProcess, organisation: transferProcess, renewProcess, restoreProcess, createProcess, user: transferProcess, renewProcess, restoreProcess, createProcess)

## rule-conflict: Rules of draft-ietf-rpp-json conflict; generator choice applied

- Rule 18 requires process data in the 'processes' element of create requests, but 'processes' is read-only and Rule 5 forbids read-only properties in requests; Rule 18 applied
  (domainName)

## yaml-gap: Information not present in the YAML export

- Object has no data elements
  (disclose)
- Common Data Type syntax is given only as prose (no restrictions exported); no syntax keywords generated
  (identifier)
- External type definition is not exported; an open object placeholder is generated (Rule 15)
  (RPP-JSContact-Profile:Card)

## yaml-issue: YAML content inconsistent with the data-objects conventions

- Object referenced as 'Authorisation Information Object' but defined as 'Authorisation Information'
  (domainName.authInfo, contact.authInfo)
- Object referenced as 'Disclose Object' but defined as 'Disclose'
  (contact.disclose)
