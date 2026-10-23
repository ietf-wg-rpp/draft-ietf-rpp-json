# Generator diagnostics

## rule-gap: No rule in draft-ietf-rpp-json covers this; generator choice applied

- Create-only element in a component object: components have a single schema, Rule 6 (writeOnly in requests, excluded from update) cannot be applied; no annotation
  (domainStatus.label, domainStatus.reason, hostStatus.label, hostStatus.reason, contactStatus.label, contactStatus.reason, organisationRoleStatus.label, organisationRoleStatus.reason, organisationStatus.label, organisationStatus.reason, authInfo.method, authInfo.authdata, reviewResponseMessage.message)
- Primitive type 'Object' is not listed in Primitive Type Mappings (Rule 24 only permits additionalProperties: true for it)
  (dnsRecord.rdata)
- Dictionary[Type] primitive has no mapping in Primitive Type Mappings (mapped to object with additionalProperties)
  (dnsControls.ttl, dnsControls.maxSigLifetime)
- Polymorphism (an object extending the referenced base object may be used in its place) has no JSON rule; oneOf over all candidates applied
  (processes.transferProcess -> transferProcess, domainTransferProcess, processes.createProcess -> createProcess, domainCreateProcess, baseMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, reviewResponseMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, transferRequestMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, transferOutcomeMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, expirationDeletionMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, autoRenewalMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, serviceNoticeMessage.process -> baseProcess, transferProcess, domainTransferProcess, restoreProcess, renewProcess, createProcess, domainCreateProcess, message.data -> baseMessage, reviewResponseMessage, transferRequestMessage, transferOutcomeMessage, expirationDeletionMessage, autoRenewalMessage, serviceNoticeMessage)
- Aggregation with cardinality 1 or 0-1: Rule 8 only covers 0+ and 1+
  (baseMessage.process, reviewResponseMessage.process, transferRequestMessage.process, transferOutcomeMessage.process, expirationDeletionMessage.process, autoRenewalMessage.process, serviceNoticeMessage.process)
- Annotation of create-only elements in read responses is not defined (Rule 6 covers requests only); readOnly applied following the draft schemas
  (transferProcess.transferDir, transferProcess.gainingClientId, renewProcess.expiryDate, renewProcess.renewalPeriod, domainCreateProcess.period, domainTransferProcess.transferDir, domainTransferProcess.gainingClientId, domainTransferProcess.transferPeriod, domainName.name, domainName.uName, domainName.lgr, contact.id, organisation.id, message.data, user.id)
- Primitive type 'Fully Qualified Domain Name' is not listed in Primitive Type Mappings
  (domainName.name, host.hostName)
- Bare 'Type' notation (= Composition[Type] in data-objects) is not mentioned in the Association Rules; embedded as composition
  (domainName.registrant, organisation.parent, profile.baseProfile)
- Operation parameters have no JSON representation rule; not included in any schema
  (domainName.read.hostsFilter, message.query.type)
- Cardinality '1-2' is not covered by Rules 1-4; mapped to an array with minItems/maxItems
  (contact.contactInfo)
- DictionaryComposition with cardinality 1+: Rules 10/12 do not define how cardinality maps to a JSON object; minProperties 1 applied
  (organisation.roles)
- Query response representation is not defined by a rule; array of read representations applied following the draft
  (message)
- LabelledAggregation of a primitive type: Rule 9/11 only cover associations with objects
  (discovery.links)

## rule-conflict: Rules of draft-ietf-rpp-json conflict; generator choice applied

- Rule 18 requires process data in the 'processes' element of create requests, but 'processes' is read-only and Rule 5 forbids read-only properties in requests; Rule 18 applied
  (domainName, contact, host, organisation, user)

## yaml-gap: Information not present in the YAML export

- Object has no data elements
  (disclose)
- 'Unique Identifier' object attribute is not exported; derived heuristically for the reference view
  (domainName -> name, contact -> id, host -> hostName, organisation -> id, user -> id, message -> id, profile -> name)
- Owner Data Object of an object-specific Process Object is not exported; derived from the identifier prefix
  (domainCreateProcess -> domainName)
- Common Data Types (syntax, length, pattern) are not exported; a plain string placeholder is generated
  (clientIdentifier, identifier)
- External type definition is not exported; an open object placeholder is generated (Rule 15)
  (RPP-JSContact-Profile:Card)

## yaml-issue: YAML content inconsistent with the data-objects conventions

- Derived object redefines inherited data element 'processId' (data-objects Inheritance: MUST NOT)
  (domainTransferProcess)
- Object referenced as 'Authorisation Information Object' but defined as 'Authorisation Information'
  (domainName.authInfo)
- Data type value has a trailing period
  (contact.id, contact.disclose)
- Object referenced as 'Disclose Object' but defined as 'Disclose'
  (contact.disclose)
- Data type uses the '<Object Name> Reference' notation, which is not one of the defined association types
  (user.organisationId)
