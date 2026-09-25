# Consistency fixes (from qa/calc-audit.md and deck-agent reviews)

Every fix changes the lesson Markdown in `parts/` AND the matching deck spec in `slides/src/` (slide text and speaking notes), then rebuilds that deck. Compute every new number in python. Keep canonical numbers unchanged. Keep the voice rules (no em/en dashes, no banned words, sentences under 25 words). Mark new invented numbers "(assumption)".

## Set X: the Cedar Ridge money thread

X1. **Savings and emergency fund.** The emergency fund is $51,000 everywhere (0.3, PA.1 already say so). 0.3's funding condition is saving $3,500 a month (assumption). Decision: by the time Maya and Chris write the offer in PA.8, six months after the 0.3 scorecard, their liquid savings are **$231,000** ($210,000 + 6 x $3,500, assumption). Replace PA.8's "$30,000 emergency fund" and "$210,000" with $51,000 and $231,000, and say in one or two sentences that the 0.3 funding condition was met. Money available for the property stays $180,000, so the Test 3 ceiling (about $409,984), the $11,020 unallocated, and PA.9's cash test should come out the same: verify in python and correct if not. Update PA.8's cash table and any deck slides and notes.

X2. **PA.12 carrying cost and post-close cash.** Use the full monthly carry of $3,257 (0.3's figure, including software and the handyman retainer), not $3,007. The 45-day carry becomes $4,885.50. Recompute cash left after closing from $231,000 (less total cash in $142,688, PA.9's $2,955 repairs, and the carry), recompute "cash out between closing and the first guest", and restate what the set-asides ($15,342 property reserve, $51,000 emergency fund, $12,000 weak-case cushion) leave. Update the deck.

X3. **OP.11 starting liquidity.** Step 4 must start from PA.12's post-close cash (from X2), not $210,000 - $142,688. Rewrite Step 4 and re-run Step 5's reserve test on the new figure. Keep the conclusion only if it still follows; otherwise state the new result honestly. Also explain the trailing supplies line ($1,596 = about $28 a stay vs $25 planned) in the narrative. Update the deck.

X4. **PA.9 must apply the buy-box rules it inherited.** After diligence, PA.9's revised weak case is -$9,295, beyond the -$6,000 funded-shortfall limit from PA.1/PA.8, and NOI / P&I is about 1.07 against PA.1's 1.20 minimum. Add a short subsection or paragraph in PA.9 (before the decision) that runs those two rules on the revised numbers, shows both fail, and records the decision rule: renegotiate or walk. Then resolve it within the story in a way that is arithmetically true, for example: the recurring items that overlap the canonical 5% capital reserve (roof sinking fund) are funded from that reserve line instead of added on top, and/or the seller's septic and well work removes or reduces some recurring costs, and/or a further price or credit concession. Whatever you choose, recompute NOI, cash flow, weak case, and coverage in python and show they now meet both rules; if no honest fix gets there, the decision is to proceed only as a documented, signed exception to the buy box, stated plainly as a weaker choice. Carry the final revised figures into PA.10 and PA.12 wherever they quote PA.9's numbers. Update the decks.

X5. **Later lessons and PA.9's revision.** OP.7, OP.11, and OP.12 use the canonical B1 underwriting. Add one or two sentences near the start of each lesson's worked example: these comparisons use the original underwriting (B1); PA.9's diligence changed the operating baseline by $X a year (the final figure from X4), so subtract it from every cash-flow number shown, and what that does to the lesson's conclusion. For OP.11's trailing-12, state whether PA.9's recurring items are inside the trailing lines; if not, show the trailing cash flow with them included. Update the decks where the notes discuss these figures.

X6. **Other debts.** 0.3 uses $600 a month of other debts; PA.7 uses $400. Change PA.7 to $600 and recompute (today about 19.5%; with the conventional PITIA about 35.6%). Check that PA.7's statements about Fannie Mae limits still hold at 35.6% (36% manual limit) and adjust wording ("just under"). Update the deck.

X7. **Earnest money.** 0.1 says $3,850 (1%). Add that the figure is an early placeholder and that PA.8 negotiates 2% ($7,700). Update the deck if it shows $3,850.

X8. **Hours.** PA.1 says "about 3 hours a week (assumption, from 0.3)"; 0.3 computes 2.7. Change PA.1 to "about 2.7 hours a week". OP.7's 2 hours per stay vs 0.3's 1.5: align OP.7 to 1.5 hours per stay and recompute anything that depends on it, or state why OP.7 uses a different figure.

X9. **PA.11 insurance double count.** Add a sentence: the $3,200 first-year premium prepaid at closing is the same premium that appears in the B1 operating budget, so count it once in year-one cash.

X10. **PA.9.8** "at the OP.10 review" for a 12-month check: change to the 12-month review in OP.11 (OP.10 is Sam's 30/90-day review).

X11. **0.1.6** PITIA definition should include association dues (none at Cedar Ridge). **0.3.4** remove the duplicated reserve-definition sentence. **0.1.5 Gate 6**: reword so Yes means continue and No means renegotiate or cancel, like the other gates (the deck already does this).

X12. **Unmarked thresholds.** Label 0.3.9's readiness-scorecard cut-offs as assumptions (teaching defaults).

Files in Set X: parts 08, 10, 11, 13, 14, 15, 16, 17, 18, 20, 23, 24 and slides/src 08, 10, 11, 13, 14, 15, 16, 17, 18, 20, 23, 24.

## Set Y: everything else

Y1. **PA.6.10** Lender B maximum loan: use the unrounded P&I limit as PA.6.5 does. Stated $276,096 / $12,654 become $276,094 / $12,656. Fix Markdown and deck.

Y2. **3.1.9** break-even nightly rate at 120 nights: say "about $308" (it solves to $308.01). Fix Markdown and deck.

Y3. **3.4.6** scorecard point bands and label cut-offs: label them as assumptions (teaching defaults), as 1.3 does. Deck too.

Y4. **SR.1** RSO cut-off wording: "before October 1, 1978" to match 3.1 and 3.4. Deck too.

Y5. **SR.3.7** "the first four rows come straight from" Pub 5653: row 5 also cites it; make it "first five" if row 5 is sourced to Pub 5653. **SR.3.2**: B23, B25, B26 (212 days, 61 stays) are marked "Verified from reports" but are hypothetical teaching figures; relabel their status as example inputs (assumption) while explaining that a real user would mark them verified from platform reports. Decks too.

Y6. **OP.8.2** alarm test: the proof column says "weekly test logged" but the text puts the full button test in the monthly inspection. Make them consistent: the turnover step is a visual check of the alarm's status light plus a log entry; the button test is monthly. **OP.8.3** par levels: two rows have par equal to reorder point (sheet sets 1 per bed / 1 per bed; towel sets 8 / 8). Set a reorder point below par and say what it means. Decks too.

Y7. **Authoring notes in reader text.** Remove phrases like "computed in python", "I computed both in Python", "Python finds it" from the lesson prose in every part file except those in Set X (Set X handles its own files). Replace with plain wording ("works out to", "solves to"). Keep such notes in the sources sections, where they document method. Decks too if the notes say it.

Files in Set Y: parts 02, 04, 12, 19, 21, 22, 25, 26, and any other non-Set-X part file for Y7; slides/src with the same numbers.
