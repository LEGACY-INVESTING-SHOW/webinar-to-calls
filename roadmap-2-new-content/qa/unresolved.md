# Unresolved facts and professional review

This list comes from the eight research logs in `parts/sources-*.md`, which hold the claim-by-claim detail. Check every item before recording the lesson that uses it.

## How the sources were checked

This cloud environment's network policy blocked direct page fetches from airbnb.com, irs.gov, consumerfinance.gov, fanniemae.com, nyc.gov, lacity.gov, help.vrbo.com, kiavi.com and most other official sites. Every rule in the lessons was checked against the official domain through a web-search tool restricted to that domain. The tool returns summaries of the page, not the page itself. The session's search budget (200 searches) ran out near the end of research, and several late items could not be checked at all.

What this means for production:

1. Open each linked official page once in a normal browser before recording, and confirm the sentence it supports. The full list is in `qa/url-list.txt`. The lessons avoid quoting a page word for word unless a summary gave the exact wording.
2. Treat every item below as open until the named person confirms it.

## Platform and product checks (production team)

| Item | Lessons | Check |
|---|---|---|
| Airbnb co-host permission level names and what each allows | 6.5, OP.7 | Open help 1534 and the live co-host settings screen |
| Which Airbnb page says co-hosts can't see or change payout and taxpayer info; the co-host payout base ("host's earnings") | 6.5, OP.7 | Help 3389 and 1534 |
| Where the permit or registration field sits in Airbnb's host screens | 3.3 | Help 3953 and the live screen |
| What Airbnb does when a permit number expires or fails verification, outside NYC and LA | 3.3 | Help 3953 and the target city's Airbnb page |
| Whether Airbnb includes the cleaning fee in the taxable base where it collects occupancy tax | 3.3 | Help 1036 |
| Whether help 39 names "host behavior" as a separate search factor (the brief says so; the summary did not) | OP.9 | Read help 39 directly |
| Airbnb device rules (help 3061) and the indoor-camera ban wording | OP.6, OP.8 | Read help 3061 directly |
| Whether AirCover applies to bookings made off Airbnb (lessons read it as Airbnb stays only) | PA.12, 5.7 | Help 3733 and the insurer |
| Vrbo occupancy-tax collection in Los Angeles | SR.1 | Vrbo tax help pages |
| AirDNA 2026 outlook figures (occupancy about -1%, ADR +1.5%, RevPAR +0.5%) and the midyear update figures | 1.3 | Open the AirDNA outlook and midyear pages |
| Whether the CPSC vacation-rental PDF contains every cited safety bullet | OP.6, OP.8 | Open the PDF |
| CFPB page attributions where the search summary mixed several pages (en-1907, en-184) | PA.11 | Open each page |
| FinCEN beneficial ownership reporting status for domestic LLCs | PA.10 | Recheck FinCEN before recording |
| Vendor pricing for PMS, pricing, and messaging tools (left blank on purpose) | SR.5 | The student, from vendor quotes |
| What the STR Concierge team provides to members | 0.1 | Program owner; Preston states it on the recording |

## Local government and attorney

