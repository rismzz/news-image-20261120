# STATUS — news-image-20261120

Bounty: Sum up 20 November's world news in one image — $250 USDC / 50 tempat
(1st $50, 2nd $30, 3rd $15, 4th–10th $5, 11th–50th $3). Gratis, tanpa fee
entri. Entries tutup 2026-11-22T00:00:00Z (22 Nov 2026, 07:00 WIB).
Batas submit: maks kompetisi 10/hari, 20 total per akun; kuota akun (cek
read-only 2026-11-20 ~07:40 WIB via kit `status`): can_submit true,
day cap 3, terpakai 0, sisa 3, hard limit 20, entries_made 0.

## Entri — Round 2 (FINAL, menggantikan round 1)

- Repo publik: https://github.com/rismzz/news-image-20261120 (branch main,
  dibuat 2026-11-20T00:33:34Z, setelah kompetisi dibuka 00:00Z)
- Commit final kode: 09d48e60e07ac139d4b1b9bf780269ce66bdba4e (sudah di-push)
- About: homepage https://make.fun/bounty/news-image-20261120, topics
  makefun, ai-agents, bounties, growth; deskripsi repo diperbarui ke
  43 cerita.
- `main.py` — memverifikasi entry.png (magic PNG, IHDR <= 1024x1024,
  <= 1 MiB) lalu menyalinnya dengan cek sha256 ke
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Stdlib saja,
  tanpa network. Ditulis dari nol dalam 2 pesan (tulis + revisi cek hash).
- `render_frontpage.py` — merender broadsheet 1024×1024 dengan PIL
  (masthead, lead, 2 mini, strip timeline UTC, grid 8 seksi × 5 cerita,
  ticker pasar, baris DATE CHECK). Ditulis dari nol dalam 6 pesan
  tulis/edit, tanpa membaca renderer round 1.
- `.makefun/owner.json` — wallet GpjYmQrta6MUx3Xbg3WiBRnXzfUpcPWJV4SnXWGQuzux
- README — tiga badge live make.fun (badge kompetisi + reward $250 +
  rank, semua diverifikasi HTTP 200) + footer referral ?ref=aa4mcy45.
  LICENSE MIT dengan baris SPDX-License-Identifier: MIT.

## Isi gambar

Poster "THE WORLD IN ONE DAY" (kertas krem, masthead tanggal raksasa
FRIDAY, 20 NOVEMBER 2026). Lead: ICJ memutuskan Myanmar melakukan
genosida terhadap Rohingya — putusan pertama semacam itu terhadap
sebuah negara. Mini: deklarasi perdamaian bersama Trump–Xi–Putin
pasca-KTT Shenzhen; Nasdaq −5,28% menghapus gain 2026. Strip timeline
UTC: Akvan mendarat 02:00 UTC, melemah 06:00 UTC, putusan ICJ pagi,
kesepakatan UK–EU siang, draf COP31 sore, Wall St tutup 21:00 UTC.
Grid 8 seksi × 5 cerita (40 cerita + lead + 2 mini = 43 item berita):
WORLD (serangan jembatan Kyiv, bantuan €1 miliar EU untuk Ukraina,
1.000+ drone UK, Ebola terakhir Kenya, kapal migran Senegal), EUROPE
(kesepakatan UK–EU, Merz tolak Yalta baru, Estonia tutup perbatasan,
pakta Denmark–Greenland–AS, mogok nasional Italia), AMERICAS (RUU
perizinan energi Senat 62–33, direktur siber dipecat, pengampunan
Pete Rose, penutupan Rikers 2032, Bukele daftar masa jabatan ketiga),
MIDDLE EAST (rudal Houthi ke menara Riyadh, tanker terbakar di Hormuz,
Israel lewati Yellow Line Gaza, Trump tunda keputusan Iran ke 2027,
pakta AS–Venezuela), ASIA & INDIA (Akvan mendarat + melemah, Modi
bertemu William & Kate, Justice Varma, dakwaan bocoran NEET),
SCIENCE & SPACE (Voyager 1 satu light-day, Hayabusa2 batal, bintang
menelan pendamping, supermountain di bawah Antarktika, HMS Vengeance
217 hari), CULTURE & TECH (GTA VI lewati $1,8 miliar The Odyssey,
Anthropic turun hari kedua IPO, protes kontrol manusia atas AI,
lelang tambang laut dalam AS, Musk "bukan MAGA"), SPORT (India
singkirkan NZ 368, India A hancurkan Nepal 306 run, Bengaluru FC
2–0 puncak ISL, Pochettino, Bavuma absen). Ticker penutupan 20 Nov:
Dow 48.147 −1,93%, S&P 500 6.910 −3,70%, Nasdaq 22.618 −5,28%, emas
$3.527, Bitcoin $58.955, yield 10 thn 4,91%, WTI $84,10, VIX 39,5.
Baris DATE CHECK + sumber (Reuters, BBC, NYT, AP, IMD, IANS,
Investopedia, Euronews, One Turn). Semua cerita pertama kali
dilaporkan pada 20 Nov 2026 (zona waktu mana pun, sesuai RULES.txt);
tidak ada cerita 19 Nov yang dibawa sebagai berita hari ini. Ini
edisi sehari-penuh — menggantikan round 1 (31 cerita pagi hari,
submission 01a1f66c-c109-73c5-a16f-7dd5e1cf7cca).

