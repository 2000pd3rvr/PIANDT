# Triadic Information Architecture and Signal Navigation Framework

## Field of the Invention
An **information‑based organisational structure and modelling framework** that serves as a **blueprint for both physical and electronic organisational site design and structuring**. This includes, but is not limited to, digital user interfaces (websites, intranets, dashboards) and the underlying organisational units, processes, and spaces they represent. The concept creates a **clear blueprint for 360-degree organisational information systems**, whether this concept is implemented on an electronic site or a physical organisational site.

## Background
Conventional organisational websites and sites (both physical and electronic) are typically arranged according to static, role-agnostic sections such as *Home*, *About*, *Services*, and *Contact*. These menu structures mirror content silos and departments rather than the actual flow of information and decisions through the organisation.

As a result:
- Users are not shown how their interactions move from *input* to *processing* to *outcome*.
- Different parts of the site use unrelated child categories, making it difficult to understand where a given request or signal sits in its life-cycle.
- The same type of interaction (for example, a job enquiry or a complaint) is scattered across multiple unconnected pages.

There is therefore a need for an information-based structure that represents organisational activity as a *natural order of information processing*, and that can be used as a common blueprint for both digital interfaces and underlying organisational design.

## Summary
The invention provides a **Triadic Information Architecture and Signal Navigation Framework** based on three primary stages:
- **In**: inbound intents, requests, and signals.
- **Proc**: internal handling, evaluation, and decision-making.
- **Out**: outbound results, outcomes, and published artefacts.

Each stage exposes the **same shared set of child categories** (for example: organisational units such as Machine Intelligence Unit, and their associated categories such as products, services, and sub-categories such as vision, research, consultancy, software, and education), forming a triadic matrix that maps each interaction type across its life-cycle from In to Proc to Out.

Unlike conventional architectures that group content purely by topic or department, this triadic framework organises navigation according to the **natural order of information processing**---from inbound signals (**In**), through internal transformation (**Proc**), to outbound results (**Out**). This explicit In→Proc→Out triad provides a **first-of-its-kind conceptual scaffold** for organisational sites, aligning the user's mental model with the actual life-cycle of information and decisions within the organisation.

The same triadic model can be applied to the underlying organisational structure, aligning units, roles, and key performance indicators (KPIs) with the In, Proc, and Out stages. This yields a more resilient and "fit" organisational information system that is easier to measure, manage, and scale. The framework provides a **clear blueprint for 360-degree organisational information systems**, whether implemented on an electronic site or a physical organisational site, ensuring comprehensive coverage of all organisational operations and signal interactions.

The triadic structure is founded on a scientific principle of signal proportionality: **the total signal received (In) is proportional to the total signal being processed (Proc), which is in turn proportional to the total signal output (Out)**. The level of proportionality, whether linear or non-linear, varies with the nature of the signal, but the fundamental relationship remains proportional. This scientific foundation explains why categories are mirrored across all three stages: every type of incoming signal must have a corresponding processing pathway and output mechanism, maintaining balance and completeness in the organisational information system.

## Detailed Description

### Triadic top-level navigation and structure

The triadic framework can be implemented in two primary modalities: **electronic sites** (digital interfaces) and **physical sites** (spatial organisational structures). Both implementations maintain the same triadic structure, with stage-specific adaptations.

#### Electronic site implementation

In electronic implementations, a digital organisational interface (for example, a website, intranet, or dashboard) presents a persistent navigation bar containing three primary nodes:
- **In** -- representing inbound interactions such as applications, partnership offers, feedback, complaints, ideas, support requests, and information requests.
- **Proc** -- representing internal operations that act on those inbound items, including triage, routing, decision-making, and execution.
- **Out** -- representing externally visible results, including responses, published artefacts, decisions, reports, and other outcomes.

These nodes represent the natural order in which information and signals flow through an organisational information system: first arriving (*In*), then being handled internally (*Proc*), then generating observable results (*Out*).

