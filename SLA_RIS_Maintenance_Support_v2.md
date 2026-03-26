# SERVICE LEVEL AGREEMENT (SLA)

**for**

## RIS Software Maintenance & Support Services

---

**Submitted to**
Mr. Gagandeep Gupta
Scan4Health

**Prepared by**
Jina Code Systems
855, Spaze iTech Park,
Sector 49, Gurugram
Mar, 2026

---

## SERVICE LEVEL AGREEMENT (SLA)

This Service Level Agreement ("Agreement") is entered into between:

- **Service Provider:** Jina Code Systems ("Provider")
- **Client:** Scan4Health ("Client")
- **Effective Date:** 25/03/2026
- **Term:** 1 Year from Effective Date

---

## 1. PURPOSE

This Agreement defines the service levels, support structure, responsibilities, performance commitments, and commercial terms for ongoing maintenance and support of the software system developed and deployed by the Provider for the Client.

The objective of this SLA is to ensure uninterrupted system performance, quick issue resolution, and continuous operational efficiency for Scan4Health's diagnostic workflows.

---

## 2. SCOPE OF SERVICES

The Provider agrees to deliver comprehensive post-deployment support services, including but not limited to:

### 2.1 Maintenance & Support
- Preventive maintenance to avoid system failures
- Fixing bugs, defects, and system errors

### 2.2 Issue Resolution
- Diagnosis and resolution of functional and technical issues
- Database-level troubleshooting (if applicable)
- API and integration-level debugging (existing integrations only)

### 2.3 System Health Monitoring
- Periodic system health checks (monthly)
- Performance tuning and optimization recommendations

### 2.4 Technical Assistance
- Support to front-office and operational teams
- Guidance on system usage and best practices

### 2.5 Minor Enhancements (Fair Usage)

Minor enhancements and non-critical improvements may be accommodated under this SLA, subject to the following limits:

- Each individual task must not exceed **4 hours** of effort
- A maximum of **20 hours per month** of cumulative enhancement effort is included
- Any task exceeding 4 hours, or effort exceeding the monthly cap, will be treated as a Change Request (CR) per Section 12
- Minor enhancements **exclude**: database schema changes, new workflow creation, new integrations, new module development, and migration tasks

### 2.6 Important Clarifications

- Any new feature development, module addition, or major workflow change is **not** included in the base SLA scope and will be treated as a Change Request (CR), as defined in Section 12
- Provider's support responsibility is limited to the **application layer only** (software, application logic, UI, and application-level configurations)
- Infrastructure-level issues including but not limited to OS, networking, hardware, and server administration are outside Provider's scope

---

## 3. PRE-SLA SYSTEM AUDIT & BASELINE ACCEPTANCE

### 3.1 System Audit

Prior to SLA commencement, the Provider shall conduct a system audit ("Baseline Audit") of the application in its current deployed state. The audit will document:

- Current system version and configuration
- List of known issues, bugs, or defects existing at the time of audit ("Known Issues")
- Infrastructure environment and recommended minimum specifications

### 3.2 Known Issues Register

A **Known Issues Register** will be jointly signed by both parties. Issues listed in this register:

- Will be addressed on a best-effort basis and are **not** subject to the resolution timelines defined in Section 5
- Major remediation of known issues may be treated as a Change Request (CR) at the Provider's discretion

### 3.3 Recommended Infrastructure

The Provider will provide a **Recommended Infrastructure Specification** document. The SLA commitments in this Agreement are contingent upon the Client maintaining infrastructure that meets or exceeds these specifications.

---

## 4. SYSTEM AVAILABILITY & INFRASTRUCTURE DEPENDENCY

The application is deployed on the Client's in-house infrastructure.

**No uptime percentage or availability guarantee** is provided under this SLA, as system availability is dependent on the Client's infrastructure which is outside the Provider's control.

The Provider shall use commercially reasonable efforts to ensure that the **software application** remains stable and functional under normal operating conditions, provided the Client's infrastructure meets the Recommended Infrastructure Specification (Section 3.3).

System availability is dependent on the Client's infrastructure, including:

- Server uptime
- Network connectivity
- Power supply
- Third-party services

**The Provider shall not be responsible for downtime caused by:**

- Server failures or hardware issues
- Network outages
- Improper or sub-standard infrastructure configuration
- Third-party software, OS, or service failures
- Client-side modifications to the system (see Section 7)

In case of infrastructure-related downtime, the Provider will assist in diagnosis and support resolution on a best-effort basis, but such assistance will not count toward SLA resolution timelines.

---