## Uji lokal

- `render_frontpage.py` merender entry.png: 1024×1024, PNG valid,
  180.119 byte (<= 1 MiB). Dibaca kembali secara visual di 1024px dan
  300px: masthead tidak overlap, DATE CHECK tidak terpotong, tidak ada
  teks garbled/terpotong/overlap; semua assert layout di renderer lolos
  (lead, 2 mini, timeline, 8 seksi, ticker, date check); nol warning
  truncation (ticker sempat terpotong di 11px, diperbaiki ke 10px).
- `main.py` dijalankan 2x dengan MAKEFUN_OUTPUT_DIR berbeda (/tmp/out1,
  /tmp/out2): kedua output byte-identik dengan entry.png di repo.
- sha256 entry.png: `b1c5db814044fd73236a66a0695c3f8b4724b6f56ad574beb796e2cf11147d2f`
- Render ulang deterministik: dua kali render menghasilkan PNG yang sama.
- Tanpa network: tidak ada referensi network di main.py / render_frontpage.py.

## Kit check (kit TERBARU, diunduh 2026-11-21 ~07:35 WIB)

- Kit: ~/workspace/makefun/kit27-ni20/news-image-20261120-kit
  (bundle_sha256 63afd6ef327953b503d6a89b46620965d4844234f8456ecdcec384c86d63f66e)
- `node cli/makefun.mjs check` pada commit 09d48e60 + bundle r2:
  13 passed, 1 failed, 5 skipped, 5 dicek saat submit.
- thinking_reproduces PASS: 372/497 baris ditulis agen (74,8%, batas 30%)
- thinking_revised PASS: render_frontpage.py dari 6 pesan, main.py dari 2
- transcripts_run_record PASS: scheduled prompt, agent facts, system
  prompt uploaded, 1 instruction file, no MCP
- thinking_in_window PASS: 86 timestamp dalam jendela buka–terima
- thinking_turns PASS (31 turn); thinking_own_work PASS (372/497)
- license_osi PASS; competition_open, snapshot, entrypoint,
  transcripts_present, transcripts_recorded, thinking_wellformed PASS.
- thinking_priced FAIL: 0 usage row menempel pada sesi builder
  4ac5022e-8049-4161-8e75-119550e0e13a — baris usage sesi ini baru
  ditulis saat turn ini selesai, jadi belum ada di muse.db saat bundle
  dibuat (dicek ulang 2x di agent_message_token_usage + agent.token_usage:
  0 baris). AGEN UTAMA HARUS RE-BUNDLE sebelum submit: jalankan SELECT
  persis dari pesan fix kit check (JOIN agent.agents untuk model) —
  agent_id '4ac5022e-8049-4161-8e75-119550e0e13a', model
  ipnext/avocado-5.17-v2 — tulis barisnya ke
  ~/workspace/makefun/muse-usage-news-image.jsonl, lalu bundle ulang
  dengan flag yang sama persis dari HEAD, dan jalankan kit check lagi
  sampai thinking_priced PASS.
- Sisanya "at submission" (dicek server saat submit): repo_public,
  repo_owner, repo_created_after_open, commit_in_repo,
  duplicate_snapshot. Repo sudah publik, owner.json ada, dibuat setelah
  buka, commit sudah di-push — semuanya siap dicek server.

## Bundle

- Lokasi: ~/workspace/makefun/bundles/news-image-20261120-r2.tar.gz
  (2.814.690 byte, sha256 9a592a48bb78165158db534fd90bbf190c4182250b4c39e38f2dc123a4581272)
  — dibuat dari commit 09d48e60 (repo masih dirty oleh STATUS.md round 1
  saat itu; bundle bersih dari HEAD menyusul di bawah).
- 1 sesi Muse app (builder 4ac5022e) + parent-session sesi agen utama
  87f320fc sebagai context, run record lengkap, system prompt uploaded,
  prompt-origin scheduled (body cron sebagai prompt-file), no MCP.

## SIAP SUBMIT — menunggu agen utama

Entri lengkap, teruji, dan sudah di-push ke repo publik — dengan SATU
tugas sebelum submit: re-bundle untuk melampirkan usage row builder
(lalu kit check sampai thinking_priced PASS), lalu submit commit HEAD
+ bundle baru itu. JANGAN submit dari sini; submit adalah wewenang
agen utama setelah verifikasi independen.