**Implementation Structure:** In a current implementation, the triadic framework is structured as follows:
- **Directory Structure:** The electronic site implements the triad through directory paths: `in/` for inbound signals, `processing/` for internal processing (displayed as "Proc" in navigation), and `out/` for outbound results.
- **Section Organization:** Under each triad directory, the system organizes content into consistent sections such as `about_piandt/` (organisational information) and `units/` (organisational units), with each section maintaining the same structure across In, Proc, and Out.
- **File Naming Convention:** Files follow a consistent naming pattern where each file is prefixed with its triad identifier: `in_` for In files, `proc_` for Proc files, and `out_` for Out files (e.g., `in_about_piandt.html`, `proc_about_piandt.html`, `out_about_piandt.html`).
- **Child Menu Structure:** Each section maintains consistent child menus across the triad. For example, the `about_piandt/` section includes child categories such as: our mission and vision, charitable purposes, our approach, trustees, and governance, with the same categories appearing under In, Proc, and Out stages.

#### Physical site implementation

In physical implementations, the triadic structure is manifested through spatial organisation and operational workflows:
- **In** -- physical spaces and processes for receiving inbound signals, such as reception areas, mail rooms, intake desks, and designated entry points for different signal types.
- **Proc** -- internal spaces and workflows for handling received signals, such as processing centers, evaluation rooms, decision-making areas, and internal routing systems.
- **Out** -- physical spaces and processes for delivering outbound results, such as output distribution centers, delivery areas, publication spaces, and communication hubs.

The physical implementation maintains the same triadic mapping as the electronic version, with spatial organisation reflecting the signal processing lifecycle. Physical sites may incorporate signage, wayfinding systems, and spatial layouts that mirror the electronic navigation structure, enabling users to navigate physical spaces using the same triadic mental model.

### Mirrored child menus (triadic matrix) and scientific foundation

Under each of the three primary nodes, the system exposes the same shared set of organisational units and categories. In one embodiment, the system is structured around organisational units (for example, Machine Intelligence Unit, or MIU), with each unit having consistent sub-categories across the triad.

For example, under each of In, Proc, and Out, the system may expose:
> machine intelligence (or MIU), products, services, vision, research, consultancy, software, education.

**Current Implementation Example:** In a current implementation, the triadic structure includes:
- **Primary Sections:** `about_piandt/` (organisational information) and `units/` (organisational units)
- **About PIANDT Child Categories:** our mission and vision, charitable purposes, our approach, trustees, governance
- **Units Structure:** Organisational units such as Machine Intelligence Unit (MIU), with sub-categories including products and services, where services further includes vision, and vision includes research, consultancy, software, and education
- **Consistent Naming:** All categories maintain lowercase naming conventions (e.g., "our approach" rather than "Our Approach") to ensure consistency across the triadic matrix

The structure forms a hierarchical navigation where each level maintains triadic mapping:
- **Organisational Units** (e.g., Machine Intelligence Unit) appear under In, Proc, and Out, representing the unit's inbound signals, processing activities, and outbound results respectively.
- **Primary Categories** (e.g., products, services) appear consistently under each unit across the triad.
- **Sub-categories** (e.g., vision under services, and research, consultancy, software, education under vision) maintain the same hierarchical structure across In, Proc, and Out.

The semantics of each category are specific to the stage:
- Under **In**, categories represent incoming signals, requests, and communications (e.g., product inquiries, service requests, research collaboration inquiries).
- Under **Proc**, the same categories represent internal workflows handling those items (e.g., analyzing product inquiries, processing service requests, evaluating research collaborations).
- Under **Out**, the same categories represent externally visible outcomes (e.g., product responses, service deliverables, research outcomes).

This gives rise to a three-by-N hierarchical matrix in which each category and sub-category can be traced across its entire life-cycle:
```
In(unit/category) → Proc(unit/category) → Out(unit/category)
```

The triadic matrix makes the life-cycle of interactions transparent to users and decision-makers, with the hierarchical structure enabling navigation through multiple levels of organisational granularity.

#### Scientific theory of signal proportionality

The triadic navigation structure and mirrored child categories are founded on a scientific principle of signal proportionality within organisational information systems. This principle states that:

**The total signal received (In) is proportional to the total signal being processed (Proc), which is in turn proportional to the total signal output (Out).**

Mathematically: S_In ∝ S_Proc ∝ S_Out

