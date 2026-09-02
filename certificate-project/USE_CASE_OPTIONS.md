# New Use-Case Options

Choose one of these scenarios or propose your own. These are starting points,
not completed evaluation designs. You must define the cases, scorers, rubric,
version change, and operating policy yourself.

Do not reuse BeeVerse/PatchPilot as the certificate-project use case.

## Option 1: Refund Resolution Agent

### Situation

An online retailer uses an AI agent to review refund requests. The agent reads
the request, order details, customer identity, refund policy, and prior account
activity. It recommends approving the refund, denying it, or sending it to a
person.

### Possible inputs

- Requesting customer ID.
- Order ID and order owner.
- Purchase amount and requested refund amount.
- Purchase and delivery dates.
- Refund reason.
- Current refund policy.
- Prior refund or retry records.

### Possible output

A structured recommendation containing the decision, refund amount, policy
evidence, confidence, and whether human review is required.

### Risks to investigate

- Refunding an order owned by another customer.
- Exceeding the amount permitted by policy.
- Issuing a duplicate refund after a retry.
- Approving a request when required evidence is missing.
- Producing a plausible explanation that is unsupported by the policy.

## Option 2: Employee Policy Assistant

### Situation

An internal AI assistant answers employee questions using approved company
policies. It retrieves relevant documents and produces an answer with citations
or routes the question to the appropriate team.

### Possible inputs

- Employee question.
- Employee location or employment type when relevant.
- Retrieved policy passages.
- Policy version and effective date.
- Access permissions.

### Possible output

A structured answer containing the response, citations, policy version,
confidence, and escalation recommendation.

### Risks to investigate

- Answering from an expired policy.
- Returning a citation that does not support the claim.
- Answering confidently when no relevant source was retrieved.
- Revealing a policy or document the employee cannot access.
- Giving an incomplete answer to an ambiguous question.

## Option 3: Expense Review Agent

### Situation

A finance team uses an AI agent to review employee expenses. The agent reads
the expense, receipt, policy, and prior submissions, then recommends approval,
rejection, or human review.

### Possible inputs

- Employee and expense IDs.
- Amount, date, category, and business purpose.
- Receipt data.
- Applicable expense policy.
- Prior or potentially duplicate submissions.
- Manager or cost-center information.

### Possible output

A structured recommendation containing the decision, policy checks, evidence,
confidence, and review reason.

### Risks to investigate

- Approving an expense above a policy limit.
- Approving the same expense twice.
- Treating a missing receipt as evidence that the expense is valid.
- Applying the wrong policy or currency.
- Accepting a vague business purpose without review.

## Propose your own use case

Your own scenario is acceptable when it has all of the following:

- A named user or team.
- A bounded agent task or recommendation.
- Inspectable inputs and outputs.
- At least one exact requirement suitable for deterministic scoring.
- At least one nuanced requirement suitable for a written rubric.
- A meaningful reason to distinguish automatic operation, human review, and
  blocking.
- Fictional or sanitized data that is safe to show in a video.

Prefer a narrow workflow over a broad assistant. For example, “recommend a
refund for one order” is easier to evaluate than “improve customer service.”

If your scenario involves employment, finance, health, legal, or another
high-impact domain, keep the project fictional and make the agent recommend or
route decisions rather than claiming it should operate without appropriate
professional oversight.

## Choosing the V1-to-V2 change

Choose one targeted change that could plausibly affect the failure you want to
measure. Examples include:

- A clearer instruction or prompt.
- A customer, permission, or policy constraint.
- A retrieval-source filter.
- A validation step.
- A new bounded tool.
- A different model.

Change only one declared dimension. If several things change at once, the
evaluation cannot clearly tell you what caused the result to move.