| Item | Lessons | Who confirms |
|---|---|---|
| NYC: "two guests" vs "two paying guests"; the registration term (a summary said "up to four years", or until lease end for tenants) | 3.1, 3.3, SR.1 | NYC Office of Special Enforcement pages or OSE |
| Whether an NYC or LA registration can transfer to a new operator (the lessons infer it can't from the eligibility rules) | 3.1, 3.4, SR.1 | OSE; LA City Planning; STR attorney |
| LA fees ($89 Home-Sharing, $850 and $5,660 Extended Home-Sharing) from a City Planning FAQ that may be out of date | 3.1, SR.1 | LA City Planning fee schedule |
| LA Extended Home-Sharing criteria beyond the six-month registration rule; responsible-contact response time; safety rules taken partly from a draft ordinance | 3.1, SR.1 | LA City Planning; adopted Ordinance 185,931 and its guidelines |
| Whether LA adopted a route for non-primary residences (the draft Vacation Rental Ordinance) | 3.4, SR.1 | LA City Planning in writing; LA STR attorney |
| LA landlord authorization form (only its title was seen) | 3.5 | Open the current form |
| NY Real Property Law 226-b and how it applies to a given lease | 3.5 | New York attorney |
| Sample consent and addendum clauses in 3.5 (illustrative, not reviewed) | 3.5, 5.7 | Attorney in the property's state; align with updated lesson 5.3 |
| Whether a paid helper, co-host, or manager needs a real estate or management license (Tennessee is the only state example checked) | 6.5, OP.7 | State licensing board; attorney |
| Earnest money, contingency, and appraisal-gap mechanics | PA.8, PA.9 | Licensed agent and real estate attorney in the state |
| Prepayment penalty enforceability by state | PA.6, PA.7 | Lender and attorney |
| Deeding the property to an LLC after closing (due-on-sale and lender consent) | PA.10 | Lender and attorney |
| Local alarm, extinguisher, occupancy, and egress rules; CO-alarm first actions; severe-weather alert source | OP.6, OP.8, PA.12 | Local fire marshal, building department, emergency management office |
| The unnamed city (Alder Street), the "Alder City" tax rates, and Cedar Ridge's county rules (septic bedroom count, occupancy cap) | 1.3, 3.3, 3.4, PA.9 | These are teaching assumptions, not real rules. Keep them labeled. |

## Lender

| Item | Lessons |
|---|---|
| Fannie Mae B3-3.8-03 (STR income): the section and the November 1, 2026 application-date requirement are confirmed. Not confirmed: which occupancy types and transactions qualify, required history, accepted alternative documents, and the income calculation. PA.7.4 has a production note for the lender reviewer | PA.7, 0.3 |
| Fannie Mae reserve months for a one-unit investment purchase (lessons use 6 months of PITIA as a labeled assumption) and the 2% of UPB tier for other financed properties | 0.3, PA.1 |
| Kiavi's STR specifics: income sizing with no history, minimum score, maximum LTV, guarantee terms, reserve and prepayment statements by product | PA.6 |
| Whether DSCR lenders require a personal guarantee on LLC loans | PA.6, PA.10 |
| Seller-contribution limits for investment properties (B3-4.1-02) and whether a credit can fund repairs | PA.8 |
| Loan sized on the lower of price or appraised value (B2-1.2-01) | PA.8, PA.9 |
| Whether a business-purpose DSCR loan gets a Loan Estimate and Closing Disclosure (and the three-day rule), or a term sheet and settlement statement; fee tolerance rules; the appraisal-copy rule for business-purpose credit | PA.7, PA.9, PA.11 |
| Whether a conventional investment loan carries a prepayment penalty | PA.7 |
| HELOC terms: combined LTV limit (80% is an assumption), index and margin, interest-only draw payments, repayment term | OP.11, 0.3 |

## CPA

| Item | Lessons |
|---|---|
| 27.5-year vs 39-year recovery period for a single-family STR with a 3.5-night average stay (the canonical example shows both and uses 39) | 0.2, SR.3, OP.12 |
| Material participation: hour thresholds, whether spouses' hours combine, and whether the 7-day average-stay rule takes the activity out of the rental category | 0.2, 0.3, PA.10, SR.3 |
| Whether the $25,000 active-participation allowance can apply when the 7-day rule applies (moot at the example's income) | SR.3 |
| Whether depreciation is divided by the rental-use share when personal use stays under the "used as a home" threshold | SR.3 |
| The 2026 excess business loss threshold (only the 2025 figure was found) | SR.3 |
| Schedule C vs Schedule E and self-employment tax when guest services are provided; S-corporation effects for real estate | PA.10 |
| Classification of furnishings, linens, consumables, and 15-year land improvements (section 1245 vs 1250) and recapture of bonus taken on them | OP.6, SR.3, OP.12 |
| Suspended passive losses on sale; net investment income tax and state tax on the gain | OP.12 |
| Rev. Proc. 2008-16 vacation-home safe harbor specifics (24 months; 14 days at fair rent; personal-use limit), boot, and carryover basis in a 1031 exchange | OP.12 |
| Whether HELOC interest can be deducted as a rental expense under tracing rules | OP.11 |
| The full list of Pub 5653 "principal elements" of a quality cost segregation study (SR.3 labels the unconfirmed rows as recommendations) | SR.3 |
| LLC fee, registered agent, and return preparation figures ($300, $125, $1,200) are assumptions | PA.10 |

## Insurer

| Item | Lessons |
|---|---|
| Whether Airbnb host liability coverage treats a tenant-operator's landlord the same as an owner's; whether an operator's STR policy covers every channel and can name the landlord | 5.7, 3.5 |
| STR policy terms for Cedar Ridge: deductibles, exclusions, business interruption, bunk beds, grills, vendor insurance, incident notice | PA.12, OP.6, OP.7 |
