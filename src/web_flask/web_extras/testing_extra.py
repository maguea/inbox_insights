SAMPLE_EMAILS = [
    {
        "id": 101,
        "sender": "John Doe <john@acme.com>",
        "subject": "Q4 Launch Plan",
        "preview": "Here's the quick summary of the Q4 launch milestones...",
        "timestamp": "2:30 PM",
        "date": "Oct 1, 2025",
        "body": "<p><b>Hi team,</b></p><p>Here's the latest Q4 plan. We are on track.</p><ul><li>Beta: Oct 20</li><li>GA: Nov 15</li></ul><p>Thanks,<br>John</p>",
        "attachments": ["Q4-launch-plan.pdf"]
    },
    {
        "id": 102,
        "sender": "Jane Smith <jane@contoso.com>",
        "subject": "Design review notes",
        "preview": "I attached the latest comps and Figma link. Main feedback is...",
        "timestamp": "9:12 AM",
        "date": "Oct 3, 2025",
        "body": "<p>Notes from design review:</p><ol><li>Reduce hero height</li><li>Unify button radius</li><li>Add dark mode tokens</li></ol><p>– Jane</p>",
        "attachments": ["homepage-v7.fig", "tokens.json"]
    },
    {
        "id": 103,
        "sender": "Billing <billing@service.com>",
        "subject": "Invoice #31294 due",
        "preview": "Your invoice #31294 is due on Oct 20. Amount due: $1,240.00.",
        "timestamp": "4:58 PM",
        "date": "Oct 5, 2025",
        "body": "<p>Amount due: <b>$1,240.00</b></p><p>Due date: Oct 20, 2025</p><p><a href='#'>View invoice</a></p>",
        "attachments": ["invoice-31294.pdf"]
    },

    # -------- NEW FAKE EMAILS BELOW -------- #

    {
        "id": 104,
        "sender": "AWS Notifications <no-reply@amazonaws.com>",
        "subject": "[Action Required] IAM key rotation",
        "preview": "One or more access keys are older than 90 days...",
        "timestamp": "6:41 AM",
        "date": "Oct 6, 2025",
        "body": "<p>Your IAM keys are older than 90 days. Please rotate them to maintain security compliance.</p>",
        "attachments": []
    },
    {
        "id": 105,
        "sender": "HR <hr@acme.com>",
        "subject": "Reminder — Open Enrollment closes Friday",
        "preview": "Don't forget to choose your 2026 benefits before the deadline...",
        "timestamp": "11:05 AM",
        "date": "Oct 6, 2025",
        "body": "<p>Open Enrollment closes this Friday at 5PM ET.</p><p>Please log in to the portal and choose your benefits.</p>",
        "attachments": []
    },
    {
        "id": 106,
        "sender": "Mark Cuban <mark@investments.com>",
        "subject": "Follow-up on deck",
        "preview": "Got your deck — a couple questions before I set time with partners...",
        "timestamp": "7:22 PM",
        "date": "Oct 7, 2025",
        "body": "<p>Thanks for sending the deck.</p><p>Two questions:</p><ul><li>Unit economics post-scale?</li><li>Churn assumptions validated?</li></ul><p>– Mark</p>",
        "attachments": ["deck-v3.pdf"]
    },
    {
        "id": 107,
        "sender": "Spotify <no-reply@spotify.com>",
        "subject": "Your Premium receipt",
        "preview": "Your next billing date is Nov 2...",
        "timestamp": "3:11 PM",
        "date": "Oct 8, 2025",
        "body": "<p>Thanks for being a Premium listener!</p><p>Next billing: Nov 2 — $9.99.</p>",
        "attachments": []
    },
    {
        "id": 108,
        "sender": "Slack <noreply@mail.slack.com>",
        "subject": "Export ready",
        "preview": "Your workspace export is ready to download...",
        "timestamp": "8:03 AM",
        "date": "Oct 8, 2025",
        "body": "<p>Your data export is ready.</p><p><a href='#'>Download export</a> (expires in 72h)</p>",
        "attachments": ["export.zip"]
    },
    {
        "id": 109,
        "sender": "CircleCI <bot@circleci.com>",
        "subject": "Workflow failed — backend-build",
        "preview": "Step test-api exited with status 1...",
        "timestamp": "12:55 PM",
        "date": "Oct 9, 2025",
        "body": "<p>Job <code>test-api</code> failed on commit <code>a9b33af</code>.</p>",
        "attachments": []
    },
    {
        "id": 110,
        "sender": "Github <noreply@github.com>",
        "subject": "[security] 1 dependency needs attention",
        "preview": "A vulnerability was found in your repository...",
        "timestamp": "10:14 AM",
        "date": "Oct 9, 2025",
        "body": "<p>1 moderate vulnerability detected in <code>axios</code>.</p><p>Run <code>npm audit fix</code>.</p>",
        "attachments": []
    },
    {
        "id": 111,
        "sender": "Notion <updates@notion.so>",
        "subject": "New: AI autofill & DB summaries",
        "preview": "Big update just landed — here's what's new...",
        "timestamp": "9:02 AM",
        "date": "Oct 10, 2025",
        "body": "<p>We shipped:</p><ul><li>AI autofill</li><li>Summary rows in DB</li><li>Cross-workspace sync</li></ul>",
        "attachments": []
    },
    {
        "id": 112,
        "sender": "Figma <team@figma.com>",
        "subject": "You were mentioned in a comment",
        "preview": "Ana mentioned you in Components-v9...",
        "timestamp": "5:46 PM",
        "date": "Oct 10, 2025",
        "body": "<p>You were mentioned in <b>Components-v9.fig</b></p><p>“Can we reduce padding here?”</p>",
        "attachments": []
    },
    {
        "id": 113,
        "sender": "Support <help@saas.io>",
        "subject": "Ticket #88914 resolved",
        "preview": "We've pushed a fix to production — should be resolved...",
        "timestamp": "2:08 PM",
        "date": "Oct 11, 2025",
        "body": "<p>We fixed the billing mismatch bug.</p><p>Let us know if you still see issues.</p>",
        "attachments": []
    },
    {
        "id": 114,
        "sender": "Calendly <no-reply@calendly.com>",
        "subject": "Meeting confirmed — Tuesday 3PM",
        "preview": "Mark Cuban accepted your meeting request...",
        "timestamp": "7:33 AM",
        "date": "Oct 12, 2025",
        "body": "<p>Your meeting is confirmed:</p><ul><li><b>When:</b> Tue 3PM ET</li><li><b>With:</b> Mark Cuban</li></ul>",
        "attachments": []
    },
    {
        "id": 115,
        "sender": "Stripe <no-reply@stripe.com>",
        "subject": "Payout initiated — $4,230.44",
        "preview": "Funds will arrive in 2-5 business days...",
        "timestamp": "1:19 PM",
        "date": "Oct 12, 2025",
        "body": "<p>Your payout of <b>$4,230.44</b> is on the way.</p>",
        "attachments": []
    },
    {
        "id": 116,
        "sender": "Zoom <no-reply@zoom.us>",
        "subject": "Cloud recording ready",
        "preview": "Your meeting recording is now available...",
        "timestamp": "8:59 AM",
        "date": "Oct 13, 2025",
        "body": "<p>Your cloud recording is ready.</p><p><a href='#'>View recording</a></p>",
        "attachments": []
    },
    {
        "id": 117,
        "sender": "Legal <legal@acme.com>",
        "subject": "NDA counter-signed",
        "preview": "The mutual NDA with Contoso has been executed...",
        "timestamp": "4:22 PM",
        "date": "Oct 13, 2025",
        "body": "<p>NDA is fully executed. Safe to share materials.</p>",
        "attachments": ["nda-signed.pdf"]
    },
    {
        "id": 118,
        "sender": "PagerDuty <alerts@pagerduty.com>",
        "subject": "⚠ Incident triggered — checkout-errors",
        "preview": "Error rate > 2% in last 5 minutes...",
        "timestamp": "2:47 AM",
        "date": "Oct 14, 2025",
        "body": "<p>Incident <b>checkout-errors</b> triggered at 02:45.</p>",
        "attachments": []
    },
    {
        "id": 119,
        "sender": "Alice <alice@acme.com>",
        "subject": "Can you review PR #912?",
        "preview": "Mostly refactor but want a sanity check...",
        "timestamp": "11:06 AM",
        "date": "Oct 14, 2025",
        "body": "<p>Refactor of auth handler — can you give a pass?</p>",
        "attachments": []
    },
    {
        "id": 120,
        "sender": "LinkedIn <messaging@linkedin.com>",
        "subject": "You appeared in 47 searches last week",
        "preview": "Your profile is turning up in recruiter searches...",
        "timestamp": "6:14 AM",
        "date": "Oct 15, 2025",
        "body": "<p>You appeared in 47 searches last week — up 19%</p>",
        "attachments": []
    },
        {
        "id": 121,
        "sender": "Google Calendar <no-reply@calendar.google.com>",
        "subject": "Event reminder — 1:1 with Sarah",
        "preview": "Starts in 30 minutes — Zoom link inside...",
        "timestamp": "1:30 PM",
        "date": "Oct 15, 2025",
        "body": "<p>Reminder: 1:1 with Sarah at 2:00 PM.</p><p><a href='#'>Join Zoom</a></p>",
        "attachments": []
    },
    {
        "id": 122,
        "sender": "Twitter <security@twitter.com>",
        "subject": "New login detected",
        "preview": "We noticed a login from a new device...",
        "timestamp": "8:14 PM",
        "date": "Oct 15, 2025",
        "body": "<p>New login from Chrome (Mac).</p><p>If this wasn't you, secure your account.</p>",
        "attachments": []
    },
    {
        "id": 123,
        "sender": "PayPal <no-reply@paypal.com>",
        "subject": "Payment received — $82.00",
        "preview": "You received a payment from Marketplace Co...",
        "timestamp": "10:09 AM",
        "date": "Oct 16, 2025",
        "body": "<p>You received: <b>$82.00</b></p><p>Sender: Marketplace Co</p>",
        "attachments": []
    },
    {
        "id": 124,
        "sender": "Dropbox <no-reply@dropbox.com>",
        "subject": "Shared folder updated",
        "preview": "Alice updated 'Brand Assets'...",
        "timestamp": "3:02 PM",
        "date": "Oct 16, 2025",
        "body": "<p>Alice added <b>Logo-final.ai</b> to Brand Assets folder.</p>",
        "attachments": []
    },
    {
        "id": 125,
        "sender": "Uber Receipts <no-reply@uber.com>",
        "subject": "Your Thursday trip receipt",
        "preview": "Trip • $18.23 • 2.9 mi • 14 min",
        "timestamp": "12:43 AM",
        "date": "Oct 17, 2025",
        "body": "<p>Thanks for riding!</p><p>Total: <b>$18.23</b></p>",
        "attachments": []
    },
    {
        "id": 126,
        "sender": "Zoom <no-reply@zoom.us>",
        "subject": "Recording auto-deleted soon",
        "preview": "Your recording will be removed in 7 days...",
        "timestamp": "9:15 AM",
        "date": "Oct 17, 2025",
        "body": "<p>This recording expires in 7 days.</p><p><a href='#'>Manage recordings</a></p>",
        "attachments": []
    },
    {
        "id": 127,
        "sender": "Fidelity <alerts@fidelity.com>",
        "subject": "Trade confirmation",
        "preview": "You bought 5 shares TSLA @ 242.14...",
        "timestamp": "4:11 PM",
        "date": "Oct 17, 2025",
        "body": "<p>Trade executed.</p><ul><li>5× TSLA</li><li>Price: 242.14</li></ul>",
        "attachments": []
    },
    {
        "id": 128,
        "sender": "AWS Billing <no-reply@amazonaws.com>",
        "subject": "Your invoice is now available",
        "preview": "October AWS usage is ready...",
        "timestamp": "6:48 PM",
        "date": "Oct 17, 2025",
        "body": "<p>Your AWS bill is ready.</p>",
        "attachments": ["aws-october.pdf"]
    },
    {
        "id": 129,
        "sender": "GitLab <noreply@gitlab.com>",
        "subject": "Pipeline succeeded — main",
        "preview": "All stages passed on commit 1ac99c...",
        "timestamp": "8:21 AM",
        "date": "Oct 18, 2025",
        "body": "<p>Pipeline succeeded for commit <code>1ac99c</code>.</p>",
        "attachments": []
    },
    {
        "id": 130,
        "sender": "Slack <digest@mail.slack.com>",
        "subject": "Daily summary",
        "preview": "12 messages you missed in #product...",
        "timestamp": "7:52 AM",
        "date": "Oct 18, 2025",
        "body": "<p>You missed:</p><ul><li>#product — 12 msgs</li><li>#support — 5 msgs</li></ul>",
        "attachments": []
    },
    {
        "id": 131,
        "sender": "Meet <no-reply@meet.google.com>",
        "subject": "Meeting ended — recording available",
        "preview": "Click to watch and share...",
        "timestamp": "11:09 AM",
        "date": "Oct 18, 2025",
        "body": "<p><a href='#'>Watch recording</a></p>",
        "attachments": []
    },
    {
        "id": 132,
        "sender": "Bank Alerts <alerts@yourbank.com>",
        "subject": "Deposit posted",
        "preview": "Payroll deposit of $1,628.31 was received...",
        "timestamp": "6:03 AM",
        "date": "Oct 19, 2025",
        "body": "<p>Deposit: <b>$1,628.31</b></p>",
        "attachments": []
    },
    {
        "id": 133,
        "sender": "Discord <no-reply@discord.com>",
        "subject": "You have unread mentions",
        "preview": "Someone pinged you in #ai-research...",
        "timestamp": "12:29 PM",
        "date": "Oct 19, 2025",
        "body": "<p>You were mentioned in <b>#ai-research</b>.</p>",
        "attachments": []
    },
    {
        "id": 134,
        "sender": "Stripe <no-reply@stripe.com>",
        "subject": "Charge refunded — $49.00",
        "preview": "A customer refund has been processed...",
        "timestamp": "2:51 PM",
        "date": "Oct 19, 2025",
        "body": "<p>Refund amount: $49.00 successfully processed.</p>",
        "attachments": []
    },
    {
        "id": 135,
        "sender": "Airbnb <booking@airbnb.com>",
        "subject": "Your reservation is confirmed",
        "preview": "Staying in Philadelphia — Dec 12-15...",
        "timestamp": "5:10 PM",
        "date": "Oct 19, 2025",
        "body": "<p>Trip confirmed Dec 12–15.</p>",
        "attachments": ["itinerary.pdf"]
    },
    {
        "id": 136,
        "sender": "Drive <drive-noreply@google.com>",
        "subject": "File shared with you",
        "preview": "Dylan shared '4-unit pro forma.xlsx'...",
        "timestamp": "9:48 AM",
        "date": "Oct 20, 2025",
        "body": "<p>Dylan shared <b>4-unit pro forma.xlsx</b></p>",
        "attachments": ["4-unit-proforma.xlsx"]
    },
    {
        "id": 137,
        "sender": "DocuSign <system@docusign.net>",
        "subject": "Please sign — Operating Agreement",
        "preview": "Dylan sent you a document to sign...",
        "timestamp": "12:03 PM",
        "date": "Oct 20, 2025",
        "body": "<p>Please review and sign the Operating Agreement.</p>",
        "attachments": ["operating-agreement.pdf"]
    },
    {
        "id": 138,
        "sender": "Notion AI <update@notion.so>",
        "subject": "AI meeting summary ready",
        "preview": "Your 'Darden pitch call' summary is generated...",
        "timestamp": "1:22 PM",
        "date": "Oct 20, 2025",
        "body": "<p>AI summary for <b>Darden pitch call</b> is ready.</p>",
        "attachments": []
    },
    {
        "id": 139,
        "sender": "Property Manager <office@metroproperties.com>",
        "subject": "Rent Posted — Nov 1",
        "preview": "Upcoming charge $1,105.00 will auto-post...",
        "timestamp": "4:41 PM",
        "date": "Oct 20, 2025",
        "body": "<p>Rent will post automatically on Nov 1.</p>",
        "attachments": []
    },
    {
        "id": 140,
        "sender": "USPS <tracking@usps.com>",
        "subject": "Package delivered",
        "preview": "Your package from Amazon was delivered...",
        "timestamp": "7:14 PM",
        "date": "Oct 20, 2025",
        "body": "<p>Delivered at Front Door.</p>",
        "attachments": []
    },
    {
        "id": 141,
        "sender": "Hersheypark <info@hershey.com>",
        "subject": "Your tickets for Sunday",
        "preview": "Present attached QR to enter...",
        "timestamp": "9:33 AM",
        "date": "Oct 21, 2025",
        "body": "<p>Attached are your Sunday tickets.</p>",
        "attachments": ["hershey-tickets.pdf"]
    },
    {
        "id": 142,
        "sender": "Enterprise Mobility HR <hr@enterprise.com>",
        "subject": "Commission payout notice",
        "preview": "Commission for October will be issued Friday...",
        "timestamp": "10:58 AM",
        "date": "Oct 21, 2025",
        "body": "<p>Commission will be paid on Friday's paycheck.</p>",
        "attachments": []
    },
    {
        "id": 143,
        "sender": "Calendly <no-reply@calendly.com>",
        "subject": "Reschedule request — Dylan",
        "preview": "Dylan proposed new time for build meeting...",
        "timestamp": "1:04 PM",
        "date": "Oct 21, 2025",
        "body": "<p>Dylan proposed new back-and-forth time for the 4-unit build review.</p>",
        "attachments": []
    },
    {
        "id": 144,
        "sender": "JetBlue <travel@jetblue.com>",
        "subject": "Check-in now open",
        "preview": "Your flight to PHL is within 24 hours...",
        "timestamp": "5:22 PM",
        "date": "Oct 21, 2025",
        "body": "<p>You can now check-in online.</p>",
        "attachments": []
    },
    {
        "id": 145,
        "sender": "Gmail Security <no-reply@accounts.google.com>",
        "subject": "Password change confirmation",
        "preview": "Your password was changed at 6:55 PM...",
        "timestamp": "6:59 PM",
        "date": "Oct 21, 2025",
        "body": "<p>If this was not you, secure your account immediately.</p>",
        "attachments": []
    },
    {
        "id": 146,
        "sender": "Netflix <no-reply@netflix.com>",
        "subject": "We added new titles you might like",
        "preview": "New thriller, documentary, and sci-fi releases...",
        "timestamp": "8:14 PM",
        "date": "Oct 21, 2025",
        "body": "<p>New titles just added this week.</p>",
        "attachments": []
    },
    {
        "id": 147,
        "sender": "Etsy <order@etsy.com>",
        "subject": "Your order has shipped",
        "preview": "The seller sent your order and provided tracking...",
        "timestamp": "9:05 AM",
        "date": "Oct 22, 2025",
        "body": "<p>Your item is on its way.</p>",
        "attachments": []
    },
    {
        "id": 148,
        "sender": "Wells Fargo <alert@wellsfargo.com>",
        "subject": "Card charge posted",
        "preview": "A charge of $43.90 was made at Trader Joe's...",
        "timestamp": "10:42 AM",
        "date": "Oct 22, 2025",
        "body": "<p>Charge posted: <b>$43.90</b> at Trader Joe's.</p>",
        "attachments": []
    },
    {
        "id": 149,
        "sender": "Apple <no-reply@apple.com>",
        "subject": "Your App Store receipt",
        "preview": "You were charged $4.99...",
        "timestamp": "11:50 AM",
        "date": "Oct 22, 2025",
        "body": "<p>App Store charge: <b>$4.99</b></p>",
        "attachments": []
    },
    {
        "id": 150,
        "sender": "IRS <no-reply@irs.gov>",
        "subject": "Tax refund processed",
        "preview": "A refund of $200.00 has been issued...",
        "timestamp": "2:18 PM",
        "date": "Oct 22, 2025",
        "body": "<p>Refund issued: $200.00.</p>",
        "attachments": []
    },
    {
        "id": 151,
        "sender": "Harvard Business <hbs@edu>",
        "subject": "Case study packet",
        "preview": "Attached: TopGolf entry, Nucor steel analysis...",
        "timestamp": "3:14 PM",
        "date": "Oct 22, 2025",
        "body": "<p>Case packet attached.</p>",
        "attachments": ["topgolf.pdf", "nucor.pdf"]
    },
    {
        "id": 152,
        "sender": "UVA Darden <admissions@darden.edu>",
        "subject": "Thank you for your submission",
        "preview": "We received your advertising concept analysis...",
        "timestamp": "4:09 PM",
        "date": "Oct 22, 2025",
        "body": "<p>Your materials were received and are under review.</p>",
        "attachments": []
    },
    {
        "id": 153,
        "sender": "ChatGPT Billing <billing@openai.com>",
        "subject": "Your Plus subscription renewed",
        "preview": "We charged your card ending •••• 4242...",
        "timestamp": "5:12 PM",
        "date": "Oct 22, 2025",
        "body": "<p>Subscription renewed successfully.</p>",
        "attachments": []
    },
    {
        "id": 154,
        "sender": "Hertz <no-reply@hertz.com>",
        "subject": "Return confirmed",
        "preview": "Vehicle return completed at PIT airport...",
        "timestamp": "7:48 PM",
        "date": "Oct 22, 2025",
        "body": "<p>Vehicle successfully returned at PIT.</p>",
        "attachments": []
    },
    {
        "id": 155,
        "sender": "Microsoft Teams <noreply@teams.microsoft.com>",
        "subject": "You were added to a team",
        "preview": "Sarah added you to 'Growth Q4' workspace...",
        "timestamp": "8:14 PM",
        "date": "Oct 22, 2025",
        "body": "<p>You were added to <b>Growth Q4</b> team.</p>",
        "attachments": []
    },
    {
        "id": 156,
        "sender": "DocuSign <system@docusign.net>",
        "subject": "Completed — all parties signed",
        "preview": "Operating Agreement is now fully executed...",
        "timestamp": "9:22 PM",
        "date": "Oct 22, 2025",
        "body": "<p>All signatures received.</p>",
        "attachments": ["operating-agreement-final.pdf"]
    },
    {
        "id": 157,
        "sender": "Intuit Mint <alerts@mint.com>",
        "subject": "Budget trend — Over groceries target",
        "preview": "You exceeded your monthly food target by $38...",
        "timestamp": "7:18 AM",
        "date": "Oct 23, 2025",
        "body": "<p>You exceeded groceries budget by <b>$38</b>.</p>",
        "attachments": []
    },
    {
        "id": 158,
        "sender": "YouTube <no-reply@youtube.com>",
        "subject": "New upload from 'Veritasium'",
        "preview": "Dark matter experiment just dropped...",
        "timestamp": "10:02 AM",
        "date": "Oct 23, 2025",
        "body": "<p>New video available: <i>The Dark Matter Lab</i>.</p>",
        "attachments": []
    },
    {
        "id": 159,
        "sender": "LinkedIn Jobs <jobs@linkedin.com>",
        "subject": "9 new roles match your profile",
        "preview": "AM roles in MD + WV at Enterprise Mobility...",
        "timestamp": "12:44 PM",
        "date": "Oct 23, 2025",
        "body": "<p>New jobs matching Enterprise AM track.</p>",
        "attachments": []
    },
    {
        "id": 160,
        "sender": "Enterprise Branch 54 <manager@enterprise.com>",
        "subject": "ESQi weekly — Action items",
        "preview": "Keep callbacks inside 48hrs, resolve pendings...",
        "timestamp": "4:31 PM",
        "date": "Oct 23, 2025",
        "body": "<p>Action items this week:</p><ul><li>48h callbacks</li><li>Resolve closed-pends</li><li>Clean car caption</li></ul>",
        "attachments": []
    },
]
