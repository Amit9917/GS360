Set-Location "E:\git hub\GS360-1"
$repo = "JINA-CODE-SYSTEMS/GS360"
$ms = "GS360 v1 - 16 Week Roadmap"

for ($i=3; $i -le 19; $i++) { gh issue edit $i --repo $repo --milestone $ms | Out-Null }

for ($i=3; $i -le 18; $i++) { gh issue edit $i --repo $repo --add-label "type:execution" | Out-Null }
gh issue edit 3 --repo $repo --add-label "type:spike" --remove-label "type:execution" | Out-Null
gh issue edit 19 --repo $repo --add-label "type:tracker" | Out-Null

for ($i=3; $i -le 4; $i++) { gh issue edit $i --repo $repo --add-label "priority:p0" | Out-Null }
for ($i=5; $i -le 18; $i++) { gh issue edit $i --repo $repo --add-label "priority:p1" | Out-Null }
gh issue edit 19 --repo $repo --add-label "priority:p0" | Out-Null

for ($i=3; $i -le 4; $i++) { gh issue edit $i --repo $repo --add-label "phase:0" | Out-Null }
for ($i=5; $i -le 8; $i++) { gh issue edit $i --repo $repo --add-label "phase:1" | Out-Null }
for ($i=9; $i -le 12; $i++) { gh issue edit $i --repo $repo --add-label "phase:2" | Out-Null }
for ($i=13; $i -le 15; $i++) { gh issue edit $i --repo $repo --add-label "phase:3" | Out-Null }
for ($i=16; $i -le 18; $i++) { gh issue edit $i --repo $repo --add-label "phase:4" | Out-Null }

$backend = 3,4,5,6,8,11,12,13,14
$frontend = 7,9,10,12
$security = 3,4,13
$content = 11,12
$infra = 14,16
$community = 15,16,19

foreach ($n in $backend) { gh issue edit $n --repo $repo --add-label "area:backend" | Out-Null }
foreach ($n in $frontend) { gh issue edit $n --repo $repo --add-label "area:frontend" | Out-Null }
foreach ($n in $security) { gh issue edit $n --repo $repo --add-label "area:security" | Out-Null }
foreach ($n in $content) { gh issue edit $n --repo $repo --add-label "area:content" | Out-Null }
foreach ($n in $infra) { gh issue edit $n --repo $repo --add-label "area:infra" | Out-Null }
foreach ($n in $community) { gh issue edit $n --repo $repo --add-label "area:community" | Out-Null }

Write-Output "DONE"