The level of proportionality may be linear or non-linear, and varies with the nature of the signal:
- **Linear proportionality** may apply to signals that undergo straightforward transformation (e.g., simple information requests that generate direct responses).
- **Non-linear proportionality** may apply to signals that require complex processing, aggregation, or transformation (e.g., research collaborations that generate multiple publications, or product inquiries that lead to customised solutions).

Regardless of whether the relationship is linear or non-linear, the fundamental principle of proportionality holds: every signal that enters the system (In) must be processed (Proc) and must generate an output (Out), maintaining a consistent relationship across the three stages.

This scientific foundation explains why categories are mirrored across In, Proc, and Out:
- If a category exists at the In stage (e.g., "research" signals are received), then by the principle of signal proportionality, there must be a corresponding Proc stage for those signals (e.g., research collaboration processing) and a corresponding Out stage (e.g., research outcomes).
- The mirrored structure ensures that the organisational system maintains balance and completeness: every type of incoming signal has a defined processing pathway and a defined output mechanism.
- The triadic matrix structure reflects the inherent proportionality of information flow, making the relationship between input, processing, and output explicit and navigable.

This scientific principle provides the theoretical foundation for the triadic framework, ensuring that the mirrored category structure is not merely a design choice but a reflection of the fundamental nature of information processing within organisational systems.

### Minimal surface embodiment and hierarchical navigation

In a preferred electronic embodiment, the primary page surface is reduced to a single hero statement (for example, "people, innovation and technology"), with minimal or no scrollable sections. The triadic navigation bears most of the semantic load: users access specific life-cycle views of each interaction type via the In, Proc, and Out menus and their hierarchical child categories.

The navigation structure supports multi-level hierarchies, where each level maintains triadic consistency. For example, a navigation path may be represented as:
> In → Machine Intelligence Unit → services → vision → research

where each segment in the path is a clickable link to its corresponding page, and the same hierarchical path structure is maintained under Proc and Out. This creates a breadcrumb-like navigation system where users can navigate to any level of the hierarchy while maintaining awareness of their position within the triadic structure.

**Current Implementation Path Examples:**
- `in/about_piandt/in_about_piandt.html` → `processing/about_piandt/proc_about_piandt.html` → `out/about_piandt/out_about_piandt.html`
- `in/units/miu/in_miu.html` → `processing/units/miu/proc_miu.html` → `out/units/miu/out_miu.html`
- `in/units/miu/vision/in_miu_vision.html` → `processing/units/miu/vision/proc_miu_vision.html` → `out/units/miu/vision/out_miu_vision.html`

Each path maintains the same hierarchical structure across the triad, with only the triad identifier (in/proc/out) and file prefix (in_/proc_/out_) changing between stages.

#### Triadic Matrix Structure: Example Category Mapping

| Category | In Stage | Proc Stage | Out Stage |
|----------|----------|------------------|-----------|
| Research | Research collaboration inquiries, project proposals, academic partnership requests | Analyzing proposals, evaluating collaborations, processing research agreements | Research outcomes, published papers, collaboration results |
| Consultancy | Advisory service requests, strategic consulting inquiries | Proc consultancy requests, developing advisory frameworks | Consultancy deliverables, strategic reports, advisory outcomes |
| Software | Software development requests, custom solution inquiries | Analyzing requirements, developing software solutions, testing implementations | Software products, deployed solutions, technical documentation |
| Education | Training program inquiries, educational course requests | Proc enrollment, developing curricula, managing educational programs | Educational outcomes, course completions, certification deliverables |

### Customisation, refinement, and accessibility

The shared child categories can be customised:
- **Refined/shortened** by collapsing multiple categories into a smaller, simplified set (for example, merging feedback, complaints, and suggestions into "feedback") to reduce cognitive load.
- **Expanded** into more granular sub-categories (for example, splitting "work" into "employment", "consulting", and "volunteering") to meet accessibility requirements, regulatory obligations, or the needs of specific audiences.

In all cases, the triadic mapping is preserved: each refined or expanded category maintains its representation across In, Proc, and Out.

### Access control and information visibility

Through the In→Proc→Out concept, information may be subject to different access levels and visibility controls. Some information may be designated for public access and displayed publicly, while other information may be restricted to internal use, specific user roles, or authenticated access only.

