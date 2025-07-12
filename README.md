
# 🧩 SQLite DPM Sync Tool: Mass Data Migration and Field Update Across Nested Databases

This Python-based tool automates the synchronization and mass update of `dpm` table data across multiple SQLite databases. It is designed to handle nested directory structures commonly used in mobile or distributed systems, ensuring all target databases are updated consistently from a central source.

---

## 🔧 Features

- **📁 Nested Directory Scanning**  
  Automatically detects and lists databases (`icmo_api`) across deeply nested folders.

- **🧬 Selective Data Sync**  
  Transfers only matching columns from a source database `dpm` table into each target’s `dpm2` table.

- **📆 Bulk Schedule Update**  
  Efficiently updates the `blth` and `tgl_schedule` fields across all target databases with a new value.

- **📦 Lightweight Dependency**  
  Built entirely on standard Python libraries (`sqlite3`, `os`) — no external packages required.

---

## 📁 Project Structure

```
updateDpmPasca/
├── update_dpm.py                 # Main processing script
├── JAB/JABA/databases/icmo_api  # Sample nested SQLite database
├── ...                          # Additional database folders
```

---

## ⚙️ How It Works

1. **Scans** a given directory tree and finds all files named `icmo_api`.
2. **Connects** to each database using `sqlite3`.
3. **Clears** the `dpm2` table in the target database.
4. **Reads** from the source database’s `dpm` table.
5. **Copies** only columns that exist in both source and target tables.
6. **Commits** the transfer and optionally updates `blth` and `tgl_schedule`.

---

## 🛠 Requirements

- Python 3.x
- No external packages required

---

## 🚦 Usage

1. Modify `update_dpm.py` to specify:
   - Base folder path
   - Source and target database pairs
   - New values for `blth` and `tgl_schedule` as needed

2. Run the script:
```bash
python update_dpm.py
```

You’ll see console outputs for:
- Data copy status
- Missing databases
- Update success or failure

---

## ✅ Example Use Cases

- Updating mobile app SQLite data files collected from field teams
- Synchronizing master data to regional instances
- Auditing schedule updates across distributed systems

---

## 👨‍💻 About the Developer

I’m a freelance Python developer specializing in automation and backend operations. If you're managing dozens or hundreds of databases and want to avoid repetitive SQLite work — I can help design smarter solutions tailored to your infrastructure.

✉️ Contact: [plusenergi77@gmail.com](mailto:email@email.com)

---

## 📄 License

This project is licensed under the Apache License 2.0 – you are free to use, modify, and distribute it with proper attribution.
