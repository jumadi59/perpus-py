```mermaid
graph TD
    Start(Start) --> A[Halaman Depan]
    A --> B[Login]
    A --> C[Registrasi]
    A --> D[Keluar]
    
    B --> E[Input Username dan Password]
    E --> F{Validasi Login}
    F -->|Valid| G[Halaman Menu setelah Login]
    F -->|Tidak Valid| B1[Pesan Error dan Kembali ke Halaman Login]
    B1 --> E
    
    C --> H[Input Data Registrasi]
    H --> I{Proses Registrasi}
    I -->|Berhasil| J[Registrasi Berhasil dan Kembali ke Halaman Login]
    I -->|Gagal| K[Pesan Error dan Kembali ke Halaman Registrasi]
    J --> A
    K --> I

    G --> L[Daftar Buku]
    G --> M[Cari Buku]
    G --> N[Daftar pinjam buku]
    G --> O[Pinjam Buku]
    G --> P[Kembalikan buku]
    G --> D[Keluar]

    M --> R[Input nama buku]
    R --> S{Proses cari Buku}
    S -->|Ada| T[Tampil buku yang di cari] 
    S -->|tidak Ada| U[kembali cari buku]
    U --> M
    
    End(End)
    D --> End
