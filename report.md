1. Jelaskan karakteristik utama sistem terdistribusi dan trade-off yang umum pada desain Pub-Sub log aggregator.
Jawaban:
Sistem terdistribusi memiliki karakteristik utama berupa resource sharing, distribution transparency, openness, dependability, dan scalability. Tujuan dari sistem ini adalah memungkinkan akses sumber daya secara luas melalui jaringan tanpa memperlihatkan kompleksitas distribusinya kepada pengguna. Di sisi lain, setiap karakteristik tersebut membawa konsekuensi dalam desain. Sebagai contoh, peningkatan transparency, seperti failure transparency atau replication transparency, dapat menambah overhead komunikasi dan sinkronisasi antar node sehingga berdampak pada penurunan performa. Pada desain Publish–Subscribe (Pub-Sub) log aggregator, terdapat beberapa trade-off penting, seperti antara consistency dan availability (CAP), ordering dan throughput, serta latency dan durability. Sistem yang dioptimalkan untuk throughput tinggi umumnya mengorbankan konsistensi kuat dan hanya menyediakan eventual consistency. Untuk menjaga hasil tetap konsisten, digunakan pendekatan idempotent consumer tanpa memerlukan koordinasi yang kompleks.

2. Bandingkan arsitektur client-server vs publish-subscribe untuk aggregator. Kapan memilih Pub-Sub? Berikan alasan teknis.
Jawaban:
Arsitektur client-server bekerja dengan pola komunikasi synchronous, di mana client mengirim permintaan dan server memberikan respons secara langsung. Sebaliknya, model publish-subscribe menggunakan broker sebagai perantara antara publisher dan subscriber, sehingga keduanya tidak saling bergantung secara langsung. Pendekatan Pub-Sub bersifat asynchronous dan mendukung decoupling dalam hal waktu, lokasi, serta sinkronisasi. Hal ini memberikan fleksibilitas yang lebih tinggi dibandingkan client-server. Dalam sistem log aggregator berskala besar, Pub-Sub lebih tepat digunakan karena mendukung dynamic subscription, memiliki fault isolation yang lebih baik, serta dapat diskalakan secara horizontal. Sementara itu, client-server lebih cocok untuk kebutuhan komunikasi yang membutuhkan respons cepat dan bersifat deterministik. Oleh karena itu, Pub-Sub dipilih ketika sistem mengandalkan alur berbasis event dan membutuhkan distribusi data ke banyak konsumen.

3. Uraikan at-least-once vs exactly-once delivery semantics. Mengapa idempotent consumer krusial di presence of retries?
Jawaban:
Dalam sistem pengiriman pesan, terdapat beberapa jaminan delivery, yaitu at-most-once, at-least-once, dan exactly-once. At-least-once menjamin bahwa setiap pesan akan terkirim minimal satu kali, namun berpotensi menimbulkan duplikasi akibat mekanisme retry. Sebaliknya, exactly-once memastikan setiap pesan hanya diproses satu kali, tetapi memerlukan koordinasi transaksi dan pencatatan yang lebih kompleks. Dalam kondisi tersebut, idempotent consumer menjadi komponen penting. Dengan sifat idempotent, pemrosesan pesan akan menghasilkan output yang sama meskipun pesan yang sama diterima lebih dari sekali. Implementasinya dilakukan dengan menyimpan event_id yang telah diproses dalam deduplication store, sehingga sistem dapat menghindari pemrosesan ulang dan mencapai efek semantik exactly-once di atas mekanisme at-least-once.

4. Rancang skema penamaan untuk topic dan event_id (unik, collision-resistant). Jelaskan dampaknya terhadap dedup.
Jawaban:
Dalam sistem terdistribusi, penamaan yang terstruktur dan bersifat unik sangat penting untuk menghindari konflik identitas. Salah satu skema yang dapat digunakan adalah:
- topic = /domain/service/entity
- event_id = SHA256(source_id + timestamp + seq)
Pendekatan ini menghasilkan identifier yang bersifat unik dan tahan terhadap collision. Struktur hierarkis pada topic juga mempermudah proses filtering dalam sistem Publish–Subscribe. Konsep ini sejalan dengan Named-Data Networking (NDN), di mana setiap data memiliki nama yang berbeda untuk setiap versi. Dengan demikian, proses deduplication menjadi lebih efektif karena sistem dapat mengidentifikasi duplikasi berdasarkan event_id tanpa perlu membandingkan keseluruhan isi data.

