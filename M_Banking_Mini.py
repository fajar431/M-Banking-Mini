import getpass  # Untuk input PIN yang tidak terlihat

user_database = []  # Tempat menyimpan semua akun yang sudah registrasi
current_user = None  # Penanda akun yang sedang login

def menu_utama():
    """Menampilkan menu utama setelah login"""
    print("\n" + "="*30)
    print("MENU UTAMA M-BANKING")
    print("="*30)
    print("1. Cek Saldo")
    print("2. Setor")
    print("3. Tarik")
    print("4. Transfer")
    print("5. Riwayat Transaksi")
    print("6. Informasi Akun")
    print("7. Ubah PIN")
    print("8. Logout")

def menu_awal():
    """Menampilkan menu awal sebelum login"""
    print("\n" + "="*45)
    print("SELAMAT DATANG DI APLIKASI M-BANKING")
    print("="*45)
    print("1. Registrasi")
    print("2. Login")
    print("3. Exit")

def input_angka(prompt, min_value=0, max_value=None):
    """Fungsi helper untuk input angka dengan validasi"""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Nilai tidak boleh kurang dari {min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"Nilai tidak boleh lebih dari {max_value}")
                continue
            return value
        except ValueError:
            print("Mohon masukkan angka yang valid!")

def hitung_fee_transfer(tipe_kartu):
    """Menghitung fee transfer berdasarkan tipe kartu"""
    fee = {
        "Silver": 5000,
        "Gold": 3000,
        "Platinum": 0
    }
    return fee.get(tipe_kartu, 5000)


# PROGRAM UTAMA

print("\n" + "="*50)
print("APLIKASI M-BANKING")
print("="*50)