Regardless of access level or visibility, all information belongs to its appropriate category within the triadic framework:
- Information that is not meant for public access may be categorised under In, Proc, or Out but displayed only to authorised users or kept internal to the organisation.
- Publicly accessible information is similarly categorised within the triadic structure but made visible to all users.
- The same category (for example, "research" under "services" under "vision") may contain both public and restricted information, with access controls determining what is displayed to each user based on their permissions.

This access control mechanism ensures that the triadic organisational structure remains consistent and complete, regardless of information visibility. The framework maintains the integrity of the In→Proc→Out lifecycle mapping while supporting granular access control at the content level, enabling organisations to manage sensitive information appropriately while preserving the triadic structure.

### Implementation comparison: Electronic versus physical sites

The following table provides a systematic comparison of electronic and physical site implementations, demonstrating how the triadic framework adapts to different modalities while maintaining structural consistency.

| Aspect | Electronic Site | Physical Site |
|--------|-----------------|---------------|
| **In Stage** | Digital interfaces for signal reception: web forms, email systems, API endpoints, digital intake portals | Physical spaces for signal reception: reception areas, mail rooms, intake desks, designated entry points |
| **Proc Stage** | Automated workflows, agentic systems, digital routing, algorithmic decision-making, database operations | Physical processing centers, evaluation rooms, decision-making areas, manual routing systems, workflow stations |
| **Out Stage** | Digital outputs: web pages, email responses, API responses, published documents, automated reports | Physical outputs: printed materials, delivery areas, publication spaces, communication hubs, distribution centers |
| **Navigation** | Persistent navigation bars, dropdown menus, hierarchical links, breadcrumb trails, search interfaces | Spatial wayfinding, signage systems, floor plans, directional indicators, physical routing guides |
| **Automation** | High automation potential: agentic systems can execute up to 80% of automatic tasks, 24/7 operation | Lower automation: primarily manual processes with potential for automated routing and tracking systems |
| **Scalability** | Virtually unlimited scalability through cloud infrastructure and distributed systems | Limited by physical space constraints, requiring expansion or relocation for significant growth |
| **Access Control** | Granular digital permissions, role-based access, authentication systems, encryption | Physical security measures, access cards, restricted areas, visitor management systems |

### Organisational structure alignment and strategic benefits

Beyond site-specific implementations, the same triadic framework can be applied as a core organisational structuring principle. In such embodiments:
- "In" functions focus on sensing, acquiring, and prioritising inputs (opportunities, risks, requests, ideas).
- "Proc" functions focus on transforming those inputs into decisions, actions, and artefacts.
- "Out" functions focus on communicating, delivering, and monitoring outcomes back to stakeholders.

Governance, reporting lines, and metrics can be aligned along the triad, producing organisational information systems that are more resilient and adaptable to change. Because each stage and category is explicitly represented, the organisation becomes easier to measure (per stage and category), manage (via clear hand-offs between stages), and scale (by expanding specific triad lanes rather than re-architecting the whole system).

#### Strategic advantages for modern organizations

The triadic framework provides substantial strategic advantages for contemporary organizations operating in complex, information-intensive environments:

**1. Enhanced Operational Transparency and Accountability**
The explicit In→Proc→Out mapping creates unprecedented visibility into organizational processes, enabling stakeholders to trace any signal, request, or interaction through its complete lifecycle. This transparency facilitates:
- Clear accountability at each stage of information processing
- Rapid identification of bottlenecks or inefficiencies in signal flow
- Enhanced auditability for regulatory compliance and governance requirements
- Improved stakeholder trust through demonstrable process visibility

**2. Scalable Organizational Architecture**
Modern organizations face constant pressure to adapt, expand, or restructure in response to market dynamics, regulatory changes, or strategic pivots. The triadic framework provides a scalable architecture that:
- Enables incremental expansion by adding new categories or units without system-wide re-architecture
- Maintains structural consistency during organizational growth or restructuring
- Reduces technical debt by providing a stable, extensible foundation for information systems
- Supports organizational agility through predictable, modular expansion patterns