## 5. SUPPORT HOURS

### 5.1 Standard Support
- **Monday to Friday**
- **09:30 AM to 5:30 PM (IST)**

### 5.2 Emergency Support
- **24/7** support available **only** for Severity 1 (Critical) issues
- Emergency support outside standard business hours may be charged at **1.5x the CR hourly rate** (₹3,000/hour) if the issue is subsequently determined to be caused by Client infrastructure, unauthorized changes, or factors outside Provider's application scope

### 5.3 Public Holidays
- Indian national gazetted holidays and Haryana state holidays are **excluded** from business hours
- Response and resolution timelines that reference "business hours" or "working days" do not include public holidays
- A holiday calendar will be shared with the Client at the start of each calendar year

---

## 6. ISSUE CLASSIFICATION, RESPONSE & RESOLUTION

### 6.1 Severity Levels

| Severity Level | Description | Target Response Time | Target Resolution Time |
|---|---|---|---|
| **Severity 1 (Critical)** | Complete system downtime / core operations blocked | Within 2 hours | Within 12 hours* |
| **Severity 2 (High)** | Major functionality impacted with no workaround | Within 8 hours (business hours) | Within 2 working days* |
| **Severity 3 (Medium)** | Partial functionality issue / workaround available | Within 1 working day | 3–5 working days* |
| **Severity 4 (Low)** | Cosmetic/UI issues / non-critical improvements | Within 2 working days | Next planned release cycle |

> **\*Important Notes:**
> - All response and resolution times are **target / best-effort timelines**, not guaranteed commitments. The Provider will make commercially reasonable efforts to meet these targets.
> - Resolution times may vary depending on complexity, dependency on third parties, or infrastructure constraints.
> - **No financial penalties** shall be imposed on the Provider for failure to meet target resolution times. The Provider's total liability is limited as stated in Section 16.
> - Response and resolution clocks run only during **business hours** (Section 5) unless the issue is Severity 1 with 24/7 emergency support engaged.

### 6.2 Severity Classification

- Final severity classification shall be **mutually agreed** between the Provider and the Client at the time of issue logging
- In case of disagreement, the **Provider's assessment shall prevail** until reviewed at the next escalation level
- The Provider reserves the right to **reclassify severity** upon investigation if the initial classification is found to be inaccurate

### 6.3 SLA Clock Suspension

The response and resolution timers shall be **automatically paused** when:

- The Provider is awaiting information, access, credentials, or approvals from the Client
- The issue requires action from a third-party vendor or service outside Provider's control
- The Client's infrastructure is unavailable or inaccessible
- The Client requests a hold or postponement of work on a ticket

The clock resumes upon receipt of the required information/access.

### 6.4 Workaround vs. Permanent Fix

- **Resolution** under this SLA may include a **temporary workaround** that restores functionality or unblocks operations, even if a permanent fix is pending
- A workaround that restores business operations will be considered a **valid and complete resolution** for the purpose of SLA timelines
- Permanent fixes for workaround-resolved issues will be scheduled in the next planned release cycle at the Provider's discretion
- The Provider is under no obligation to provide a permanent fix within a specific timeframe once a workaround has been delivered

### 6.5 Fair Usage of Support

- The SLA covers a maximum of **30 support hours per month** for issue resolution and maintenance (excluding minor enhancements defined in Section 2.5)
- Hours are tracked based on tickets logged through official support channels
- If the Client exceeds the monthly support cap, the Provider reserves the right to:
  - Charge additional hours at the CR rate (₹2,000/hour)
  - Defer non-critical tickets to the next month
  - Propose an upgraded support plan
- Unused hours **do not carry over** to subsequent months

### 6.6 Right to Decline

The Provider reserves the right to decline or defer any support request that:

- Falls outside the scope defined in Section 2
- Relates to issues caused by unauthorized changes, infrastructure failures, or third-party dependencies
- Would require effort disproportionate to the SLA fee (e.g., major refactoring disguised as a bug fix)

In such cases, the Provider will communicate the rationale in writing and may offer to address the request as a Change Request (Section 12).

---

## 7. SUPPORT CHANNELS

- **Email Support:** tech@attention.sh
- **Ticketing System** (if applicable)

### 7.1 Official Channel Enforcement

- **Only issues logged through official support channels** (email or ticketing system) will be tracked and counted under this SLA
- Issues communicated verbally, via personal messaging, or informal channels (WhatsApp, phone calls, etc.) will **not** be considered valid SLA tickets unless subsequently logged through official channels
- Each ticket must include: issue description, severity assessment, steps to reproduce, and relevant screenshots/logs