while True:
    menu_awal()
    menu = input("Pilih menu (1-3): ").strip()

    # REGISTRASI

    if menu == "1":
        print("\n" + "-"*20)
        print("REGISTRASI AKUN BARU")
        print("-"*20)
        
        # Validasi Nama
        while True:
            nama = input("Silakan masukkan nama Anda: ").strip().title()
            if nama == "":
                print("⚠️  Nama tidak boleh kosong!")
                continue
            
            # Cek apakah nama terlalu pendek
            if len(nama) < 3:
                print("⚠️  Nama terlalu pendek (minimal 3 karakter)")
                continue
            
            # Cek apakah nama hanya mengandung huruf dan spasi
            if not all(c.isalpha() or c.isspace() for c in nama):
                print("⚠️  Nama hanya boleh mengandung huruf dan spasi")
                continue
            
            break

        # Validasi PIN
        while True:
            pin = input("Masukkan PIN 6 digit angka: ").strip()
            
            if len(pin) != 6:
                print("⚠️  PIN harus tepat 6 digit!")
                continue
            
            if not pin.isdigit():
                print("⚠️  PIN hanya boleh mengandung angka!")
                continue
            
            # Konfirmasi PIN
            pin_konfirmasi = input("Konfirmasi PIN: ").strip()
            if pin != pin_konfirmasi:
                print("⚠️  PIN tidak cocok! Silakan ulangi")
                continue
            
            print("✅ PIN berhasil dibuat!")
            print(f"📝 PIN Anda: {pin}. Mohon dijaga dengan baik!")
            break

        # Pilih Tipe Kartu
        while True:
            print("\nPilih tipe kartu:")
            print("1. Silver - Fee transfer Rp 5.000")
            print("2. Gold   - Fee transfer Rp 3.000")
            print("3. Platinum - Tidak ada fee transfer")
            
            pilihan_kartu = input("Pilih tipe kartu (1-3): ").strip()
            
            if pilihan_kartu == "1":
                card_type = "Silver"
            elif pilihan_kartu == "2":
                card_type = "Gold"
            elif pilihan_kartu == "3":
                card_type = "Platinum"
            else:
                print("⚠️  Pilihan tidak valid!")
                continue
            
            break

        # Generate User ID
        user_id = "MBK-" + str(len(user_database) + 1).zfill(4)
        
        # Buat akun baru dengan struktur: 
        # [id, nama, pin, saldo, riwayat, tipe_kartu, counter_transaksi]
        akun = [
            user_id,        # 0: ID User
            nama,           # 1: Nama
            pin,            # 2: PIN
            0,              # 3: Saldo (awal 0)
            [],             # 4: Riwayat transaksi
            card_type,      # 5: Tipe kartu
            0               # 6: Counter transaksi (untuk nomor urut)
        ]
        
        user_database.append(akun)
        
        print("\n" + "="*40)
        print("✅ REGISTRASI BERHASIL!")
        print("="*40)
        print(f"👤 Nama      : {nama}")
        print(f"🆔 User ID   : {user_id}")
        print(f"💳 Tipe Kartu: {card_type}")
        print(f"💰 Saldo Awal: Rp 0")
        print("="*40)
        print("Silakan login untuk mulai transaksi.")

    # LOGIN

    elif menu == "2":
        print("\n" + "-"*20)
        print("LOGIN AKUN")
        print("-"*20)
        
        user_id = input("User ID: ").strip().upper()
        pin = getpass.getpass("PIN: ")  # PIN tidak terlihat di layar
        
        current_user = None
        
        # Cek kredensial
        for akun in user_database:
            if akun[0] == user_id and akun[2] == pin:
                current_user = akun
                break
        
        if current_user:
            print(f"\n✅ Login berhasil! Selamat datang, {current_user[1]}!")
        else:
            print("\n❌ User ID atau PIN salah!")
            continue

        # MENU UTAMA SETELAH LOGIN

        while current_user:
            menu_utama()
            pilih = input("Pilih menu (1-8): ").strip()

            # CEK SALDO
            if pilih == "1":
                print("\n" + "-"*20)
                print("CEK SALDO")
                print("-"*20)
                print(f"💰 Saldo Anda: Rp {current_user[3]:,}")
                print(f"💳 Tipe Kartu: {current_user[5]}")

            # SETOR TUNAI
            elif pilih == "2":
                print("\n" + "-"*20)
                print("SETOR TUNAI")
                print("-"*20)
                
                while True:
                    jumlah = input_angka("Jumlah setor (min Rp 10.000): Rp ", 10000)
                    
                    if jumlah > 10000000:  # Maksimal 10 juta
                        print("⚠️  Maksimal setor Rp 10.000.000 per transaksi")
                        continue
                    
                    konfirmasi = input(f"Setor Rp {jumlah:,}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        # Update saldo
                        current_user[3] += jumlah
                        
                        # Update counter transaksi
                        current_user[6] += 1
                        
                        # Tambahkan ke riwayat
                        current_user[4].append([
                            current_user[6],  # Nomor transaksi
                            "Setor",
                            jumlah,
                            current_user[3]  # Saldo setelah transaksi
                        ])
                        
                        print(f"✅ Setor Rp {jumlah:,} berhasil!")
                        print(f"💰 Saldo baru: Rp {current_user[3]:,}")
                        break
                    else:
                        print("❌ Transaksi dibatalkan")
                        break

            # TARIK TUNAI
            elif pilih == "3":
                print("\n" + "-"*20)
                print("TARIK TUNAI")
                print("-"*20)
                
                print(f"Saldo tersedia: Rp {current_user[3]:,}")
                
                while True:
                    jumlah = input_angka("Jumlah tarik (min Rp 50.000): Rp ", 50000)
                    
                    # Validasi saldo
                    if jumlah > current_user[3]:
                        print(f"❌ Saldo tidak cukup! Saldo Anda: Rp {current_user[3]:,}")
                        continue
                    
                    # Batas maksimal tarik
                    if jumlah > 5000000:  # Maksimal 5 juta
                        print("⚠️  Maksimal tarik Rp 5.000.000 per transaksi")
                        continue
                    
                    konfirmasi = input(f"Tarik Rp {jumlah:,}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        # Update saldo
                        current_user[3] -= jumlah
                        
                        # Update counter transaksi
                        current_user[6] += 1
                        
                        # Tambahkan ke riwayat
                        current_user[4].append([
                            current_user[6],  # Nomor transaksi
                            "Tarik",
                            jumlah,
                            current_user[3]  # Saldo setelah transaksi
                        ])
                        
                        print(f"✅ Tarik Rp {jumlah:,} berhasil!")
                        print(f"💰 Sisa saldo: Rp {current_user[3]:,}")
                        break
                    else:
                        print("❌ Transaksi dibatalkan")
                        break

            # TRANSFER
            elif pilih == "4":
                print("\n" + "-"*20)
                print("TRANSFER")
                print("-"*20)
                
                # Cari akun tujuan
                tujuan_id = input("User ID tujuan: ").strip().upper()
                tujuan = None
                
                for akun in user_database:
                    if akun[0] == tujuan_id and akun != current_user:  # Tidak bisa transfer ke diri sendiri
                        tujuan = akun
                        break
                
                if tujuan is None:
                    print("❌ Akun tujuan tidak ditemukan atau tidak valid!")
                    continue
                
                print(f"Transfer ke: {tujuan[1]} ({tujuan_id})")
                print(f"Tipe kartu Anda: {current_user[5]}")
                
                # Hitung fee transfer
                fee = hitung_fee_transfer(current_user[5])
                if fee > 0:
                    print(f"💰 Fee transfer: Rp {fee:,}")
                
                while True:
                    jumlah = input_angka("Jumlah transfer (min Rp 10.000): Rp ", 10000)
                    
                    # Hitung total yang akan dikurangkan
                    total = jumlah + fee
                    
                    # Validasi saldo
                    if total > current_user[3]:
                        print(f"❌ Saldo tidak cukup! Diperlukan: Rp {total:,}")
                        print(f"   Saldo Anda: Rp {current_user[3]:,}")
                        continue
                    
                    # Batas maksimal transfer
                    if jumlah > 20000000:  # Maksimal 20 juta
                        print("⚠️  Maksimal transfer Rp 20.000.000 per transaksi")
                        continue
                    
                    konfirmasi = input(f"Transfer Rp {jumlah:,} + fee Rp {fee:,} = Rp {total:,}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        # Update saldo pengirim
                        current_user[3] -= total
                        
                        # Update counter transaksi pengirim
                        current_user[6] += 1
                        trx_number = current_user[6]
                        
                        # Tambahkan ke riwayat pengirim
                        current_user[4].append([
                            trx_number,
                            f"Transfer ke {tujuan_id}",
                            jumlah,
                            current_user[3],
                            fee  # Tambahkan fee di riwayat
                        ])
                        
                        # Update saldo penerima
                        tujuan[3] += jumlah
                        
                        # Update counter transaksi penerima
                        tujuan[6] += 1
                        
                        # Tambahkan ke riwayat penerima
                        tujuan[4].append([
                            tujuan[6],
                            f"Transfer dari {current_user[0]}",
                            jumlah,
                            tujuan[3]
                        ])
                        
                        print("✅ Transfer berhasil!")
                        print(f"💰 Sisa saldo: Rp {current_user[3]:,}")
                        break
                    else:
                        print("❌ Transfer dibatalkan")
                        break

            # RIWAYAT TRANSAKSI
            elif pilih == "5":
                print("\n" + "-"*30)
                print("RIWAYAT TRANSAKSI")
                print("-"*30)
                
                if not current_user[4]:  # Jika riwayat kosong
                    print("📭 Belum ada transaksi")
                else:
                    print(f"No  | Jenis Transaksi{' ' * 15} | Jumlah{' ' * 10} | Saldo{' ' * 10} | Fee")
                    print("-" * 80)
                    
                    for trx in reversed(current_user[4]):  # Tampilkan dari yang terbaru
                        jenis = trx[1][:25]  # Potong jika terlalu panjang
                        jumlah = f"Rp {trx[2]:,}"
                        saldo = f"Rp {trx[3]:,}"
                        
                        # Format output
                        if len(trx) > 4:  # Jika ada fee (transfer)
                            fee = f"Rp {trx[4]:,}"
                        else:
                            fee = "Rp 0"
                        
                        print(f"{trx[0]:<4} | {jenis:<25} | {jumlah:<15} | {saldo:<15} | {fee}")

            # INFORMASI AKUN
            elif pilih == "6":
                print("\n" + "-"*25)
                print("INFORMASI AKUN")
                print("-"*25)
                
                # Konfirmasi PIN untuk keamanan
                pin_konfirmasi = getpass.getpass("Masukkan PIN untuk konfirmasi: ")
                
                if current_user[2] == pin_konfirmasi:
                    print("\n📋 DATA AKUN ANDA:")
                    print("-" * 40)
                    print(f"👤 Nama Lengkap : {current_user[1]}")
                    print(f"🆔 User ID      : {current_user[0]}")
                    print(f"💳 Tipe Kartu   : {current_user[5]}")
                    print(f"💰 Saldo        : Rp {current_user[3]:,}")
                    print(f"📊 Total Transaksi: {current_user[6]} transaksi")
                    print("-" * 40)
                    
                    # Informasi fee berdasarkan tipe kartu
                    fee = hitung_fee_transfer(current_user[5])
                    if fee > 0:
                        print(f"💡 Info: Fee transfer untuk kartu {current_user[5]}: Rp {fee:,}")
                    else:
                        print(f"💡 Info: Kartu {current_user[5]} tidak dikenakan fee transfer")
                else:
                    print("❌ PIN salah! Akses ditolak.")

            # UBAH PIN
            elif pilih == "7":
                print("\n" + "-"*20)
                print("UBAH PIN")
                print("-"*20)
                
                # Verifikasi PIN lama
                pin_lama = getpass.getpass("PIN lama: ")
                
                if current_user[2] != pin_lama:
                    print("❌ PIN lama salah!")
                    continue
                
                # Input PIN baru
                while True:
                    pin_baru = input("PIN baru (6 digit angka): ").strip()
                    
                    if len(pin_baru) != 6 or not pin_baru.isdigit():
                        print("⚠️  PIN harus 6 digit angka!")
                        continue
                    
                    konfirmasi = input("Konfirmasi PIN baru: ").strip()
                    
                    if pin_baru != konfirmasi:
                        print("⚠️  PIN tidak cocok!")
                        continue
                    
                    # Update PIN
                    current_user[2] = pin_baru
                    print("✅ PIN berhasil diubah!")
                    break

            # LOGOUT
            elif pilih == "8":
                print("\n" + "="*40)
                print(f"Terima kasih, {current_user[1]}!")
                print("Anda telah logout dari sistem.")
                print("="*40)
                current_user = None
                break

            else:
                print("⚠️  Pilihan menu tidak valid! Silakan pilih 1-8")

    # EXIT PROGRAM

    elif menu == "3":
        print("\n" + "="*40)
        print("TERIMA KASIH TELAH MENGGUNAKAN")
        print("APLIKASI M-BANKING")
        print("="*40)
        break

    else:
        print("⚠️  Pilihan tidak valid! Silakan pilih 1-3")