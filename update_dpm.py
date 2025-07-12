import sqlite3
import os


def list_folders(base_path):
    """Menampilkan daftar folder utama yang ada dalam path."""
    return [
        folder for folder in os.listdir(base_path) if os.path.isdir(
            os.path.join(
                base_path,
                folder))]


def list_databases(folder_path):
    """Mendata semua file 'icmo_api' dalam subfolder."""
    databases = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "icmo_api":
                databases.append(os.path.join(root, file))
    return databases


def copy_data(source_db, target_db):
    """Menyalin data hanya kolom yang sesuai dari dpm database sumber ke target."""
    if not os.path.exists(source_db):
        print(f"Database sumber tidak ditemukan: {source_db}")
        return
    if not os.path.exists(target_db):
        print(f"Database target tidak ditemukan: {target_db}")
        return

    try:
        conn_source = sqlite3.connect(source_db)
        conn_target = sqlite3.connect(target_db)

        cursor_target = conn_target.cursor()
        cursor_target.execute("DELETE FROM dpm2;")  # Menghapus data lama di tabel target

        cursor_source = conn_source.cursor()
        cursor_source.execute("SELECT * FROM dpm;")
        rows = cursor_source.fetchall()

        # Nama kolom di sumber
        cursor_source.execute("PRAGMA table_info(dpm);")
        source_columns = [info[1] for info in cursor_source.fetchall()]

        # Nama kolom di target
        cursor_target.execute("PRAGMA table_info(dpm);")
        target_columns = [info[1] for info in cursor_target.fetchall()]

        # Kolom yang sama
        common_columns = list(set(source_columns) & set(target_columns))
        placeholders = ', '.join(['?' for _ in common_columns])
        columns_str = ', '.join(common_columns)

        for row in rows:
            values = [row[source_columns.index(col)] for col in common_columns]
            cursor_target.execute(
                f"INSERT INTO dpm ({columns_str}) VALUES ({placeholders});",
                values
            )

        conn_target.commit()
        print(f"Data berhasil disalin dari {source_db} ke {target_db}.")
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan saat menyalin data dari {source_db} ke {target_db}: {e}")
    finally:
        conn_source.close()
        conn_target.close()


def update_schedule(databases, new_blth):
    """
    Mengubah nilai kolom blth dan tgl_schedule di setiap database.
    'databases' adalah list of tuples (db_path, tgl_schedule).
    """
    for db_path, new_tgl_schedule in databases:
        if not os.path.exists(db_path):
            print(f"Database tidak ditemukan: {db_path}")
            continue

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE dpm
                SET blth = ?,
                    tgl_schedule = ?;
            """, (new_blth, new_tgl_schedule))
            conn.commit()
            print(f"Jadwal berhasil diperbarui di {db_path}.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat memperbarui jadwal di {db_path}: {e}")
        finally:
            conn.close()


def main():
    base_path = os.getcwd()
    print("1. Salin Data")
    print("2. Ubah Jadwal")
    choice = input("\nMasukkan pilihan (1/2): ").strip()

    if choice == '1':
        # Opsi 1: Salin Data
        print("\nFolder utama yang tersedia:")
        folders = list_folders(base_path)

        if not folders:
            print("Tidak ada folder yang tersedia.")
            return

        print("\nPilih folder sumber:")
        for idx, folder in enumerate(folders, start=1):
            print(f"{idx}. {folder}")

        try:
            source_choice = int(input("\nMasukkan nomor folder sumber: ").strip())
            if 1 <= source_choice <= len(folders):
                source_folder = os.path.join(base_path, folders[source_choice - 1])
            else:
                print("Pilihan nomor folder sumber tidak valid.")
                return
        except ValueError:
            print("Input tidak valid. Harap masukkan nomor yang benar.")
            return

        print("\nPilih folder target:")
        for idx, folder in enumerate(folders, start=1):
            print(f"{idx}. {folder}")

        try:
            target_choice = int(input("\nMasukkan nomor folder target: ").strip())
            if 1 <= target_choice <= len(folders):
                target_folder = os.path.join(base_path, folders[target_choice - 1])
            else:
                print("Pilihan nomor folder target tidak valid.")
                return
        except ValueError:
            print("Input tidak valid. Harap masukkan nomor yang benar.")
            return

        # Mendapatkan semua db icmo_api pada subfolder
        source_databases = list_databases(source_folder)
        target_databases = list_databases(target_folder)

        if not source_databases:
            print("Tidak ada database 'icmo_api' ditemukan di folder sumber.")
            return
        if not target_databases:
            print("Tidak ada database 'icmo_api' ditemukan di folder target.")
            return

        # Salin setiap pasangan db
        for source_db, target_db in zip(source_databases, target_databases):
            copy_data(source_db, target_db)
        print("Penyalinan data selesai.")

    elif choice == '2':
        # Opsi 2: Ubah Jadwal
        print("\nFolder utama yang tersedia:")
        folders = list_folders(base_path)

        if not folders:
            print("Tidak ada folder yang tersedia.")
            return

        print("\nPilih folder yang akan diproses untuk 'Ubah Jadwal':")
        for idx, folder in enumerate(folders, start=1):
            print(f"{idx}. {folder}")

        try:
            folder_choice = int(input("\nMasukkan nomor folder yang akan diproses: ").strip())
            if 1 <= folder_choice <= len(folders):
                selected_folder = os.path.join(base_path, folders[folder_choice - 1])
            else:
                print("Pilihan nomor folder tidak valid.")
                return
        except ValueError:
            print("Input tidak valid. Harap masukkan nomor yang benar.")
            return

        # Mendapatkan semua db icmo_api pada folder yang dipilih
        source_databases = list_databases(selected_folder)

        if not source_databases:
            print("Tidak ada database 'icmo_api' ditemukan di folder yang dipilih.")
            return

        new_blth = 202507

        # Membuat daftar tuple (db_path, new_tgl_schedule) untuk setiap db
        # Contoh penetapan tgl_schedule, Anda dapat menyesuaikannya sesuai kebutuhan
        databases = [
            (db_path, f"06/{23 + idx}/2025")
            for idx, db_path in enumerate(source_databases)
        ]

        update_schedule(databases, new_blth)
        print("Jadwal berhasil diperbarui.")

    else:
        print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