5. Bahas ordering: kapan total ordering tidak diperlukan? Usulkan pendekatan praktis (mis. event timestamp + monotonic counter) dan batasannya.
Jawaban:
Total ordering tidak selalu dibutuhkan dalam semua sistem. Kebutuhan ini biasanya muncul pada sistem yang sangat bergantung pada urutan, seperti transaksi keuangan. Pada log aggregator, causal ordering umumnya sudah mencukupi. Salah satu pendekatan praktis adalah menggunakan kombinasi timestamp dan monotonic counter pada setiap sumber data, sehingga urutan lokal tetap terjaga tanpa memerlukan koordinasi global. Namun, pendekatan ini memiliki keterbatasan, terutama terkait clock skew antar node yang dapat menyebabkan event diterima tidak berurutan. Alternatif seperti Lamport clock atau vector clock dapat digunakan untuk meningkatkan akurasi urutan kausal, tetapi menambah kompleksitas sistem. Oleh karena itu, banyak implementasi memilih approximate ordering untuk menjaga performa.

6. Identifikasi failure modes (duplikasi, out-of-order, crash). Jelaskan strategi mitigasi (retry, backoff, durable dedup store).
Jawaban:
Beberapa failure mode yang umum dalam sistem terdistribusi meliputi duplikasi pesan, pengiriman yang tidak berurutan, dan kegagalan node (crash). Untuk mengatasinya, dapat diterapkan beberapa strategi, seperti retry dengan exponential backoff untuk mencegah lonjakan beban, penggunaan durable deduplication store (misalnya Redis atau RocksDB) untuk mencatat event yang telah diproses, serta mekanisme checkpoint dan log replay untuk pemulihan sistem. Selain itu, kombinasi acknowledgment dan pengaturan timeout juga membantu menjaga keseimbangan antara keandalan dan performa sistem.

7. Definisikan eventual consistency pada aggregator; jelaskan bagaimana idempotency + dedup membantu mencapai konsistensi.
Jawaban:
Eventual consistency adalah kondisi di mana seluruh node dalam sistem akan mencapai keadaan yang konsisten setelah periode propagasi tertentu. Dalam log aggregator, konsistensi ini dicapai melalui kombinasi idempotent consumer dan deduplication. Idempotency memastikan bahwa hasil pemrosesan tetap sama meskipun terjadi pengiriman ulang, sedangkan deduplication mencegah pemrosesan data yang sama secara berulang. Dengan pendekatan ini, sistem dapat mencapai konsistensi tanpa memerlukan mekanisme koordinasi yang kompleks, seperti two-phase commit, dan tetap mempertahankan ketersediaan yang tinggi sesuai prinsip BASE.

8. Rumuskan metrik evaluasi sistem (throughput, latency, duplicate rate) dan kaitkan ke keputusan desain.
Jawaban:
Evaluasi sistem terdistribusi umumnya menggunakan metrik seperti throughput, latency, dan duplicate rate. Throughput mengukur jumlah event yang dapat diproses dalam satuan waktu, latency menunjukkan waktu pemrosesan per event, sedangkan duplicate rate menggambarkan tingkat duplikasi pesan. Selain itu, metrik seperti durability dan recovery time juga penting untuk menilai ketahanan sistem terhadap kegagalan. Dalam praktiknya, peningkatan throughput sering kali berdampak pada peningkatan latency atau duplicate rate. Oleh karena itu, diperlukan pendekatan desain yang seimbang, seperti penggunaan asynchronous I/O, batch acknowledgment, serta pembatasan retry, agar sistem tetap optimal dari sisi performa, keandalan, dan konsistensi.

Keputusan Desain Utama

- Idempotency: Setiap event diidentifikasi secara unik menggunakan pasangan (topic, event_id) yang disimpan dalam deduplication store berbasis SQLite. Dengan pendekatan ini, event yang sama tidak akan diproses lebih dari satu kali meskipun dikirim ulang.
- Dedup Store: Sistem menggunakan database SQLite dengan tabel persisten (topic, event_id, processed_at). Penyimpanan ini memastikan bahwa data deduplication tetap tersedia meskipun terjadi restart pada container.
- Ordering: Sistem menggunakan timestamp dalam format ISO 8601 sebagai pendekatan ordering secara aproksimasi. Namun, sistem tidak menjamin total ordering karena tidak adanya global clock dalam sistem terdistribusi.
- Retry Mechanism: Sistem menerapkan pendekatan at-least-once delivery, di mana publisher dapat mengirim ulang event. Untuk menghindari efek duplikasi, digunakan idempotent consumer yang memanfaatkan deduplication store.
- Persistence: Data disimpan secara persisten menggunakan SQLite yang dapat dihubungkan dengan volume Docker (misalnya .data) untuk memastikan data tetap tersimpan di host meskipun container dihentikan atau di-restart.

RINGKASAN ARSITEKTUR Publisher → [POST /publish] → Aggregator (FastAPI) │ ↓ Dedup Store (SQLite) │ ↓ [GET /events] / [GET /stats]

DAFTAR PUSTAKA Van Steen, M., & Tanenbaum, A. S. (2023). Distributed systems: Principles and paradigms (4th ed.). Vrije Universiteit Amsterdam.