**3. Optimized Resource Allocation and Performance Measurement**
The triadic structure enables precise measurement and optimization of organizational performance at granular levels:
- Stage-specific metrics (In, Proc, Out) provide actionable insights into organizational efficiency
- Category-level performance indicators enable targeted resource allocation
- Proportional signal relationships (S_In ∝ S_Proc ∝ S_Out) provide early warning systems for organizational imbalances
- Data-driven decision-making through quantifiable signal flow analysis

**4. Reduced Cognitive Load and Improved User Experience**
The consistent triadic structure across all organizational touchpoints reduces cognitive overhead for both internal stakeholders and external users:
- Predictable navigation patterns reduce training requirements and support costs
- Consistent mental models across digital and physical spaces improve wayfinding and task completion
- Reduced decision fatigue through clear, hierarchical information architecture
- Enhanced accessibility through systematic, logical organization of information

**5. Integration with Modern Technology Stacks**
The triadic framework is inherently compatible with contemporary technology architectures:
- RESTful API design naturally maps to In (POST), Proc (PUT/PATCH), and Out (GET) operations
- Microservices architectures can be organized along triadic boundaries
- Event-driven systems align with signal flow from In through Proc to Out
- Machine learning and AI systems can leverage the triadic structure for training data organization and model deployment

**6. Regulatory Compliance and Risk Management**
The explicit signal lifecycle mapping supports comprehensive compliance and risk management:
- Complete audit trails for all organizational interactions
- Clear data lineage from input through processing to output
- Simplified compliance reporting through stage-specific data categorization
- Enhanced risk assessment through visibility into signal processing pathways

### Electronic implementation with agentic systems and automation benefits

In electronic implementations, the triadic framework can be enhanced through **agentic systems** that automate a significant portion of organisational tasks. Specifically, the electronic version implements agentic systems that can execute up to **80% of automatic tasks**, leaving the remaining **20% for administrative sign-off**. This automation capability enables the organisational information system to operate **24/7 with limited human resources**, significantly enhancing operational efficiency, productivity, and system throughput. The triadic structure provides the necessary framework for these agentic systems to understand and navigate the complete information processing lifecycle, from inbound interactions through processing to outbound results, ensuring that automated tasks are properly routed, handled, and completed within the appropriate stage and category of the organisational matrix.

The agentic systems leverage the triadic matrix structure to:
- Automatically route incoming signals (In) to appropriate processing workflows based on category classification.
- Execute processing tasks (Proc) within the correct organisational unit and category context.
- Generate and deliver outputs (Out) that maintain consistency with the triadic structure and signal proportionality principles.

This automated implementation demonstrates the scalability and efficiency advantages of electronic sites over physical sites, while maintaining the same triadic structural principles.

#### Quantifiable business value for modern organizations

The integration of agentic systems within the triadic framework delivers measurable business value:

**Operational Efficiency Gains:**
- **80% automation rate** reduces human resource requirements for routine signal processing tasks
- **24/7 operation** eliminates temporal constraints on organizational responsiveness
- **Reduced processing latency** through automated routing and execution within the triadic structure
- **Consistent quality** through systematic application of organizational rules and workflows

**Cost Optimization:**
- Significant reduction in operational overhead through automation of high-volume, low-complexity tasks
- Scalable infrastructure that grows incrementally with organizational needs rather than requiring periodic major investments
- Reduced training costs through consistent, predictable system architecture
- Lower maintenance costs through systematic organization and clear signal pathways

**Competitive Advantages:**
- Faster response times to stakeholder inquiries and market signals
- Enhanced organizational agility through systematic, scalable architecture
- Improved customer experience through consistent, predictable interaction patterns
- Better resource utilization through data-driven optimization of signal processing workflows

**Risk Mitigation:**
- Reduced human error through automated processing of routine tasks
- Enhanced compliance through systematic tracking of all signals through their complete lifecycle
- Improved auditability through explicit In→Proc→Out mapping
- Better disaster recovery through structured, replicable organizational processes

## Example Claims (Draft)

