Set-Location "E:\git hub\GS360-1"
New-Item -ItemType Directory -Force -Path "docs/tickets" | Out-Null

$items = @(
  @{W=1; T='Week 1: Multi-Tenancy Spike (Blocking Gate)'; S=@('Run DeepTutor locally and verify baseline','Audit core file-path usage and produce PATH_AUDIT.md','Prototype UserNamespace patching on 2 modules','Run 2-user isolation test for uploads and sessions','Record decision gate YES/NO for multi-tenancy'); A=@('PATH_AUDIT.md produced','2-user isolation evidence attached','Decision gate outcome documented')},
  @{W=2; T='Week 2: Auth + Content Pack Foundation'; S=@('Set up NextAuth.js (Google + GitHub OAuth)','Implement security middleware for path validation and audit logs','Build pack schema validation and ingest pipeline','Ingest first content pack and verify RAG retrieval'); A=@('OAuth works in hosted mode','Invalid path requests are blocked and logged','First pack queryable in RAG')},
  @{W=3; T='Week 3: AI Core + Eval Baseline (Part 1)'; S=@('Patch priority modules for per-user namespace','Implement AI Notes generation from RAG','Build eval harness and 30-question micro set','Run baseline accuracy reading on stock pipeline'); A=@('AI Notes grounded by content','Eval harness outputs stored','30-question micro set available')},
  @{W=4; T='Week 4: Quiz Engine + Chunking Lever (Part 2)'; S=@('Implement quiz generation from content packs + AI','Add rate limiter and LLM fallback chain','Evaluate chunking strategies and pick winner','Patch remaining high-risk namespace paths'); A=@('Quiz generation functional','Fallback chain behavior verified','Chunking decision documented with metrics')},
  @{W=5; T='Week 5: Platform Features + Offline Foundation'; S=@('Build Content Pack Manager UI','Build KB manager for private vault uploads','Enable PWA manifest and service worker foundation'); A=@('Pack manager browse/search/install flow works','Private uploads are isolated per user','App install/caching baseline works')},
  @{W=6; T='Week 6: Retrieval Tuning + Milestone Tests'; S=@('Implement hybrid retrieval and reranking lever','Build performance dashboard for quiz progress','Run T1 quiz quality and T2 throughput checks','Publish Week 6 scorecard'); A=@('Hybrid retrieval evaluated with delta','Dashboard tracks quiz history and scores','T1/T2 reports published')},
  @{W=7; T='Week 7: GS360 Theme + Command Center (Part 1)'; S=@('Implement GS360 design tokens/components','Build Daily Command Center layout','Add sidebar navigation and keyboard shortcuts'); A=@('Theme applied consistently','Command Center works on desktop/web','Shortcuts functional and documented')},
  @{W=8; T='Week 8: Accessibility + RAG Levers 3-4'; S=@('Run WCAG AA accessibility pass','Implement factual vs analytical prompt split','Run embedding model A/B tests and compare deltas'); A=@('Critical a11y issues resolved','Prompt split deployed','Embedding model decision documented')},
  @{W=9; T='Week 9: Integration Debugging + Lever 5'; S=@('Run end-to-end integration tests across runtimes','Fix CORS/auth token/WebSocket issues','Implement query rewriting (HyDE)'); A=@('Core E2E flows pass','Auth and socket reliability improved','HyDE impact measured')},
  @{W=10; T='Week 10: UX Polish + Feature Freeze'; S=@('Polish error/loading/offline UI states','Run T6 desktop/web usability checks','Finalize answer-model A/B tests','Enforce feature freeze for post-week work'); A=@('T6 feedback captured and triaged','Feature freeze rules published','Only bug-fix backlog remains')},
  @{W=11; T='Week 11: Cold-Start Content Creation'; S=@('Generate 8 seed content packs','Structure PYQs (2000-2025) into pack format','Generate NCERT summaries, MCQs, flashcards'); A=@('8 seed packs available','PYQ dataset validated','Generated assets pass schema checks')},
  @{W=12; T='Week 12: Expert Review + Full Golden Set'; S=@('Domain expert review of AI-generated content','Scale golden set from 30 to 200 Q&A pairs','Run full T3 eval and launch-threshold check','Block launch if hallucination >10%'); A=@('200-question set verified','T3 report with go/no-go recommendation','Hallucination rate documented')},
  @{W=13; T='Week 13: Security + Bug-Fix Buffer'; S=@('Run pre-launch pen test (10 vectors)','Fix high-priority integration bugs','Test copyright scan pipeline','Verify backup+restore and run load tests'); A=@('Pen test report with remediations','Backup restore drill passed','Load test targets reported')},
  @{W=14; T='Week 14: Deployment + Infrastructure'; S=@('Deploy frontend and backend','Configure DNS/SSL/domain','Enable live backup pipeline and health checks','Run production smoke tests'); A=@('Production deployment stable','Domain and SSL verified','Smoke tests complete')},
  @{W=15; T='Week 15: Documentation + Community Setup'; S=@('Finalize README/CONTRIBUTING/CONTENT_GUIDE/SECURITY/DMCA','Set up Discord and Telegram channels','Optionally enable Plausible analytics'); A=@('Core docs complete','Community channels launched','Analytics decision captured')},
  @{W=16; T='Week 16: Soft Launch + Feedback Loop'; S=@('Invite 20-30 beta users','Monitor 5 days for crashes/data leaks/UX confusion','Run daily hotfix cycle for critical issues','Public launch and v1.1 planning from feedback'); A=@('Beta monitoring report complete','Critical issues mitigated','v1.1 backlog seeded')}
)

foreach ($i in $items) {
  $num = '{0:d2}' -f [int]$i.W
  $slug = ($i.T.ToLower() -replace '[^a-z0-9]+','-' -replace '(^-|-$)','')
  $path = "docs/tickets/ISSUE-$num-week-$num-$slug.md"

  $scope = ($i.S | ForEach-Object { "- [ ] $_" }) -join "`r`n"
  $ac = ($i.A | ForEach-Object { "- [ ] $_" }) -join "`r`n"

  $md = @"
# ISSUE-${num}: $($i.T)

## Summary
Execution ticket for Week $($i.W) from docs/implementation_plan.md.

## Scope Checklist
$scope

## Acceptance Criteria
$ac

## Deliverables
- Week status update with links to PRs/commits
- Evidence artifacts (logs/screenshots/reports)
- Handoff note for next week

## Source
- docs/implementation_plan.md
"@

  Set-Content -Path $path -Value $md -Encoding utf8
  gh issue create --repo JINA-CODE-SYSTEMS/GS360 --title $i.T --body-file $path | Out-Null
  Write-Output ("Created week {0}: {1}" -f $i.W, $i.T)
}

Write-Output "DONE"