---

## 8. CLIENT RESPONSIBILITIES

The Client agrees to:

- Provide detailed issue descriptions with screenshots/logs where applicable
- Ensure timely access to systems, servers, or credentials when required (within 2 business hours of request for Severity 1; within 1 business day for other severities)
- Nominate a **single point of contact** (SPOC) for coordination
- **Not make unauthorized changes** to codebase, database, or infrastructure. Any such unauthorized changes will void Provider's obligation to resolve resulting issues under this SLA
- Maintain infrastructure (server, internet, third-party tools) in accordance with the Recommended Infrastructure Specification (Section 3.3)
- Ensure adequate data backup procedures are in place (backups are the Client's sole responsibility)

---

## 9. ESCALATION MATRIX

In case of delays or unresolved issues, escalation will follow:

| Level | Role | Target Response Time |
|---|---|---|
| **Level 1** | Support Engineer | As per Section 6.1 |
| **Level 2** | Project Manager | Within 4 business hours of escalation |
| **Level 3** | Senior Management | Within 1 business day of escalation |

Escalation to the next level may be initiated by the Client if the current level has not acknowledged or responded within the above timelines.

---

## 10. EXCLUSIONS

The following are explicitly excluded from this SLA:

- Development of new modules or features
- Major workflow redesign
- New third-party integrations
- Hardware or infrastructure failures
- Issues caused due to misuse, unauthorized changes, or tampering by Client or third parties
- External system/API failures beyond Provider's control
- Database administration tasks (backups, replication, server tuning)
- Data migration or bulk data operations
- Issues arising from Client's failure to maintain Recommended Infrastructure Specifications
- Issues arising from unauthorized modifications to the codebase, database schema, or system configuration by the Client or third parties
- Force majeure events (natural disasters, pandemics, government orders, widespread outages, etc.)
- Any issue that the Provider reasonably determines to be outside the application layer

---

## 11. DATA SECURITY & CONFIDENTIALITY

### 11.1 Confidentiality

- All Client data will be treated as strictly confidential
- No data sharing with third parties without written consent
- Both parties agree to maintain confidentiality of proprietary and business information shared during the term of this Agreement

### 11.2 Access Control

- Provider personnel will access Client systems **only** through authorized credentials provided by the Client
- Access will be limited to personnel directly involved in support and maintenance
- Access will be through **encrypted remote connections** (SSH/VPN) only

### 11.3 Data Handling

- The Provider will **not** copy, export, or store Client data on external systems unless required for troubleshooting, with **prior written approval** from the Client
- Any temporarily copied data will be **securely deleted** within a reasonable timeframe after issue resolution

### 11.4 Security Practices

- The Provider will follow industry-standard security practices including:
  - Encrypted remote access (SSH/VPN)
  - Secure credential handling (no plaintext storage of credentials)
  - Principle of least privilege for all access
  - Multi-factor authentication where supported by Client infrastructure
- The Provider is **not** responsible for:
  - Data backups or disaster recovery
  - Data loss caused by infrastructure failures, Client actions, or external factors
  - Security breaches resulting from Client's failure to maintain secure infrastructure

---

## 12. CHANGE REQUESTS (CR) & NEW FEATURES

Any requirement outside the defined SLA scope — including but not limited to:

- New feature development
- Changes in existing workflows
- Additional reports or dashboards
- Integration with new systems
- Database schema changes or migrations
- Any enhancement exceeding the limits defined in Section 2.5

Will be treated as a **Change Request (CR)**.

### 12.1 Commercial Terms for Change Requests

- All CRs will be charged at a rate of: **₹2,000/hour** (exclusive of applicable taxes)
- Effort estimation will be shared in writing and must be **approved by the Client before execution**
- Work will commence **only after written approval** from the Client
- The Provider's effort estimates are good-faith estimates; actual effort may vary by up to **20%** without requiring additional approval. Overruns beyond 20% will be communicated and require Client approval before proceeding
- CR invoices are payable within **15 days** of invoice date

### 12.2 Delivery Timelines

- Timelines will depend on scope and complexity
- Will be mutually agreed and documented before development begins
- CR work will not affect or delay ongoing SLA support obligations

---

## 13. PAYMENT TERMS

### 13.1 SLA Fee

- **Annual SLA Fee:** ₹1,50,000/- (Rupees One Lakh Fifty Thousand only), **exclusive of applicable GST** (currently 18%)
- **Total payable (inclusive of GST):** ₹1,77,000/- (Rupees One Lakh Seventy-Seven Thousand only)
- **Payment Terms:** 100% advance payment before SLA commencement
- **SLA validity begins only after payment is received and confirmed**
- All amounts stated in this Agreement are exclusive of applicable taxes unless explicitly stated otherwise

### 13.2 Delay in Payment

- If payment is not received within **7 days** of the due date, a written reminder will be sent to the Client
- If payment remains outstanding after **15 days** from the due date, the Provider **will suspend all support services** under this SLA until payment is received
- Any service downtime or issues arising during the suspension period **will not be covered** under the SLA and the Provider shall bear no liability for the same

### 13.3 Reinstatement

- Upon receipt of overdue payment, services will be reinstated within **2 business days**
- The SLA term will **not** be extended to compensate for the suspension period

---

## 14. INTELLECTUAL PROPERTY

### 14.1 Provider IP

- The Provider **retains full ownership** of all intellectual property in the core software, including source code, architecture, libraries, frameworks, tools, and methodologies used in the application
- Nothing in this Agreement shall be construed as a transfer of IP rights from the Provider to the Client
- The Client is granted a **non-exclusive, non-transferable license** to use the software as deployed, for the duration of this Agreement and any subsequent valid agreement

### 14.2 Change Request IP

- Intellectual property created as part of Change Requests (CRs) shall be owned by the **Provider**, unless explicitly agreed otherwise in writing for a specific CR
- Reusable components, libraries, or tools developed during CR execution remain the exclusive property of the Provider

### 14.3 Client Data

- All data entered, generated, or stored by the Client within the system remains the **exclusive property of the Client**
- The Provider shall have no claim over Client data

---

## 15. TERMINATION

### 15.1 Termination by Provider

The Provider may terminate this Agreement with **30 days** written notice in the following circumstances:

- Non-payment of fees beyond **30 days** from due date
- Breach of confidentiality or IP terms by the Client
- Unauthorized modifications to the system by the Client that fundamentally compromise the software
- Client's repeated failure to maintain Recommended Infrastructure Specifications after written notice
- If the Client's support usage consistently exceeds fair usage limits (Section 6.5) and the Client declines an upgraded plan
- Any other material breach of this Agreement by the Client that remains uncured for 15 days after written notice

### 15.2 Termination by Client

The Client may terminate this Agreement with **30 days** written notice. However:

- **No refund** will be provided for the remaining SLA term
- If terminated within the **first 6 months**, the Client shall pay the **full annual SLA fee** (any outstanding balance becomes immediately due)
- Termination does not release the Client from payment obligations for Change Requests already executed or in progress
- All outstanding CR invoices become immediately due and payable upon termination

### 15.3 Post-Termination

- Upon termination, the Provider will:
  - Cease all support services after the notice period
  - Revoke access to Provider's tools or systems (if any)
  - Return or securely delete any Client data in Provider's possession within 30 days
- The Client's license to use the software shall be governed by the original software license agreement (if any), separate from this SLA

---

## 16. LIMITATION OF LIABILITY

- **Total aggregate liability** of the Provider under this Agreement shall **not exceed 50% of the annual SLA fee** actually paid by the Client in the 12 months preceding the claim
- Provider shall **not** be liable for:
  - Indirect, incidental, consequential, special, or punitive damages of any kind
  - Loss of revenue, profits, data, or business opportunities
  - Business interruption or operational losses
  - Data loss due to infrastructure failures, Client actions, or external factors
  - Delays caused by Client's failure to provide timely access, information, or approvals
  - Issues arising from unauthorized changes made by Client or third parties
  - Damages arising from the Client's reliance on the Provider's recommendations
- **This limitation applies regardless of the form of action**, whether in contract, tort, negligence, strict liability, or otherwise, and regardless of whether the Provider was advised of the possibility of such damages
- **No SLA penalties, service credits, or liquidated damages** shall apply under this Agreement. The remedies set forth in the escalation process (Section 9) are the Client's **sole and exclusive remedies** for any service level failures
- The Provider shall have no liability for any period during which services are suspended due to Client's non-payment

---

## 16A. INDEMNIFICATION

- The Client shall **indemnify, defend, and hold harmless** the Provider, its officers, employees, and agents from any claims, losses, damages, liabilities, or expenses (including reasonable legal fees) arising from:
  - The Client's unauthorized modifications to the software, database, or infrastructure
  - The Client's failure to maintain infrastructure as per Recommended Specifications
  - Any third-party claims related to the Client's use of the software or data
  - The Client's breach of any terms of this Agreement
- This indemnification obligation survives termination of this Agreement

---

## 17. RENEWAL

- This Agreement may be renewed annually based on mutual consent, to be confirmed in writing at least **30 days** before expiry
- The Provider **reserves the right to revise** the SLA fee, terms, and scope at the time of renewal. Revised terms will be communicated **30 days prior** to the renewal date
- If no renewal terms are agreed upon before expiry, the Agreement will **lapse** and no support obligations will exist beyond the expiry date
- Renewal is contingent upon clearance of all outstanding dues (SLA fees and CR invoices)

---

## 18. DISPUTE RESOLUTION

- Any dispute arising under this Agreement shall first be attempted to be resolved through **good-faith negotiation** between the parties
- If unresolved within **30 days**, the dispute shall be referred to **arbitration** under the Arbitration and Conciliation Act, 1996, with the seat of arbitration in **Gurugram, Haryana**
- The language of arbitration shall be **English**
- Each party shall bear its own costs of arbitration unless the arbitrator orders otherwise

---

## 19. GOVERNING LAW

This Agreement shall be governed by and construed in accordance with the laws of **India**. The courts of **Gurugram, Haryana** shall have exclusive jurisdiction over any matters not subject to arbitration.

---

## 20. FORCE MAJEURE

- Neither party shall be liable for any delay or failure to perform obligations under this Agreement due to force majeure events including but not limited to: natural disasters, pandemics, epidemics, war, terrorism, riots, government orders, widespread internet/power outages, or any event beyond the reasonable control of the affected party
- The affected party shall notify the other party in writing within **5 business days** of the occurrence of a force majeure event
- If a force majeure event continues for more than **60 consecutive days**, either party may terminate this Agreement with **15 days** written notice, without penalty
- During force majeure, all SLA timelines and obligations shall be suspended
- **No refund** of SLA fees shall be provided for the force majeure suspension period

---

## 21. NOTICES

- All formal notices under this Agreement (including payment reminders, termination notices, and dispute communications) shall be delivered via:
  - **Email** to the designated contact addresses of each party, **AND**
  - **Registered post / courier** to the registered address of the party
- A notice shall be deemed delivered:
  - On the date of email delivery (with read receipt or delivery confirmation), OR
  - 3 business days after dispatch via registered post/courier, whichever is earlier
- Designated contacts:
  - **Provider:** Amit Joshi, COO — [email to be specified]
  - **Client:** [SPOC name] — [email to be specified]
- Either party may update their designated contact by providing 7 days written notice

---

## 22. ENTIRE AGREEMENT & AMENDMENTS

- This Agreement (together with its Annexures) constitutes the **entire agreement** between the parties with respect to the subject matter hereof and **supersedes all prior** discussions, negotiations, representations, and agreements (whether written or oral)
- No amendment, modification, or waiver of any provision of this Agreement shall be effective unless made in **writing and signed by authorized representatives** of both parties
- The failure of either party to enforce any provision of this Agreement shall not be construed as a waiver of such provision or the right to enforce it at a later time
- If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect (**severability**)

---

## 23. ACCEPTANCE

By signing below, both parties acknowledge and agree to the terms and conditions outlined in this Service Level Agreement.

**For Jina Code Systems**

- **Name:** Amit Joshi
- **Designation:** COO
- **Signature:** _________________________
- **Date:** 25/03/2026

**For Scan4Health**

- **Name:** ____________________________
- **Designation:** ______________________
- **Signature:** _________________________
- **Date:** _____________________________

---

## ANNEXURE A: KNOWN ISSUES REGISTER

| # | Issue Description | Severity | Date Identified | Remarks |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

*To be completed during Pre-SLA System Audit (Section 3)*

**Acknowledged by Provider:** _________________ **Date:** ___________

**Acknowledged by Client:** _________________ **Date:** ___________

---

## ANNEXURE B: RECOMMENDED INFRASTRUCTURE SPECIFICATION

| Component | Minimum Specification |
|---|---|
| Server OS | |
| CPU | |
| RAM | |
| Storage | |
| Network | |
| Database | |
| Other | |

*To be completed during Pre-SLA System Audit (Section 3)*

---

## CHANGE LOG

| Version | Date | Description | Author |
|---|---|---|---|
| 1.0 | 25/03/2026 | Initial SLA draft | Jina Code Systems |
| 2.0 | 25/03/2026 | Revised SLA with risk mitigations | Jina Code Systems |
| 3.0 | 25/03/2026 | Provider-protective hardening: clock pause, fair usage caps, GST, holidays, indemnity, force majeure, entire agreement, notices | Jina Code Systems |