1. A method of organising content and navigation in an organisational information system interface, configured to reflect the natural order of information processing within the organisation, comprising: defining three primary navigation sections representing inbound signals (In), internal processing (Proc), and outbound results (Out); and defining a shared set of child categories representing types of signal interactions; wherein each of the three primary sections exposes the shared set of child categories, and wherein each instance of a child category in a given primary section presents information specific to that stage of the signal processing life-cycle.

2. The method of claim 1, wherein the shared set of child categories comprises organisational units (e.g., Machine Intelligence Unit) and their associated categories such as products, services, and sub-categories such as vision, research, consultancy, software, and education, with the same hierarchical structure maintained across In, Proc, and Out.

3. The method of claim 1, wherein the organisational information system interface presents a minimal surface comprising a concise hero statement and relies primarily on the triadic navigation and its child categories for semantic organisation.

4. The method of claim 1, wherein selecting a child category under the In section provides options for initiating a corresponding signal type, selecting the same child category under the Proc section provides status of internal processing for that signal type, and selecting the same child category under the Out section provides externally visible results for that signal type.

5. The method of claim 1, wherein the triadic navigation is presented in a persistent navigation bar, and the child categories are displayed as dropdown or expandable menus for each of the three primary sections.

6. The method of claim 1, wherein the mapping of child categories across the three primary sections forms a triadic matrix representation of signal processing within organisational information systems, enabling a user to understand, from the navigation alone, the life-cycle of each signal type through the In→Proc→Out pipeline.

7. A non-transitory computer-readable medium storing instructions which, when executed by one or more processors, cause a computing system to display an organisational information system interface according to any of claims 1-6.

8. The method of any preceding claim, wherein the shared set of child categories is configurable such that multiple categories may be collapsed into a shorter, simplified list and/or expanded into more granular sub-categories while maintaining a consistent triadic mapping of each resulting category across the In, Proc, and Out sections to support accessibility and audience-specific navigation needs.

9. The method of any preceding claim, wherein the triadic model used in the digital user interface is applied to the internal organisational structure such that organisational units and performance indicators are aligned with inbound activities, processing activities, and outbound activities respectively, thereby facilitating improved measurement, management, and scalable growth of the organisation's information system operations.

10. The method of any preceding claim, wherein information within the triadic structure may be subject to different access levels and visibility controls, such that some information may be publicly accessible while other information may be restricted to internal use or specific user roles, and wherein all information, regardless of access level, maintains its appropriate categorisation within the In, Proc, and Out framework.

11. The method of any preceding claim, wherein the triadic navigation structure and mirrored child categories are founded on a scientific principle of signal proportionality, wherein the total signal received (In) is proportional to the total signal being processed (Proc), which is in turn proportional to the total signal output (Out), and wherein the level of proportionality, whether linear or non-linear, varies with the nature of the signal but maintains a consistent proportional relationship, thereby explaining why categories are mirrored across all three stages to ensure that every type of incoming signal has a defined processing pathway and output mechanism.

12. The method of any preceding claim, wherein the triadic framework is implemented in an electronic site modality, comprising digital interfaces, automated workflows, and agentic systems capable of executing up to 80% of automatic tasks, enabling 24/7 operation with limited human resources.

13. The method of any preceding claim, wherein the triadic framework is implemented in a physical site modality, comprising spatial organisation, physical workflows, and manual or semi-automated processes, with wayfinding systems and spatial layouts that mirror the electronic navigation structure.

14. The method of any preceding claim, wherein the triadic framework provides strategic advantages for modern organizations including: enhanced operational transparency and accountability through explicit signal lifecycle mapping; scalable organizational architecture enabling incremental expansion without system-wide re-architecture; optimized resource allocation through stage-specific and category-level performance metrics; reduced cognitive load through consistent navigation patterns across digital and physical spaces; integration compatibility with modern technology stacks including RESTful APIs, microservices, and event-driven architectures; and comprehensive regulatory compliance support through complete audit trails and data lineage tracking.

15. The method of any preceding claim, wherein the integration of agentic systems within the triadic framework delivers quantifiable business value including: operational efficiency gains through 80% automation of routine tasks and 24/7 operation; cost optimization through reduced operational overhead and scalable infrastructure; competitive advantages through faster response times and enhanced organizational agility; and risk mitigation through reduced human error, enhanced compliance, and improved disaster recovery capabilities.
