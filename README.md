# Pub-Sub Log Aggregator (FastAPI + SQLite + Docker)

Layanan aggregator sederhana yang menerima event dari publisher melalui endpoint `POST /publish`, kemudian diproses oleh consumer secara asynchronous dengan mekanisme **idempotent** (dedup berdasarkan `(topic, event_id)`). Sistem menyediakan observabilitas melalui endpoint `/events` dan `/stats`. Deduplication store menggunakan SQLite (local-only) sehingga tetap persisten dan tahan terhadap restart container.

---

## Fitur

* `POST /publish`: menerima event tunggal maupun batch dalam format JSON
* Idempotent consumer: deduplication berdasarkan `(topic, event_id)`
* Persisten: SQLite mencegah pemrosesan ulang setelah restart
* `GET /events?topic=...`: menampilkan daftar event unik yang telah diproses
* `GET /stats`: menampilkan `received`, `unique_processed`, `duplicate_dropped`, `topics`, `uptime`
* At-least-once delivery: mendukung pengiriman ulang event (duplikasi)

---

## Skema Event

```json
{
  "topic": "string",
  "event_id": "string-unik",
  "timestamp": "ISO8601",
  "source": "string",
  "payload": { "any": "json" }
}
```

---

## Menjalankan Secara Lokal

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.main
```

Akses API:

```
http://localhost:8080/docs
```

---

## Menjalankan dengan Docker

```bash
docker build -t uts-aggregator-11231070 .
docker run --rm -p 8080:8080 `
  -e AGG_DB_PATH=/data/agg.db `
  -v ${PWD}/.data:/data `
  uts-aggregator-11231070
```

---

## Docker Compose (Opsional)

```bash
docker compose up --build
```

---

## Contoh Pengujian

Kirim event melalui Swagger UI (`/docs`), lalu kirim ulang event yang sama untuk mensimulasikan duplikasi.

Hasil yang diharapkan:

* Event pertama → diproses
* Event kedua (sama) → dideteksi sebagai duplicate

Cek:

* `/events` → hanya menyimpan event unik
* `/stats` → menunjukkan peningkatan `duplicate_dropped`

`DEMONSTRASI`
[https://youtu.be/WSfML3TnHU8]

`LINK LAPORAN(PDF)`
[https://drive.google.com/file/d/1bzLuIvDUKa88o4-3eemYlmPbxdP0bXQu/view?usp=sharing]